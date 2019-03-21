//index.js
//获取应用实例
const app = getApp();
var util = require('../../utils/util.js');
var recommendBookList;
var newBookList;
Page({
  data: {
    loading: false,
    loadingComplete: false,
    isFromSearch: true,
    recommendBookList: [],
    newBookList: [],
    imgUrls: [{
      url: '../images/indexswiper6.png'
    }, {
      url: '../images/indexswiper1.png'
    }, {
      url: '../images/indexswiper4.png'
    }, ],
    newsInfo: [],
    images: {},
  },
  imageLoad: function(e) {
    var width = e.detail.width, //获取图片真实宽度
      height = e.detail.height,
      ratio = width / height; //图片的真实宽高比例
    var viewWidth = 650, //设置图片显示宽度，左右留有27rpx边距
      viewHeight = 650 / ratio; //计算的高度值
    var image = this.data.images;
    //将图片的datadata-index作为image对象的key,然后存储图片的宽高值
    image[e.target.dataset.index] = {
      width: viewWidth,
      height: viewHeight
    }
    this.setData({
      images: image
    })
  },

  searchInput: function(e) {
    wx.navigateTo({
      url: "../book/search"
    })
  },

  toAppointIndex: function(e) {
    wx.navigateTo({
      url: '../reservation/index',
    })
  },
  toNewBookIndex: function(e) {
    wx.navigateTo({
      url: "../book/newBook",
    })
  },

  toRecommendBookIndex: function(e) {
    wx.navigateTo({
      url: "../book/recommendBook",
    })
  },

  toLocationIndex: function(e) {
    wx.navigateTo({
      url: '../location/index',
    })
  },

  toRankIndex: function(e) {
    wx.navigateTo({
      url: '../rank/index',
    })
  },

  toGuessIndex: function(e) {
    wx.navigateTo({
      url: '../guessYouLike/index',
    })
  },

  onLoad: function() {
    var studentId = wx.getStorageSync('studentId')
    var password = wx.getStorageSync('password')
    if (studentId == "" || password == "") {
      wx.navigateTo({
        url: '/pages/user/login',
      })
    }
    this.getNewBook()
    this.getRecommendBook()
  },
  
  getNewBook: function() {
    var that = this;
    util.req('book/get/newbook/', {
        currentType: 1,
        bookPageNum: 1,
        callbackCount: 3,
      },
      function(data) {
        if (data.result) {
          wx.hideLoading()
        }
        if (data.list.length == 0) {
          wx.showToast({
            title: "没有更多了",
            icon: "success",
          })
          that.setData({
            loading: false,
            loadingComplete: true,
          })
        } else {
          var tempBookList = []
          that.data.isFromSearch ? tempBookList = data.list : tempBookList = that.data.newBookList.concat(data.list)
          for (var i = 0; i < tempBookList.length; i++) {
            that.data.newBookList.push(tempBookList[i])
          };
          that.setData({
            newBookList: tempBookList,
            loading: true,
          });
        }
      })
  },

  getRecommendBook: function() {
    var that = this;
    util.req('book/get/newbook/', {
        currentType: 2,
        bookPageNum: 1,
        callbackCount: 3,
      },
      function(data) {
        if (data.result) {
          wx.hideLoading()
        }
        if (data.list.length == 0) {
          wx.showToast({
            title: "没有更多了",
            icon: "success",
          })
          that.setData({
            loading: false,
            loadingComplete: true,
          })
        } else {
          var tempBookList = []
          that.data.isFromSearch ? tempBookList = data.list : tempBookList = that.data.recommendBookList.concat(data.list)
          for (var i = 0; i < tempBookList.length; i++) {
            that.data.recommendBookList.push(tempBookList[i])
          };
          that.setData({
            recommendBookList: tempBookList,
            loading: true,
          });
        }
      })
  },
})