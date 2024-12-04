#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from ros_gz_interfaces.msg import Float32Array
#manualPLUSauto.py에서는 /ros_cmd_effort라는 데이터(타입: std_msgs/msg/Float64MultiArray)를 퍼블리시한다. 이걸 ROS2로 받아와서 가제보로 넘겨주기 위해 브리지를 설정하고 타입을 맞춰줘야 함
# 로스에서 가제보 방향으로 effort 제어에 관한 브릿지를 설정하기 위하여, std_msgs/msg/Float64MultiArray와 ignition.msgs.Double_V를 연결해주었는데, 이때 두 메시지 타입은 각각 다차원 배열과 일차원 array라는 차이가 있어서, (우리 프로젝트의 경우 데이터 간 순서만 유지된다면 다차원을 반드시 유지할 필요는 없어서) 일차원 array로 맞춰주기 위하여 해당 스크립트를 추가로 작성

class MultiArrayToFloat32(Node):
    def __init__(self):
        super().__init__('multi_array_to_float32')

        # ROS 2 메시지 구독
        self.ros2_subscription = self.create_subscription(
            Float64MultiArray,
            '/ros_cmd_effort',  # ROS 2 MultiArray 주제
            self.ros2_callback,
            10  # QoS 설정
        )

        # Gazebo Sim 메시지 퍼블리싱
        self.ignition_publisher = self.create_publisher(
            Float32Array,
            '/cmd_effort',  # 가제보 주제
            10  # QoS 설정
        )
        self.get_logger().info("MultiArrayToFloat32 Node Started!")

    def ros2_callback(self, msg):
        # ROS 2 메시지를 Ignition 메시지로 변환
        ign_msg = Float32Array()

        # 데이터를 Ignition Double_V 메시지의 `data` 필드에 매핑
        ign_msg.data = [float(x) for x in msg.data]

        # 변환된 메시지를 퍼블리싱
        self.ignition_publisher.publish(ign_msg)
        self.get_logger().info(f"Published Ignition Float32Array: {ign_msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = MultiArrayToFloat32()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down node.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
