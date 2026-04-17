# Lưu ý terminal cd <path to workspace>
1. Đổi link trong file start.sh, stop.sh (biến LINK)

2. Đổi DELAY nếu cần thời gian dài/ngắn hơn (Tăng nếu map full, giảm nếu map aws)

3. Đổi link trong file nav2_simple_navigation/config/nav2_params.yaml, tìm dòng tương tự sau: 
default_nav_to_pose_bt_xml: "/home/nhan/Documents/ros/project/src/nav2_simple_navigation/behavior_tree/navigate_smart.xml"

4. Đổi link trong file robot_omni/urdf/omni_base.urdf, tìm dòng tương tự sau: 
<parameters>/home/nhan/Documents/ros/project/src/robot_omni/config/configuration.yaml</parameters>

5. export lại file robot_omni/models bằng cách gõ lệnh sau trong terminal:
nano ~/.bashrc
paste đoạn này vào cuối file
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:<path to your workspace>/src/robot_omni/models
Ctrl + O -> Ctrl + X -> Enter

6. Đổi map trong robot_omni/launch/hopistal_gazebo_control.launch.py nếu cần, tìm ddòng tương tự sau:
world_file = os.path.join(pkg, 'worlds', 'hospital_full.world')
chọn lại 'hospital_aws.world' hoặc 'hospital_full.world'

7. gõ trên terminal:
sudo chmod +x *.sh
./start.sh -> bắt đầu chạy
./stop.sh -> để dừng

Cách chạy goal:
Cách 1. Trong rviz2 chọn công cụ "Publish Point", click vào điểm bất kỳ để robot đến

Cách 2. Gõ terminal ./go_to_room.sh <danh sách các goal>
Ví dụ
./go_to_room.sh room1 home

# Lưu ý tên phòng được định nghĩa trong: nav2_simple_navigation/config/rooms.yaml