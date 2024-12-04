#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class ManualPlusAutoEffort(Node):
    def __init__(self):
        super().__init__('manual_plus_auto_effort')
        self.manual_effort = [0.0, 0.0, 0.0]
        self.auto_effort = [0.0, 0.0, 0.0]

        self.publisher = self.create_publisher(Float64MultiArray, '/ros_cmd_effort', 10)
        self.manual_subscription = self.create_subscription(Float64MultiArray, '/manual_cmd_effort', self.manual_callback, 10)
        self.auto_subscription = self.create_subscription(Float64MultiArray, '/auto_cmd_effort', self.auto_callback, 10)
        self.timer = self.create_timer(0.1, self.publish_combined_effort)

    def manual_callback(self, msg):
        self.manual_effort = msg.data

    def auto_callback(self, msg):
        self.auto_effort = msg.data

    def publish_combined_effort(self):
        combined_effort = [
            m + a for m, a in zip(self.manual_effort, self.auto_effort)
        ]
        msg = Float64MultiArray()
        msg.data = combined_effort
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = ManualPlusAutoEffort()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
