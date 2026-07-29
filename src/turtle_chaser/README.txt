1.项目：ROS2 乌龟追踪器
一只乌龟（turtle2）自动追踪另一只乌龟（turtle1）追到天荒地老的 ROS2 练习。

2.环境要求
- Ubuntu 22.04
- ROS2 Humble

## Demo完整运行演示（2分钟全过程）
https://www.bilibili.com/video/BV1qM3169Eof/?vd_source=10acb7bb4ea6ccbe0d60d3fa561b9ab2

3. 安装
cd ~/ros2_ws/src
git clone https://github.com/5683925/ros2-learning.git
cd ~/ros2_ws
colcon build --packages-select turtle_tracker
source install/setup.bash


4.如何 运行
终端1：启动仿真器
ros2 run turtlesim turtlesim_node

终端2：启动追踪节点
首次运行前需要先编译：colcon build --packages-select turtle_chaser 并 source install/setup.bash
ros2 run turtle_chaser turtle_tracker

终端3：控制 turtle1，turtle2 会自动追踪
ros2 run turtlesim turtle_teleop_key

5.原理
turtle2 每 0.1 秒计算一次与 turtle1 的距离和角度误差，使用比例控制（P控制）输出线速度和角速度，距离越远速度越大，角度偏差越大转向越快。
