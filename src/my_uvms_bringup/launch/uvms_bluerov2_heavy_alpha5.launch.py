import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction, RegisterEventHandler
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import AnyLaunchDescriptionSource, PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    args = [
        DeclareLaunchArgument('use_sim', default_value='true'),
        DeclareLaunchArgument('use_rviz', default_value='false'),
        DeclareLaunchArgument('use_camera', default_value='false'),
        DeclareLaunchArgument('use_mocap', default_value='false'),
        DeclareLaunchArgument('localization_source', default_value='gazebo'),
        DeclareLaunchArgument('use_manager', default_value='true'),
        DeclareLaunchArgument('use_mock_hardware', default_value='true'),
        DeclareLaunchArgument('serial_port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('prefix', default_value=''),
        DeclareLaunchArgument('load_blue_velocity_controller', default_value='true'),
        DeclareLaunchArgument('load_arm_position_controllers', default_value='true'),
    ]

    use_sim = LaunchConfiguration('use_sim')
    use_rviz = LaunchConfiguration('use_rviz')
    use_camera = LaunchConfiguration('use_camera')
    use_mocap = LaunchConfiguration('use_mocap')
    localization_source = LaunchConfiguration('localization_source')
    use_manager = LaunchConfiguration('use_manager')
    use_mock_hardware = LaunchConfiguration('use_mock_hardware')
    serial_port = LaunchConfiguration('serial_port')
    prefix = LaunchConfiguration('prefix')
    load_blue_velocity_controller = LaunchConfiguration('load_blue_velocity_controller')
    load_arm_position_controllers = LaunchConfiguration('load_arm_position_controllers')

    description_file = PathJoinSubstitution([
        FindPackageShare('my_uvms_description'), 'description', 'bluerov2_heavy_alpha5', 'config.xacro'
    ])
    controllers_file = PathJoinSubstitution([
        FindPackageShare('my_uvms_description'), 'config', 'bluerov2_heavy_alpha5', 'controllers.yaml'
    ])
    robot_description = Command([
        'xacro ', description_file,
        ' use_sim:=', use_sim,
        ' prefix:=', prefix,
        ' use_mock_hardware:=', use_mock_hardware,
        ' serial_port:=', serial_port,
        ' controllers_file:=', controllers_file,
    ])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim}],
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', PathJoinSubstitution([FindPackageShare('blue_description'), 'rviz', 'bluerov2_heavy_reach.rviz'])],
        parameters=[{'use_sim_time': use_sim}],
        condition=IfCondition(use_rviz),
    )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='both',
        parameters=[controllers_file, {'use_sim_time': use_sim}],
        remappings=[('/controller_manager/robot_description', '/robot_description')],
        condition=UnlessCondition(use_sim),
    )

    jsb_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        parameters=[{'use_sim_time': use_sim}],
        condition=IfCondition(load_arm_position_controllers),
    )
    arm_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['forward_position_controller', '--controller-manager', '/controller_manager'],
        parameters=[{'use_sim_time': use_sim}],
        condition=IfCondition(load_arm_position_controllers),
    )
    tcp_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['tcp_position_controller', '--controller-manager', '/controller_manager'],
        parameters=[{'use_sim_time': use_sim}],
        condition=IfCondition(load_arm_position_controllers),
    )

    spawn_after_cm = RegisterEventHandler(
        OnProcessStart(
            target_action=controller_manager,
            on_start=[jsb_spawner, arm_spawner, tcp_spawner],
        )
    )

    # In simulation the gz_ros2_control plugin creates the controller manager when the model is spawned.
    sim_arm_controllers = TimerAction(period=8.0, actions=[jsb_spawner, arm_spawner, tcp_spawner], condition=IfCondition(use_sim))

    ardusub_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('ardusub_bringup'), 'launch', 'ardusub.launch.yaml'])),
        launch_arguments={
            'mavros_file': PathJoinSubstitution([FindPackageShare('blue_description'), 'config', 'ardusub', 'mavros.yaml']),
            'gazebo_world_file': PathJoinSubstitution([FindPackageShare('blue_description'), 'gazebo', 'worlds', 'underwater.world']),
            'ardusub_params_file': PathJoinSubstitution([FindPackageShare('blue_description'), 'config', 'bluerov2_heavy_reach', 'ardusub.parm']),
            'manager_file': PathJoinSubstitution([FindPackageShare('blue_description'), 'config', 'ardusub', 'ardusub_manager.yaml']),
            'model_name': 'bluerov2_heavy_reach',
            'use_sim': use_sim,
            'use_manager': use_manager,
        }.items(),
    )

    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('blue_localization'), 'launch', 'localization.launch.py'])),
        launch_arguments={
            'localization_source': localization_source,
            'use_camera': use_camera,
            'use_mocap': use_mocap,
            'use_sim_time': use_sim,
            'config_filepath': PathJoinSubstitution([FindPackageShare('blue_description'), 'config', 'bluerov2_heavy_reach', 'localization.yaml']),
        }.items(),
    )

    thruster_tf_launch = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('blue_bringup'), 'launch', 'bluerov2_heavy_reach', 'thrusters.launch.yaml']))
    )

    blue_controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([FindPackageShare('blue_demos'), 'control_integration', 'launch', 'bluerov2_heavy_controllers.launch.py'])),
        launch_arguments={'use_sim': use_sim}.items(),
        condition=IfCondition(load_blue_velocity_controller),
    )
    delayed_blue_controllers = TimerAction(period=10.0, actions=[blue_controller_launch], condition=IfCondition(use_sim))

    return LaunchDescription(args + [
        robot_state_publisher,
        rviz_node,
        controller_manager,
        spawn_after_cm,
        sim_arm_controllers,
        ardusub_launch,
        localization_launch,
        thruster_tf_launch,
        delayed_blue_controllers,
    ])
