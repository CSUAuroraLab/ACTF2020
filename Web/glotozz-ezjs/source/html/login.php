<?php
	//懒得写数据库啦~~~
    header("Content-Type: text/html;charset=utf-8");
	if ($_POST['username'] === "admin" && $_POST['password'] === '087bdf4c11317af76020ea61c1026439'){
		$status = "flag_here";//登录成功
	}else{
		$status = 0;//登录失败
	}
	echo json_encode($status);//将返回结果转为json格式
?>