from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, SetEnvironmentVariable, IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, FindExecutable
#from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 파일 경로 정의
    world_file = '/home/yerim/Yonsei_ws/install/HuRo/share/HuRo/resource/worlds/sand_heightmap_world/sand_heightmap_world.sdf'
    urdf_file = '/home/yerim/Yonsei_ws/install/HuRo/share/HuRo/urdf/excavator_03.urdf'
    yaml_file = '/home/yerim/Yonsei_ws/install/HuRo/share/HuRo/config/torque_control_config.yaml'
    sdf_file = '/home/yerim/Yonsei_ws/install/HuRo/share/HuRo/resource/excavator_03.sdf'
    
    # robot_description 토픽에 게시할 내용 설정
#    robot_description = {
#        "robot_description": Command([
#            FindExecutable(name="xacro"), " ",
#            urdf_file
#        ])
#    }
    

    # Gazebo Fortress 실행 (world file포함)
    gz_sim_process = ExecuteProcess(
        cmd=['gz', 'sim', world_file],
        output='screen'
    )

#    gz_sim_process = IncludeLaunchDescription(
#        PythonLaunchDescriptionSource(
#            '/opt/ros/humble/share/ros_gz_sim/launch/gz_sim.launch.py'
#        ),
#        launch_arguments={'world': world_file}.items()
#    )

    # sdf 파일 로드
    gz_sim_model = TimerAction(
        period=1.0,  # Gazebo 초기화 시간 (1초 대기)
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'run', 'ros_gz_sim', 'create',
                    '-file', sdf_file,
                    '-name', 'excavator_03'
                ],
                output='screen'
            )
        ]
    )
    

    # ROS-GZ 브리지 설정
    ros_gz_bridge = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='ros_gz_bridge',
                executable='parameter_bridge',
                name='ros_gz_bridge',
                arguments=[
                # Gazebo → ROS 브릿지
                    #로봇의 전체 상태(링크, 조인트의 동적 상태)퍼블리시
                    '/world/sand_heightmap_world/model/excavator_03/pose/info@gz.msgs.Pose_V[geometry_msgs/msg/PoseArray',
                    #조인트의 상태(위치, 속도, 힘 등)을 퍼블리시
                    '/world/sand_heightmap_world/model/excavator_03/joint_state@gz.msgs.JointState[/bridge_joint_states',
                    #월드와의 상호작용은 일단 생략
                    
                    # ROS → Gazebo 브릿지
                    # 현재 로봇 상태를 기반으로 힘, 토크 명령을 전송
                    # gui를 통한 수동제어, 자동제어 (통합노드를 별개로 생성함)
                    '/ros_cmd_effort@ros_gz_interfaces/msg/Float32Array[gz.msgs.Double_V@/cmd_effort'
                    # ^ effort_bridge.py에서 나온 데이터(타입:Float32Array로 변환됨)를 여기에...
                    # ^ 브리지에서 위의 데이터를 구독하게 하기 위해 sdf의 plugin 설정 중 topic에 cmd_effort를 추가해야 함
                ],
                output='screen'
            )
        ]
    )
    
    
    # 브리지 effort 변환노드
    effort_bridge = TimerAction(
        period=2.2, #브리지와 동시
        actions=[
            Node(
                package='HuRo',
                executable='effort_bridge.py',
                name='effort_bridge',
                output='screen'
            )
        ]
    )
    
    
    # 브리지 joint 변환노드
    joint_state_bridge = TimerAction(
        period=4.0,  # 브리지와 동시(보다 조금 늦게,,, 초기화 이후)
        actions=[
            Node(
                package='HuRo',
                executable='joint_state_bridge.py',
                name='joint_state_bridge',
                output='screen'
            )
        ]
    )


    # 로봇 State Publisher 실행
    robot_state_publisher = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                parameters=[{'robot_description': open(urdf_file).read()}],
                output='screen'
            )
        ]
    )
    
    # Controller Manager 노드
    controller_manager_node = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='controller_manager',
                executable='gz_ros2_control_node',
                name='controller_manager',
                parameters=[{'update_rate': 100}],  # 기본적으로 ~/robot_description을 구독함, robot_state_publisher노드에서 가져온 robot_description을 참조하도록
                output='screen'
            )
        ]
    )

    # Joint State Publisher 실행
#    joint_state_publisher = Node(
#        package='joint_state_publisher',
#        executable='joint_state_publisher',
#        name='joint_state_publisher',
#        output='screen',
#        parameters=[{'source_list': ['/joint_states']}]
#    )

    # Joint State Broadcaster 스폰
    joint_state_broadcaster = TimerAction(
        period=10.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster'],
                parameters=[{'state_topic': '/joint_states'}],
                output='screen'
            )
        ]
    )

   
    # 수동 컨트롤러
    manual_effort_spawner = TimerAction(
        period=11.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['manual_effort_controller'],
                output='screen'
            )
        ]
    )

    # 자동 컨트롤러
    auto_effort_spawner = TimerAction(
        period=12.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['auto_effort_controller'],
                output='screen'
            )
        ]
    )

    # 제어 통합
    manualPLUSauto = TimerAction(
        period=13.0,  # 컨트롤러 초기화 후 실행
        actions=[
            Node(
                package='HuRo',
                executable='manualPLUSauto.py',
                name='manualPLUSauto',
                output='screen'
            )
        ]
    )
    
#    # rqt활용한 GUI -> 안쓰고 PyQt 기반 슬라이더 GUI 생성할 것
#    rqt_gui = ExecuteProcess(
#    	cmd=['rqt'],
#    	output='screen'
#    )
    

    # 수동 제어 (scripts/gui2effort)
    gui2effort = TimerAction(
        period=14.0,  # manual_effort_controller 이후
        actions=[
            Node(
                package='HuRo',
                executable='gui2effort.py',
                name='gui2effort',
                output='screen'
            )
        ]
    )
    
    # 자동 제어
    auto_terra = TimerAction(
        period=15.0,  # auto_effort_controller 이후
        actions=[
            Node(
                package='HuRo',
                executable='auto_terra.py',
                name='auto_terra',
                output='screen'
            )
        ]
    )
    
    

    return LaunchDescription([
        # Gazebo 실행
        gz_sim_process,
        # 모델
        gz_sim_model,
        # ROS-GZ 브리지 실행
        ros_gz_bridge,
        # 변환노드들 
        effort_bridge, #브리지와 함께 실행
        joint_state_bridge, #브리지보다 조금 늦게 실행(초기화 후)
        # 로봇 상태 게시
        robot_state_publisher, #컨트롤러보다 먼저 와야 됨
        # 컨트롤러
        controller_manager_node,
        manualPLUSauto, #컨트롤러가 먼저 와야 됨
        #joint_state_publisher, #broadcaster로 대체
        joint_state_broadcaster,
        manual_effort_spawner,
        auto_effort_spawner,
        #제어스크립트
        gui2effort,
        auto_terra,
        #rqt_gui,
    ])
