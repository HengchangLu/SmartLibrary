var util = require("../../utils/util.js")
var bookList = []
Page({
  data: {
    bookPageNum: 1,
    callbackCount: 15,
    loading: false,
    loadingComplete: false,
    isFromSearch: true,
    bookList: [],
  },
  onLoad: function(options) {
    var that = this;
    that.getNewBook()
  },

  getNewBook: function() {
    var that = this;
    util.req('book/get/newbook/', {
        currentType: 1,
        bookPageNum: that.data.bookPageNum,
        callbackCount: that.data.callbackCount,
      },
      function(data) {
        if (data.result) {
          wx.hideLoading()
        }
        if (data.list.length == 0) {
          wx.showToast({
            title: "已经到底了",
            icon: "success",
          })
          that.setData({
            loading: false,
            loadingComplete: true,
          })
        } else {
          var tempBookList = []
          that.data.isFromSearch ? tempBookList = data.list : tempBookList = that.data.bookList.concat(data.list)
          for (var i = 0; i < tempBookList.length; i++) {
            bookList.push(tempBookList[i])
          };
          that.setData({
            bookList: tempBookList,
            loading: true,
          });
        }
      })
  },

  searchContentSubmit: function(e) {
    var that = this;
    util.req('book/search/', {
      currentType: 1,
      searchContent: e.detail.value["searchContent"],
    }, function(data) {
      for (var i = 0; i < data.list.length; i++) {
        bookList.push(data.list[i])
      };
      that.setData({
        bookList: data.list
      });
    })
  },
  loadMoreBooks: function(e) {
    var that = this;
    console.log('scrollLower function')
    if (that.data.loading && !that.data.loadingComplete) {
      that.setData({
        bookPageNum: that.data.bookPageNum + 1,
        isFromSearch: false,
      });
    }
    that.getNewBook()
  },
})