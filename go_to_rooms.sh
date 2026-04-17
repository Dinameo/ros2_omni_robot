
ROOMS="$*"
cd /home/nhan/Documents/ros/project
source install/setup.bash
ros2 topic pub /room std_msgs/msg/String "{data: ${ROOMS}}" --once
