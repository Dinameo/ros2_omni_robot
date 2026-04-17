cd /home/nhan/Documents/ros/project
colcon build --packages-select robot_omni
cd /home/nhan/Documents/ros/project
source install/setup.bash
ros2 launch robot_omni hopistal_gazebo_control.launch.py