<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN">
<head>
<?php
if(isset($title))
  echo "<title>".htmlspecialchars($title)."电影资源|网盘资源|豆瓣电影评分|在线观看</title>";
else
  echo "<title>".$this->config->item('site_title')."</title>";   

if(isset($keywords))
  echo meta('keywords', htmlspecialchars($keywords));
if(isset($description))
  echo meta('description', htmlspecialchars($description));

echo link_tag('static/css/bootstrap.min.css');
echo link_tag('static/css/style.css?v=1.0');
?>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=yes">
<meta name="HandheldFriendly" content="true">
<meta name="baidu-site-verification" content="lnrw6T2nxa" />
<meta name="robots" content="all" />
<meta name="author" content="肖雨" />
<meta name="title" content="百度-电影资源" />
<meta name="google" content="all" />
<meta name="googlebot" content="all" />

<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "//hm.baidu.com/hm.js?d6f2cc959fca88c3caee40f7b97e53bc";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>

<script>
(function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') {
        bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';        
    }
    else {
        bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    }
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(bp, s);
})();
</script>
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top" style="font-size:13px">
    <div class="container-fluid">
      <div class="navbar-header">
        <a style="float: left;text-decoration: none;
    height: 50px;
    padding: 15px 15px;
    font-size: 18px;
    line-height: 20px;color: #fff;" href="<?php echo site_url() ?>" title="返回网盘搜索">caoliao.net.cn</a>
        <button style="height: 50px;" type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
      </div>

      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav">
        </ul>
      </div>
    </div>
</nav>
