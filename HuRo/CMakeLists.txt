cmake_minimum_required(VERSION 3.8)
project(HuRo)

# Python 코드 지원
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)  # Python ROS 2 클라이언트 라이브러리

# Python 패키지 설치 설정
ament_python_install_package(${PROJECT_NAME})

# ROS 2와 관련된 의존성
find_package(rclcpp REQUIRED)  # C++ ROS 2 클라이언트 라이브러리
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(ros_gz_bridge REQUIRED)
find_package(ros_gz_sim REQUIRED)
find_package(controller_manager REQUIRED) # ROS 2 컨트롤 매니저
find_package(ros2_control REQUIRED)       # ROS 2 컨트롤 인터페이스


# 설치 경로 설정 (share)
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY resource DESTINATION share/${PROJECT_NAME}/)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/HuRo/excavator_03.urdf DESTINATION share/${PROJECT_NAME}/urdf)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/torque_control_config.yaml DESTINATION share/${PROJECT_NAME}/config)

# Python 스크립트 설치 경로 설정 (lib)
install(PROGRAMS
  scripts/joint_state_bridge.py
  scripts/effort_bridge.py
  scripts/gui2effort.py
  scripts/auto_terra.py
  scripts/manualPLUSauto.py
  DESTINATION lib/${PROJECT_NAME}
)

# 실행 시 의존성 등록
ament_package()
