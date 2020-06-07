// EasyLogin.cpp : 定义应用程序的入口点。
//

#include "framework.h"
#include "EasyLogin.h"
#include  "windowsx.h"

#define MAX_LOADSTRING 100

// 全局变量:
HINSTANCE hInst;                                // 当前实例
WCHAR szTitle[MAX_LOADSTRING];                  // 标题栏文本
WCHAR szWindowClass[MAX_LOADSTRING];            // 主窗口类名
HWND hdlg = NULL;
WCHAR userText[MAX_LOADSTRING];
WCHAR passwordText[MAX_LOADSTRING];
WCHAR test1[] = { 73, 42, 4, 2, 17,0};
WCHAR test2[] = { 67, 63, 74, 15, 109, 121, 121, 103, 100, 115, 7, 60, 57, 104, 64, 93, 85, 12, 60, 123, 64, 18, 35, 109, 115, 93, 122, 89, 31, 14, 35, 126,0 };
WCHAR radnir[] = { 82, 110, 123, 53, 34, 80, 70, 92, 64, 108, 56, 29, 36, 126, 108, 34, 70, 29 };
// 此代码模块中包含的函数的前向声明:
ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);
LRESULT CALLBACK    FormViewProc(HWND, UINT, WPARAM, LPARAM);
BOOL userCheck(WCHAR*);
BOOL passwordCheck(WCHAR*);

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPWSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);

    // TODO: 在此处放置代码。

    // 初始化全局字符串
    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_EASYLOGIN, szWindowClass, MAX_LOADSTRING);
    MyRegisterClass(hInstance);

    // 执行应用程序初始化:
    if (!InitInstance (hInstance, nCmdShow))
    {
        return FALSE;
    }

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_EASYLOGIN));

    MSG msg;

    // 主消息循环:
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }

    return (int) msg.wParam;
}



//
//  函数: MyRegisterClass()
//
//  目标: 注册窗口类。
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
    WNDCLASSEXW wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style          = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc    = WndProc;
    wcex.cbClsExtra     = 0;
    wcex.cbWndExtra     = 0;
    wcex.hInstance      = hInstance;
    wcex.hIcon          = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_EASYLOGIN));
    wcex.hCursor        = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
    wcex.lpszMenuName   = MAKEINTRESOURCEW(IDC_EASYLOGIN);
    wcex.lpszClassName  = szWindowClass;
    wcex.hIconSm        = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

    return RegisterClassExW(&wcex);
}

//
//   函数: InitInstance(HINSTANCE, int)
//
//   目标: 保存实例句柄并创建主窗口
//
//   注释:
//
//        在此函数中，我们在全局变量中保存实例句柄并
//        创建和显示主程序窗口。
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hInst = hInstance; // 将实例句柄存储在全局变量中

   HWND hWnd = CreateWindowW(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
      0, 0, 370, 300, nullptr, nullptr, hInstance, nullptr);

   if (!hWnd)
   {
      return FALSE;
   }

   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}

//
//  函数: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  目标: 处理主窗口的消息。
//
//  WM_COMMAND  - 处理应用程序菜单
//  WM_PAINT    - 绘制主窗口
//  WM_DESTROY  - 发送退出消息并返回
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)
    {
    case WM_COMMAND:
        {
            int wmId = LOWORD(wParam);
            // 分析菜单选择:
            switch (wmId)
            {
            case IDM_ABOUT:
                DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
                break;
            case IDM_EXIT:
                DestroyWindow(hWnd);
                break;
            default:
                return DefWindowProc(hWnd, message, wParam, lParam);
            }
        }
        break;
    case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);
            // TODO: 在此处添加使用 hdc 的任何绘图代码...
            //const WCHAR *notice = L"Enter your password:";

            EndPaint(hWnd, &ps);
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    case WM_CREATE:
        //build dialog
        
        hdlg = CreateDialog(hInst, MAKEINTRESOURCE(IDD_FORMVIEW), hWnd, (DLGPROC)FormViewProc);
        ShowWindow(hdlg, SW_SHOWNA);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

// “关于”框的消息处理程序。
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}

LRESULT FormViewProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message)
    {
    case WM_COMMAND: {
        int wmId = LOWORD(wParam);
        switch (wmId)
        {
        case IDC_EDIT_USER: {
            int ctrlCode = HIWORD(wParam);
            Edit_LimitText((HWND)lParam, 5);
            if (ctrlCode == EN_CHANGE) {
                int nChar = GetWindowTextLength((HWND)lParam);
                Edit_GetText((HWND)lParam, userText, nChar + 1);
                if (userText[nChar - 1] < '0' || (userText[nChar - 1] > '9' && userText[nChar - 1] < 'A') || (userText[nChar - 1] > 'Z' && userText[nChar - 1] < 'a') || userText[nChar - 1]>'z') {
                    userText[nChar - 1] = '\0';
                    Edit_SetText((HWND)lParam, userText);
                    Edit_SetSel((HWND)lParam,nChar - 1, nChar - 1);
                }
                                    
                
            }
            break;
        }
        case IDC_EDIT_PASSWD: {
            int ctrlCode = HIWORD(wParam);
            Edit_LimitText((HWND)lParam, 100);
            if (ctrlCode == EN_CHANGE) {
                int nChar = GetWindowTextLength((HWND)lParam);
                Edit_GetText((HWND)lParam, passwordText, nChar + 1);
                
            }
            break;
        }
        case IDC_BUTTON_CHECK: {
            if (userCheck(userText)) {
                if (passwordCheck(passwordText)) {
                    WCHAR cong[256];
                    swprintf(cong, 256, L"you got the correct password!\n the flag is flag{%s}", passwordText);

                    MessageBoxW((HWND)hdlg, cong, L"Congratulations", MB_OK);
                }
                else {
                    MessageBox((HWND)hdlg, L"Incorrect password!try again!" , NULL, MB_OK);
                }
            }
            else {
                MessageBox((HWND)hdlg, L"Incorrect user!try again!", NULL, MB_OK);
            }
        }
        default:
            break;
        }
    }
    }
    return 0;
}
BOOL userCheck(WCHAR* user) {
    int len = wcslen(user)+1;
    for (int i = 0; i < len - 1; ++i) {
        if (((user[i]+1) ^ user[(i + len - 1) % len]) != test1[i])
            return false;
    }
    
    return true;
}
BOOL passwordCheck(WCHAR* password) {
    int len1 = wcslen(userText);
    int len2 = wcslen(radnir);
    int len3 = wcslen(password);
    WCHAR tmp1[256];
    for (int i = 0; i < len2; ++i) {
        tmp1[i] = radnir[i] ^ userText[i % len1];
    }
    if (len3 != wcslen(test2)) return false;
    for (int i = 0; i < len3; ++i) {
        if (test2[i] != (~(password[i] & tmp1[i % len2]) & (password[i] | tmp1[i % len2])))
            return false;
    }
    return true;
}