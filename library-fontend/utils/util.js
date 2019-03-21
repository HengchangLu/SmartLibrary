const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('/') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}
const formatTime1 = date => {
  const hour = date.getHours()
  const minute = date.getMinutes()
  return[hour, minute].map(formatNumber).join(':')
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : '0' + n
}



var rootDocment = 'https://lib.lu2322.top/';

function req(url, data, cb) {
  wx.request({
    url: rootDocment + url,
    data: data,
    method: 'GET',
    header: {
      'Content-Type': 'application/json'
    },
    success: function(res) {
      return typeof cb == "function" && cb(res.data)
    },
    fail: function() {
      return typeof cb == "function" && cb(false)
    }
  })
}

module.exports = {
  formatTime: formatTime,
  req:req,
  formatTime1: formatTime1,
  
}