getSearchResult("隧道", this.type, null, null, null, function(c) {
			if (c && c.value) {
				this.type = c.value.type;
				this.tokens = c.value.words;
				this.needLog = c.value.needLog;
				this.actionId = c.value.actionId;
				this.trackId = c.value.trackId;
				if (this.type == 4) {
					this.addSearchActionLog();
					var d = String.format("{0}?q={1}", siteGoodsListUrl, this.keyword);
					$redirect(d)
				} else {
					this.renderResult(c.value)
				}
			}

type: 0,
	requestType: 0,
	ignore: 0,
	hlFormatF: '<span class="edit_color">',
	hlFormatB: "</span>",
	server: {
		getSearchResult: function(j, l, h, i, k, g) {
			return Mtime.Component.Ajax.crossDomainCallBack(siteChannelServiceUrl, "Mtime.Channel.Services", "GetSearchResult", [j, l, h, i, k], g, "/Search.api", "get", "60000", null)
		},

	crossDomainCallBack: function(t, s, r, n, o, x, p, v, u) {
		var d = new Date(),
			c = [];
		c.push(d.getFullYear());
		c.push(d.getMonth() + 1);
		c.push(d.getDate());
		c.push(d.getHours());
		c.push(d.getMinutes());
		c.push(d.getSeconds());
		c.push(parseInt(Math.random() * 100000, 10));
		var w = c.join("")

		var q = this.getRequestUrl(t, s, r, n, x, w);
		if (q.length > 2048) {
			Ajax.getTransport = CrossdomainAjax.getTransport;
			this._callBack(s, r, n, o, t + x, p, v, u)
		} else {
			this.request(t, s, r, n, o, x, p, v, u)
		}
	},

	getRequestUrl: function(n, m, l, j, p, o) {
		var k = []
		if (p.indexOf("Ajax_CallBack=true") < 0) {
			k.push["Ajax_CallBack=true&"]
		}
		k.push["Ajax_CallBackType="];
		k.push[m];
		k.push["&Ajax_CallBackMethod="];
		k.push[l];
		k.push["&Ajax_CrossDomain=1"];
		k.push["&Ajax_RequestUrl="];
		k.push[encodeURIComponent(location.href)];
		k.push["&t="];
		k.push[o];
		k.push[this.toQueryString(j)];
		p = p.indexOf("http") !== 0 ? n + p : p;
		if ("https:" == document.location.protocol) {
			if (!p.startsWith("https://")) {
				p = p.replace("http://", "https://")
			}
		}
		if (p.indexOf("?") > 0) {
			p += "&" + k.toString()
		} else {
			p += "?" + k.toString()
		}
		return p
	},