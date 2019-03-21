Page({

  data: {
    
  },

  onLoad: function (options) {
    var userInfo = wx.getStorageSync('userInfo')
    var account = wx.getStorageSync('account')
    var name = wx.getStorageSync('name')
    this.setData({
      userInfo: userInfo,
      account: account,
      name: name
    })
  },

  toMyBorrow:function(e){
    wx.navigateTo({
      url: '../user/myBorrow',
    })
  },

  toFeedback: function (e) {
    wx.navigateTo({
      url: '../user/feedback',
    })
  },

  toMap: function(e){
    wx.navigateTo({
      url: '/pages/map/index',
    })
  },

  toLoginPage:function(e){
    wx.showModal({
      title: '警告',
      content: '是否退出当前账号？',
      success:function(res){
        if(res.confirm){
          wx.redirectTo({          //正式版使用 必须让用户登录才能正常使用
            url: '../user/login',
          })
          // wx.navigateTo({
          //   url: '../me/login',
          // })
          wx.removeStorageSync('account')
          wx.removeStorageSync('password')
          wx.removeStorageSync('name')
          wx.removeStorageSync('gender')
          wx.removeStorageSync('deptName')
          wx.removeStorageSync('studentId')
          wx.removeStorageSync('loginSession')
        }
      }
    })
  }
})
