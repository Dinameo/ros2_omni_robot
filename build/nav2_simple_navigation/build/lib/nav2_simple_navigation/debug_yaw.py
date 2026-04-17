import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class YawDebugger(Node):
    def __init__(self):
        super().__init__('yaw_debugger')
        self.lastest_yaw = None
        self.latest_yaw_deg = None
        self.sub = self.create_subscription(
            Odometry,
            '/mobile_base_controller/odometry',
            self.odom_callback,
            10
        )
        self.timer = self.create_timer(
            0.5,
            self.print_yaw,
        )

    def odom_callback(self, msg):
        x = msg.pose.pose.orientation.x
        y = msg.pose.pose.orientation.y
        z = msg.pose.pose.orientation.z
        w = msg.pose.pose.orientation.w

        yaw = math.atan2(
            2.0 * (w * z + x * y),
            1.0 - 2.0 * (y * y + z * z)
        )
        self.lastest_yaw = yaw
        self.latest_yaw_deg = math.degrees(yaw)
    def print_yaw(self):
        self.get_logger().info(f"Current Yaw: {self.latest_yaw_deg:.2f} deg")

def main():
    rclpy.init()
    node = YawDebugger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()