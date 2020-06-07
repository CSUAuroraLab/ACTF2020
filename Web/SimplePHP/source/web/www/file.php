<?php 
header("content-type:text/html;charset=utf-8");  
include 'function.php'; 
include 'class.php';
$file = $_GET["file"] ? $_GET['file'] : "";
$high_light = $_GET["high_light"] ? $_GET['high_light'] : "";

if(empty($file)) { 
    echo "<h2>There is no file to show!<h2/>"; 
}

if(preg_match('/http|https|file:|gopher|dict|php|zip|\.\/|\.\.|flag/i',$file) || preg_match('/http|https|file:|gopher|dict|zip|\.\/|\.\.|flag/i',$high_light)) {
            die('hacker!');
}

if(strtolower(substr($file,0,4))=='phar' || strtolower(substr($high_light,0,4))=='phar'){
            die('hacker!');
}

if(!preg_match('/\//i',$file))
{
    die('hacker!');
}
highlight_file($high_light);

$show = new Show();

if(file_exists($file)) { 
    $show->source = $file; 
    $show->_show(); 
} else if (!empty($file)){ 
    die('file doesn\'t exists.'); 
}

?> 