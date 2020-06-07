#include <bits/stdc++.h>
using namespace std;
class VM{
    int NO,store;
    char mem[256]={112,67,69,114,66,119,44,122,63,71, 94, 17, 68, 126, 97, 53, 122, 35, 126, 105, 71, 126, 17, 56, 36, 122, 7, 76, 91, 7, 105, 89, 68, 57, 103, 39,0};

public:
    void judge(char *inp){
        mainpart(inp);
        char comp[10];
        strncpy(comp,mem,9);
        comp[9]=0;
        if(strcmp(comp,"curiosity\0")==0){
            cout<<"Congratulations! The flag is: actf{";
            mainpart(inp);
            mainpart(inp);
            mainpart(inp);
            printf("%s}\n",mem+9);
        }
        else{
            cout<<"Incorrect incantation!Try again."<<endl;
        }
    }
    void mainpart(char *inp){
        int len=strlen(inp);
        for(int i=0;i<len;++i){
            switch(inp[i]){
                case 'F':mem[NO++]^=store;
                    break;
                case 'C':store++;
                    break;
                case 'J':store=((store>>2)|(store<<6))&255;
                    break;
                case 'M':store=((store<<3)|(store>>5))&255;
                    break;
                case 'K':store=mem[256-NO];
                    break;
                case 'X':store=store>>1&127;
                    break;
                default: puts("Error operation!");exit(0);
            }
        }
    }

    VM(){
        NO=0;
        store=70;
        for(int i=1;i<=36;++i){
            mem[256-i]=(1<<(i%9))&255;
        }
    }
};
int main() {
    char inp[256];
    cout<<"Enter the Incantation:"<<endl;
    scanf("%s",inp);
    VM vm;
    vm.judge(inp);
    return 0;
}
