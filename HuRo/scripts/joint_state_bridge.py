#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from ros_gz_interfaces.msg import JointWrench
# gazebo에서 제공하는 /world/.../joint_state topic을 읽고 ROS2의 /joint_states (yaml파일에 있음) topic으로 변환하기 위함
# 다시 말해, launch 파일에서는  가제보로부터 로스 방향으로 조인트 상태에 대한 브릿지를 설정하기 위하여. ignition.msgs.JointState와 sensor_msgs/msg/JointState 를 연결해주었는데, 두 메시지 타입 간 header 정보 차이가 있어 이 스크립트를 작성하여 메시지 타입을 맞춰줌

class JointStateBridge(Node):
    def __init__(self):
        super().__init__('joint_state_bridge')
        # Subscribe to Gazebo topic
        self.subscription = self.create_subscription(
            JointWrench,
            '/world/sand_heightmap_world/model/excavator_03/joint_state',
            self.joint_callback,
            10
        )
        # Publisher for ROS 2 topic
        self.publisher = self.create_publisher(
            JointState,
            '/bridge_joint_states',
            10
        )

    def joint_callback(self, msg):
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        # Convert joint data (adjust for your specific Model message fields)
        for joint in msg.wrench:
            joint_state_msg.name.append(joint.name)
            joint_state_msg.position.append(joint.position)
            joint_state_msg.velocity.append(joint.velocity)
            joint_state_msg.effort.append(joint.effort)
        self.publisher.publish(joint_state_msg)

def main(args=None):
    rclpy.init(args=args)
    node = JointStateBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
