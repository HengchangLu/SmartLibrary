var util = require('../../utils/util.js');
var today = util.formatTime(new Date((new Date()).getTime())).split(' ')[0];
var minday = util.formatTime(new Date((new Date()).getTime() + (1000 * 60 * 60))).split(' ')[0];
var maxday = util.formatTime(new Date((new Date()).getTime() + (1000 * 60 * 60 * 24 * 62))).split(' ')[0];
Page({

  /**
   * 页面的初始数据
   */
  data: {
    citys: ['请选择城市', '济南', '青岛', '北京', '上海', '南京'],
    targets: ['请选择出行偏好', '休闲游','摄影游', '美食游', '小众游', '其他'],
    days: ['请选择出行天数', '1天', '2天', '3天', '4天', '5天', '6天', '7天', '更多'],
    peoples:['请选择人员关系', '亲子', '情侣', '朋友', '其他'],
    traffics:['请选择出行交通方式','自驾游','火车', '飞机', '大巴'],
    date: today,
    minday: today,
    maxday: maxday,
    campus: 0,
    target: 0,
    city:0,
    day:0,
    traffic:0,
    people:0,
  },
  


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
  },

  getcity: function (event) {
    this.setData({
      city: event.detail.value,
      searchPageNum: 1,
      list: [],
      searchLoading: false,
      searchLoadingComplete: false,
    })
  },

  gettarget: function (event) {
    this.setData({
      target: event.detail.value,
      searchPageNum: 1,
      list: [],
      searchLoading: false,
      searchLoadingComplete: false,
    })
  },

  getdays: function (event) {
    this.setData({
      day: event.detail.value,
    })
  },

  gettraffic: function (event) {
    this.setData({
      traffic: event.detail.value,
    })
  },
  getpeople: function (event) {
    this.setData({
      people: event.detail.value,
    })
  },
  
  toView:function(e){
    wx.showToast({
      title: "加载中",
      icon: 'loading',
      duration: 1000,
    })

    setTimeout(function () {
      wx.navigateTo({
        url: './view',
      })
    }, 1000)
   
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  }
})