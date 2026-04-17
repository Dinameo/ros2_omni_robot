import yaml
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
from std_msgs.msg import String
import os
from .optimal_path_planner import OptimalPathPlanner

class GoToRoomsOptimized(Node):
    def __init__(self):
        super().__init__('go_to_rooms_optimized')
        
        self.declare_parameter('rooms_list', 'room1 room2 room3')
        self.declare_parameter('use_ga', True)
        self.declare_parameter('ga_generations', 50)
        self.declare_parameter('room_topic', '/room')
        
        pkg_share = get_package_share_directory('nav2_simple_navigation')
        rooms_file = os.path.join(pkg_share, 'config', 'rooms.yaml')
        
        with open(rooms_file, 'r') as f:
            self.rooms_data = yaml.safe_load(f)['rooms']
        
        rooms_raw = self.get_parameter('rooms_list').value
        self.rooms_list = rooms_raw.split() if rooms_raw else []
        
        use_ga = self.get_parameter('use_ga').value
        ga_generations = self.get_parameter('ga_generations').value
        self.room_topic = self.get_parameter('room_topic').value

        self.room_pub = self.create_publisher(String, self.room_topic, 10)
        
        # Sử dụng GA để tối ưu hóa đường đi
        if use_ga and len(self.rooms_list) > 1:
            planner = OptimalPathPlanner(self.rooms_data)
            self.rooms_list = planner.find_optimal_route(
                self.rooms_list,
                generations=ga_generations
            )
            self.get_logger().info(f"Optimized route: {self.rooms_list}")

    def publish_optimized_rooms(self):
        if not self.rooms_list:
            self.get_logger().error('No rooms specified')
            return False

        valid_rooms = []
        for room_name in self.rooms_list:
            if room_name not in self.rooms_data:
                self.get_logger().error(f'Room {room_name} not found')
                continue
            valid_rooms.append(room_name)

        if not valid_rooms:
            self.get_logger().error('No valid goals to publish')
            return False

        msg = String()
        msg.data = ' '.join(valid_rooms)

        # Wait briefly for subscribers so the one-shot publish is not dropped.
        wait_steps = 20
        while self.room_pub.get_subscription_count() == 0 and wait_steps > 0:
            rclpy.spin_once(self, timeout_sec=0.1)
            wait_steps -= 1

        self.room_pub.publish(msg)
        self.get_logger().info(
            f'Published optimized rooms to {self.room_topic}: {msg.data}'
        )
        return True

def main(args=None):
    rclpy.init(args=args)

    node = GoToRoomsOptimized()

    # Reuse existing /room -> waypoints -> waypoints_exc pipeline.
    node.publish_optimized_rooms()
    # Give middleware a moment to flush publisher queue before shutdown.
    rclpy.spin_once(node, timeout_sec=0.2)
    node.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()