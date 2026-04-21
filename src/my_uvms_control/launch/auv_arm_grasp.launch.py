from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(package='my_uvms_control', executable='auv_arm_grasp', output='screen')
    ])
