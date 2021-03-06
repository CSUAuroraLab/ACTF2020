// ConsoleApplication4.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <Windows.h>
#include <tchar.h>
#include <stdio.h>


#define DEF_MUTEX_NAME      L"Debug_Blocker"

void DoParentProcess();
void DoChildProcess();


void _tmain(int argc, TCHAR *argv[])
{
	HANDLE hMutex = NULL;

	if (!(hMutex = CreateMutex(NULL, FALSE, DEF_MUTEX_NAME)))
	{
		printf("CreateMutex() failed! [%d]\n", GetLastError());
		return;
	}

	// check mutex 
	if (ERROR_ALREADY_EXISTS != GetLastError())
		DoParentProcess();
	else
		DoChildProcess();
}


void DoChildProcess()
{
	// 8D C0 ("LEA EAX, EAX") 말도 안되는 명령어
	// 명령어 길이 (0x17)
	__asm
	{
		nop
		nop
	}

	//MessageBox(NULL, L"ChildProcess", L"TEST", MB_OK);
	HMODULE exe = GetModuleHandleA(0);
	WCHAR subKey[256];
	WCHAR value[256];
	WCHAR data[256];

	WCHAR enc_flag[25] = { 0x19,0x35,0x40,0x74,0x3,0x13,0x55,0x21,0x1,0x9,0x70,0x77,0x1a,0x23,0x53,0x4d,0x3a,0x67,0x5b,0x71,0x13,0x33,0x46,0x6f,0 };
	int i = 0;
	WCHAR *penc_flag = enc_flag;

	long err;
	DWORD dataType;

	LPWSTR psubKey = (LPWSTR)subKey;
	LPWSTR pvalue = (LPWSTR)value;
	PVOID pdata = (PVOID)data;
	DWORD size = sizeof(data);
	LPWSTR pvalue1 = pvalue;

	if (!LoadStringW(exe, 101, psubKey, 255))
		return ;

	if (!LoadStringW(exe, 102, pvalue, 255))
		return ;

	while (*pvalue1 != 0)
	{
		*pvalue1 ^= 0x30;
		//printf("%c", *pvalue1);
		pvalue1++;
	}

	err = RegGetValueW(HKEY_CURRENT_USER, (LPCWSTR)psubKey, (LPCWSTR)pvalue, 0xFFFF, &dataType, pdata, &size);

	if (err != ERROR_SUCCESS)
	{
		printf("No!");
		return ;
	}
	else
	{
		while (enc_flag[i])
		{
			printf("%c", (char)enc_flag[i] ^ *((char *)pdata + i % 4));
			i++;
		}

	}
}


void DoParentProcess()
{
	TCHAR                   szPath[MAX_PATH] = { 0, };
	STARTUPINFO				si = { sizeof(STARTUPINFO), };
	PROCESS_INFORMATION		pi = { 0, };
	DEBUG_EVENT             de = { 0, };
	CONTEXT                 ctx = { 0, };
	BYTE                    pBuf[0x34] = { 0, };
	DWORD                   dwExcpAddr = 0, dwExcpCode = 0;
	const DWORD             DECODING_SIZE = 0x28;
	const DWORD             DECODING_KEY = 0x7F;
	const DWORD             EXCP_ADDR_1 = 0x0040103F;
	const DWORD             EXCP_ADDR_2 = 0x00401050;

	// create debug process
	GetModuleFileName(
		GetModuleHandle(NULL),
		szPath,
		MAX_PATH);

	if (!CreateProcess(
		NULL,
		szPath,
		NULL, NULL,
		FALSE,
		DEBUG_PROCESS | DEBUG_ONLY_THIS_PROCESS,
		NULL, NULL,
		&si,
		&pi))
	{
		printf("CreateProcess() failed! [%d]\n", GetLastError());
		return;
	}

	//printf("Parent Process\n");

	// debug loop
	while (TRUE)
	{
		ZeroMemory(&de, sizeof(DEBUG_EVENT));

		if (!WaitForDebugEvent(&de, INFINITE))
		{
			printf("WaitForDebugEvent() failed! [%d]\n", GetLastError());
			break;
		}

		if (de.dwDebugEventCode == EXCEPTION_DEBUG_EVENT)
		{
			dwExcpAddr = (DWORD)de.u.Exception.ExceptionRecord.ExceptionAddress;
			dwExcpCode = de.u.Exception.ExceptionRecord.ExceptionCode;

			if (dwExcpCode == EXCEPTION_ILLEGAL_INSTRUCTION)
			{
				if (dwExcpAddr == EXCP_ADDR_1)
				{
					// decoding
					ReadProcessMemory(
						pi.hProcess,
						(LPCVOID)(dwExcpAddr + 0x11),
						pBuf,
						DECODING_SIZE,
						NULL);

					for (DWORD i = 0; i < DECODING_SIZE; i++)
						pBuf[i] ^= DECODING_KEY;

					WriteProcessMemory(
						pi.hProcess,
						(LPVOID)(dwExcpAddr + 0x11),
						pBuf,
						DECODING_SIZE,
						NULL);

					// change EIP
					ctx.ContextFlags = CONTEXT_FULL;
					GetThreadContext(pi.hThread, &ctx);
					ctx.Eip += 0x11;
					SetThreadContext(pi.hThread, &ctx);
				}
				/*else if (dwExcpAddr == EXCP_ADDR_2)
				{
					pBuf[0] = 0x68;
					pBuf[1] = 0x1C;
					WriteProcessMemory(
						pi.hProcess,
						(LPVOID)dwExcpAddr,
						pBuf,
						2,
						NULL);
				}*/
			}
		}
		else if (de.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT)
		{
			break;
		}

		ContinueDebugEvent(de.dwProcessId, de.dwThreadId, DBG_CONTINUE);
	}
}


/*

실습 파일을 완성시키기 위해서는

#1
OllyDbg 에서 DoChildProcess() NOP 2 byte 를 8D C0 으로 변경하고...
PUSH "Child Process" 명령어 앞 2 byte 를 8D C0 으로 변경...

#2
frhed 에서 DoChildProcess() 의 MessageBox() 호출 부분 20(0x14) byte 를 0x7F 로 XOR 인코딩한다.

*/

/*
int main()
{
	HMODULE exe = GetModuleHandleA(0);
	WCHAR subKey[256];
	WCHAR value[256];
	WCHAR data[256];

	WCHAR enc_flag[25] = { 0x19,0x23,0x46,0x7d,0xa,0x37,0x4f,0x41,0x17,0x25,0x5b,0x4d,0xb,0x3b,0x55,0x7e,0x14,0x9,0x5b,0x66,0xc,0x33,0x46,0x6f,0};
	int i = 0;
	WCHAR *penc_flag = enc_flag;

	long err;
	DWORD dataType;

	LPWSTR psubKey = (LPWSTR)subKey;
	LPWSTR pvalue = (LPWSTR)value;
	PVOID pdata = (PVOID)data;
	DWORD size = sizeof(data);
	LPWSTR pvalue1 = pvalue;

	if (!LoadStringW(exe, 101, psubKey, 255))
		return -1;

	if (!LoadStringW(exe, 102, pvalue, 255))
		return -1;

	while(*pvalue1!=0)
	{
		*pvalue1 ^= 0x30;
		//printf("%c", *pvalue1);
		pvalue1++;
	}

	err = RegGetValueW(HKEY_CURRENT_USER, (LPCWSTR)psubKey, (LPCWSTR)pvalue, 0xFFFF, &dataType, pdata, &size);

	if (err != ERROR_SUCCESS)
	{
		printf("No!");
		return -1;		
	}
	else
	{
		while(enc_flag[i])
		{
			printf("%c", (char)enc_flag[i] ^ *((char *)pdata+i%4));
			i++;
		}
		
	}


	/*HMODULE exe = GetModuleHandle(0);

	HKEY hKey = HKEY_CURRENT_USER;
	LPCWSTR subKey = L"Keyboard Layout\\Toggle";

	DWORD options = 0;
	REGSAM samDesired = KEY_READ;// | KEY_WRITE - need ?;

	HKEY OpenResult;

	LPCWSTR pValue = L"UltraMegaOtter";
	DWORD flags = RRF_RT_ANY;

	//Allocationg memory for a DWORD value.
	DWORD dataType;

	WCHAR value[255];
	PVOID pvData = value;

	DWORD size = sizeof(value);// not 8192;

	LONG err = RegOpenKeyEx(hKey, subKey, options, samDesired, &OpenResult);

	if (err != ERROR_SUCCESS)
	{
		wprintf(L"The %s subkey could not be opened. Error code: %x\n", subKey, err);
	}
	else
	{
		wprintf(L"Subkey opened!\n");
		err = RegGetValue(OpenResult, NULL, pValue, flags, &dataType, pvData, &size);

		if (err != ERROR_SUCCESS)
		{
			wprintf(L"Error getting value. Code: %x\n", err);
		}
		else
		{
			switch (dataType)
			{
			case REG_DWORD:
				wprintf(L"Value data: %x\n", *(DWORD*)pvData);
				break;
			case REG_SZ:
				//if ( !*((PWSTR)((PBYTE)pvData + size)-1) )
				wprintf(L"Value data: %s\n", (PWSTR)pvData);
				break;
				//...
			}
		}
		RegCloseKey(OpenResult);// don't forget !
	}

	return err;
	*/






