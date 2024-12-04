#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Pose

class AutoEffortPublisher(Node):
    def __init__(self):
        super().__init__('auto_effort_publisher')
        self.publisher = self.create_publisher(Float64MultiArray, '/auto_cmd_effort', 10)
        self.subscription = self.create_subscription(Pose, '/world/sand_heightmap_world/model/excavator_03/pose/info', self.pose_callback, 10)

        self.target_z = 0.0  # 목표 Z 좌표
        self.current_z = None  # 현재 Z 좌표
        self.timer = self.create_timer(0.1, self.publish_effort)

    def pose_callback(self, msg):
        # 엔드이펙터의 현재 Z 좌표 업데이트
        self.current_z = msg.position.z

    def compute_effort(self):
        if self.current_z is not None and self.current_z > 2.0:
            return [0.0, 0.0, 0.0]  # Z > 2.0이면 Effort 0
        error = self.target_z - self.current_z if self.current_z is not None else 0.0
        effort = error * 0.5  # 단순 비례 Effort 계산(일단은... 나중에pid로)
        return [effort, effort, effort]  # 3개의 조인트에 동일한 Effort(추후 꼭 수정 필요)

    def publish_effort(self):
        msg = Float64MultiArray()
        msg.data = self.compute_effort()
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = AutoEffortPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
