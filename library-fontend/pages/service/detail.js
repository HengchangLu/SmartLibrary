var WxParse = require('../wxParse/wxParse.js');
var util = require('../../utils/util.js')
Page({

  data: {
    url: '',
    urls: [],
    title: '',
    time: '',
    title1: '',
    flag: true, // flag=true  往后台请求 flag=false 不往后台请求
    titleUrl: {
      '中心校区蒋震图书馆': ['http://www.lib.sdu.edu.cn/download?id=527'],
      '洪家楼校区政法分馆': ['http://www.lib.sdu.edu.cn/download?id=529'],
      '千佛山校区工学分馆': ['http://www.lib.sdu.edu.cn/download?id=530'],
      '趵突泉校区医学分馆': ['http://www.lib.sdu.edu.cn/download?id=531'],
      '兴隆山校区图书馆': ['http://www.lib.sdu.edu.cn/download?id=802',
        'http://www.lib.sdu.edu.cn/download?id=803',
        'http://www.lib.sdu.edu.cn/download?id=807',
        'http://www.lib.sdu.edu.cn/download?id=808',
      ],
      '软件园校区图书馆': ['http://www.lib.sdu.edu.cn/download?id=533']
    },
  },

  onLoad: function(options) {
    console.log('options.title', options.title)
    //尝试用 switch case
    if (options.title == '中心校区蒋震图书馆' || options.title == '洪家楼校区政法分馆' || options.title == '千佛山校区工学分馆' || options.title == '趵突泉校区医学分馆' || options.title == '兴隆山校区图书馆' || options.title == '软件园校区图书馆') {
      this.setData({
        title: options.title,
        urls: this.data.titleUrl[options.title],
        time: '2013.07.11',
        flag: false,
      })
    } else {
      this.setData({
        title: options.title,
        flag: true,
      })
      this.getServiceContent()
    }
  },

  imgYu: function(e) {
    var src = e.currentTarget.dataset.src; //获取data-src
    var imgList = e.currentTarget.dataset.list; //获取data-list
    //图片预览
    wx.previewImage({
      current: src, // 当前显示图片的http链接
      urls: imgList // 需要预览的图片http链接列表
    })
  },
  wxParseTagATap: function(e) {
    var url = e.currentTarget.dataset.src;
    this.setData({
      url: url
    })
    if (url != 'http://58.194.172.14/autoservice/') {
      this.getServiceContent()
    }

  },

  getServiceContent: function() {
    wx.showLoading({
      title: '加载中',
    })
    var that = this;
    util.req('news/get/service/', {
      title: that.data.title,
      url: that.data.url,
    }, function(data) {
      if (data.result) {
        wx.hideLoading()
      }
      console.log(data.url)
      that.setData({
        title: data.title,
        time: data.time,
        url: data.url
      })
      WxParse.wxParse('article', 'html', data.content, that, 5);
    })
  },
})