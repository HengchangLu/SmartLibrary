Page({

  /**
   * 页面的初始数据
   */
  data: {
    viewList: [
      { 'book_img': 'http://p2-q.mafengwo.net/s5/M00/A4/98/wKgB21B0F1uqJYiiAA5hdmwr9xI79.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100', 'name': '栈桥', 'desc': '青岛栈桥是青岛海滨风景区的景点之一，是国务院于1982年首批公布的国家级风景名胜区，也是首批国家AAAA级旅游景区.青岛栈桥位于游人如织的青岛中山路南端，桥身从海岸探入如弯月般的青岛湾深处。桥身供游人参观并在此停靠旅游船，由此乘船可看海上青岛'},

      { 'book_img': 'https://dimg03.c-ctrip.com/images/100a0u000000j4wtsC082_C_350_230.jpg', 'name': '八大关', 'desc': '八大关(Eight Great Passes)，位于山东省青岛市市南区汇泉东部，太平山南麓，始建于20世纪30年代，是中国著名的风景疗养区，面积70余公顷。十条幽静清凉的大路纵横其间，主要大路因以我国八大著名关隘命名，故统称为八大关。'},

      { 'book_img': 'https://gss0.baidu.com/7LsWdDW5_xN3otqbppnN2DJv/lvpics/pic/item/0e2442a7d933c89518458d34d01373f082020041.jpg', 'name': '崂山', 'desc': '崂山，古称劳山、牢山，位于中国青岛市，黄海之滨，是中国著名的旅游名山，被誉为“海上第一仙山”，主峰巨峰（崂顶）海拔1132.7米，为山东省第三高峰。1982年被国务院设为中国名胜景区之一。其上道教宫观太清宫1983年获称道教全国重点宫观。' },

      { 'book_img': 'https://gss0.baidu.com/7LsWdDW5_xN3otqbppnN2DJv/lvpics/pic/item/6609c93d70cf3bc70035d8a3d000baa1cd112a43.jpg', 'name': '极地海洋世界', 'desc': '青岛极地海洋世界位于山东省青岛市崂山区东海东路60号，是一个集休闲、娱乐、购物、文化为一体的大型海洋世界综合体，于2006年7月竣工，其中一期核心项目极地海洋动物展示和表演馆、海洋博览与科普展示馆，现为国家AAAA级旅游景区。' },

      { 'book_img': 'https://gss0.baidu.com/7LsWdDW5_xN3otqbppnN2DJv/lvpics/pic/item/d35a10f450bed836dcc47460.jpg', 'name': '信号山公园', 'desc': '信号山公园位于山东省青岛市市南区中部，海拔98米。德国侵占青岛后，为指挥进出胶州湾的船只，在山顶部建信号发布台1处，每天悬挂各类信号标志及气象、风力标志，命名为“华兹马克山”，市民称“挂旗山”或“旗台山”。' },

      { 'book_img': 'https://gss0.baidu.com/7LsWdDW5_xN3otqbppnN2DJv/lvpics/pic/item/37d12f2eb9389b5004fded8d8435e5dde6116eea.jpg', 'name': '观象山公园', 'desc': '观象山公园 观象山原名水道山，海拔78.9米，占地6.25公顷。后因建气象台故名。规划为以天文、气象科普教育为主要内容的公园，为市南区域性公园，并作为对外开放的登高眺望点。' },

      { 'book_img': 'https://gss0.baidu.com/7LsWdDW5_xN3otqbppnN2DJv/lvpics/pic/item/1e30e924b899a901aa0759731d950a7b0208f541.jpg', 'name': '小鱼山公园', 'desc': '小鱼山位于青岛市莱阳路东段以北，中国海洋大学鱼山校区东南角。海拔60米，面积2.5公顷，绿地面积2.1公顷，绿地率84%。是青岛市第一座古典风格的山头园林公园。附近有鱼山路，因此得名。' },

      { 'book_img': 'https://img1.qunarzz.com/travel/d6/1707/99/4ff167ff1db221b5.jpg', 'name': '老舍公园', 'desc': '老舍公园位于青岛市市南区安徽路中段中部。北临德县路、曲阜路交汇处，南与湖南路相接，面向青岛湾。湖北路横贯其中，分南北两部分，为敞开式公园。2005年公园面积9800平方米，职工10人，年游人量50万人次。' },

    ]
  },
  toPic: function(options){
    wx.showToast({
      title: "生成中",
      icon: 'loading',
      duration: 2000,
    })
    
    setTimeout(function () {
      wx.navigateTo({
        url: '././pic',
      })
    }, 2000)
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
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