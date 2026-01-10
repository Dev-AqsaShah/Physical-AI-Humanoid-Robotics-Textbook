---
sidebar_position: 3
title: "1.2 ROS 2 Architecture"
description: Deep dive into nodes, topics, services, and actions
---

# ROS 2 Architecture

In this chapter, we explore the fundamental building blocks that make ROS 2 a powerful middleware for robotics. Understanding these architectural components is essential before you can build complex robotic systems. By the end of this chapter, you will be able to create nodes, publish and subscribe to topics, implement services, and work with actions for long-running tasks.

## Learning Objectives

After completing this chapter, you will be able to:

- Explain the role and lifecycle of ROS 2 nodes
- Implement publish-subscribe communication using topics
- Create request-response patterns using services
- Handle long-running tasks with actions and feedback
- Define and use custom message types
- Inspect the ROS 2 graph using command-line tools

## The ROS 2 Computation Graph

Before diving into individual components, it helps to understand the **computation graph**—the network of ROS 2 processes that communicate with each other. The graph consists of:

- **Nodes**: Independent executables that perform computation
- **Topics**: Named buses for asynchronous message streaming
- **Services**: Named request-response pairs for synchronous calls
- **Actions**: Named goal-oriented behaviors with feedback
- **Parameters**: Configuration values stored within nodes

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROS 2 Computation Graph                      │
│                                                                 │
│   ┌──────────┐    /camera/image     ┌──────────────┐           │
│   │  Camera  │ ─────────────────────▶│   Object    │           │
│   │   Node   │      (Topic)         │  Detector   │           │
│   └──────────┘                      └──────────────┘           │
│        │                                   │                    │
│        │ /camera/info                      │ /detections       │
│        ▼                                   ▼                    │
│   ┌──────────┐                      ┌──────────────┐           │
│   │  Image   │                      │  Navigation  │           │
│   │ Viewer   │                      │   Planner    │           │
│   └──────────┘                      └──────────────┘           │
│                                                                 │
│        ◀────────── Service Call ──────────▶                     │
│                /get_map (Request/Response)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

This diagram illustrates how nodes communicate through topics (arrows) and services (bidirectional). Let us examine each component in detail.

---

## Nodes: The Fundamental Building Blocks

A **node** is the smallest unit of computation in ROS 2. Each node is designed to perform a single, well-defined task—a camera driver, an image processor, a motor controller, or a path planner. This modular approach allows you to:

- Develop and test components independently
- Replace individual nodes without affecting others
- Distribute processing across multiple machines
- Reuse nodes across different robots

### Node Naming Conventions

Every node has a unique name within the ROS 2 system. Names follow these conventions:

- Must start with an alphabetic character or underscore
- Can contain alphanumeric characters and underscores
- Are case-sensitive (`my_node` differs from `My_Node`)
- Can be organized into namespaces using forward slashes (e.g., `/robot1/camera_node`)

Namespaces are particularly useful when running multiple robots in the same ROS 2 network, as they prevent name collisions.

### Node Lifecycle

ROS 2 introduces **managed nodes** (also called lifecycle nodes) that follow a state machine pattern. This provides predictable startup and shutdown behavior, which is critical for safety-critical robotics applications.

```
                    ┌─────────────┐
                    │  Unconfigured│
                    └──────┬──────┘
                           │ configure()
                           ▼
                    ┌─────────────┐
           ┌────────│   Inactive  │◀───────┐
           │        └──────┬──────┘        │
           │               │ activate()    │ deactivate()
           │               ▼               │
           │        ┌─────────────┐        │
           │        │   Active    │────────┘
           │        └──────┬──────┘
           │               │ shutdown()
           │               ▼
           │        ┌─────────────┐
           └───────▶│  Finalized  │
     cleanup()      └─────────────┘
```

The lifecycle states are:

1. **Unconfigured**: Node has been instantiated but not configured
2. **Inactive**: Node is configured but not processing data
3. **Active**: Node is fully operational
4. **Finalized**: Node is shutting down

### Creating a Basic Node in Python

Here is a minimal ROS 2 node using `rclpy`:

```python
#!/usr/bin/env python3
"""A minimal ROS 2 node example."""

import rclpy
from rclpy.node import Node


class MinimalNode(Node):
    """A simple ROS 2 node that logs a greeting."""

    def __init__(self):
        # Initialize the node with a unique name
        super().__init__('minimal_node')
        self.get_logger().info('Minimal node has been started!')

        # Create a timer that fires every second
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        """Called every second by the timer."""
        self.counter += 1
        self.get_logger().info(f'Timer fired: count = {self.counter}')


def main(args=None):
    # Initialize the ROS 2 Python client library
    rclpy.init(args=args)

    # Create and spin the node
    node = MinimalNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Inspecting Nodes with CLI

ROS 2 provides powerful command-line tools for introspection. To list all running nodes:

```bash
# List all active nodes
ros2 node list

# Output example:
# /minimal_node
# /camera_driver
# /navigation_node
```

To get detailed information about a specific node:

```bash
# Get information about a node
ros2 node info /minimal_node

# Output example:
# /minimal_node
#   Subscribers:
#     /parameter_events: rcl_interfaces/msg/ParameterEvent
#   Publishers:
#     /parameter_events: rcl_interfaces/msg/ParameterEvent
#     /rosout: rcl_interfaces/msg/Log
#   Service Servers:
#     /minimal_node/describe_parameters: ...
#     /minimal_node/get_parameters: ...
#   Service Clients:
#   Action Servers:
#   Action Clients:
```

---

## Topics: Publish-Subscribe Communication

**Topics** are named buses that enable asynchronous, many-to-many communication. Any node can publish messages to a topic, and any number of nodes can subscribe to receive those messages. This pattern is ideal for streaming data like sensor readings, images, or robot state.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Topic: /robot/joint_states                  │
│                                                                 │
│   Publishers                              Subscribers           │
│   ┌──────────────┐                    ┌──────────────┐         │
│   │ Joint State  │ ──────────────────▶│   Motion    │         │
│   │  Publisher   │         │          │  Controller  │         │
│   └──────────────┘         │          └──────────────┘         │
│                            │                                    │
│                            ▼          ┌──────────────┐         │
│                      ┌──────────┐     │   Logging   │         │
│                      │  Topic   │────▶│   Node      │         │
│                      │  Buffer  │     └──────────────┘         │
│                      └──────────┘                               │
│                            │          ┌──────────────┐         │
│                            └─────────▶│Visualization│         │
│                                       │    Node     │         │
│                                       └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Message Types

Each topic has an associated **message type** that defines the structure of data it carries. ROS 2 includes many standard message types:

| Package | Message Type | Description |
|---------|-------------|-------------|
| `std_msgs` | `String`, `Int32`, `Float64` | Basic data types |
| `geometry_msgs` | `Twist`, `Pose`, `Point` | Geometric primitives |
| `sensor_msgs` | `Image`, `LaserScan`, `Imu` | Sensor data |
| `nav_msgs` | `Odometry`, `Path`, `OccupancyGrid` | Navigation data |

### Quality of Service (QoS)

ROS 2 introduces **Quality of Service** policies that control how messages are delivered. This is essential for real-time robotics where reliability and latency requirements vary:

| QoS Policy | Options | Use Case |
|------------|---------|----------|
| **Reliability** | `RELIABLE` or `BEST_EFFORT` | Sensor data (best effort) vs. commands (reliable) |
| **Durability** | `VOLATILE` or `TRANSIENT_LOCAL` | Whether late subscribers receive old messages |
| **History** | `KEEP_LAST(N)` or `KEEP_ALL` | How many messages to buffer |
| **Deadline** | Time duration | Maximum expected time between messages |
| **Lifespan** | Time duration | How long messages remain valid |

### Publisher Example

Here is a node that publishes velocity commands:

```python
#!/usr/bin/env python3
"""Publisher node that sends velocity commands."""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityPublisher(Node):
    """Publishes velocity commands to control robot motion."""

    def __init__(self):
        super().__init__('velocity_publisher')

        # Create publisher with topic name, message type, and queue size
        self.publisher = self.create_publisher(
            Twist,           # Message type
            '/cmd_vel',      # Topic name
            10               # Queue size (QoS history depth)
        )

        # Publish at 10 Hz
        self.timer = self.create_timer(0.1, self.publish_velocity)
        self.get_logger().info('Velocity publisher started')

    def publish_velocity(self):
        """Create and publish a Twist message."""
        msg = Twist()
        msg.linear.x = 0.5   # Move forward at 0.5 m/s
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.1  # Rotate at 0.1 rad/s

        self.publisher.publish(msg)
        self.get_logger().debug(f'Published: linear={msg.linear.x}, angular={msg.angular.z}')


def main(args=None):
    rclpy.init(args=args)
    node = VelocityPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Subscriber Example

Here is a corresponding subscriber:

```python
#!/usr/bin/env python3
"""Subscriber node that receives velocity commands."""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocitySubscriber(Node):
    """Subscribes to velocity commands and logs them."""

    def __init__(self):
        super().__init__('velocity_subscriber')

        # Create subscription
        self.subscription = self.create_subscription(
            Twist,                    # Message type
            '/cmd_vel',               # Topic name
            self.velocity_callback,   # Callback function
            10                        # Queue size
        )
        self.get_logger().info('Velocity subscriber started')

    def velocity_callback(self, msg: Twist):
        """Called whenever a message is received."""
        self.get_logger().info(
            f'Received velocity: linear.x={msg.linear.x:.2f}, '
            f'angular.z={msg.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = VelocitySubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Using QoS Profiles

For sensor data that tolerates dropped messages:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)

self.subscription = self.create_subscription(
    LaserScan,
    '/scan',
    self.scan_callback,
    sensor_qos
)
```

### Topic CLI Commands

```bash
# List all active topics
ros2 topic list

# Show detailed topic info including message type
ros2 topic info /cmd_vel

# Output:
# Type: geometry_msgs/msg/Twist
# Publisher count: 1
# Subscription count: 2

# Display messages in real-time
ros2 topic echo /cmd_vel

# Show message structure
ros2 interface show geometry_msgs/msg/Twist

# Publish a message from command line
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.1}}"

# Check publication rate
ros2 topic hz /cmd_vel
```

---

## Services: Request-Response Communication

While topics are ideal for streaming data, **services** provide synchronous, one-to-one communication. A client sends a request and blocks until it receives a response. Use services when you need:

- A guaranteed response (success/failure confirmation)
- One-time queries (get current position, check status)
- Triggering specific actions (reset, calibrate, save)

```
┌─────────────────────────────────────────────────────────────────┐
│                  Service: /get_robot_state                      │
│                                                                 │
│   ┌──────────────┐                    ┌──────────────┐         │
│   │    Client    │───── Request ─────▶│   Server    │         │
│   │    Node      │                    │    Node     │         │
│   │              │◀──── Response ─────│             │         │
│   └──────────────┘                    └──────────────┘         │
│                                                                 │
│   Request:  Empty                                               │
│   Response: RobotState                                          │
│             - pose: Pose                                        │
│             - velocity: Twist                                   │
│             - battery_level: float                              │
└─────────────────────────────────────────────────────────────────┘
```

### Service Definition

Services are defined in `.srv` files with request and response sections separated by `---`:

```
# Example: AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

### Service Server Example

```python
#!/usr/bin/env python3
"""Service server that adds two integers."""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AdditionServer(Node):
    """Provides a service to add two integers."""

    def __init__(self):
        super().__init__('addition_server')

        # Create the service
        self.service = self.create_service(
            AddTwoInts,              # Service type
            'add_two_ints',          # Service name
            self.add_callback        # Callback function
        )
        self.get_logger().info('Addition service ready')

    def add_callback(self, request, response):
        """Handle incoming service requests."""
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Request: {request.a} + {request.b} = {response.sum}'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AdditionServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Service Client Example

```python
#!/usr/bin/env python3
"""Service client that calls the addition service."""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AdditionClient(Node):
    """Calls the addition service."""

    def __init__(self):
        super().__init__('addition_client')

        # Create the client
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        # Wait for service to be available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        self.get_logger().info('Service available')

    def send_request(self, a: int, b: int):
        """Send a request and return the result."""
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        # Asynchronous call
        future = self.client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)
    client = AdditionClient()

    # Send request
    future = client.send_request(41, 1)

    # Wait for response
    rclpy.spin_until_future_complete(client, future)

    result = future.result()
    client.get_logger().info(f'Result: {result.sum}')

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Service CLI Commands

```bash
# List all services
ros2 service list

# Show service type
ros2 service type /add_two_ints

# Show service interface definition
ros2 interface show example_interfaces/srv/AddTwoInts

# Call a service from command line
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts \
  "{a: 5, b: 3}"
```

---

## Actions: Long-Running Tasks with Feedback

**Actions** combine the best of topics and services for long-running tasks. Unlike services, actions:

- Are asynchronous (do not block the client)
- Provide continuous feedback during execution
- Can be canceled mid-execution
- Return a final result upon completion

Actions are ideal for navigation, manipulation, and any task that takes significant time.

```
┌─────────────────────────────────────────────────────────────────┐
│                Action: /navigate_to_pose                        │
│                                                                 │
│   ┌──────────────┐                    ┌──────────────┐         │
│   │    Client    │──── Goal ─────────▶│   Server    │         │
│   │              │                    │             │         │
│   │              │◀─── Feedback ──────│             │         │
│   │              │    (continuous)    │             │         │
│   │              │                    │             │         │
│   │              │◀─── Result ────────│             │         │
│   └──────────────┘    (final)         └──────────────┘         │
│                                                                 │
│   Goal:     target_pose, behavior_tree                          │
│   Feedback: current_pose, distance_remaining, time_elapsed      │
│   Result:   success/failure, final_pose, total_time             │
└─────────────────────────────────────────────────────────────────┘
```

### Action Definition

Actions are defined in `.action` files with three sections: goal, result, and feedback:

```
# Example: NavigateToPose.action
# Goal
geometry_msgs/PoseStamped pose
---
# Result
bool success
float64 total_time
---
# Feedback
geometry_msgs/PoseStamped current_pose
float64 distance_remaining
```

### Action Server Example

```python
#!/usr/bin/env python3
"""Action server for a simple countdown task."""

import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from example_interfaces.action import Fibonacci


class CountdownServer(Node):
    """Action server that counts down with feedback."""

    def __init__(self):
        super().__init__('countdown_server')

        self.action_server = ActionServer(
            self,
            Fibonacci,
            'countdown',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )
        self.get_logger().info('Countdown action server ready')

    def goal_callback(self, goal_request):
        """Accept or reject incoming goals."""
        self.get_logger().info(f'Received goal: order={goal_request.order}')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject cancel requests."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        """Execute the countdown action."""
        self.get_logger().info('Executing countdown...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = []

        for i in range(goal_handle.request.order):
            # Check for cancellation
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            # Simulate work
            feedback_msg.partial_sequence.append(i)
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
            time.sleep(1.0)

        # Complete the goal
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info(f'Goal succeeded: {result.sequence}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = CountdownServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Action Client Example

```python
#!/usr/bin/env python3
"""Action client that sends a goal and monitors progress."""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci


class CountdownClient(Node):
    """Sends goals to the countdown action server."""

    def __init__(self):
        super().__init__('countdown_client')
        self.action_client = ActionClient(self, Fibonacci, 'countdown')
        self.get_logger().info('Countdown client ready')

    def send_goal(self, order: int):
        """Send a goal and set up callbacks."""
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.action_client.wait_for_server()

        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal acceptance/rejection."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """Process feedback during execution."""
        self.get_logger().info(
            f'Feedback: {feedback_msg.feedback.partial_sequence}'
        )

    def get_result_callback(self, future):
        """Handle the final result."""
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    client = CountdownClient()
    client.send_goal(5)
    rclpy.spin(client)


if __name__ == '__main__':
    main()
```

### Action CLI Commands

```bash
# List all actions
ros2 action list

# Show action info
ros2 action info /countdown

# Show action interface
ros2 interface show example_interfaces/action/Fibonacci

# Send a goal from command line
ros2 action send_goal /countdown example_interfaces/action/Fibonacci \
  "{order: 5}" --feedback
```

---

## Message Types and Custom Messages

### Standard Message Packages

ROS 2 provides extensive standard message packages:

```bash
# List available message types
ros2 interface list

# Common packages:
# - std_msgs: String, Int32, Float64, Bool, Header
# - geometry_msgs: Pose, Point, Twist, Quaternion, Transform
# - sensor_msgs: Image, LaserScan, PointCloud2, Imu, JointState
# - nav_msgs: Odometry, Path, OccupancyGrid, MapMetaData
```

### Creating Custom Messages

For robotics applications, you often need custom messages. Create a package and define your message:

```bash
# Create package for custom interfaces
ros2 pkg create --build-type ament_cmake my_robot_interfaces
```

Define a custom message in `msg/RobotStatus.msg`:

```
# RobotStatus.msg - Custom message for robot health monitoring

# Header with timestamp
std_msgs/Header header

# Robot identification
string robot_name
uint32 robot_id

# Status information
bool is_operational
float64 battery_percentage
float64 cpu_temperature

# Current pose
geometry_msgs/Pose current_pose

# Array of joint positions
float64[] joint_positions
```

Update `CMakeLists.txt`:

```cmake
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  DEPENDENCIES std_msgs geometry_msgs
)
```

Update `package.xml`:

```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

Build and use:

```bash
colcon build --packages-select my_robot_interfaces
source install/setup.bash
```

```python
from my_robot_interfaces.msg import RobotStatus

msg = RobotStatus()
msg.robot_name = "humanoid_01"
msg.battery_percentage = 85.5
msg.is_operational = True
```

---

## Node Communication Patterns

Understanding common communication patterns helps you design effective ROS 2 systems.

### Pattern 1: Sensor Pipeline

```
Camera → Image Processing → Object Detection → Navigation
 (pub)      (sub/pub)           (sub/pub)        (sub)
```

```python
# Image processor node (subscriber + publisher)
class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')

        self.subscription = self.create_subscription(
            Image, '/camera/raw', self.process_image, 10)

        self.publisher = self.create_publisher(
            Image, '/camera/processed', 10)

    def process_image(self, msg):
        # Process and republish
        processed = self.apply_filters(msg)
        self.publisher.publish(processed)
```

### Pattern 2: State Machine with Services

```
┌─────────────────┐
│  State Machine  │
│                 │──── /start_task (service) ──▶ Task Executor
│                 │◀─── /task_complete (topic) ──
└─────────────────┘
```

### Pattern 3: Hierarchical Control

```
         ┌─────────────────┐
         │  Mission Planner │
         │    (actions)     │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │ Behavior Manager │
         │   (services)     │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌───────┐    ┌───────┐    ┌───────┐
│ Motor │    │Sensor │    │ Arm   │
│Control│    │ Node  │    │Control│
│(topics)    │(topics)    │(topics)
└───────┘    └───────┘    └───────┘
```

---

## Complete Working Example

Let us create a complete example that demonstrates nodes, topics, and services working together. This simulates a simple robot status monitoring system.

### Robot Status Publisher

```python
#!/usr/bin/env python3
"""Publishes simulated robot status at regular intervals."""

import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Bool, String


class RobotStatusPublisher(Node):
    """Simulates and publishes robot status data."""

    def __init__(self):
        super().__init__('robot_status_publisher')

        # Publishers for different status values
        self.battery_pub = self.create_publisher(Float64, '/robot/battery', 10)
        self.temperature_pub = self.create_publisher(Float64, '/robot/temperature', 10)
        self.status_pub = self.create_publisher(String, '/robot/status', 10)
        self.emergency_pub = self.create_publisher(Bool, '/robot/emergency', 10)

        # Simulated state
        self.battery_level = 100.0
        self.temperature = 25.0

        # Timer for periodic publishing (10 Hz)
        self.timer = self.create_timer(0.1, self.publish_status)
        self.get_logger().info('Robot status publisher started')

    def publish_status(self):
        """Publish current status values."""
        # Simulate battery drain
        self.battery_level = max(0.0, self.battery_level - 0.01)

        # Simulate temperature fluctuation
        self.temperature += random.uniform(-0.1, 0.15)
        self.temperature = max(20.0, min(80.0, self.temperature))

        # Publish battery level
        battery_msg = Float64()
        battery_msg.data = self.battery_level
        self.battery_pub.publish(battery_msg)

        # Publish temperature
        temp_msg = Float64()
        temp_msg.data = self.temperature
        self.temperature_pub.publish(temp_msg)

        # Publish status string
        status_msg = String()
        if self.battery_level < 20.0:
            status_msg.data = "LOW_BATTERY"
        elif self.temperature > 60.0:
            status_msg.data = "OVERHEATING"
        else:
            status_msg.data = "NOMINAL"
        self.status_pub.publish(status_msg)

        # Publish emergency flag
        emergency_msg = Bool()
        emergency_msg.data = self.battery_level < 10.0 or self.temperature > 70.0
        self.emergency_pub.publish(emergency_msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotStatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Robot Monitor with Service

```python
#!/usr/bin/env python3
"""Monitors robot status and provides a reset service."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Bool, String
from std_srvs.srv import Trigger


class RobotMonitor(Node):
    """Monitors robot status and logs warnings."""

    def __init__(self):
        super().__init__('robot_monitor')

        # State tracking
        self.battery_level = 100.0
        self.temperature = 25.0
        self.status = "UNKNOWN"
        self.emergency = False

        # Subscribers
        self.create_subscription(Float64, '/robot/battery', self.battery_cb, 10)
        self.create_subscription(Float64, '/robot/temperature', self.temp_cb, 10)
        self.create_subscription(String, '/robot/status', self.status_cb, 10)
        self.create_subscription(Bool, '/robot/emergency', self.emergency_cb, 10)

        # Service to get current status
        self.service = self.create_service(
            Trigger, '/robot/get_report', self.report_callback)

        # Periodic logging
        self.timer = self.create_timer(5.0, self.log_summary)
        self.get_logger().info('Robot monitor started')

    def battery_cb(self, msg):
        self.battery_level = msg.data

    def temp_cb(self, msg):
        self.temperature = msg.data

    def status_cb(self, msg):
        self.status = msg.data

    def emergency_cb(self, msg):
        if msg.data and not self.emergency:
            self.get_logger().error('EMERGENCY CONDITION DETECTED!')
        self.emergency = msg.data

    def log_summary(self):
        """Log periodic summary."""
        self.get_logger().info(
            f'Status: {self.status} | '
            f'Battery: {self.battery_level:.1f}% | '
            f'Temp: {self.temperature:.1f}C | '
            f'Emergency: {self.emergency}'
        )

    def report_callback(self, request, response):
        """Service callback to return status report."""
        response.success = not self.emergency
        response.message = (
            f"Battery: {self.battery_level:.1f}%, "
            f"Temperature: {self.temperature:.1f}C, "
            f"Status: {self.status}"
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = RobotMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Run the example:

```bash
# Terminal 1: Start the status publisher
ros2 run my_robot_pkg robot_status_publisher

# Terminal 2: Start the monitor
ros2 run my_robot_pkg robot_monitor

# Terminal 3: Query the service
ros2 service call /robot/get_report std_srvs/srv/Trigger

# Terminal 4: Echo topics
ros2 topic echo /robot/status
```

---

## Summary

In this chapter, we explored the core architectural components of ROS 2:

- **Nodes** are independent processes that perform specific tasks and can be managed through lifecycle states
- **Topics** enable asynchronous publish-subscribe communication for streaming data with configurable QoS policies
- **Services** provide synchronous request-response communication for one-time queries and commands
- **Actions** handle long-running tasks with continuous feedback and cancellation support
- **Messages** define the structure of data exchanged, with both standard and custom types available

These primitives form the foundation for building complex robotic systems. In the next chapter, we will explore `rclpy` in greater depth, learning how to create complete ROS 2 packages and manage node lifecycles programmatically.

## What's Next

In [Chapter 1.3: Python Programming with rclpy](./1-3-rclpy-basics.md), we will:

- Create complete ROS 2 Python packages from scratch
- Implement managed lifecycle nodes
- Handle parameters and launch files
- Build a multi-node robot control system

---

## Exercises

1. **Node Creation**: Create a node that publishes your system's current time to a topic called `/system_time` every second.

2. **Topic Communication**: Build a publisher that sends random temperature readings and a subscriber that logs warnings when temperature exceeds 50 degrees.

3. **Service Implementation**: Create a service called `/calculate_distance` that takes two 3D points and returns the Euclidean distance between them.

4. **Action Challenge**: Implement an action server that simulates a robot moving to a target position, publishing its current position as feedback.

5. **Combined System**: Create a three-node system where one node publishes sensor data, another processes it, and a third provides a service to query the processed results.
