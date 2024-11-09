from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():

    # Gazebo 실행을 위한 경로 설정
    gazebo_launch_file_dir = '/opt/ros/humble/share/gazebo_ros/launch'

    return LaunchDescription([

        # Gazebo 시뮬레이터 실행
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gazebo_launch_file_dir, 'gazebo.launch.py')
            ),
        ),

        # Gazebo가 시작된 후 로봇을 스폰 (약간의 지연시간 추가)
        TimerAction(
            period=5.0,  # 5초 지연 후 실행
            actions=[
                Node(
                    package='gazebo_ros',
                    executable='spawn_entity.py',
                    name='spawn_entity',
                    arguments=[
                        '-entity', 'excavator',
                        '-file', '/home/yerim/Yonsei_ws/src/HuRo/HuRo/simple_excavator.xml'
                    ],
                    output='screen'
                )
            ]
        ),

        # robot_state_publisher를 통해 로봇의 상태를 게시
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': open('/home/yerim/Yonsei_ws/src/HuRo/HuRo/simple_excavator.xml', 'r').read()}]  # <robot의 경로>를 실제 URDF 파일 경로로 변경
        ),

        # joint_state_publisher_gui를 통해 조인트 상태 조정
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),

        # ros_gz_bridge를 통해 Gazebo와의 통신 설정
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/joint_states@sensor_msgs/msg/JointState@gz.msgs.JointState'],
            output='screen'
        ),

        # controller_manager 실행 (지연 시간 추가)
        TimerAction(
            period=10.0,  # 10초 지연 후 실행
            actions=[
                Node(
                    package='controller_manager',
                    executable='ros2_control_node',
                    name='controller_manager',
                    output='screen',
                    parameters=[
                        '/home/yerim/Yonsei_ws/src/HuRo/controller_config.yml',  # YAML 파일 경로
                        {'robot_description': open('/home/yerim/Yonsei_ws/src/HuRo/HuRo/simple_excavator.xml', 'r').read()}  # URDF 파일 경로
                    ]
                )
            ]
        ),

        # 컨트롤러 로드 및 시작
        TimerAction(
            period=15.0,  # controller_manager 실행 후 추가 지연
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'control', 'load_controller', 'joint_trajectory_controller'],
                    output='screen'
                ),
                ExecuteProcess(
                    cmd=['ros2', 'control', 'switch_controller', '--start-controllers', 'joint_trajectory_controller'],
                    output='screen'
                )
            ]
        )
    ])
