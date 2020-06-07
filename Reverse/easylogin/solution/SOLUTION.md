# easylogin

程序初看确实摸不着头脑，但是实际运行一下就会发现有"Incorrect,try again！"的弹窗。则可以根据此在IDA中进行字符串搜索，继而定位到程序主体，对user和password的判断部分。

虽然经过了一定的代码混淆，导致伪代码看起来不是很清晰，但是仔细推敲一下+动调一下跟踪一下数组变化，还是能看得出来哪些是判断部分。这里贴一下源码中关于这两段判断的代码，以供参考。

```cpp
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
```

所以我们就可以依照判断逻辑写出脚本解出用户名与密码，脚本见solution.py