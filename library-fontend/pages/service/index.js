Page({

  data: {
    service: [{
        title: '开放时间',
        show: false,
      },
      {
        title: '借阅服务',
        show: true,
        secondTitle: ['借还书管理规定', '借阅册数与期限', '委托借阅和预约借阅', '借阅违章处理办法']
      },
      {
        title: '空间与设施',
        show: true,
        secondTitle: ['中心校区文理分馆', '中心校区蒋震图书馆', '洪家楼校区政法分馆', '千佛山校区工学分馆', '趵突泉校区医学分馆', '兴隆山校区图书馆', '软件园校区图书馆', '空间设施', '研讨间设备']
      },
      {
        title: 'ISSN号与CNSN号的区别',
        show: false,
      },
      {
        title: '联系我们',
        show: false,
      },
      {
        title: '常见问题',
        show: false,
      },
    ]
  },
  // toDetailPage:function(e){
  //   console.log(e.data)
  //   wx.navigateTo({
  //     url: '../service/detail?title='+ ,

  //   })
  // },
  //点击最外层列表展开 收齐
  listTap(e) {
    console.log('触发了最外层')
    var Index = e.currentTarget.dataset.parentindex;
    var service = this.data.service
    service[Index].show1 = !service[Index].show1 || false;
    //如果点击后是展开状态，则让其他已经展开的列表变为收起状态
    if (service[Index].show1) {
      this.packUp(service, Index);
    }
    this.setData({
      service
    })
  },
  packUp(service, index) {
    for (let i = 0, len = service.length; i < len; i++) { //其他最外层列表变为关闭状态 
      if (index != i) {
        service[i].show1 = false;
      }
    }
  },
  onLoad: function(options) {
    
  },

})