#-*- coding:utf-8 -*-
#
# 模拟百度登录 for Python2.7
# 其中显示验证码部分 需要使用PIL库
# 需要验证码时，会创建一个Tkinter窗口，用于显示和输入验证码，回车后窗口关闭。
# author:zx(www.zh30.com)
#
import urllib, urllib2, cookielib, re, time
import datetime
username   = '1034709616@qq.Chrome' #用户名
password   = 'a123456' #密码
cookiefile = '--login-baidu--'  #cookie文件
#模拟header信息
headers = {
        "Host":"passport.baidu.com",
        "Referer":"http://www.caoliao.net.cn",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
        "Origin":"http://www.baidu.com",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive"   
        }
cookie = cookielib.MozillaCookieJar(cookiefile)
now = datetime.datetime.now()
#尝试加载cookie文件并验证有效性
try:
    cookie.load(ignore_discard=True, ignore_expires=True)
    print '读取登录状态的cookie成功'
    #do something...
    
except Exception:
    #cookie不存在或无效时 开始进行模拟登录并重新生成cookie文件
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

    loginUrl = 'http://www.baidu.com/cache/user/html/login-1.2.html'
    getTokenUrl = 'https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true'
    getCodeStringUrl = 'https://passport.baidu.com/v2/api/?logincheck&callback=bdPass.api.login._needCodestringCheckCallback&tpl=mn&charset=UTF-8&index=0&username=' + username + '&isphone=false&time='+str(now)
    loginPostUrl = 'https://passport.baidu.com/v2/api/?login'
    #获取BAIDUID、token
    request = urllib2.Request(loginUrl, headers=headers)
    response = opener.open(request)

    request = urllib2.Request(getTokenUrl, headers=headers)
    response = opener.open(request)
    hasToken = response.read()
    print hasToken
    token = re.search(r'login_token\s*=\s*\'(.+?)\'',hasToken).group(1)
    
    #检查username是否需要验证码
    request = urllib2.Request(getCodeStringUrl, headers=headers)
    response = opener.open(request)
    getCodeString = response.read()
    codestring = re.search(r'"codestring":"?([^"]+)"?,', getCodeString).group(1)
    if codestring == 'null' :
        codestring = ''
        verifycode = ''
    else:
        #需要验证码 创建一个tk显示验证码 并提示用户输入
        genimageUrl = 'https://passport.baidu.com/cgi-bin/genimage?' + codestring + '&v=' + str(long(time.time()*1000))
        import io, Tkinter as tk
        from PIL import Image, ImageTk
        request = urllib2.Request(genimageUrl, headers=headers)
        image_bytes = opener.open(request).read()
        pil_image = Image.open(io.BytesIO(image_bytes))

        def presskey(event):
            global verifycode
            if event.keycode == 13:
                    verifycode = entry.get()
                    tk_root.destroy()

        tk_root = tk.Tk()
        tk_image = ImageTk.PhotoImage(pil_image)
        label1 = tk.Label(tk_root, text='您的帐号异常，需要输入验证码')
        label1.pack()

        label2 = tk.Label(tk_root, image=tk_image)
        label2.pack()

        label3 = tk.Label(tk_root, text='输入验证码并按回车确认')
        label3.pack()
        entry = tk.Entry(tk_root)
        entry.bind('<Key>', presskey)
        entry.pack()
        tk_root.mainloop()

    

    #构造登录表单
    data = {
            "ppui_logintime":str(now),
            "charset":"utf-8",
            "codestring":"",
            "isPhone":"false",
            "index":"0",
            "u":"",
            "safeflg":"0",
            "staticpage":"http://www.baidu.com/",
            "loginType":"1",
            "tpl":"mn",
            "callback":"parent.bdPass.api.login._postCallback",
            "mem_pass":"on"
    }
    data['token'] = token
    data['username'] = username
    data['password'] = password
    data['codestring'] = codestring
    data['verifycode'] = verifycode
    #开始登录
    req = urllib2.Request(loginPostUrl, urllib.urlencode(data), headers)
    result = opener.open(req).read()
    #验证登录结果
    
    errno = re.search(r'&error=(\d+)', result).group(1)
    if errno == '0':
        print '登录成功'
        cookie.save(ignore_discard=True,ignore_expires=True)
    elif errno == '4':
        print '登录失败：密码错误'
    elif errno == '257':
        print '登录失败：验证码错误'
    else:
        print '登录失败'
        print result #失败后 打印返回字符 by zh30.com