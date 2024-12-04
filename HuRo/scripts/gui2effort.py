#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class GUIEffortPublisher(Node):
    def __init__(self):
        super().__init__('gui_effort_publisher')
        self.publisher = self.create_publisher(Float64MultiArray, '/manual_cmd_effort', 10)
        self.target_positions = [0.0, 0.0, 0.0]  # GUI에서 입력받은 목표 조인트 값
        self.current_efforts = [0.0, 0.0, 0.0]  # Effort 초기값
        self.timer = self.create_timer(0.1, self.publish_effort)

    def update_target_position(self, joint_index, position_value):
        # GUI에서 특정 조인트의 목표 위치를 업데이트
        self.target_positions[joint_index] = position_value

    def calculate_effort(self, joint_index):
        # 목표 위치와 현재 Effort를 기반으로 Effort 계산
        target_position = self.target_positions[joint_index]
        current_effort = self.current_efforts[joint_index]
        return current_effort + (target_position - current_effort) * 0.1  # 단순 비례 계산

    def publish_effort(self):
        # 모든 Effort를 업데이트하고 퍼블리시
        msg = Float64MultiArray()
        msg.data = [self.calculate_effort(i) for i in range(len(self.target_positions))]
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = GUIEffortPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
