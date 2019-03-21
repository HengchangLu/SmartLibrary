var util = require('../../utils/util.js');
// var RSA = require('../../utils/rsa.js');
import rsa from '../../utils/rsa.js';
var app = getApp();
Page({
  data: {
    account: '',
    password: ''
  },
  onLoad: function(options) {
    var userInfo = wx.getStorageSync('userInfo')
    this.setData({
      userInfo: userInfo
    })
  },

  accountInput: function(e) {
    this.setData({
      account: e.detail.value
    })
  },

  passwordInput: function(e) {
    this.setData({
      password: e.detail.value
    })
  },
  
  login: function(e) {
    var that = this;
    // console.log(rsa(that.data.password))
    // console.log(rsa(that.data.password).length)
    if (that.data.account.length == 0) {
      wx.showModal({
        title: '警告',
        content: '账号不能为空',
        showCancel: false
      })
      return;
    } else if (that.data.password.length == 0) {
      wx.showModal({
        title: '警告',
        content: '密码不能为空',
        showCancel: false
      })
      return;
    }else{
    wx.setStorageSync('userInfo', e.detail.userInfo)
    that.setData({
      userInfo: e.detail.userInfo
    })
    wx.showLoading({
      title: '验证中...',
    })

    util.req('user/login/appoint/seat/', {
        account: that.data.account,
        // password: that.data.password
      password: rsa(that.data.password)
      },
      function(data) {
        var psw_rsa = this
        if (data.result) {
          wx.hideLoading()
          wx.showToast({
            title: data.msg,
            icon: 'success',
            duration: 2000,
          })
          wx.setStorageSync('account', that.data.account)
          wx.setStorageSync('studentId', data.user_info.student_id)
          wx.setStorageSync('password', that.data.password)
          wx.setStorageSync('name', data.user_info.name)
          wx.setStorageSync('gender', data.user_info.gender)
          wx.setStorageSync('deptName', data.user_info.dept_name)
          setTimeout(function() {
            wx.switchTab({
              url: '/pages/index/index',
            })
          }, 2000)
        } else {
        wx.hideLoading()
        wx.showModal({
          title: data.msg,
          showCancel: false
        })
      }
      }
    )}
  },
})