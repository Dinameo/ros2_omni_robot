LINK="~/Documents/ros/project"
DELAY=20
echo "Running gazebo!"
gnome-terminal --title="Run gazebo" -- bash -c "cd $LINK;colcon build --packages-select robot_omni;source install/setup.bash;ros2 launch robot_omni hospital_gazebo_control.launch.py"
echo "wait ${DELAY} seconds"
for i in $(seq "${DELAY}" -1 0)
do
    echo "Please wait ${i} seconds..."
    sleep 1
done
echo "Running nav2 and rendering map!"
gnome-terminal --title="Run nav2" -- bash -c "cd $LINK;colcon build --packages-select nav2_simple_navigation;source install/setup.bash;ros2 launch nav2_simple_navigation nav2_control.launch.py"
echo "wait ${DELAY} seconds"
for i in $(seq "${DELAY}" -1 0)
do
    echo "Please wait ${i} seconds..."
    sleep 1
done
# echo "Rendering map!"
# gnome-terminal --title="Run rviz2" -- bash -c "cd $LINK;source install/setup.bash;rviz2"
# gnome-terminal --title="Start waypoints" -- bash -c "cd $LINK;./run_waypoints.sh"
# gnome-terminal --title="Start waypoints" -- bash -c "cd $LINK;./run_waypoints_exc.sh"
echo "Succesfully!"
