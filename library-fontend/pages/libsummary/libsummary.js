var WxParse = require('../wxParse/wxParse.js');
var util = require('../../utils/util.js');
Page({
  data: {
    flag: 0,
    currentTab: 0,
    title: '馆情介绍',
    time: '',
  },
  switchNav: function(e) {
    var that = this;
    var id = e.target.id;
    var title = e.target.dataset.text;
    console.log(e.target.title)
    if (this.data.currentTab == id) {
      return false;
    } else {
      that.setData({
        currentTab: id
      });
    }
    that.setData({
      flag: id,
      title: title,
    });
    that.getLibSummary()
    // console.log('flag', that.data.flag)
    // console.log('currentTab', that.data.currentTab)
    // console.log('title', that.data.title)
  },
  onLoad: function(options) {
    this.getLibSummary()
  },
  getLibSummary: function() {
    wx.showLoading({
      title: '加载中...',
    })
    var that = this;
    util.req('news/get/summary/', {
      title: that.data.title,
      url:'',
    }, function(data){
          if(data.result){
          wx.hideLoading()
        }
        that.setData({
          title:data.title,
          time: data.time,
          url:data.url,
        })
        WxParse.wxParse('article', 'html', data.content, that, 5);
      }
    )
  },
})