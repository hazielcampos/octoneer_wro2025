import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Bool

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.get_logger().info('Robot Controller Node has been initialized.')
        self.speedPublisher = self.create_publisher(Int32, 'robot_speed', 10)
        self.turnPublisher = self.create_publisher(Int32, 'robot_turn_angle', 10)
        self.create_timer(0.05, self.robot_main)  # Call robot_main every 0.1 seconds
        self.create_subscription(Int32, 'obstacle_position', self.obstacle_position_callback, 10)
        self.create_subscription(Int32, 'turn_lines', self.turn_lines_callback, 10)
        self.create_subscription(Bool, 'turning', self.turning_callback, 10)
        
        self.turns_count = 0
        self.laps_count = 0
        
        self.turn_line_color = 0 # 0 for none, 1 for orange, 2 for green
        
    
    def obstacle_position_callback(self, msg):
        self.get_logger().info(f'Obstacle detected at position: {msg.data}')
        # Here you can add logic to handle the obstacle
    def obstacle_avoidance(self, obstacle_position):
        self.get_logger().info(f'Handling obstacle at position: {obstacle_position}')
        # Implement obstacle avoidance logic here
    
    def turn_lines_callback(self, msg):
        self.get_logger().info(f'Turn lines detected: {msg.data}')
        self.turn_line_color = msg.data
    def turning_callback(self, msg):
        self.get_logger().info(f'Start turning: {msg.data}')
        # Here you can add logic to start turning
        if msg.data == True:
            if self.turn_line_color == 1:  # Orange line
                self.turn(45)
                self.move(100)  # Set speed to 100 when turning
            elif self.turn_line_color == 2:  # Green line
                self.turn(90)
                self.move(30) # Set speed to 30 when ending the turn to help avoid the next obstacle
            else: 
                self.turn(0)  # No line detected, do not turn
            if self.turns_count < 3:
                self.turns_count += 1
            else:
                self.laps_count += 1
                self.turns_count = 0
            
    
    def robot_main(self):
        self.get_logger().info('Robot Controller is running.')

    def move(self, speed):
        self.get_logger().info(f'Moving at speed {speed}.')
        self.speedPublisher.publish(Int32(data=speed))

    def turn(self, angle):
        self.get_logger().info(f'Turning {angle} degrees.')
        self.turnPublisher.publish(Int32(data=angle))
        

def main(args=None):
    rclpy.init(args=args)
    robot_controller = RobotController()
    rclpy.spin(robot_controller)
    robot_controller.destroy_node()
    rclpy.shutdown()