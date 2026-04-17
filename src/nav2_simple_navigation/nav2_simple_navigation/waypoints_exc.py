from geometry_msgs.msg import Pose, PoseArray, PoseStamped
from rclpy.node import Node
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory
import os
import math
import yaml
from nav_msgs.msg import Path
import rclpy
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

class WaypointsExcutor(Node):
    def __init__(self):
        super().__init__('waypoints_excutor')
        self.queue = []
        self.goal = None
        self.frame_id = None
        self.running = False



        self.create_subscription(
            PoseArray,
            '/waypoints',
            self.get_sub,
            10

        )
        self.pub = self.create_publisher(
            PoseArray,
            '/waypoints_update',
            10
        )
        self.pub_pt = self.create_publisher(
            Path,
            '/waypoints_path',
            10
        )

        self.client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.client.wait_for_server()

        self.create_timer(0.5, self.loop)

        self.get_logger().info(f"Waypoints excutor started!")

    def pub_path(self, msg):
        path = Path()
        path.header.frame_id = self.frame_id
        current_time = self.get_clock().now().to_msg()
        path.header.stamp = current_time

        for pose in msg.poses:
            new_pose_stamped = PoseStamped()
            new_pose_stamped.header.stamp = current_time
            new_pose_stamped.header.frame_id = self.frame_id
            new_pose_stamped.pose = pose
            path.poses.append(new_pose_stamped)


        self.pub_pt.publish(path)
    def get_sub(self, msg):
        self.frame_id = msg.header.frame_id
        self.queue = list(msg.poses)
        self.pub_path(msg)

    def get_point(self):
        
        pose = self.queue[0]

        self.goal = NavigateToPose.Goal()
        ps = PoseStamped()
        ps.header.frame_id = self.frame_id
        ps.header.stamp = self.get_clock().now().to_msg()

        ps.pose = pose


        self.goal.pose = ps

        self.running = True

        
        self.future = self.client.send_goal_async(self.goal)
        self.future.add_done_callback(self.goal_response)

    def goal_response(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.queue.pop(0)
            self.update_waypoints_prep()
            self.get_logger().info(f"Goal rejected")
            self.running = False
            return
        
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)
        

    def result_callback(self, future):
        self.get_logger().info("Goal finished")

        self.running = False
        self.queue.pop(0)
        self.update_waypoints_prep()
        self.goal = None

    def loop(self):
        if self.running:
            return
        if not self.queue:
            return
        
        self.get_point()
    def update_waypoints_prep(self):
        msg = PoseArray()
        msg.poses = self.queue
        msg.header.frame_id = self.frame_id
        self.pub.publish(msg=msg)


def main(args=None):

    rclpy.init(args=args)
    node_exc = WaypointsExcutor()
    rclpy.spin(node_exc)
    node_exc.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
