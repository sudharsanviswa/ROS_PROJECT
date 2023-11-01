import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient

class NavigateToPoseClient(Node):

    def __init__(self):
        super().__init__('navigate_to_pose_client')
        self.client = ActionClient(self, NavigateToPose, 'NavigateToPose')
        
    def send_goal(self, x, y, theta):
        goal_msg = NavigateToPose.Goal()
        print('A')
        # Set the frame (typically map frame)
        goal_msg.pose.header.frame_id = 'map'
        print('B')
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        print('C')
        
        # Set the position
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0
        
        # Set the orientation using a simple quaternion for a given yaw
        from math import sin, cos
        half_theta = theta * 0.5
        goal_msg.pose.pose.orientation.w = cos(half_theta)
        goal_msg.pose.pose.orientation.z = sin(half_theta)
        
        # Send the goal
        self.client.wait_for_server()
        print('D')
        self.goal_future = self.client.send_goal_async(goal_msg)
        print('E')
        self.goal_future.add_done_callback(self.goal_response_callback)
        print('F')
        
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        
        self.get_logger().info('Goal accepted :)')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.get_result_callback)
        
    def get_result_callback(self, future):
        status = future.result().status
        if status == NavigateToPose.Result.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        else:
            self.get_logger().info('Goal failed with status code: {0}'.format(status))
            
def main(args=None):
    rclpy.init(args=args)

    # Create the node
    node = NavigateToPoseClient()
    print(1)
    # Send the robot to the desired pose (x, y, theta)
    node.send_goal(20.0, 1.0, 0.0)  # Example pose
    print(2)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
