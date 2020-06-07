<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
    <title>Bootstrap 101 Template</title>

    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim 和 Respond.js 是为了让 IE8 支持 HTML5 元素和媒体查询（media queries）功能 -->
    <!-- 警告：通过 file:// 协议（就是直接将 html 页面拖拽到浏览器中）访问页面时 Respond.js 不起作用 -->
    <!--[if lt IE 9]>
      <script src="https://cdn.jsdelivr.net/npm/html5shiv@3.7.3/dist/html5shiv.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/respond.js@1.4.2/dest/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <h1>你好，ctfer，来签个到，准备好字典了吗！</h1>
    <hr>
    <div class="container">
        <form>
          <div class="form-group">
            <label>username</label>
            <input type="username" class="form-control" id="username">
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" class="form-control" id="password">
          </div>
          <button id="login" class="btn btn-primary">Submit</button>
          
        </form>
    </div> <!-- /container -->
    <!-- jQuery (Bootstrap 的所有 JavaScript 插件都依赖 jQuery，所以必须放在前边) -->
    <script src="https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js"></script>
    <!-- 加载 Bootstrap 的所有 JavaScript 插件。你也可以根据需要只加载单个插件。 -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js"></script>
    <script src="./mymd5.js"></script>
    <script>
        $(function(){
      //jQuery中的oncilck点击事件，'#login'为选择id为login的元素
          $('#login').on('click', function(){
              var username = $('#username').val(); 
              var password = vdsSetCipher('password', 'gqyyy');
              $.ajax({
                type: 'POST',
                url: "login.php",
                data: {username: username, password: password},
                dataType: 'json',
                success: function(status){
                  if (status == 0) {
                      alert("登录失败");
                  } else {
                      alert(status);
                  }
                }
              });
            })
         })
    </script>
  </body>
</html>