from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Get package path
    pkg_share = get_package_share_directory('nav2_simple_navigation')
    

    # Config files
    ekf_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    nav2_config = os.path.join(pkg_share, 'config', 'nav2_params.yaml')

    # Map file
    map_file = os.path.join(pkg_share, 'config', 'hospital_map.yaml')

    # Rviz config
    rviz_config_path = os.path.join(pkg_share, 'config', 'rviz_config.rviz')

    # -------------------------
    # EKF node
    # -------------------------
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config, {'use_sim_time': True}]
    )

    # -------------------------
    # Nav2 nodes
    # -------------------------
    planner_node = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_config, {'use_sim_time': True}],
    )

    controller_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_config, {'use_sim_time': True}],
        remappings=[('/cmd_vel', '/mobile_base_controller/reference')]
    )

    recoveries_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='recoveries_server',
        output='screen',
        parameters=[nav2_config, {'use_sim_time': True}],
    )
    twist_stamper_node = Node(
        package='twist_stamper',
        executable='twist_stamper',
        name='twist_stamper',
        output='screen',
        remappings=[
            ('cmd_vel_in', '/cmd_vel'),
            ('cmd_vel_out', '/mobile_base_controller/reference')
        ],
        parameters=[{'use_sim_time': True}]
    )

    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_config, {'use_sim_time': True}],
    )

    #  Node map server
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            {'use_sim_time': True},
            {'yaml_filename': map_file}
        ]
    )

    # Node amcl
    amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_config, {'use_sim_time': True}]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': [
                'map_server',
                'amcl',
                'planner_server',
                'controller_server',
                'recoveries_server',
                'bt_navigator'
            ],

            'bond_timeout': 10.0,

            'attempt_respawn_reconnection': True,
            'bond_respawn_max_duration': 10.0
        }]
    )
    waypoints_node = Node(
        package='nav2_simple_navigation',
        executable='waypoints',
        parameters=[{'use_sim_time': True}],
        name='waypoints',
        output='screen',
    )

    waypoints_exc_node = Node(
        package='nav2_simple_navigation',
        executable='waypoints_exc',
        name='waypoints_exc',
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    # RViz
    rviz_node = Node(
        package='rviz2',
        executable=f'rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        name='rviz2',
        output='screen'
    )

    
    

    return LaunchDescription([
        twist_stamper_node,
        map_server_node,
        amcl_node,
        ekf_node,
        planner_node,
        controller_node,
        recoveries_node,
        bt_navigator_node,
        rviz_node,
        waypoints_node,
        waypoints_exc_node,
        lifecycle_manager_node,
    ])