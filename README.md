# ROS 2 Omni Navigation Project

Dự án mô phỏng robot omni trong Gazebo Harmonic và điều hướng bằng Nav2 trong bản đồ bệnh viện.

## Thành viên

- Lưu Tấn Phát - MSSV: 23134043
- Nguyễn Thiện Nhân - MSSV: 23134041

## 1. Tổng quan

Project gồm 2 package chính:

- `src/robot_omni`: mô tả robot, world Gazebo, bridge ROS <-> Gazebo, `ros2_control`.
- `src/nav2_simple_navigation`: map, tham số Nav2, Behavior Tree, script di chuyển theo room/waypoint.

Luồng chạy tổng quát:

1. Khởi động Gazebo + spawn robot (`robot_omni`).
2. Khởi động Nav2 stack + RViz (`nav2_simple_navigation`).
3. Gửi goal bằng RViz hoặc bằng script (tên room trong `rooms.yaml`).

## 2. Yêu cầu môi trường

- Ubuntu Linux.
- ROS 2 (khuyến nghị bản tương thích với workspace hiện tại).
- Gazebo Harmonic + `ros_gz` bridge.
- Đã cài các package Nav2, `robot_localization`, `twist_stamper`, `slam_toolbox`.
- `colcon`.

Nếu chưa cấp quyền script:

```bash
cd <path_to_your_ws>
chmod +x *.sh
```

Nên build toàn workspace ít nhất 1 lần trước khi chạy nhanh:

```bash
cd <path_to_your_ws>
colcon build --symlink-install
```

## 3. Cấu trúc thư mục nhanh

```text
project/
	start.sh, stop.sh
	go_to_rooms.sh, go_to_rooms_optimized.sh
	move.sh
	src/
		robot_omni/
			launch/hospital_gazebo_control.launch.py
			config/configuration.yaml
			config/bridge_config.yaml
			worlds/
			urdf/omni_base.urdf
		nav2_simple_navigation/
			launch/nav2_control.launch.py
			config/nav2_params.yaml
			config/hospital_map.yaml
			config/rooms.yaml
			behavior_tree/navigate_smart.xml
```

## 4. Chạy nhanh (khuyến nghị)

### Cách nhanh nhất

```bash
cd <path_to_your_ws>
./start.sh
```

Script sẽ:

1. Build và chạy Gazebo/robot.
2. Đợi theo `DELAY` trong `start.sh`.
3. Build và chạy Nav2 + RViz.

Nếu máy yếu hoặc world nặng, tăng `DELAY` trong `start.sh` để các node lên ổn định hơn.

Dừng toàn bộ:

```bash
cd <path_to_your_ws>
./stop.sh
```

## 5. Gửi goal điều hướng

### Cách 1: Gửi trực tiếp trong RViz

- Dùng công cụ `2D Goal Pose` (hoặc Publish Point tùy setup RViz).
- Click vào điểm đích trong map.

### Cách 2: Đi theo danh sách phòng

```bash
cd <path_to_your_ws>
./go_to_rooms.sh room1 room2_1 room6_1 home
```

Bản tối ưu thứ tự phòng (GA):

```bash
cd <path_to_your_ws>
./go_to_rooms_optimized.sh room1 room2_1 room6_1 home
```

Tên phòng được định nghĩa tại:

- `src/nav2_simple_navigation/config/rooms.yaml`

## 6. Chạy thủ công từng thành phần

Nếu không dùng `start.sh`, có thể mở nhiều terminal:

1. Gazebo + robot

```bash
cd <path_to_your_ws>
colcon build --packages-select robot_omni
source install/setup.bash
ros2 launch robot_omni hospital_gazebo_control.launch.py
```

2. Nav2 + RViz

```bash
cd <path_to_your_ws>
colcon build --packages-select nav2_simple_navigation
source install/setup.bash
ros2 launch nav2_simple_navigation nav2_control.launch.py
```

3. Waypoint node (tùy chọn)

```bash
cd <path_to_your_ws>
source install/setup.bash
ros2 run nav2_simple_navigation waypoints
```

## 7. Tùy chỉnh trước khi chạy

1. Kiểm tra biến `LINK` trong:

- `start.sh`
- `stop.sh`

2. Điều chỉnh `DELAY` trong `start.sh`:

- Tăng nếu world/map nặng.
- Giảm nếu máy khởi động nhanh.

3. Kiểm tra đường dẫn BT trong `nav2_params.yaml` (nếu dùng đường dẫn tuyệt đối):

- `src/nav2_simple_navigation/config/nav2_params.yaml`
- Ví dụ: `default_nav_to_pose_bt_xml: ".../navigate_smart.xml"`

4. Kiểm tra đường dẫn file controller trong URDF:

- `src/robot_omni/urdf/omni_base.urdf`
- Ví dụ: `<parameters>.../src/robot_omni/config/configuration.yaml</parameters>`

5. Chọn world Gazebo nếu cần đổi map mô phỏng:

- `src/robot_omni/launch/hospital_gazebo_control.launch.py`
- Dòng cần sửa: `world_file = os.path.join(pkg, 'worlds', 'hospital_full.world')`

6. Export thư mục models để Gazebo tìm thấy model tùy chỉnh:

```bash
echo 'export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:<path_to_your_ws>/src/robot_omni/models' >> ~/.bashrc
source ~/.bashrc
```

7. Nếu workspace của bạn không phải `<path_to_your_ws>`, sửa lại đường dẫn trong các script shell:

- `start.sh`
- `stop.sh`
- `go_to_rooms.sh`
- `go_to_rooms_optimized.sh`

## 8. Một số script hỗ trợ

- `move.sh`: tạo vật cản động trong Gazebo (wheelchair/scrubs).
- `run_slam.sh`: chạy `slam_toolbox` với `mapper_params.yaml`.
- `save_map.sh`: lưu map về `src/nav2_simple_navigation/config/hospital_map`.
- `render_map.sh`: mở RViz nhanh.

## 9. Lỗi thường gặp

1. `command not found: ros2`:

- Chưa source ROS 2 môi trường.

2. Không spawn được model/mesh:

- Kiểm tra `GZ_SIM_RESOURCE_PATH`.
- Kiểm tra folder `src/robot_omni/models` tồn tại đầy đủ.

3. Nav2 không lên hoặc lifecycle fail:

- Dùng `./stop.sh`, xóa `build install log` nếu cần, rồi build/chạy lại.
- Kiểm tra map file, TF (`map -> odom -> base_footprint`) và topic `/scan_front_raw`.

4. Script chạy được nhưng robot không đi:

- Kiểm tra remap cmd vel trong `nav2_control.launch.py` đến `/mobile_base_controller/reference`.
- Kiểm tra `mobile_base_controller` đã spawn thành công trong launch Gazebo.

## 10. Lệnh dọn workspace (tùy chọn)

```bash
cd <path_to_your_ws>
rm -rf build/ install/ log/
```

Sau đó build/chạy lại bằng `./start.sh`.