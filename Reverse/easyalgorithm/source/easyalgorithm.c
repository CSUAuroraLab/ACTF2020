#include<stdio.h>
#include<stdlib.h>
#include<stddef.h>
#include<memory.h>


typedef unsigned char BYTE;

/*********************** FUNCTION DECLARATIONS **********************/
// Input: state - the state used to generate the keystream
//        key - Key to use to initialize the state
//        len - length of key in bytes (valid lenth is 1 to 256)
void arcfour_key_setup(BYTE state[],  BYTE key[], int len);

// Pseudo-Random Generator Algorithm
// Input: state - the state used to generate the keystream
//        out - Must be allocated to be of at least "len" length
//        len - number of bytes to generate
void arcfour_generate_stream(BYTE state[], BYTE out[], size_t len);

void arcfour_key_setup(BYTE state[],  BYTE key[], int len)
{
	int i, j;
	BYTE t;
	//printf("%s\n",key);

	for (i = 0; i < 256; ++i)
		state[i] = i;
	for (i = 0, j = 0; i < 256; ++i) {
		j = (j + state[i] + key[i % len]) % 256;
		t = state[i];
		state[i] = state[j];
		state[j] = t;
	}
}

// This does not hold state between calls. It always generates the
// stream starting from the first  output byte.
void arcfour_generate_stream(BYTE state[], BYTE out[], size_t len)
{
	int i, j;
	size_t idx;
	BYTE t;

	for (idx = 0, i = 0, j = 0; idx < len; ++idx)  {
		i = (i + 1) % 256;
		j = (j + state[i]) % 256;
		t = state[i];
		state[i] = state[j];
		state[j] = t;
		out[idx] ^= state[(state[i] + state[j]) % 256];
		//printf("%d ",out[idx]);
	}
}

void func()
{

	BYTE state[256];
    BYTE key[4]={"ACTF"};

	char input[21];
	BYTE in[1024];
	BYTE enc_flag[15]={196,197,137,138,204,156,24,68,8,10,106,41,210,228,46};

	memset(state,0,256);
	memset(input,0,21);
	memset(in,0,1024);


	printf("Please input:");
	scanf("%s",input);
	

	if(input[0]!=65 || input[1]!=67 || input[2]!=84 || input[3]!=70 || input[4]!=123 || input[20]!=125)
    {
        return ;
    }
    else
    {
    	memcpy(in,input+5,15);

    }

    //printf("%s\n",in);

    arcfour_key_setup(state,key,4);
    //int i;
    //for (i = 0; i<256; i++)
    //{
        //printf("%02X", state[i]);
        //if ((i + 1) % 16 == 0)
        	//putchar('\n');
    //}
    //BYTE state2[256];
    //int i;
    //for(i=0;i<256;i++)
    	//state2[i]=state[i];
    arcfour_generate_stream(state,in,15);
    int i;
    for(i=0;i<15;i++){
    	if(in[i]!=enc_flag[i]){
    		printf("Error!");
    		return;
    	}
    }
    printf("Great!");
    //arcfour_generate_stream(state2,in,strlen(in));
    //printf("%s",in);
    //printf("%s",in);
}	


int main()
{
	func();
	return 0;
}