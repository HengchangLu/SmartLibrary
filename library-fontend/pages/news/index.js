var util = require("../../utils/util.js")
var newsList = []
Page({
  data: {
    currentTab: 1,
    newsPageNum: 1,
    callbackCount: 8,
    loading: false,
    loadingComplete: false,
    isFromSearch: true,
  },
  onLoad: function (options) {
    this.getNews()
  },

  switchNav: function (e) {
    var index = e.target.dataset.current;
    console.log(index)
    if (this.data.currentTab == index) {
      return false;
    } else {
      this.setData({
        currentTab: index,
        newsPageNum:1,
        loading: false,
        loadingComplete: false,
        isFromSearch: true,
      });
    }
    this.getNews()
  },

  getNews: function () {
    var that = this;
    wx.showLoading({
      title: '加载中...',
    })
    util.req('news/get/news/', {
      currentTab: this.data.currentTab,
      newsPageNum: this.data.newsPageNum,
      callbackCount: this.data.callbackCount,
    }, function (data) {
      if (data.result) {
        wx.hideLoading()
      }
      if (data.news_list.length == 0){
        wx.showToast({
          title: "已经到底了",
          icon: "success",
        })
        that.setData({
          loading: false,
          loadingComplete: true,
        })
      }else{
        var tempNewsList = []
        console.log(data.news_list)
        that.data.isFromSearch ? tempNewsList = data.news_list : tempNewsList = that.data.newsList.concat(data.news_list)
        for (var i = 0; i < tempNewsList.length; i++) {
          newsList.push(tempNewsList[i])
        };
        that.setData({
          newsList: tempNewsList,
          loading: true,
        });
      }
    })
  },
  loadMoreNews: function (e) {
    var that = this;
    console.log('scrollLower function')
    if (that.data.loading && !that.data.loadingComplete) {
      that.setData({
        newsPageNum: that.data.newsPageNum + 1,
        isFromSearch: false,
      });
    }
    that.getNews()
  },
  toLibSummaryIndex: function (e) {
    wx.navigateTo({
      url: "../libsummary/libsummary",
    })
  },
  toFriendLinkIndex: function (e) {
    wx.navigateTo({
      url: "../friendlylink/index",
    })
  },

  toServiceIndex: function (e) {
    wx.navigateTo({
      url: "../service/index",
    })
  },

  toClassificationIndex: function (e) {
    wx.navigateTo({
      url: "../classification/index",
    })
  },
})