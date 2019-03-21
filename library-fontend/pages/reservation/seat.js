var util = require('../../utils/util.js');
var nowTime = util.formatTime1(new Date());
var today = util.formatTime(new Date((new Date()).getTime() + (1000 * 60 * 60 * 24 * 1))).split(' ')[0];
var minday = util.formatTime(new Date()).split(' ')[0];
var maxday = util.formatTime(new Date((new Date()).getTime() + (1000 * 60 * 60 * 24 * 7))).split(' ')[0];
Page({

  data: {
    navbar: ["座位预约", "研讨室预约"],
    roomRange:["101", "102", "103"],
    room:'请选择研讨室',
    activeIndex: 1, // 0 是座位预约  1 是研讨室预约
    isChecked: false, // 传送到后台，0 是今天，1是明天
    selectDate: 0,
    displayList: [],
    spaceSeat: [],
    seatIndex: 0,
    seatImg: '',
    nowTime: nowTime,
    regionId: 0,
    lib: '',
    info: 'hide',
    selectedRoomDate: '请选择日期',
    start: minday,
    end: maxday,
    tempFilePaths: '',
    bookbegintime:["08:00"],
    bookendtime:["11:20"],
    leftMin: 1200,       //左边滑块最小值
    leftMax: 1500,   //左边滑块最大值
    rightMin: 1200,      //右边滑块的最小值
    rightMax: 1500,  //右边滑块最大值
    leftValue: 1300,  //左边滑块默认值
    rightValue: 1400, //右边滑块默认值
    leftWidth: '50',  //左边滑块可滑动长度：百分比
    rightWidth: '50', //右边滑块可滑动长度：百分比
  },

  onLoad: function(options) {
    this.setData({
      regionId: 0,
    })
    this.compareTime()

    // wx.showLoading({
    //   title: '查询中...',
    // })

    this.setData({
      lib: options.libraryname
    })
    console.log(this.data.lib)
    wx.setNavigationBarTitle({
      title: options.libraryname + '预约',
    })
    if (!this.data.activeIndex) {
      this.getSeatRegion()
    } else {
      this.getRoomRegion()
    }
  },

  getRoomRegion: function() {

  },

  getSeatRegion: function() {
    var that = this;
    util.req('reservation/seat/region/', {
      account: wx.getStorageSync('account'),
      password: wx.getStorageSync('password'),
      lib: this.data.lib,
    }, function(data) {
      if (data.result) {
        wx.hideLoading()
      }
      that.setData({
        displayList: data.region_list
      })
    })
  },

  listenerSwitch: function(e) {
    this.setData({
      isChecked: e.detail.value
    });
    console.log(this.data.isChecked)
  },
  // bindRoomChange: function (e) {
  //   this.setData({
  //     room: e.detail.value
  //   })
  //   console.log(this.data.room)
  // },
  selectRoom: function () {
    var page = this;
    // var room = ['101', '102', '103', '104', '105'];
    var room = page.data.roomRange
    wx.showActionSheet({
      itemList: room,
      success: function (res) {
        if (!res.cancel) {
          page.setData({ room: room[res.tapIndex] });
        }
      }
    })
  },
  
  bindDateChange: function(e) {
    console.log(this.data.room)
    this.setData({
      selectedRoomDate: e.detail.value
    })
    console.log(this.data.selectedRoomDate)
  },

  chooseimage: function() {
    var that = this;
    wx.showActionSheet({
      itemList: ['从相册中选择', '拍照'],
      itemColor: "#CED63A",
      success: function(res) {
        if (!res.cancel) {
          if (res.tapIndex == 0) {
            that.chooseWxImage('album')
          } else if (res.tapIndex == 1) {
            that.chooseWxImage('camera')
          }
        }
      }
    })

  },

  chooseWxImage: function(type) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'],
      sourceType: [type],
      success: function(res) {
        console.log(res);
        that.setData({
          tempFilePaths: res.tempFilePaths[0],
        })
      }
    })
  },

  navbarTap: function(e) {
    this.setData({
      activeIndex: e.currentTarget.dataset.idx
    });
    console.log(this.data.activeIndex)
  },
  // 图书馆到了22:10是不能预约当天的，只能预约明天的 
  compareTime: function() {
    if (!this.data.selectDate) {
      if (this.data.nowTime.replace(':', '') >= 2210) {
        this.setData({
          selectDate: 1
        })
        console.log('>=22:10')
        return true
      } else {
        console.log('<22:10')
        return false
      }
    }
  },

  // 左边滑块滑动的值
  leftChange: function (e) {
    console.log('左边改变的值为：' + e.detail.value);
    var that = this;
    that.setData({
      leftValue: e.detail.value //设置左边当前值
    })
  },
  // 右边滑块滑动的值
  rightChange: function (e) {
    console.log('右边改变的值为：' + e.detail.value);
    var that = this;
    that.setData({
      rightValue: e.detail.value,
    })
  },

  selectTime: function(e) {
    var that = this;
    this.compareTime()
    var id = parseInt(e.currentTarget.dataset.id);
    if (!id) {
      if (this.compareTime()) {
        wx.showModal({
          title: '警告',
          content: '该时间段不可预约, 正常预约时间是8:00-22:10',
          showCancel: false,
        })
      } else {
        this.setData({
          selectDate: id
        })
        console.log('that.data.regionId', that.data.regionId)
        if (that.data.regionId != 0) {
          wx.showLoading({
            title: '获取空闲座位中...',
          })
          util.req('reservation/get/seat/', {
            account: wx.getStorageSync('account'),
            password: wx.getStorageSync('password'),
            selectDate: that.data.selectDate,
            // regionId: that.data.displayList[parseInt(id / 10)].region[id % 10].id,
            regionId: that.data.regionId,
          }, function(data) {
            if (data.result) {
              wx.hideLoading()
            }
            wx.setStorageSync('segment', data.segment)
            that.setData({
              spaceSeat: data.seat_list,
              seatImg: data.seat_img,
              seatId: data.seat_id
            })
          })
        }
      }
    } else {
      this.setData({
        selectDate: id
      })
      console.log('that.data.regionId', that.data.regionId)
      if (that.data.regionId != 0) {
        wx.showLoading({
          title: '获取空闲座位中...',
        })
        util.req('reservation/get/seat/', {
          account: wx.getStorageSync('account'),
          password: wx.getStorageSync('password'),
          selectDate: that.data.selectDate,
          // regionId: that.data.displayList[parseInt(id / 10)].region[id % 10].id,
          regionId: that.data.regionId,
        }, function(data) {
          if (data.result) {
            wx.hideLoading()
          }
          wx.setStorageSync('segment', data.segment)
          that.setData({
            spaceSeat: data.seat_list,
            seatImg: data.seat_img,
            seatId: data.seat_id
          })
        })
      }
    }
  },

  selectRegion: function(e) {
    var that = this;
    var id = e.currentTarget.dataset.id;
    this.setData({
      currentTag1: id,
      regionId: that.data.displayList[parseInt(id / 10)].region[id % 10].id,
    })
    wx.showLoading({
      title: '获取空闲座位中...',
    })
    console.log(that.data.displayList[parseInt(id / 10)].region[id % 10].id)
    util.req('reservation/get/seat/', {
      account: wx.getStorageSync('account'),
      password: wx.getStorageSync('password'),
      selectDate: that.data.selectDate,
      regionId: that.data.displayList[parseInt(id / 10)].region[id % 10].id,
    }, function(data) {
      if (data.result) {
        wx.hideLoading()
      }
      wx.setStorageSync('segment', data.segment)
      that.setData({
        spaceSeat: data.seat_list,
        seatImg: data.seat_img,
        seatId: data.seat_id
      })
    })
  },

  pickerSeat: function(e) {
    var that = this;
    this.setData({
      seatIndex: e.detail.value
    })
    console.log(that.data.seatId[that.data.seatIndex].id)
  },

  reserveSeat: function(e) {
    var that = this;
    wx.showModal({
      title: '提示',
      content: '确定选择',
      success: function(res) {
        if (res.confirm) {
          wx.showLoading({
            title: '请求中...',
          })
          util.req('reservation/reserve/seat/', {
              account: wx.getStorageSync('account'),
              password: wx.getStorageSync('password'),
              segment: wx.getStorageSync('segment'),
              seat: that.data.seatId[that.data.seatIndex].id
            },
            function(data) {
              if (data.result) {
                wx.hideLoading()
                wx.showModal({
                  title: '提示',
                  content: data.reserve_seat_msg,
                })
              }
            })
        }
      }
    })
  },

  previewImg: function(e) {
    wx.previewImage({
      urls: [this.data.seatImg],
    })
  },
  checkValue: function(e) {
    // console.log(e);
    // var name = e.detail.value;
    // if (name != '') {
    //   this.setData({
    //     info: 'hide'
    //   });
    // }
  },
  formSubmit: function (e){
    console.log(e.detail.value)
  }
})