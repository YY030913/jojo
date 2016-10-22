<?php 
defined('BASEPATH') OR exit('No direct script access allowed');
load_template('public/header',array(
  'title'        => $title
));
date_default_timezone_set("PRC");
?>

<!-- <?php
$rootdir=getcwd();
$rootdir=substr($rootdir, 0, strripos($rootdir, "/"));
$cmd = exec("python ".getcwd()."／spider/main.py --config ".getcwd()."/spider/config.json");
?> -->
<style>
#top-search-bar{border-collapse:separate;border-spacing:2px;background:#f1f1f1;border-bottom:1px solid #e5e5e5;padding:10px 0;position:relative;}
#logo{height:35px;width:115px;display:block;left:10px;top:20px;position:absolute;background:url(<?php echo base_url('static/img/logo-bar.png') ?>);}
body{font-family: arial,sans-serif;}
@media (min-width:992px) {.container {margin-left:130px;}}
.link a{color:#545454}
@media (max-width:992px){#logo{display:none;}}
#search-bar a{padding:5px 10px;margin-right:5px;}
td,th{ white-space:nowrap;text-overflow:ellipsis; overflow:hidden;max-width:150px}
</style>
<div class="container" style="margin-top: 30px">
	<div class="row">
		<div class="col-md-12">
			<!-- <script type="text/javascript">(function(){document.write(unescape('%3Cdiv id="bdcs"%3E%3C/div%3E'));var bdcs = document.createElement('script');bdcs.type = 'text/javascript';bdcs.async = true;bdcs.src = 'http://znsv.baidu.com/customer_search/api/js?sid=7998786979103457666' + '&plate_url=' + encodeURIComponent(window.location.href) + '&t=' + Math.ceil(new Date()/3600000);var s = document.getElementsByTagName('script')[0];s.parentNode.insertBefore(bdcs, s);})();</script> -->

			<div class="panel panel-default">
			  <div class="panel-heading">影视</div>
			  <div class="panel-body">
			  	<table class="table">
					<tr>
						<th>标题</th>
						<th>分享时间</th>
						<th>豆瓣评分</th>
					</tr>
					<?php foreach($videos as $i):?>
						<tr>
							<td><a target="_blank" href="<?php echo $i['link']?>"><img src="<?php echo $i['cover_img']?>" alt="<?php echo $i['title']?>"><h1><?php echo $i['title']?></h1></a></td>
							<td><?php echo timeago($i['feed_time']) ?></td>
							<td><a arget="_blank" href="<?php echo $i['douban_url']?>"><?php echo ($i['douban_score']) ?></a></td>
						</tr>
					<?php endforeach; ?>
				</table>
				<?php 
					echo $page
				?>
			  </div>
			</div>
		</div>

	</div>
</div>
<?php
load_template('public/leftsead');
load_template('public/js');
load_template('public/footer');
?>
