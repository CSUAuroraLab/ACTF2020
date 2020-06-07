#include <stdio.h>
#include <stdlib.h>

void Init()
{
    setbuf(stdout, 0);
    setbuf(stdin, 0);
}

void repeat()
{
    char buf[0x38];
    int cnt = 20;
    puts("I am monitoring your screen...");
    puts("Have a try...");
    
    while(cnt){
        cnt -= 1;
        printf(">> ");
        buf[read(0, buf, 0x30)] = 0x00;
        if(!strncmp(buf, "quit", 4))
            break;
        printf(buf);
    }

    puts("Ok...");
    puts("I am going to monitor others...");
}
int main()
{
    Init();
    repeat();
    puts("bye...");
}