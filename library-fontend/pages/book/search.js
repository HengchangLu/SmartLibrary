//search.js
var util = require('../../utils/util.js');
var app = getApp()
var searchResult = []
Page({
  data: {
    currentTab: 0,
    searchContent: '',
    searchResult : [],
  },
  searchContentSubmit: function(e){
    searchResult = []
    var that = this;
    var searchContent = e.detail.value;
    console.log(searchContent)
    wx.request({
      url: 'https://lib.lu2322.top/book/search/',
      // url: 'http://123.206.34.13/book/search/',
      data: searchContent,
      method: 'get',
      header: { 'Content-Type': 'application/json' },
      success: function (res) {
        for(var i = 0; i < res.data.list.length; i++){
          // res.data.list[i].url = '../bookdetail/bookdetail?ISBN=' + res.data.list[i].ISBN
          searchResult.push(res.data.list[i])
        };
        that.setData({
          searchResult: res.data.list
        });
        console.log(searchResult)
      }
    })
  }

})