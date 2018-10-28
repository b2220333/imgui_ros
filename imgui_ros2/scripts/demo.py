#!/usr/bin/env python3
# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from imgui_ros2.srv import AddWindow

import rclpy
from rclpy.node import Node


class Demo(Node):

    def __init__(self):
        super().__init__('demo')
        self.cli = self.create_client(AddWindow, 'add_window')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddWindow.Request()

    def send_request(self):
        self.req.name = "image_raw"
        self.req.topic = "/image_raw"
        self.future = self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)

    demo = Demo()
    demo.send_request()

    while rclpy.ok():
        rclpy.spin_once(demo)
        if demo.future.done():
            if demo.future.result() is not None:
                response = demo.future.result()
                demo.get_logger().info(
                    'Result %s' % (str(response)))
            else:
                demo.get_logger().info(
                    'Service call failed %r' % (demo.future.exception(),))
            break

    demo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()