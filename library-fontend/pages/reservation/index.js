Page({
  data: {
  },
  selectLibrary:function(e){
    wx.navigateTo({
      url: '../reservation/seat?id='+e.currentTarget.dataset.id+'&libraryname='+e.currentTarget.dataset.libraryname,
    })
  },
  onLoad: function (options) {
    
  },
})