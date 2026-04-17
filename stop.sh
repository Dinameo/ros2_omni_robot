LINK="./"
cd $LINK
echo "Stop all!"
pkill -9 -f 'gz sim|ros2|rviz2|robot_state_publisher|controller_manager|spawner|slam_toolbox|ekf_node|parameter_bridge|ros_gz|mobile_base_controller'
# echo "remove all log!"
# rm -rf log
echo "Done!"