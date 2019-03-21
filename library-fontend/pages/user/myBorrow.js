var util = require('../../utils/util.js')
Page({
  data: {
    myBorrowList: [

    ],
  },
  renew: function(e) {
    wx.showModal({
      title: '提示',
      content: '是否确定续借',
      success: function(res) {
        console.log(e.currentTarget.dataset.check)
        if (res.confirm) {
          wx.showLoading({
            title: '请求中...',
          })
          util.req('book/renew/', {
            account: wx.getStorageSync('account'),
            password: wx.getStorageSync('password'),
            code: e.currentTarget.dataset.code,
            check: e.currentTarget.dataset.check,
          }, function(data) {
            wx.hideLoading()
            wx.showModal({
              title: '提示',
              content: data.renew_msg,
              showCancel: false,
            })
          })
        }
      }
    })
  },
  onLoad: function(options) {
    var that = this;
    wx.showLoading({
      title: '加载中...',
    })
    var account = wx.getStorageSync('account')
    var password = wx.getStorageSync('password')
    util.req('book/borrowed/', {
      account: account,
      password: password,
    }, function(data) {
      if (data.result) {
        wx.hideLoading()
        var myBorrowList = []
        var tempList = data.borrow_book_list
        console.log(data.borrow_book_list)
        for (var i = 0; i < tempList.length; i++) {
          var tempDict = {}
          tempDict['code'] = tempList[i][0]
          tempDict['name'] = tempList[i][1]
          tempDict['borrowTime'] = tempList[i][2]
          tempDict['returnTime'] = tempList[i][3]
          tempDict['location'] = tempList[i][4]
          tempDict['check'] = tempList[i][5]
          myBorrowList.push(tempDict)
        }
        that.setData({
          myBorrowList: myBorrowList
        })
      } else {
        wx.hideLoading()
        wx.showModal({
          title: data.msg,
          showCancel: false
        })
      }
    })
  },

})