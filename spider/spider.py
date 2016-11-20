# -*- coding: utf-8 -*-
import urllib2,re,argparse,json,time
import MySQLdb as mdb
import metautils,traceback,Queue,socket
from HTMLParser import HTMLParser
from db.SQLiteHelper import SqliteHelper
from config import USER_AGENTS
import random
import ssl
import requests
import socks
import socket
import jieba
import re

ssl._create_default_https_context = ssl._create_unverified_context

DB_HOST='127.0.0.1'
DB_PORT='3306'
DB_USER='root'
# MySQL密码
DB_PASS='root'
# 数据库名称
DB_NAME='pan'

ERR_NO=0#正常
ERR_REFUSE=1#爬虫爬取速度过快，被拒绝
ERR_EX=2#未知错误
proxy = None
ONLYSIXTY = True

tags = ["独家","加拿大","TSKS","热门","英国","真人秀","分享","粤语","综艺","台湾","动漫","连载","奇幻","剧情","日本","最新","香港","罪案","经典","谍战","可播放","豆瓣高分","冷门佳片","华语","欧美","韩国","美国","网络","动作","喜剧","爱情","科幻","悬疑","恐怖","动画","美剧","英剧","韩剧","日剧","国产剧","港剧","日本动画"]

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock


def newIdentity():
        socks.setdefaultproxy()
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9051))
        s.send('AUTHENTICATE "my_password" \r\n')
        response = s.recv(128)
        if response.startswith("250"):
            s.send("SETCONF ExitNodes={in}\r\n")
            s.send("SETCONF StrictNodes=1\r\n")
            s.send("SIGNAL NEWNYM\r\n")
        s.close()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket

def checkproxy():
	sqlHelper = SqliteHelper()
	results = sqlHelper.selectAll()
	sqlcount = sqlHelper.selectCount()[0]

	global proxy
	if proxy:
		print proxy
	else:
		proxy=random.choice(results);
		print proxy;

	print "http://%s:%s"%(proxy[0],proxy[1])
	proxy_handler = urllib2.ProxyHandler({"http" : "http://%s:%s"%(proxy[0],proxy[1])})  
	opener = urllib2.build_opener(proxy_handler)
	urllib2.install_opener(opener)
	request = urllib2.Request("http://caoliao.net.cn")

	request.add_header('User-Agent', random.choice(USER_AGENTS))
	request.add_header('Referer',"http://www.baidu.com")
	urllib2.urlopen(request, timeout=60).read()
	proxy_handler = urllib2.ProxyHandler({}) # Pass empty dictionary to bypass proxy  
	opener = urllib2.build_opener(proxy)  
	urllib2.install_opener(opener)  

def getHtml(url,ref=None,reget=5):

	# try:
	# 	global proxy

	# 	checkproxy()
	# except Exception as e:
	# 	if proxy:
	# 		ip = proxy[0]
	# 		port = str(proxy[1])
	# 		condition = "ip='"+ip+"' AND "+'port='+port
	# 		sqlHelper = SqliteHelper()
	# 		sqlHelper.delete(SqliteHelper.tableName,condition)
	# 		proxy = None
	# 		if sqlHelper.selectCount()[0]>1:
	# 			return getHtml(url,ref,reget)
				
	try:
		# print urllib2.urlopen("http://icanhazip.com").read()
		# print urllib2.urlopen("http://caoliao.net.cn").read()

		request = urllib2.Request(url)

		request.add_header('User-Agent', random.choice(USER_AGENTS))
		if ref:
			request.add_header('Referer',ref)
		

		page = urllib2.urlopen(request,timeout=60)
		
		html = page.read()


	except:
		if reget>=1:
			# newIdentity()
			
			#如果getHtml失败，则再次尝试5次
			print 'getHtml error,reget...%d'%(reget)
			waittime=random.random()*60
			print "wait time %s"%waittime
			time.sleep(waittime)
			# print sqlcount
			
			return getHtml(url,ref,reget-1)
		else:
			# socks.setdefaultproxy()
			print 'request url:'+url
			print 'failed to fetch html'
			exit()
	else:
		return html

class mtimeDataParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.findUpCommingSlid = False
		self.data = ""
	#moreRegion li > img src/.filmscore p
	def handle_starttag(self, tag, attrs):
		if tag == 'strong':
			for (key, value) in attrs:
				if key == 'class' and value == 'll rating_num':
					self.findUpCommingSlid = True
					print "findUpCommingSlid"
					print self.findUpCommingSlid

	def handle_data(self, data):
		if self.findUpCommingSlid:
			self.data=data

	def handle_endtag(self, tag):
		if self.findUpCommingSlid and tag == 'strong':
			self.findUpCommingSlid = False

class Db(object):
	def __init__(self):
		self.dbconn=None
		self.dbcurr=None

	def check_conn(self):
		try:
			self.dbconn.ping()
		except:
			return False
		else:
			return True

	def conn(self):
		self.dbconn=mdb.connect(DB_HOST, DB_USER, DB_PASS,DB_NAME, charset='utf8')
		self.dbconn.autocommit(False)
		self.dbcurr = self.dbconn.cursor()

	def fetchone(self):
		return self.dbcurr.fetchone()

	def fetchall(self):
		return self.dbcurr.fetchall()

	def execute(self, sql, args=None,falg=False):
		if not self.dbconn:
			#第一次链接数据库
			self.conn()
		try:
			if args:
				rs=self.dbcurr.execute(sql,args)
			else:
				rs=self.dbcurr.execute(sql)
			return rs
		except Exception, e:
			if self.check_conn():
				print 'execute error'
				traceback.print_exc()
			else:
				print 'reconnect mysql'
				self.conn()
			if args:
					rs=self.dbcurr.execute(sql,args)
			else:
				rs=self.dbcurr.execute(sql)
		        return rs
	
	def commit(self):
		self.dbconn.commit()

	def rollback(self):
		self.dbconn.rollback()
	
	def close(self):
		self.dbconn.close()
		self.dbcurr.close()
	def last_row_id(self):
		return self.dbcurr.lastrowid


class BaiduPanSpider(object):
	def __init__(self):
		self.db=Db()
		self.files=[]
		self.got_files_count=0
		self.got_follow_count=0
		self.while_count=0
		self.spider_queue=Queue.Queue(maxsize=20)
		self.status='stop'
		self.errno=ERR_NO
		self.file_type_t={'video':0,'image':1,'document':2,'music':3,'package':4,'software':5,'torrent':6,'other':-1}

	def getShareUser(self,uk):
		url='http://yun.baidu.com/share/count?uk=%d&channel=chunlei&clienttype=0&web=1'%uk
		follows_json=json.loads(getHtml(url,uk))
		if follows_json['errno']!=0:
			if follows_json['errno']==-55:
				self.errno=ERR_REFUSE
			else:
				self.errno=ERR_EX
			return False
		return {
			'pubshare_cnt':follows_json['pubshare_cnt'],
			'fans':follows_json['fans'],
			'follow':follows_json['follow'],
			'album':follows_json['follows_json']
		}

	def getHotUser(self):
		url='http://yun.baidu.com/pcloud/friend/gethotuserlist?type=1&from=feed&start=0&limit=24&channel=chunlei&clienttype=0&web=1'
		follows_json=json.loads(getHtml(url))
		if follows_json['errno']!=0:
			print u'failed to fetch hot users'
			return False
		returns=[]
		count=0

		for item in follows_json['hotuser_list']:
			count=count+1
			hot_uname=item['hot_uname'].encode('utf-8')
			hot_uk=item['hot_uk']
			avatar_url=item['avatar_url'].encode('utf-8')
			intro=item['intro'].encode('utf-8')
			follow_count=item['follow_count']
			fans_count=item['fans_count']
			pubshare_count=item['pubshare_count']
			album_count=item['album_count']
			returns.append({'hot_uname':hot_uname,'hot_uk':hot_uk,'avatar_url':avatar_url,'intro':intro,'follow_count':follow_count,'fans_count':fans_count,'pubshare_count':pubshare_count,'album_count':album_count})
		
		if count==0:
			print "got no hot users"
			return False
		else:
			print "success to fetched hot users: %d"%count
		return returns

	def getFans(self,uk,start=0,limit=24):
		#query_uk:用户ID
		#limit:每一页最多显示数量
		#start:当前页数
		follows_url='http://yun.baidu.com/pcloud/friend/getfanslist?query_uk=%d&limit=%d&start=%d'%(uk,limit,start)
		follows_json=json.loads(getHtml(follows_url,uk))
		if follows_json['errno']!=0:
			print u'failed to fetch fens'
			return False
		total_count=follows_json['total_count']
		returns=[]
		count=0

		for item in follows_json['fans_list']:
			count=count+1
			fans_uname=item['fans_uname'].encode('utf-8')
			fans_uk=item['fans_uk']
			avatar_url=item['avatar_url'].encode('utf-8')
			intro=item['intro'].encode('utf-8')
			follow_count=item['follow_count']
			fans_count=item['fans_count']
			pubshare_count=item['pubshare_count']
			album_count=item['album_count']
			returns.append({'fans_uname':fans_uname,'fans_uk':fans_uk,'avatar_url':avatar_url,'intro':intro,'follow_count':follow_count,'fans_count':fans_count,'pubshare_count':pubshare_count,'album_count':album_count})

		return (total_count,count,returns)

	def getFollows(self,uk,start=0,limit=24):
		follows_url='http://yun.baidu.com/pcloud/friend/getfollowlist?query_uk=%d&limit=%d&start=%d&bdstoken=d82467db8b1f5741daf1d965d1509181&channel=chunlei&clienttype=0&web=1'%(uk,limit,start)
		ref='http://yun.baidu.com/pcloud/friendpage?type=follow&uk=%d&self=1'%uk
		follows_json=json.loads(getHtml(follows_url,ref))
		if follows_json['errno']!=0:
			print 'getFollows errno:%d'%follows_json['errno']
			print 'request_url:'+follows_url
			if follows_json['errno']==-55:
				self.errno=ERR_REFUSE
			else:
				self.errno=ERR_EX
			return False
		total_count=follows_json['total_count']
		returns=[]
		count=0
		if(total_count>0):
			for item in follows_json['follow_list']:
				count=count+1
				returns.append({
					'follow_uname':item['follow_uname'].encode('utf-8'),
					'follow_uk':item['follow_uk'],
					'avatar_url':item['avatar_url'].encode('utf-8'),
					'intro':item['intro'].encode('utf-8'),
					'follow_count':item['follow_count'],
					'fans_count':item['fans_count'],
					'pubshare_count':item['pubshare_count'],
					'album_count':item['album_count']
				})
		
		return (total_count,count,returns)

	def getShareLists(self,uk,start=0,limit=60):
		sharelists_url='http://yun.baidu.com/pcloud/feed/getsharelist?category=0&auth_type=1&request_location=share_home&start=%d&limit=%d&query_uk=%d&channel=chunlei&clienttype=0&web=1'%(start,limit,uk)
		ref='http://yun.baidu.com/share/home?uk=%d&view=share'%uk
		sharelists_json=json.loads(getHtml(sharelists_url,ref))

		if(sharelists_json['errno']!=0):
			print 'getShareLists errno:%d'%sharelists_json['errno']
			print 'request_url:'+sharelists_url
			if sharelists_json['errno']==-55:
				self.errno=ERR_REFUSE
			else:
				self.errno=ERR_EX
			return False
		total_count=sharelists_json['total_count']
		returns=[]
		count=0
		if total_count>0:
			for item in sharelists_json['records']:
				count=count+1
				feed_type=item['feed_type']
				isdir=0
				size=0
				md5=''
				album_id=''
				shorturl=''
				if feed_type=='share':
					if item['filecount']==1:
						filelist=item['filelist']
						isdir=filelist[0]['isdir']
						size=filelist[0]['size']
						md5=filelist[0]['md5']
					else:
						isdir=1
				elif feed_type=='album':
					album_id=item['album_id']
					isdir=2

				if item.has_key('shorturl'):
					shorturl=item['shorturl']

				if feed_type=='share' or feed_type=='album':
					returns.append({
						'title':item['title'].encode('utf-8'),
						'shorturl':shorturl,
						'shareid':item['source_id'],
						'feed_time':item['feed_time']//1000,#分享时间
						'dCnt':item['dCnt'],
						'isdir':isdir,
						'size':size,
						'md5':md5,
						'uk':uk,
						'feed_type':feed_type
					})
		return (total_count,count,returns)

	def getAlbum(self,uk,start=0,limit=60):
		url='http://yun.baidu.com/pcloud/album/getlist?start=%d&limit=%d&query_uk=%d&channel=chunlei&clienttype=0&web=1&bdstoken=d82467db8b1f5741daf1d965d1509181'%(start,limit,uk)
		album_json=json.loads(getHtml(url,uk))
		total_count=album_json['count']
		returns=[]
		count=0

		for item in album_json['album_list']:
			count=count+1
			title=item['title'].encode('utf-8')
			album_id=item['album_id']
			create_time=item['create_time']
			update_time=item['update_time']
			filecount=item['filecount']
			desc=item['desc']
			returns.append({'title':title,'album_id':album_id,'create_time':create_time,'desc':desc,'update_time':update_time,'filecount':filecount,'uk':uk})
		
		if count==0:
			print "get nothing"
			return False
		else:
			print "success to fetched : %d"%count

		if (start+count)<total_count:
			start=start+limit
			returns=returns+self.getAlbum(uk,start)
		return returns

	def seedUsers(self):
		hot_usrs=self.getHotUser()
		if not hot_usrs:
			return
		try:
			for user in hot_usrs:
				time_stamp=int(time.time())
				if user['pubshare_count']>0:
					self.db.execute(
						"REPLACE INTO share_users (uk,user_name,avatar_url,intro,follow_count,album_count,fens_count,pubshare_count,last_visited,create_time,weight) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
						(user['hot_uk'],user['hot_uname'],user['avatar_url'],user['intro'],user['follow_count'],user['album_count'],user['fans_count'],user['pubshare_count'],time_stamp,time_stamp,5)
					)
					uid=self.db.last_row_id()
					self.db.execute("REPLACE INTO spider_list (uk,uid) VALUES(%s,%s)",(user['hot_uk'],uid))
		except:
			traceback.print_exc()
			self.db.rollback()
		else:
			self.db.commit()
	
	def startSpider(self):
		# clear spider list
		spider.db.execute('DELETE FROM spider_list')

		fiveage=int(time.time())-3600*5*24
		spider.db.execute('DELETE FROM share_file where feed_time < %d'%(fiveage))

		# recreate spider list
		fetched_users=spider.db.execute('SELECT * from share_users ORDER BY uid desc')
		if fetched_users<0:
			print 'nothing to spider,spider_list is empty'
			return False
		fetchall=spider.db.fetchall()
		#将数据库中取出的待爬取的分享者，加入爬取队列
		for item in fetchall:
			spider.db.execute("REPLACE INTO spider_list (uk,uid,file_fetched,file_done,follow_done) VALUES(%s,%s,%s,%s,%s)",(item[2],item[0],0,0,item[14]))
			spider.db.commit()

		
			# start query
			if self.spider_queue.empty():
				fetched_users=self.db.execute('SELECT * from spider_list ORDER BY weight DESC limit 0,20')
				if fetched_users<=0:
					print 'nothing to spider,spider_list is empty'
					return False
				self.start='start'
				self.errno=ERR_NO
				fetchall=self.db.fetchall()
				#将数据库中取出的待爬取的分享者，加入爬取队列
				for item in fetchall:
					self.spider_queue.put({
					'sid':item[0],
					'uk':item[1],
					'file_fetched':item[2],
					'follow_fetched':item[3],
					'follow_done':item[4],
					'file_done':item[5],
					'weight':item[6],
					'uid':item[7]
				})
				self.got_follow_count=0
				self.got_files_count=0
				self.while_count=0
			time.sleep(random.random()*30)

			while not self.spider_queue.empty():
				self.while_count+=1
				share_user=self.spider_queue.get()
				#爬取分享者的文件列表
				if not share_user['file_done']:
					print '%d now spidering filese ,%d  file fetched'%(share_user['uk'],share_user['file_fetched'])
					rs=self.getShareLists(share_user['uk'],share_user['file_fetched'])
					if not rs:
						print 'uk:%d error to fetch files,try again later...'%share_user['uk']
						return True
					total_count,fetched_count,file_list=rs

					# print 'share user fetch count:%s'%share_user['file_fetched']
					# print 'total count:%s'%total_count

					total_fetched=share_user['file_fetched']+fetched_count

					# print 'fetched_file_count:%d'%fetched_count
					# print 'total_count:%d'%total_count
					if total_fetched>=total_count or total_count==0:
						share_user['file_done']=1#该分享者所有文件爬取完成
					if total_count==0:
						self.db.execute("UPDATE spider_list set file_done=%s WHERE sid=%s",(1,share_user['sid']))
						self.db.commit()
					else:
						try:
							files_count=0
							for file in file_list:
								files_count+=1
								ext=''
								file_type=''
								file_cover_img=''
								douban_url=''
								douban_score=''
								file_type_i=-1
								if file['isdir']==0 and file['feed_type']=='share':
									ext = metautils.get_extension(file['title']).lower()
									file_type = metautils.get_category(ext)
									file_type_i=self.file_type_t[file_type]
								time_stamp=int(time.time())
								if file['feed_time']>(time_stamp-3600*24*5):
									if file_type_i==0 or file_type_i==-1:
										# seg_list = jieba.cut(file['title'], cut_all=False)# 精确模式
										# seg_set = list(set(seg_list))
										# for seg in seg_set:
										# 	try:
										# 		if tags[seg]>0:
										# 			seg_set.remove(seg)
										# 		else:
										# 			print seg
										# 	except Exception as e:
										# 		print "excption"
										# print("Default Mode: " + "/ ".join(seg_list))  
										
										query=file['title']
										# print query
										try:
											if query.index("2016")>0:
												query=query[0: query.index("2016")-1]
										except Exception as e:
											print "2016 e"
										
										try:
											if query.index("更至")>0:
												query=query[0: query.index("更至")-1]
										except Exception as e:
											print "更至 e"
										
										try:
											if query.index("更新至")>0:
												query=query[0: query.index("更新至")-1]
										except Exception as e:
											print "更新至 e"

										try:
											if query.index("连载至")>0:
												query=query[0: query.index("连载至")-1]
										except Exception as e:
											print "连载至 e"

										try:
											if query.index("更新")>0:
												query=query[0: query.index("更新")-1]
										except Exception as e:
											print "更新 e"
										

										query=query.replace(" ", "")
										query=re.sub(r'第\d季.*$', "", query)
										query=query.replace(" ", "")
										query=query.replace(")", " ")
										query=query.replace("(", " ")
										query=query.replace(">", " ")
										query=query.replace("<", " ")
										query=query.replace("[", " ")
										query=query.replace("]", " ")
										query=query.replace("（", " ")
										query=query.replace("）", " ")
										query=query.replace("》", " ")
										query=query.replace("《", " ")
										query=query.replace("】", " ")
										query=query.replace("【", " ")
										query=query.replace(".", " ")

										file['tags']=''
										# print "split start"
										query_list=query.strip().split(" ")
										# for q in query_list:
										# 	print q
										
										query_list=list(set(query_list))
										global tags
										i = 0
										while i < len(query_list):
											tit = query_list[i]
											if len(tit.strip())==0:
												query_list.pop(i)
												i -= 1
												
												# query_list.remove(tit)
											else:
												try:
													if tags.index(tit.strip())>=0:
														if file['tags'] == '':
															file['tags']=tit.strip()
														else:
															file['tags']=file['tags']+","+tit.strip()
														# query_list.remove(tit)
														query_list.pop(i)
														i -= 1
														
												except Exception as e:
													print 'tags e'
												else:
													if ():
														# query_list.remove(tit)
														query_list.pop(i)
														i -= 1
											i += 1
											
										# print query_list[0]
										file['title']=query_list[0].strip()

										filefetch=self.db.execute('SELECT * from share_file where title=%s', (file['title'],))
										if filefetch>0:
											self.db.execute('delete from share_file where title=%s', (file['title'],))
											#indexOf javascript
											
											# bracketkinex=query.find(")")
											# if bracketkinex!=-1:
											# 	query=query[bracketkinex]
											# bracketkinex=query.find(">")
											# if bracketkinex!=-1:
											# 	query=query[bracketkinex]
											# bracketkinex=query.find("》")
											# if bracketkinex!=-1:
											# 	query=query[1:bracketkinex]
											# bracketkinex=query.find("】")
											# if bracketkinex!=-1:
											# 	query=query[1:bracketkinex]
											# bracketkinex=query.find("：")
											# if bracketkinex!=-1:
											# 	query=query[0:bracketkinex]
											# dotinex=query.find(".")
											# if dotinex!=-1:
											# 	##substr javascript
											# 	query=query[0:dotinex]
											# blankinex=query.find(" ")
											# if blankinex!=-1:
											# 	query=query[0:blankinex]
											# print query
										follows_json=json.loads(getHtml("https://movie.douban.com/j/subject_suggest?q="+file['title']))
										
										if len(follows_json)>0:
											i=0
											while file_cover_img=='' and i<len(follows_json):
												if follows_json[i]['img']!='' and follows_json[i].has_key("year") and follows_json[i]['year']=="2016":
													file_cover_img = follows_json[i]['img']
												if follows_json[i]['url']!='':
													douban_url = follows_json[i]['url']
												i += 1
											if file_cover_img=='':
												file_cover_img = follows_json[0]['img']
												douban_url = follows_json[0]['url']
										if douban_url!='':
											opener = urllib2.urlopen(douban_url)
											self.content = opener.read()
											
											parser = mtimeDataParser()
											parser.feed(self.content.decode('utf-8'))
											# print parser.data
											douban_score=parser.data
											parser.close()

											self.db.execute(
												"REPLACE INTO share_file (title,uk,shareid,shorturl,isdir,size,md5,ext,feed_time,create_time,file_type,uid,feed_type,cover_img,douban_url,douban_score,tags) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
												(file['title'],file['uk'],file['shareid'],file['shorturl'],file['isdir'],
												file['size'],file['md5'],ext,file['feed_time'],time_stamp,file_type_i,share_user['uid'],
												file['feed_type'],file_cover_img,douban_url,douban_score,file['tags'])
											)
							# print "file list spider finish"
						except:
							share_user['file_done']=0
							print "catch except"
							self.db.rollback()
							traceback.print_exc()
							return False
						else:
							# print "update sql"
							self.db.execute("UPDATE spider_list set file_fetched=%s,file_done=%s WHERE sid=%s",(total_fetched,share_user['file_done'],share_user['sid']))
							self.db.execute("UPDATE share_users set fetched=%s WHERE uid=%s",(total_fetched,share_user['uid']))
							share_user['file_fetched']=total_fetched
							self.got_files_count+=files_count
							self.db.commit()
							
				else:
					# print "file done"
					self.db.execute("DELETE FROM spider_list WHERE sid=%s",(share_user['sid'],))
					self.db.commit()
					del share_user
				#爬取完文件后在爬取订阅列表
				if share_user['follow_done']==0:# and share_user['file_done']==1:
					print '%d now spidering follow ,%d  follow fetched'%(share_user['uk'],share_user['follow_fetched'])
					rs=self.getFollows(share_user['uk'],share_user['follow_fetched'])
					if not rs:
						print 'error to fetch follows,try again later...'
						return
					total_count,fetched_count,follow_list=rs
					total_fetched=share_user['follow_fetched']+fetched_count

					print 'fetched_follow_count:%d'%fetched_count
					# if total_fetched>=total_count or total_count==0:
					# 	share_user['follow_done']=1
					if total_count==0:
						self.db.execute("DELETE FROM spider_list WHERE sid=%s",(share_user['sid'],))
						self.db.commit()
					else:
						try:
							follow_count=0
							for follow in follow_list:
								follow_count+=1
								#判断该用户是否已经在表中了
								# if self.db.execute('SELECT * FROM share_users WHERE uk=%s',(follow['follow_uk'],))>0:
								# 	print 'uk:%d has already in share_user table'%follow['follow_uk']
								# 	continue
								fetched_user=spider.db.execute('SELECT * from share_users where uk=%s',(follow['follow_uk'],))
								if fetched_user<=0 :
									
									time_stamp=int(time.time())
									self.db.execute(
										"REPLACE INTO share_users (uk,user_name,avatar_url,intro,follow_count,album_count,fens_count,pubshare_count,last_visited,create_time,weight,follow_done) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
										(
											follow['follow_uk'],follow['follow_uname'],follow['avatar_url'],follow['intro'],follow['follow_count'],
											follow['album_count'],follow['fans_count'],follow['pubshare_count'],time_stamp,time_stamp,5,1
										)
									)
									#将获取的新分享者加入爬取列表
									self.db.execute("REPLACE INTO spider_list (uk,uid) VALUES(%s,%s)",(follow['follow_uk'],self.db.last_row_id()))
								
						except:
							share_user['follow_done']=0
							self.db.rollback()
							traceback.print_exc()
							return False
						else:
							if share_user['follow_done']==1:
								#订阅者爬取完成，该分享者的任务完成，从待爬取列表中删除
								print 'delete follow fetched sid:%d from spider_list'%share_user['sid']
								self.db.execute("DELETE FROM spider_list WHERE sid=%s",(share_user['sid'],))
							else:
								self.db.execute("UPDATE spider_list set follow_fetched=%s,follow_done=%s WHERE sid=%s",(total_fetched,share_user['follow_done'],share_user['sid']))
							share_user['follow_fetched']=total_fetched
							self.got_follow_count+=follow_count
							self.db.commit()
				#只要分享者列表没完成，说明该分享者还未爬取完，则加入工作队列，继续爬取
				if ONLYSIXTY:
					print "first sixty spider over"
					self.db.execute("DELETE FROM spider_list WHERE sid=%s",(share_user['sid'],))
					self.db.commit()
					del share_user
				# else:
				# 	if share_user['follow_done']==0:
				# 		self.spider_queue.put(share_user)
				# 	else:
				# 		print '%d has done'%share_user['uk']
				# 		del share_user
				waittime=60*random.random()
				print "wait time %s"%waittime
				time.sleep(waittime)
	
			
		print '-----------------Done------------------'
		print 'while_count:%d'%self.while_count
		print 'got_follow_count:%d'%self.got_follow_count
		print 'got_files_count:%d'%self.got_files_count
		return True

	def stop(self):
		pass


def getaddrinfo(*args):
  return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--seed-user", help="get seed user", action="store_true")
	args = parser.parse_args()
	
	spider=BaiduPanSpider()
	
	# 做种
	if args.seed_user:
		spider.seedUsers()
	else:

		
		while(1):
			print 'start spider...'
			# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

			# # patch the socket module
			# socket.socket = socks.socksocket
			# socket.create_connection = create_connection
			# socket.getaddrinfo = getaddrinfo

			result=spider.startSpider()
			if not result:
				print 'The spider is refused, later try again auto...'
				waittime=3600*random.random()
				print "wait time %s"%waittime
				time.sleep(waittime)
			else:
				print 'one worker queue id done'
				time.sleep(1)