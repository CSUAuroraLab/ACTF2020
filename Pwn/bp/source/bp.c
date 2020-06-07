#include <stdio.h>
#include <stdlib.h>
//gcc -fno-stack-protector rdw.c -o rdw

void initBuf();
void setCookie();
void welcome();

int main()
{
    initBuf();
    setCookie();
    welcome();
    return 0;
}

void initBuf()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
}
void setCookie()
{

    char buffer[0x80];
    puts("Please show me your cookie: ");
    read(0, buffer, 0x100);

    puts("Your Cookie: ");
    puts(buffer);

    return ;
}

void welcome()
{
    puts("Yeah! You already login...");
}