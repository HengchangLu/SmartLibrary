var util = require('../../utils/util.js');
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  onLoad: function(options) {

  },

  formSubmit: function(e) {
    console.log(e.detail.value.feedbackContent)
    console.log(wx.getStorageSync('account'))
    if(e.detail.value.feedbackContent==''){
      wx.showModal({
        title: '警告',
        content: '内容不能为空，请重试',
        showCancel:false,
      })
    }else{
    util.req('user/post/feedback', {
      'feedbackMsg': e.detail.value.feedbackContent,
      'studentId': wx.getStorageSync('studentId'),
      'name': wx.getStorageSync('name'),
      'gender': wx.getStorageSync('gender'),
      'account': wx.getStorageSync('account'),
      'deptName': wx.getStorageSync('deptName'),
    },function(data){
      if(data.result){
        wx.hideLoading()
        wx.showToast({
          title: data.msg,
          icon: 'success',
          duration:1000,
        })
      }
    })
    }
  }
})