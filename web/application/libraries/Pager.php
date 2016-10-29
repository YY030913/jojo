<?php   
defined('BASEPATH') OR exit('No direct script access allowed');
/*  
 * PHP分页类  
 * @package Page  
 * @Created 2013-03-27  
 * @Modify  2013-03-27  
 * @link http://www.60ie.net  
 * Example:  
       $myPage=new Pager(1300,intval($CurrentPage));  
       $pageStr= $myPage->GetPagerContent();  
       echo $pageStr;  
 */  
class Pager {   
    private $pageSize = 10;   
    private $pageIndex;   
    private $totalNum;   

    private $totalPagesCount;   

    private $pageUrl;   
    private static $_instance;   

    public function __construct($parm) {   
        print_r($parm);
        $p_totalNum = $parm['totalNum'];
        $p_pageIndex = $parm['pageIndex'];
        $p_pageSize = isset($parm['pageSize']) || 10;
        $p_initNum = isset($parm['initNum']) || 3;
        $p_initMaxNum = isset($parm['initMaxNum']) || 5;
        if (! isset ( $p_totalNum ) || !isset($p_pageIndex)) {   
            die ( "pager initial error" );   
        }   

        $this->pageUrlPrefix = '/page-';   

        $this->totalNum = $p_totalNum;   
        $this->pageIndex = $p_pageIndex;   
        $this->pageSize = $p_pageSize;   
        $this->initNum=$p_initNum;   
        $this->initMaxNum=$p_initMaxNum;   
        $this->totalPagesCount= ceil($p_totalNum / $p_pageSize);   
        $this->pageUrl=$this->_getPageUrl();   

         $this->_initPagerLegal();   
    }   

       
  /**  
    * 获取去除page部分的当前URL字符串  
    *  
    * @return String URL字符串  
    */  
  private function _getPageUrl() {   
        // $CurrentUrl = $_SERVER["REQUEST_URI"];   
        // $arrUrl     = parse_url($CurrentUrl);   
        // if(isset($arrUrl["query"])){
        //   $urlQuery   = $arrUrl["query"];   
        // }
        

        // if(isset($urlQuery)){   
        //     $urlQuery  = preg_replace("/(^|&)page=" . $this->pageIndex."/", "", $urlQuery);   
        //     $CurrentUrl = str_replace($arrUrl["query"], $urlQuery, $CurrentUrl);   

        //     if($urlQuery){   
        //          $CurrentUrl.="&page";   
        //     }   
        //     else $CurrentUrl.="page";   

        // } else {   
        //     $CurrentUrl.="?page";   
        // }   
        // return $CurrentUrl;
    return '/page-'.$this->pageIndex.'html';   

  }   
  /*  
   *设置页面参数合法性  
   *@return void  
  */  
  private function _initPagerLegal()   
  {   
      if((!is_numeric($this->pageIndex)) ||  $this->pageIndex<1)   
      {   
          $this->pageIndex=1;   
      }elseif($this->pageIndex > $this->totalPagesCount)   
      {   
          $this->pageIndex=$this->totalPagesCount;   
      }   

         

  }   
//$this->pageUrl}={$i}   
//{$this->CurrentUrl}={$this->TotalPages}   
    public function GetPagerContent() {  
		$str = <<<EOD
<style>

	.Pagination a {margin-left:2px;padding:2px 7px 2px;}   

	.Pagination .dot{ border:medium none; padding:4px 8px}   

	.Pagination a:link, .Pagination a:visited {border:1px solid #dedede;color:#696969;text-decoration:none;}   

	.Pagination a:hover, .Pagination a:active, .Pagination a.current:link, .Pagination a.current:visited {border:1px solid #dedede;color:#fff; background-color:#ff6600; background-image:none; border:#ff6600 solid 1px;}   

	.Pagination .selectBar{ border:#dedede solid 1px; font-size:12px; width:95px; height:21px; line-height:21px; margin-left:10px; display:inline}   

	.Pagination a.tips{_padding:4px 7px 1px;}   
</style>
EOD;
        $str.= "<ul class=\"pagination\">";   
        //首页 上一页   
        if($this->pageIndex==1)   
        {   
            $str .="<li><a href='javascript:void(0)' class='tips' title='首页'>首页</a></li> "."\n";   
            $str .="<li><a href='javascript:void(0)' class='tips' title='上一页'>上一页</a></li> "."\n"."\n";   
        }else  
        {   
            // $str .="<li><a href='{$this->pageUrl}=1' class='tips' title='首页'>首页</a></li> "."\n";   
            //         $str .="<li><a href='{$this->pageUrl}=".($this->pageIndex-1)."' class='tips' title='上一页'>上一页</a></li> "."\n"."\n";   

            $str .="<li><a href='{$this->pageUrlPrefix}1.html' class='tips' title='首页'>首页</a></li> "."\n";   
                    $str .="<li><a href='{$this->pageUrlPrefix}".($this->pageIndex-1).".html' class='tips' title='上一页'>上一页</a></li> "."\n"."\n";   

            
        }   


           

        /*  

        除首末后 页面分页逻辑  

        */  
         //10页（含）以下   
         $currnt="";   
         if($this->totalPagesCount<=10)   
         {   

            for($i=1;$i<=$this->totalPagesCount;$i++)   

            {   
                       if($i==$this->pageIndex)   
                       {    $currnt=" class='active'";}   
                       else  
                       {    $currnt="";    }   
                        $str .="<li {$currnt}><a href='{$this->pageUrlPrefix}{$i}".".html'>$i</a></li>"."\n" ;   
            }   
         }else                                //10页以上   
         {   if($this->pageIndex<3)  //当前页小于3   
             {   
                     for($i=1;$i<=3;$i++)   
                     {   
                         if($i==$this->pageIndex)   
                           {    $currnt=" class='active'";}   
                         else  
                         {    $currnt="";    }   
                        $str .="<li {$currnt}><a href='{$this->pageUrlPrefix}{$i}".".html'>$i</a></li>"."\n" ;   
                     }   

                     $str.="<li><span class=\"dot\">……</span></li>"."\n";   

                 for($i=$this->totalPagesCount-3+1;$i<=$this->totalPagesCount;$i++)//功能1   
                 {   
                      $str .="<li><a href='{$this->pageUrlPrefix}{$i}".".html' >$i</a></li>"."\n" ;   

                 }   
             }elseif($this->pageIndex<=5)   //   5 >= 当前页 >= 3   
             {   
                 for($i=1;$i<=($this->pageIndex+1);$i++)   
                 {   
                      if($i==$this->pageIndex)   
                       {    $currnt=" class='active'";}   
                       else  
                       {    $currnt="";    }   
                        $str .="<li {$currnt}><a href='{$this->pageUrlPrefix}{$i}".".html '>$i</a></li>"."\n" ;   

                 }   
                 $str.="<li><span class=\"dot\">……</span></li>"."\n";   

                 for($i=$this->totalPagesCount-3+1;$i<=$this->totalPagesCount;$i++)//功能1   
                 {   
                      $str .="<li><a href='{$this->pageUrlPrefix}{$i}".".html' >$i</a></li>"."\n" ;   

                 }   

             }elseif(5<$this->pageIndex  &&  $this->pageIndex<=$this->totalPagesCount-5 )             //当前页大于5，同时小于总页数-5   

             {   

                 for($i=1;$i<=3;$i++)   
                 {   
                     $str .="<li><a href='{$this->pageUrlPrefix}{$i}".".html' >$i</a></li>"."\n" ;   
                 }   
                  $str.="<li><span class=\"dot\">……</span></li>";                
                 for($i=$this->pageIndex-1 ;$i<=$this->pageIndex+1 && $i<=$this->totalPagesCount-5+1;$i++)   
                 {   
                       if($i==$this->pageIndex)   
                       {    $currnt=" class='active'";}   
                       else  
                       {    $currnt="";    }   
                        $str .="<li {$currnt}><a href='{$this->pageUrlPrefix}{$i}".".html'>$i</a></li>"."\n" ;   
                 }   
                 $str.="<li><span class=\"dot\">……</span></li>";   

                 for($i=$this->totalPagesCount-3+1;$i<=$this->totalPagesCount;$i++)   
                 {   
                      $str .="<li><a href='{$this->pageUrlPrefix}{$i}".".html' >$i</a></li>"."\n" ;   

                 }   
             }else  
             {   

                  for($i=1;$i<=3;$i++)   
                 {   
                     $str .="<li><a href='{$this->pageUrlPrefix}{$i}".".html' >$i</a></li>"."\n" ;   
                 }   
                  $str.="<li><span class=\"dot\">……</span></li>"."\n";   

                  for($i=$this->totalPagesCount-5;$i<=$this->totalPagesCount;$i++)//功能1   
                 {   
                       if($i==$this->pageIndex)   
                       {    $currnt=" class='active'";}   
                       else  
                       {    $currnt="";    }   
                        $str .="<li {$currnt}><a href='{$this->pageUrlPrefix}{$i}".".html'>$i</a></li>"."\n" ;   

                 }   
            }          

         }   

            

            
        /*  

        除首末后 页面分页逻辑结束  

        */  

        //下一页 末页   
        if($this->pageIndex==$this->totalPagesCount)   
        {      
            $str .="\n"."<li><a href='javascript:void(0)' class='tips' title='下一页'>下一页</a></li>"."\n" ;   
            $str .="<li><a href='javascript:void(0)' class='tips' title='末页'>末页</a></li>"."\n";   

               
        }else  
        {   
            $str .="\n"."<li><a href='{$this->pageUrlPrefix}".($this->pageIndex+1).".html' class='tips' title='下一页'>下一页</a></li> "."\n";   
            $str .="<li><a href='{$this->pageUrlPrefix}{$this->totalPagesCount}".".html' class='tips' title='末页'>末页</a></li> "."\n" ;   
        }          

        $str .= "</ul>";   
        return $str;   
    }   

  

  
/**  
 * 获得实例  
 * @return    
 */  
//  static public function getInstance() {   
//      if (is_null ( self::$_instance )) {   
//          self::$_instance = new pager ();   
//      }   
//      return self::$_instance;   
//  }   

  
}   
?>   