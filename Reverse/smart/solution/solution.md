定位是一道比签到稍难一点的简单题，题目背景比较新，但实际内容很简单。

根据题目给出的链接可以拿到solidity字节码，后来考虑到给出的网站需要翻墙，所以直接提供了字节码。

![](D:\文档\理科文档\实验室\出题\2020校赛\final\smart\solution\Snipaste_2020-06-06_15-32-06.png)

将字节码直接扔到https://ethervm.io/decompile反编译

![](D:\文档\理科文档\实验室\出题\2020校赛\final\smart\solution\Snipaste_2020-06-06_15-39-23.png)

由于现在关于solidity的反编译技术还不是很成熟，所以代码看起来会比较奇怪，但是可以明显地看到一串很像flag的16进制串

![](D:\文档\理科文档\实验室\出题\2020校赛\final\smart\solution\Snipaste_2020-06-06_15-40-37.png)

再往下读，不难发现关键操作

![](D:\文档\理科文档\实验室\出题\2020校赛\final\smart\solution\Snipaste_2020-06-06_15-41-46.png)这里由于这个网站的技术问题。所以`^`操作被反编译为了`~`操作，如果接触过solidity反编译、用过这个网站的师傅会比较清楚，但如果猜不出来可以使用jeb decompiler 自带的反编译智能合约功能

![](D:\文档\理科文档\实验室\出题\2020校赛\final\smart\solution\Snipaste_2020-06-06_15-48-27.png)

当然还有一种最笨的方法，那就是根据给出的字节码，自己手动反编译

源码如下：

```solidity
pragma solidity ^0.4.25;

contract easyContract{

    
    function getflag() public pure returns (bytes){
        bytes32 seed=0xadafb8aab7a9adffb593ada2a893bfb8b9bcfda893affca2b8bea3adafb8b8b1;
        bytes memory flag=new bytes(seed.length);
        uint i;
        
        for(i=0;i<seed.length;i++){
            flag[i]=seed[i]^0xcc;
        }
        
        return flag;
    }

}
```

