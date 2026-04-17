import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
import math

class PoseDebugger(Node):
    def __init__(self):
        super().__init__('pose_debugger')
        self.yaw = None
        self.yaw_deg = None
        self.x = None
        self.y = None
        # self.sub = self.create_subscription(
        #     Odometry,
        #     '/mobile_base_controller/odometry',
        #     self.odom_callback,
        #     10
        # )
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.timer = self.create_timer(
            0.5,
            self.print_pose,
        )

    def print_pose(self):        
        try:
            trans = self.tf_buffer.lookup_transform(
                'map',
                'base_footprint',   # neu khong co frame nay thi doi thanh base_link
                rclpy.time.Time()
            )
            self.x = trans.transform.translation.x
            self.y = trans.transform.translation.y

            qx = trans.transform.rotation.x
            qy = trans.transform.rotation.y
            qz = trans.transform.rotation.z
            qw = trans.transform.rotation.w

            siny_cosp = 2.0 * (qw * qz + qx * qy)
            cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
            self.yaw = math.atan2(siny_cosp, cosy_cosp)
            self.yaw_deg = math.degrees(self.yaw)
            if None in (self.x, self.y, self.yaw_deg, self.yaw):
                self.get_logger().warning(f'Pose not ready!')
            
            else:
                self.get_logger().info(f"x:{self.x:.2f}, y:{self.y:.2f}, yaw:{self.yaw_deg:.2f} deg, yaw:{self.yaw:.2f} rad")
        except Exception as e:
            self.get_logger().warn(f"TF lookup failed: {str(e)}")
def main():
    rclpy.init()
    node = PoseDebugger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()