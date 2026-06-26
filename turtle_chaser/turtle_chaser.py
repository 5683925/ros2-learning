import rclpy   
from rclpy.node import Node 
import math

from geometry_msgs.msg import Twist 
from turtlesim.msg import Pose 
from turtlesim.srv import Spawn 


class TurtleTrackerNode(Node):
    def __init__(self):
        super().__init__('turtle_tracker')

        self.declare_parameter('linear_gain', 1.5)    
        self.declare_parameter('angular_gain', 6.0)   
        self.declare_parameter('stop_distance', 0.3) 

        self.kp_linear  = self.get_parameter('linear_gain').value 
        self.kp_angular = self.get_parameter('angular_gain').value
        self.stop_dist  = self.get_parameter('stop_distance').value

        self.pose_target  = None   
        self.pose_tracker = None   

        self.sub_target = self.create_subscription(
            Pose,  
            '/turtle1/pose',  
            self.cb_target_pose,  #回调函数
            10  
        )

        self.sub_tracker = self.create_subscription(
            Pose,
            '/turtle2/pose',
            self.cb_tracker_pose,
            10
        )

        self.pub_cmd = self.create_publisher(
            Twist,
            '/turtle2/cmd_vel',
            10
        )

        self.timer = self.create_timer(0.1, self.control_loop) #每0.1秒触发一次控制循环

        self.spawn_turtle2()

        self.get_logger().info('🐢 乌龟追踪节点已启动,turtle2 将追踪 turtle1')


    def cb_target_pose(self, msg: Pose):
        self.pose_target = msg

    def cb_tracker_pose(self, msg: Pose):
        self.pose_tracker = msg

    def spawn_turtle2(self):
        client=self.create_client(Spawn,'/spawn')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("等待/spawn服务。。")
        
        req=Spawn.Request()
        req.x=2.0
        req.y=2.0
        req.theta=0.0
        req.name='turtle2'

        future=client.call_async(req)
        rclpy.spin_until_future_complete(self,future)

        if future.result() is not None:
            self.get_logger().info(f'turtle2 已生成：{future.result().name}')
        else:
            self.get_logger().warn('turtle2可能已存在, 继续运行。。')

    
    def control_loop(self):
        if self.pose_target is None or self.pose_tracker is None:
            return
        
        dx=self.pose_target.x-self.pose_tracker.x
        dy=self.pose_target.y-self.pose_tracker.y
        distance=math.sqrt(dx**2+dy**2)

        if distance < self.stop_dist:
            self.pub_cmd.publish(Twist())
            self.get_logger().info('已追踪到目标',throttle_duration_sec=2.0)
            return
        
        target_angle=math.atan2(dy,dx)

        angle_error=target_angle-self.pose_tracker.theta
        angle_error=math.atan2(math.sin(angle_error),math.cos(angle_error))

        cmd=Twist()
        cmd.linear.x=self.kp_linear*distance
        cmd.angular.z=self.kp_angular*angle_error

        cmd.linear.x=min(cmd.linear.x,2.0)
        cmd.angular.z=max(min(cmd.angular.z,2.5),-2.5)

        self.pub_cmd.publish(cmd)

        self.get_logger().debug(
            f'距离:{distance:.2f} 角误差:{math.degrees(angle_error):.1f}° '
            f'v={cmd.linear.x:.2f} w={cmd.angular.z:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node=TurtleTrackerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('节点已停止')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()
