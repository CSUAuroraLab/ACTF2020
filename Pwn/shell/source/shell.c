#include <stdio.h>
#include <stdlib.h>
// Full RELRO 
// gcc -m32 -fPIE -pie -z now shell.c -o shell

void initBuf();

void menu();
void Create();
void Edit();
void Delete();
void showContent();
void showTag();
void heapMain();

void smallBox();
void middleBox();
void largeBox();

void rean_n();
int getNumber();
typedef struct sTag{
    int tag;
    int tagShow;
}sTag;

sTag small = {0x10, smallBox};
sTag middle = {0x100, middleBox};
sTag large = {0x20000, largeBox};

int lastStartIndex, lastEndIndex;
int heapArray[0x2000];

int main()
{
    initBuf();
    heapMain();
    return 0;
}


void heapMain()
{
    int ch;
    while(1){
        menu();
        ch = getNumber();
        switch(ch)
        {
            case 1:
                Create();
                break;
            case 2:
                Edit();
                break;
            case 3:
                Delete();
                break;
            case 4:
                showContent();
                break;
            case 5:
                showTag();
                break;
            case 6:
                puts("Bye...");
                exit(0);
            default:
                puts("Wrong Input...");
                break;
        }

    }
}

void Create()
{
    int i, j, k, l;
    int many, size, onlyCount;

    for(i = 0; i < 0x1000 && heapArray[2*i]; i++)
        ;

    if(i == 0x1000){
        puts("Already Full !!!");
        return;
    }

    onlyCount = 0x1000 - i;

    puts("How many boxes do you want ?");
    printf(">> ");
    many = getNumber();

    if(many <= 0 || many > 0x100 || (2*many > onlyCount)){
        puts("Oh, then i have boxes for you!");
        return;
    }

    printf("Type Your Message box's size >> ");
    size = getNumber();

    if(size <= 0 || size > 0x20000){
        puts("Wrong Size !!!");
        return;
    }

    for(k = 0; k < many; k++)
    {
        heapArray[2 * (k+i) + 1] = size;
        printf("malloc\n");
        heapArray[2 * (k+i)] = malloc(size + 4);
        if (!heapArray[2 * (k+i)]){
            puts("Failed in malloc");
            exit(1);
        }
    }
    
    puts("All the boxes you need are prepared for you...");
    
    for(k = 0; k < many; k++)
    {
        printf("The message >> ");
        read_n(heapArray[2 * (i+k)], heapArray[2 * (k+i) + 1]);
    }

    puts("Just add a tag for your box.");

    if(0 < size && size < 0x100){
        for(k = 0; k < many; k++){
            *(int*)(heapArray[2 * (i+k)] + size) = &small;
        }
    }
    else if(0x100 < size && size < 0x1000){
        for(k = 0; k < many; k++){
            *(int*)(heapArray[2 * (i+k)] + size) = &middle;
        }
    }
    else if(0x1000 <= size && size <= 0x20000){
        for(k = 0; k < many; k++){
            *(int*)(heapArray[2 * (i+k)] + size) = &large;
        }
    }

    lastStartIndex = i;
    lastEndIndex = i + many - 1;
    printf("Your Box's index range is %d - %d\n", lastStartIndex, lastEndIndex);
    return ;
}

void Delete()
{
    int i;
    if(lastStartIndex < 0 || lastEndIndex > 0xfff || lastStartIndex > lastEndIndex){
        puts("Error in system...");
        return ;
    }
    for(i = lastStartIndex; i <= lastEndIndex; i++){
        free(heapArray[2 * i]);
        heapArray[2 * i + 1] = 0;
        heapArray[2 * i] = 0;
    }
    puts("Delete Done!!!");
    return ;
}

void Edit()
{
    int idx, size;
    printf("Edit Index >> ");
    idx = getNumber();
    if(idx < 0 || idx > 0xfff){
        puts("Index Error...");
        return;
    }
    size = heapArray[2*idx + 1];
    printf("content>> ");
    read_n(heapArray[2 * idx], size);

    return ;
}

void showContent()
{
    int i, sIndex, eIndex;
    printf("Start index >> ");
    sIndex = getNumber();
    printf("End index >> ");
    eIndex = getNumber();

    if(sIndex < 0 || sIndex > 0xfff || eIndex < 0 || eIndex > 0xfff || eIndex < sIndex)
    {
        puts("Index Error...");
        return;
    }
    for(i = sIndex; i <= eIndex; i++)
    {
        printf("%dth Box's Message: %s\n", i,  heapArray[2 * i]);
    }
    return;
}

void showTag()
{
    int index, value;
    int *tag;

    printf("Which index>> ");
    index = getNumber();

    if((index < 0) || (index > 0xfff) || !heapArray[2*index]){
        puts("Wrong index...");
        return;
    }
    //tag value
    tag = *(int*)(heapArray[2*index] + heapArray[2*index + 1]);
    value = *tag;
    if(value){
        *tag = value - 1;
    }
    //avoid crash
    else{
        (*(void(**)(void))((int)tag + 4))();
    }

    return;
}

void menu()
{
    puts("1. Create Some Message Boxs");
    puts("2. Edit A Message Box");
    puts("3. Delete A Message Box");
    puts("4. Show Some Message Box");
    puts("5. Show Tag Of A Box");
    puts("6. Exit");
    printf(">> ");
}

int getNumber()
{
    char buf[0x10];
    read_n(buf, 0x10);
    return atoi(buf);
}

void read_n(char* buf, int size)
{
    int readn;
    int idx = 0;
    char tmp;
    while(idx < size)
    {
        readn = read(0, &tmp, 1);

        if(readn <=0 ){
            puts("Broken Read!!!");
            exit(1);
        }

        if(tmp == 10){
            *(buf + idx) = 0;
            break;
        }
        *(buf + idx) = tmp;
        idx += 1;
    }
    //null end
    *(buf + size - 1) = 0;
}
void initBuf()
{
    srand(0);
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    int rdSize = 0x500 + (rand() % 0x500);
    malloc(rdSize);
    return ;
}

void smallBox()
{
    puts("emmm...");
    puts("i am a small box!");
    return ;
}

void middleBox()
{
    puts("hhh...");
    puts("i am a middle box!");
    return ;
}

void largeBox()
{
    puts("kkk...");
    puts("i am a large box!");
    return ;
}