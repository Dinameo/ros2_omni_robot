from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'nav2_simple_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml') + glob('config/*.pgm') + glob('config/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tof',
    maintainer_email='tof@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'square_nav = nav2_simple_navigation.square_nav:main',
            'circle_nav = nav2_simple_navigation.circle_nav:main',
            'bt_nav = nav2_simple_navigation.bt_nav:main',
            'yaw_debugger = nav2_simple_navigation.debug_yaw:main',
            'go_to_room = nav2_simple_navigation.go_to_room:main',
            'pose_debugger = nav2_simple_navigation.debug_pose:main',
            'waypoints = nav2_simple_navigation.waypoints:main',
            'waypoints_exc = nav2_simple_navigation.waypoints_exc:main',
            'go_to_rooms_optimized = nav2_simple_navigation.go_to_rooms_optimized:main'
        ],
    },
)
