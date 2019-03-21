// pages/friendlylink/friendlylink.js
Page({

  data: {
    url: '',
    libLink: [{
        title: 'NDLC（国家图书馆）',
        url: 'http://www.nlc.cn/'
      },
      {
        title: 'NSTL（国科图）',
        url: 'https://www.nstl.gov.cn/'
      },
      {
        title: 'CALIS（高教图）',
        url: 'http://www.calis.edu.cn/'
      },
      {
        title: 'CASHL（人文社科）',
        url: 'http://www.cashl.edu.cn/portal/'
      },
      {
        title: 'CALIS山东省中心',
        url: 'http://58.194.172.106/portal/tpl/calis/index'
      },
      {
        title: '山东高校图工委',
        url: 'http://www.lib.sdu.edu.cn/portal/tpl/tgw/index'
      },
      {
        title: '山东省图书馆',
        url:  'http://www.sdlib.com/'
      },
      {
        title: '威海校区图书馆',
        url: 'http://www.lib.wh.sdu.edu.cn/cn/'
      },
    ]
  },
  // toFriendLink: function(e) {
  //   console.log(e.currentTarget.id)
  //   var url = ''
  //   if (e.currentTarget.id == 0) {
  //     //NDLC（国家图书馆）
  //     url = 'http://www.nlc.cn/'
  //   } else if (e.currentTarget.id == 1) {
  //     //NSTL（国科图）
  //     url = 'https://www.nstl.gov.cn/'
  //   } else if (e.currentTarget.id == 2) {
  //     //CALIS（高教图）
  //     url = 'http://www.calis.edu.cn/'
  //   } else if (e.currentTarget.id == 3) {
  //     //CASHL（人文社科）
  //     url = 'http://www.cashl.edu.cn/portal/'
  //   } else if (e.currentTarget.id == 4) {
  //     //CALIS山东省中心
  //     url = 'http://58.194.172.106/portal/tpl/calis/index'
  //   } else if (e.currentTarget.id == 5) {
  //     //山东高校图工委
  //     url = 'http://www.lib.sdu.edu.cn/portal/tpl/tgw/index'
  //   } else if (e.currentTarget.id == 6) {
  //     //山东省图书馆
  //     url = 'http://www.sdlib.com/'
  //   } else {
  //     //威海校区图书馆
  //     url = 'http://www.lib.wh.sdu.edu.cn/cn/'
  //   }
  //   this.setData({
  //     url: url
  //   })
  //   // console.log(this.data.url)
  //   wx.navigateTo({
  //     url: '../friendlylink/link?url=' + this.data.url,
  //   })
  // },
  onLoad: function(options) {

  },

})