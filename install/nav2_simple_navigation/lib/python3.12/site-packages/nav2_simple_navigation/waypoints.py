from geometry_msgs.msg import Pose, PoseArray, PointStamped
from rclpy.node import Node
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory
import os
import math
import yaml
import rclpy
from nav2_msgs.action import NavigateToPose


class WaypoitnsFollower(Node):
    def __init__(self):
        super().__init__('waypoint_node')


        pkg_share = get_package_share_directory('nav2_simple_navigation')
        rooms_file = os.path.join(pkg_share, 'config', 'rooms.yaml')


        with open(rooms_file) as f:
            self.rooms_data = yaml.safe_load(f)
            




        self.queue = []
        self.update = True

        self.pub_wp = self.create_publisher(
            PoseArray,
            '/waypoints',
            10
        )
        self.create_subscription(
            PoseArray,
            '/waypoints_update',
            self.update_queue,
            10
        )

        self.create_subscription(
            PointStamped,
            '/clicked_point',
            self.get_clickedpoint,
            10
        )

        self.create_subscription(
            String,
            '/room',
            self.get_room,
            10
        )



        self.create_timer(
            0.5, 
            self.publish_queue
        )
        self.get_logger().info('waypoints started!')

    def update_queue(self, msg):
        self.queue = list(msg.poses)
        self.update = True
    def get_room(self, msg):
        rooms_name = msg.data.strip().split()
        for room_name in rooms_name:
            if room_name not in self.rooms_data['rooms']:
                self.get_logger().info(f"Not found {room_name}!")
                continue
            room = self.rooms_data['rooms'][room_name]

            x = float(room['x'])
            y = float(room['y'])
            yaw = float(room['yaw'])

            pose = Pose()

            pose.position.x = x
            pose.position.y = y
            pose.position.z = 0.0

            self.set_yaw(pose, yaw)
            self.update = True

            self.queue.append(pose)
            self.get_logger().info(f"Queue added: {room_name}")

    def get_clickedpoint(self, msgs):
        pose = Pose()
        x = float(msgs.point.x)
        y = float(msgs.point.y)
        yaw = 0.0

        pose.position.x = x
        pose.position.y = y
        pose.position.z = 0.0
        self.update = True



        self.set_yaw(pose, yaw)

        self.queue.append(pose)

        self.get_logger().info(f"Clicked point added: (x:{x:.4f}, y:{y:.4f}, yaw:{yaw:.4f})")



    def set_yaw(self, pose, yaw):
        pose.orientation.x = 0.0
        pose.orientation.y = 0.0
        pose.orientation.z = math.sin(yaw / 2.0)
        pose.orientation.w = math.cos(yaw / 2.0)

    def publish_queue(self):
        if not self.update:
            return
        self.update = False
        msg = PoseArray()
        msg.header.frame_id = "map"

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.poses = list(self.queue)
        self.pub_wp.publish(msg)



def main(args=None):

    rclpy.init(args=args)
    node = WaypoitnsFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


