from launch import LaunchDescription #所有要启动的东西装在LaunchDescription，最后返回它
from launch_ros.actions import Node #描述启动一个ROS2节点的动作
from launch.actions import TimerAction

def generate_launch_description():
    turtlesim_node=Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen',
    )

    tracker_node=TimeAction( #延迟一秒，等turtlesim就绪再启动追踪节点
        period=1.0, 
        actions=[
            Node(
                package='turtle_tracker',
                executable='turtle_tracker_node',
                name='turtle_tracker',
                output='screen', #让日志打印到当前终端，方便调试
                parameters=[{
                    'linear_gain':1.5,
                    'angular_gain':6.0,
                    'stop_distance':0.3,                                
                }],
            )
        ]
    )
    return LaunchDescription([
        turtlesim_node,
        tracker_node,
    ])