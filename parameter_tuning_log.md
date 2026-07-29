turtle_tracker 参数调试日志

环境
ROS2 humble
日期：2026-06-28
测试场景：turtlesim默认窗口，turtle1随即游走


参数说明

参数: linear_gain
默认值: 1.5
含义:线速度比例增益，越大追的越快但容易超调

参数: angular_gain
默认值: 6.0
含义:角速度比例增益，越大转向幅度也大

参数:stop_diatance
默认值: 0.3
含义: 到达目标的停止距离 


调试记录

2026-06-29 第一轮
目标：让turtle2稳定追上turtle1,不震荡

配置
ros2 run turtle_tracker turtle_tracker \
--ros-args -p linear_gain:=4.0 -p angular_gain:6.0

现象：直线行驶没什么区别，180度反向追踪时弧度稍微小了一点
分析：肉眼其实看不出什么，尝试调整角速度
调整:angular_gain 从 6.0 → 2.0

inear:
  x: 1.311353463851627
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.006585935268111631


2026-06-29 第二轮
配置

ros2 run turtle_tracker turtle_tracker \
--ros-args -p linear_gain:=4.0 -p angular_gain:=2.0

现象：抖动, 转向变慢，追踪延迟明显 
分析：角速度降太多，可以折中 
调整:angular_gain 调到 5.0，linear_gain 提到 2.0



当前最优参数
linear_gain:  4.0
angular_gain: 5.0
stop_distance: 0.3


效果：追踪流畅，无明显震荡










