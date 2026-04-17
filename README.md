# ROS 2 Omni Navigation Project

Du an mo phong robot omni trong Gazebo Harmonic va dieu huong bang Nav2 trong ban do benh vien.

README nay viet theo trang thai repo hien tai (file launch dung la `hospital_gazebo_control.launch.py`).

## 1. Tong quan

Project gom 2 package chinh:

- `src/robot_omni`: mo ta robot, world Gazebo, bridge ROS <-> Gazebo, ros2_control.
- `src/nav2_simple_navigation`: map, tham so Nav2, Behavior Tree, script di chuyen theo room/waypoint.

Luong chay tong quat:

1. Khoi dong Gazebo + spawn robot (`robot_omni`).
2. Khoi dong Nav2 stack + RViz (`nav2_simple_navigation`).
3. Gui goal bang RViz hoac bang script (ten room trong `rooms.yaml`).

## 2. Yeu cau moi truong

- Ubuntu Linux.
- ROS 2 (khuyen nghi ban tuong thich voi workspace hien tai).
- Gazebo Harmonic + `ros_gz` bridge.
- Da cai cac package Nav2, `robot_localization`, `twist_stamper`, `slam_toolbox`.
- `colcon`.

Neu chua cap quyen script:

```bash
cd <path_to_your_ws>
chmod +x *.sh
```

Nen build tong workspace it nhat 1 lan truoc khi chay nhanh:

```bash
cd <path_to_your_ws>
colcon build --symlink-install
```

## 3. Cau truc thu muc nhanh

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

## 4. Chay nhanh (khuyen nghi)

### Cach nhanh nhat

```bash
cd <path_to_your_ws>
./start.sh
```

Script se:

1. Build va chay Gazebo/robot.
2. Doi theo `DELAY` trong `start.sh`.
3. Build va chay Nav2 + RViz.

Neu may yeu hoac world nang, tang `DELAY` trong `start.sh` de cac node len on dinh hon.

Dung toan bo:

```bash
cd <path_to_your_ws>
./stop.sh
```

## 5. Gui goal dieu huong

### Cach 1: Gui truc tiep trong RViz

- Dung cong cu `2D Goal Pose` (hoac Publish Point tuy setup RViz).
- Click vao diem dich trong map.

### Cach 2: Di theo danh sach phong

```bash
cd <path_to_your_ws>
./go_to_rooms.sh room1 room2_1 room6_1 home
```

Ban toi uu thu tu phong (GA):

```bash
cd <path_to_your_ws>
./go_to_rooms_optimized.sh room1 room2_1 room6_1 home
```

Ten phong duoc dinh nghia tai:

- `src/nav2_simple_navigation/config/rooms.yaml`

## 6. Chay thu cong tung thanh phan

Neu khong dung `start.sh`, co the mo nhieu terminal:

1. Gazebo + robot

```bash
cd <path_to_your_ws>
colcon build --packages-select robot_omni
source install/setup.bash
ros2 launch robot_omni hospital_gazebo_control.launch.py
```

Luu y: `run_robot_omni.sh` trong repo dang goi nham ten file `hopistal_gazebo_control.launch.py` (typo). Khi chay thu cong, hay dung lenh ben tren hoac sua lai script nay.

2. Nav2 + RViz

```bash
cd <path_to_your_ws>
colcon build --packages-select nav2_simple_navigation
source install/setup.bash
ros2 launch nav2_simple_navigation nav2_control.launch.py
```

3. Waypoint node (tuy chon)

```bash
cd <path_to_your_ws>
source install/setup.bash
ros2 run nav2_simple_navigation waypoints
```

## 7. Tuy chinh truoc khi chay

1. Kiem tra bien `LINK` trong:

- `start.sh`
- `stop.sh`

2. Dieu chinh `DELAY` trong `start.sh`:

- Tang neu world/map nang.
- Giam neu may khoi dong nhanh.

3. Kiem tra duong dan BT trong `nav2_params.yaml` (neu dung duong dan tuyet doi):

- `src/nav2_simple_navigation/config/nav2_params.yaml`
- Vi du: `default_nav_to_pose_bt_xml: ".../navigate_smart.xml"`

4. Kiem tra duong dan file controller trong URDF:

- `src/robot_omni/urdf/omni_base.urdf`
- Vi du: `<parameters>.../src/robot_omni/config/configuration.yaml</parameters>`

5. Chon world Gazebo neu can doi map mo phong:

- `src/robot_omni/launch/hospital_gazebo_control.launch.py`
- Dong can sua: `world_file = os.path.join(pkg, 'worlds', 'hospital_full.world')`

6. Neu workspace cua ban khong phai `<path_to_your_ws>`, sua lai duong dan trong cac script shell:

- `start.sh`
- `stop.sh`
- `go_to_rooms.sh`
- `go_to_rooms_optimized.sh`

## 8. Mot so script ho tro

- `move.sh`: tao vat can dong trong Gazebo (wheelchair/scrubs).
- `run_slam.sh`: chay `slam_toolbox` voi `mapper_params.yaml`.
- `save_map.sh`: luu map ve `src/nav2_simple_navigation/config/hospital_map`.
- `render_map.sh`: mo RViz nhanh.

## 9. Loi thuong gap

1. `command not found: ros2`:

- Chua source ROS 2 moi truong.

2. Khong spawn duoc model/mesh:

- Kiem tra `GZ_SIM_RESOURCE_PATH`.
- Kiem tra folder `src/robot_omni/models` ton tai day du.

3. Nav2 khong len hoac lifecycle fail:

- Dung `./stop.sh`, xoa `build install log` neu can, roi build/chay lai.
- Kiem tra map file, TF (`map -> odom -> base_footprint`) va topic `/scan_front_raw`.

4. Script chay duoc nhung robot khong di:

- Kiem tra remap cmd vel trong `nav2_control.launch.py` den `/mobile_base_controller/reference`.
- Kiem tra `mobile_base_controller` da spawn thanh cong trong launch Gazebo.

## 10. Lenh don workspace (tuy chon)

```bash
cd <path_to_your_ws>
rm -rf build/ install/ log/
```

Sau do build/chay lai bang `./start.sh`.