var util = require('../../utils/util.js');
var app = getApp();

function formatLocation(longitude, latitude) {
  longitude = longitude.toFixed(2)
  latitude = latitude.toFixed(2)
  return {
    longitude: longitude.toString().split('.'),
    latitude: latitude.toString().split('.')
  }
}

Page({

  data: {
    latitude: 23.099994,
    longitude: 113.324520,
    markers: [{
      id: 1,
      latitude: 23.099994,
      longitude: 113.324520,
      name: 'T.I.T 创意园'
    }],
    covers: [{
      latitude: 23.099994,
      longitude: 113.344520,
      iconPath: '/image/location.png'
    }, {
      latitude: 23.099994,
      longitude: 113.304520,
      iconPath: '/image/location.png'
    }],
    // polyline: [{
    //   points: [{
    //     latitude: 34.780254,
    //     longitude: 113.699559

    //   }, {
    //     longitude: 113.701855,
    //     latitude: 34.779778
    //   }],
    //   color: "#ff6600",
    //   width: 2,
    //   dottedLine: false,
    //   arrowLine: true,
    //   borderColor: "#000",
    //   borderWidth: 5
    // }],
  },

  onClick: function() {
    var that = this;
    wx.getLocation({
      success: function(res) {
        console.log(res)
        that.setData({
          location: formatLocation(res.longitude, res.latitude)
        })
      },
    })
  },

  getCenterLocation: function() {
    this.mapCtx.getCenterLocation({
      success: function(res) {
        console.log(res.longitude)
        console.log(res.latitude)
      }
    })
  },

  moveToLocation: function() {
    this.mapCtx.moveToLocation()
  },
  translateMarker: function() {
    this.mapCtx.translateMarker({
      markerId: 1,
      autoRotate: true,
      duration: 1000,
      destination: {
        latitude: 23.10229,
        longitude: 113.3345211,
      },
      animationEnd() {
        console.log('animation end')
      }
    })
  },
  includePoints: function() {
    this.mapCtx.includePoints({
      padding: [10],
      points: [{
        latitude: 23.10229,
        longitude: 113.3345211,
      }, {
        latitude: 23.00229,
        longitude: 113.3345211,
      }]
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    // var that = this;
    // setInterval(function () {
    //   wx.getLocation({
    //     success: function (res) {
    //       console.log(res)
    //       that.setData({
    //         location: formatLocation(res.longitude, res.latitude)
    //       })
    //     },
    //   })
    // }
    // , 2000)
    this.setData({
      polyline: [{
        points: [{
          latitude: 34.780254,
          longitude: 113.699559
        }, {
          longitude: 113.701855,
          latitude: 34.779778
          }, {
            latitude: 39.780254,
            longitude: 113.699559
          },],
        color: "#FF0000DD",
        width: 2,
        dottedLine: false
      }],
    }),
    console.log(this.data.polyline)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {
    this.mapCtx = wx.createMapContext('myMap')
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})