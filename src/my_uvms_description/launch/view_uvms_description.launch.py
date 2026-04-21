from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    use_sim = LaunchConfiguration('use_sim')
    use_rviz = LaunchConfiguration('use_rviz')
    description_file = PathJoinSubstitution([
        FindPackageShare('my_uvms_description'),
        'description',
        'bluerov2_heavy_alpha5',
        'config.xacro',
    ])

    robot_description = Command([
        'xacro ', description_file,
        ' use_sim:=', use_sim,
    ])

    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default_value='false'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim}],
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', PathJoinSubstitution([FindPackageShare('blue_description'), 'rviz', 'bluerov2_heavy_reach.rviz'])],
            condition=IfCondition(use_rviz),
            output='screen',
        ),
    ])
