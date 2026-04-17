
ROOMS="$*"
cd ./
source install/setup.bash
ros2 run nav2_simple_navigation go_to_rooms_optimized \
  --ros-args -p rooms_list:="$ROOMS" \
  -p use_ga:=true \
  -p ga_generations:=100 \
  -p room_topic:=/room