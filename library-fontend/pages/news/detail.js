var WxParse = require('../wxParse/wxParse.js');
var util = require('../../utils/util.js')
Page({

  data: {

  },

  onLoad: function(options) {
    var that = this;
    console.log(options.title)
    that.setData({
      title: options.title,
      time: options.time.replace('[', '').replace(']', ''),
      id: options.id,
      currentTab: options.currentTab
    })
    this.getNewsDetail()
  },
  getNewsDetail: function() {
    var that = this;
    wx.showLoading({
      title: '加载中...',
    })
    util.req('news/get/detail/', {
      id: that.data.id,
      currentTab: that.data.currentTab,
    }, function(data) {
      if (data.result) {
        wx.hideLoading()
        that.setData({
          url: data.url
        })
      }
      WxParse.wxParse('article', 'html', data.content, that, 5);
    })
  },
  wxParseTagATap: function(e) {
    var tempUrl = e.currentTarget.dataset.src;
    console.log('tempUrl', tempUrl)
    if (tempUrl.indexOf('http') == -1) {
      var url = 'http://www.lib.sdu.edu.cn' + e.currentTarget.dataset.src;
    } else {
      url = tempUrl
    }
    console.log(url)

    if (url.indexOf('download') == -1) {
      wx.setClipboardData({
        data: url,
        success: function(res) {
          wx.showModal({
            title: '提示',
            content: '复制链接成功',
            showCancel: false,
          })
        }
      })
    } else {
      wx.downloadFile({
        url: url,
        success: function(res) {
          var filePath = res.tempFilePath
          wx.openDocument({
            filePath: filePath,
            success: function(res) {
              console.log('打开文档成功')
            },
            fail: function(res) {
              console.log(res)
            }
          })
        },
        fail: function() {
          console.log('下载文档失败');
        }
      })
    }
  }
})