cd ./
colcon build --packages-select robot_omni
cd ./
source install/setup.bash
ros2 launch robot_omni hospital_gazebo_control.launch.py