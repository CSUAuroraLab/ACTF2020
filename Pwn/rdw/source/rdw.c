#include <unistd.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <stdio.h>
#include <stdlib.h>
// gcc -fno-stack-protector rdw.c -o rdw
void Init();
void sandbox();
void vuln();

char key[0x10];
int main()
{
    Init();
    sandbox();
    vuln();
    return 0;
}

void Init()
{
    int fp;
    char buf[0x4];
    setbuf(stdout, 0);
    setbuf(stdin, 0);


    fp = open("/dev/urandom", 0);
    read(fp, buf, 4);
    close(fp);

    printf("Give you a key>> ");
    write(1, buf, 4);
    puts("\nplease return back...");
    printf(">> ");
    read(0, key, 0x10);

    return;
}

void vuln()
{

    char buf[0x50];
    puts("hahaha...");
    puts("I have a filter");
    puts("who cares your input");
    read(0, buf, 0x200);
}
void sandbox()
{
   prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0);
	struct sock_filter sfi[] = {
		{0x20,0x00,0x00,0x00000004},
		{0x15,0x00,0x09,0xc000003e},
		{0x20,0x00,0x00,0x00000000},
		{0x35,0x07,0x00,0x40000000},
		{0x15,0x06,0x00,0x0000003b},
		{0x15,0x00,0x04,0x00000001},
		{0x20,0x00,0x00,0x00000024},
		{0x15,0x00,0x02,0x00000000},
		{0x20,0x00,0x00,0x00000020},
		{0x15,0x01,0x00,0x00000010},              //write's length
		{0x06,0x00,0x00,0x7fff0000},
		{0x06,0x00,0x00,0x00000000}
	};
	struct sock_fprog sfp = {12,sfi};

	prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&sfp);
}