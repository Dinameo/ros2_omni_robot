cd /home/nhan/Documents/ros/project
colcon build --packages-select nav2_simple_navigation
source install/setup.bash
ros2 launch nav2_simple_navigation nav2_control.launch.py