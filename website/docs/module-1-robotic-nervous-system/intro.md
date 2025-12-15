---
sidebar_position: 2
---

# Module 1: Robotic Nervous System (ROS 2)

## Introduction

The Robot Operating System 2 (ROS 2) serves as the nervous system for modern robotics applications, providing the essential communication infrastructure that enables complex robot behaviors. This module introduces the fundamental concepts of ROS 2 architecture and demonstrates how it facilitates communication between different robot components.

import EducationalBox from '@site/src/components/EducationalBox';

<EducationalBox type="objective">

By the end of this module, you will be able to:

1. Understand the architecture and design principles of ROS 2
2. Implement nodes, topics, services, and actions for robot communication
3. Control robots using Python with the rclpy client library
4. Model humanoid robots using the Unified Robot Description Format (URDF)

</EducationalBox>

## Module Overview

ROS 2 is not a traditional operating system but rather a flexible framework for writing robot software. It provides the tools, libraries, and conventions needed to build complex robotic systems. The key components of ROS 2 include:

- **Nodes**: Processes that perform computation
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Synchronous request/response communication
- **Actions**: Asynchronous goal-oriented communication
- **Parameters**: Configuration values accessible by nodes

## Prerequisites

Before starting this module, ensure you have:

- Basic Python programming knowledge
- Understanding of Linux command line (or WSL for Windows)
- Familiarity with package managers and system dependencies

---

## 1.1 ROS 2 Architecture

### Core Concepts

ROS 2 is built around the concept of distributed computing across multiple processes (potentially on multiple machines). At the core of this architecture is the concept of "nodes" - processes that perform computation. Nodes are grouped into packages for sharing and distribution.

### Communication Patterns

ROS 2 supports several communication patterns:

1. **Topics** (publish/subscribe):
   - Asynchronous, one-way communication
   - Publishers send messages to topics
   - Subscribers receive messages from topics
   - Used for streaming data like sensor readings

2. **Services** (request/response):
   - Synchronous, two-way communication
   - Client sends a request to a server
   - Server responds with a result
   - Used for operations that require a specific response

3. **Actions** (goal/cancel/result feedback):
   - Asynchronous with feedback
   - More robust than services for long-running operations
   - Supports goal preemption and cancellation
   - Provides continuous feedback during execution

#### Example: Topic Communication
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1
```

---

## 1.2 Nodes, Topics, Services, and Actions

### Nodes

A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are designed to perform a single, modular function such as:

- Controlling a motor
- Reading from a sensor
- Processing data
- Providing a user interface

Nodes organize the computation in a ROS 2 system. In the same way that an application is built from single functions organized into multiple files, a distributed robot system is built from single nodes organized into multiple packages.

### Topics and Messages

Topics provide the ROS 2 publish/subscribe communication paradigm. Nodes that send data are called publishers, and nodes that receive data are called subscribers.

Messages are the data format used to exchange information between nodes. Messages can contain:

- Primitive types (int, float, bool, string, etc.)
- Arrays of primitive types
- Nested message structures

### Services

Services follow a request/reply pattern for communication between nodes. A service client sends a request message to a service server, which processes the request and sends back a response message.

### Actions

Actions are designed for long-running tasks and include:

- Goals: Requests for an action to begin
- Results: Final outcomes of an action
- Feedback: Continuous updates during goal processing

---

## 1.3 Python Control with rclpy

### Installation and Setup

To work with ROS 2 in Python, you'll use the rclpy library, which provides Python bindings for ROS 2 client libraries.

### Basic Node Structure

```python
import rclpy
from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args)
    
    my_node = MyNode()
    
    rclpy.spin(my_node)
    
    my_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Creating Publishers and Subscribers

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TalkerNode(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(0.5, self.publish_message)
        self.counter = 0

    def publish_message(self):
        msg = String()
        msg.data = f'Hello, world! {self.counter}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.counter += 1

class ListenerNode(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: {msg.data}')
```

---

## 1.4 URDF for Humanoid Modeling

### What is URDF?

The Unified Robot Description Format (URDF) is an XML format used to describe robot models in ROS. It defines:

- Physical structure (links)
- Joints connecting links
- Inertial properties
- Visual and collision representations
- Sensors and actuators

### Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0.2 0 0" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```

### Humanoid Robot Considerations

When modeling humanoid robots in URDF, consider:

- **Joint Limits**: Define appropriate ranges of motion
- **Actuator Specifications**: Include motor capabilities
- **Sensory Equipment**: Add IMUs, cameras, LiDAR, etc.
- **Center of Mass**: Critical for stability calculations
- **Collision Avoidance**: Proper collision geometry

---

<EducationalBox type="summary">

This module introduced the foundational concepts of ROS 2 - the communication middleware that enables complex robot systems to function cohesively. You learned about nodes, topics, services, actions, and how to implement them using Python's rclpy library. Additionally, you were introduced to URDF for modeling humanoid robots.

The next module will build upon these concepts by introducing simulation environments where these ROS 2 systems can be tested and validated before deployment on physical robots.

</EducationalBox>

<EducationalBox type="quiz">

1. What are the four main communication patterns in ROS 2?
2. What is the difference between a service and an action in ROS 2?
3. What does URDF stand for and what is its primary purpose?

</EducationalBox>