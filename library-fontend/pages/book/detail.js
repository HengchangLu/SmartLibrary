//pages/bookdetail.js
var util = require("../../utils/util.js")
var book_catalog = ''
const app = getApp()
var labels = []
Page({
  data: {
    isFoldContent: true,
    isFoldAuthor: true,
    isFoldCatalog: true,
    posPr: 2,
  },
  onLoad: function(options) {
    var that = this;
    that.setData({
      isbn: options.isbn,
      title: options.title,
      ztNum: options.ztNum,
      currentType: options.currentType,
    })
    util.req("book/detail/", {
      currentType: options.currentType,
      isbn: options.isbn,
      title: options.title,
      },
      function(data) {
        if (data.result) {
          if (data.content.book_catalog) {
            that.setData({
              book_catalog: data.content.book_catalog.split('\\n'),
            })
          }
          if (data.content.book_intro) {
            that.setData({
              book_intro: data.content.book_intro.split('\\n'),
            })
          }
          if (data.content.author_intro) {
            that.setData({
              author_intro: data.content.author_intro.split('\\n'),
            })
          }
          that.setData({
            content: data.content,
            labels: data.content.label.split(' '),
          })
        }
      })
    var reg = new RegExp("[\\u4E00-\\u9FFF]+", "g");
    // console.log(that.data.book_catalog)
    setTimeout(function() {
      that.showPie()
      console.log(that.data.content)
    }, 1000)
  },
  showAllContent: function(e) {
    this.setData({
      isFoldContent: !this.data.isFoldContent
    })
  },
  showAllAuthor: function (e) {
    this.setData({
      isFoldAuthor: !this.data.isFoldAuthor
    })
  },
  showAllCatalog: function (e) {
    this.setData({
      isFoldCatalog: !this.data.isFoldCatalog
    })
  },
  
  showPie: function() {
    var context = wx.createContext('mypie');
    var array = [Number(this.data.content.emotion_1), Number(this.data.content.emotion_2), Number(this.data.content.emotion_3), Number(this.data.content.emotion_4), Number(this.data.content.emotion_5)];
    var colors = ["#EEEE00", "#EE0000", "#00C953", "#1E90FF", "#D3D3D3"]
    var total = 0;

    for (var index = 0; index < array.length; index++) {
      total += array[index]
    }
    //定义圆心坐标
    var point = {
      x: 75,
      y: 75
    }
    //定义半径大小
    var radius = 70
    for (var i = 0; i < array.length; i++) {
      context.beginPath();
      //起点弧度
      var start = 0;
      if (i > 0) {
        //计算开始弧度是前几项的总和，即从之前的基础上继续作画
        for (var j = 0; j < i; j++) {
          start += array[j] / total * 2 * Math.PI;
        }
      }
      context.arc(point.x, point.y, radius, start, start + array[i] / total * 2 * Math.PI, false);
      context.setLineWidth(1);
      //连线回圆心
      context.lineTo(point.x, point.y);
      context.setStrokeStyle("#f5f5f5");
      //填充样式
      context.setFillStyle(colors[i])
      //填充动作
      context.fill();
      context.stroke(); // 白色分界线
      context.closePath(); //关闭路径
    }
    //context.draw();
    //调用wx.drawCanvas 通过canvasId指定在哪张画布上绘制，通过actions指定绘制行为
    wx.drawCanvas({
      canvasId: 'mypie',
      actions: context.getActions()
    })
    // ["#EEEE00", "#EE0000", "#00C953", "#1E90FF", "#D3D3D3"]
    context.beginPath(); //开始一个新的路径
    context.rect(0, 0, 14, 14);
    // context.stroke();     //对当前路径进行描边
    context.setFillStyle("#EEEE00");
    context.fill();
    context.closePath();
    wx.drawCanvas({
      canvasId: 'canvasRect1',
      actions: context.getActions(),
    })

    context.beginPath(); //开始一个新的路径
    context.rect(0, 0, 14, 14);
    // context.stroke();     //对当前路径进行描边
    context.setFillStyle("#EE0000");
    context.fill();
    context.closePath();
    wx.drawCanvas({
      canvasId: 'canvasRect2',
      actions: context.getActions(),
    })

    context.beginPath(); //开始一个新的路径
    context.rect(0, 0, 14, 14);
    // context.stroke();     //对当前路径进行描边
    context.setFillStyle("#00C953");
    context.fill();
    context.closePath();
    wx.drawCanvas({
      canvasId: 'canvasRect3',
      actions: context.getActions(),
    })

    context.beginPath(); //开始一个新的路径
    context.rect(0, 0, 14, 14);
    // context.stroke();     //对当前路径进行描边
    context.setFillStyle("#1E90FF");
    context.fill();
    context.closePath();
    wx.drawCanvas({
      canvasId: 'canvasRect4',
      actions: context.getActions(),
    })

    context.beginPath(); //开始一个新的路径
    context.rect(0, 0, 14, 14);
    // context.stroke();     //对当前路径进行描边
    context.setFillStyle("#D3D3D3");
    context.fill();
    context.closePath();
    wx.drawCanvas({
      canvasId: 'canvasRect5',
      actions: context.getActions(),
    })
  },
})