import { calPieAngle } from 'calPieData'

export default function drawPieChart(series) {

  var pieSeries = calPieAngle(series);
  context.setLineWidth(2);
  context.setStrokeStyle('#ffffff');
  pieSeries.forEach((item) => {
    context.beginPath();
    // 设置填充颜色
    context.setFillStyle(item.color);
    // 移动到原点
    context.moveTo(100, 100);
    // 绘制弧度
    context.arc(100, 100, 80, item.startAngle, item.startAngle + 2 * Math.PI * item.proportion);
    context.closePath();
    context.fill();
    context.stroke();
  });


}