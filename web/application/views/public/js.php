<script src="http://cdn.bootcss.com/jquery/1.11.2/jquery.min.js"></script>
<script src="<?php echo site_url('static/js/bootstrap.min.js')?>"></script>
<script charset="gbk" src="http://www.baidu.com/js/opensug.js"></script>
<script src="<?php echo site_url('static/js/base64.min.js'); ?>"></script>
<script type="text/javascript">
function full_screen(){
    var docElm = document.documentElement;
	//W3C 
	if (docElm.requestFullscreen) 
		docElm.requestFullscreen();
	//FireFox 
	else if(docElm.mozRequestFullScreen)
		docElm.mozRequestFullScreen();
	//Chrome等 
	else if(docElm.webkitRequestFullScreen)
		docElm.webkitRequestFullScreen();
	//IE11
	else if(elem.msRequestFullscreen)
		elem.msRequestFullscreen();
}
function exit_full_screen(){
    if (document.exitFullscreen)
		document.exitFullscreen();
	else if(document.mozCancelFullScreen)
		document.mozCancelFullScreen();
	else if(document.webkitCancelFullScreen)
		document.webkitCancelFullScreen(); 
	else if (document.msExitFullscreen)
		document.msExitFullscreen();
}


var siteChannelServiceUrl = "http://service.channel.mtime.com";

function getSearchResult(j, l, h, i, k, g) {
	return Mtime.Component.Ajax.crossDomainCallBack(siteChannelServiceUrl, "Mtime.Channel.Services", "GetSearchResult", [j, l, h, i, k], g, "/Search.api", "get", "60000", null);
}

$(function(){
	$("#s-form").submit(function(e){
	    e.preventDefault();
	    var kw = $('#q').val();
	    if(!kw){
	        $('#q').focus();
	        return false;
	    }
	    var type = $("#type").val();
	    var url = '<?php echo site_url('s') ?>'+'/'+encodeURIComponent(Base64.encode(kw))+'?from=sf&type='+type;
	    window.location = url;
	    return false;
	});
	$(function(){
		$("#fulls").click(function(){
			if($(this).hasClass("on")){
				$(this).removeClass("on").addClass("off").text("开启全屏");
				exit_full_screen();
			}else{
				$(this).removeClass("off").addClass("on").text("关闭全屏");
				full_screen();
			}		
		});
	});
	console.log($(".moviename"));
	for (var i = 0; i <= $(".moviename").length - 1; i++) {
		console.log($(".moviename a").txt());
	}

	$("#leftsead a").hover(function(){

		if($(this).prop("className")=="youhui"){

			$(this).children("img.hides").show();

		}else{

			$(this).children("img.hides").show();

			$(this).children("img.shows").hide();

			$(this).children("img.hides").animate({marginRight:'0px'},'slow'); 

		}

	},function(){ 

		if($(this).prop("className")=="youhui"){

			$(this).children("img.hides").hide('slow');

		}else{

			$(this).children("img.hides").animate({marginRight:'-143px'},'slow',function(){$(this).hide();$(this).next("img.shows").show();});

		}

	});

})



</script>