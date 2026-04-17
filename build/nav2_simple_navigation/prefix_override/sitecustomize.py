import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/nhan/Documents/ros/project/install/nav2_simple_navigation'
