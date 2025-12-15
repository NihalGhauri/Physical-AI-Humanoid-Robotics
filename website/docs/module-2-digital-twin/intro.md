---
sidebar_position: 3
---

# Module 2: Digital Twin (Gazebo & Unity)

## Introduction

A digital twin is a virtual replica of a physical system that serves as a real-time digital counterpart. In robotics, digital twins enable safe testing and validation of robotic systems in virtual environments before deployment in the real world. This module covers physics simulation using Gazebo and Unity, critical tools for creating accurate digital twins of robotic systems.

import EducationalBox from '@site/src/components/EducationalBox';

<EducationalBox type="objective">

By the end of this module, you will be able to:

1. Set up and configure physics simulations with realistic physical properties
2. Model environments for robot testing and validation
3. Simulate various sensors including LiDAR, depth cameras, and IMUs
4. Visualize human-robot interactions in 3D environments
5. Bridge between simulation and real-world robot control

</EducationalBox>

## Module Overview

Digital twins play a crucial role in modern robotics development by offering:

- **Safe Testing**: Validate algorithms without risk to physical robots
- **Cost Reduction**: Reduce need for physical prototypes
- **Scenario Simulation**: Test edge cases that are difficult or dangerous to reproduce physically
- **Development Acceleration**: Parallel development of software and hardware

Two primary simulation environments dominate robotics simulation:
- **Gazebo**: Physics-accurate simulation with realistic dynamics
- **Unity**: High-fidelity graphics and interactive environments

---

## 2.1 Physics Simulation Fundamentals

### Physical Laws in Simulation

Accurate simulation of robotic systems requires faithful implementation of physical laws:

1. **Newton's Laws of Motion**: Foundation for all dynamic behavior
2. **Collision Detection and Response**: Critical for robot interactions
3. **Friction Models**: Affects robot mobility and manipulation
4. **Gravity and Environmental Forces**: Impact robot behavior

### Simulation Accuracy vs. Performance Trade-offs

Simulation environments must balance:
- **Accuracy**: Physical fidelity for reliable testing
- **Performance**: Simulation speed for efficient development
- **Stability**: Numerical stability of physics calculations

### Key Simulation Parameters

- **Physics Engine**: Selection of underlying physics solver (e.g., ODE, Bullet, Fisheye)
- **Time Step**: Balance between accuracy and performance
- **Real-time Factor**: Simulation speed relative to real-time
- **Solver Iterations**: Accuracy of constraint solving

---

## 2.2 Environment Modeling

### Creating World Descriptions

Simulation environments are typically defined using markup languages:

**Gazebo World Files (SDF format):**
```xml
<?xml version="1.0"?>
<sdf version="1.6">
  <world name="my_world">
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
    
    <!-- Custom obstacles -->
    <model name="wall">
      <pose>0 5 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>10 0.2 2</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>10 0.2 2</size>
            </box>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

### Terrain and Obstacle Types

1. **Static Obstacles**: Fixed structures in the environment
2. **Dynamic Objects**: Movable objects that robots can interact with
3. **Deformable Terrain**: Surfaces that change shape during interaction
4. **Multi-level Environments**: Buildings, stairs, ramps

### Sensor-Ready Environments

Well-designed simulation environments include:
- **Reference Markers**: For localization and mapping
- **Calibration Targets**: For sensor calibration
- **Ground Truth Data**: For performance evaluation

---

## 2.3 Sensor Simulation

### LiDAR Simulation

LiDAR sensors are simulated by casting rays and detecting intersections with objects in the environment:

```xml
<!-- Example LiDAR configuration in URDF -->
<gazebo reference="lidar_link">
  <sensor type="ray" name="lidar_sensor">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.1</min>
        <max>30.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <namespace>/lidar</namespace>
        <remapping>~/out:=scan</remapping>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
    </plugin>
  </sensor>
</gazebo>
```

Key LiDAR parameters:
- **Range**: Minimum and maximum detection distance
- **Field of View**: Angular coverage (horizontal and vertical)
- **Resolution**: Angular resolution and range precision
- **Update Rate**: Frequency of sensor readings

### Depth Camera Simulation

Depth cameras simulate both RGB and depth information:

```xml
<!-- Example depth camera configuration -->
<gazebo reference="camera_link">
  <sensor type="depth" name="camera">
    <always_on>true</always_on>
    <visualize>true</visualize>
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
      <baseline>0.2</baseline>
      <alwaysOn>true</alwaysOn>
      <updateRate>30.0</updateRate>
      <cameraName>camera</cameraName>
      <imageTopicName>/camera/image_raw</imageTopicName>
      <depthImageTopicName>/camera/depth/image_raw</depthImageTopicName>
      <pointCloudTopicName>/camera/depth/points</pointCloudTopicName>
      <cameraInfoTopicName>/camera/camera_info</cameraInfoTopicName>
      <depthImageCameraInfoTopicName>/camera/depth/camera_info</depthImageCameraInfoTopicName>
      <frameName>camera_depth_frame</frameName>
      <pointCloudCutoff>0.5</pointCloudCutoff>
      <pointCloudCutoffMax>3.0</pointCloudCutoffMax>
      <distortion_k1>0.0</distortion_k1>
      <distortion_k2>0.0</distortion_k2>
      <distortion_k3>0.0</distortion_k3>
      <distortion_t1>0.0</distortion_t1>
      <distortion_t2>0.0</distortion_t2>
      <CxPrime>0.0</CxPrime>
      <Cx>0.0</Cx>
      <Cy>0.0</Cy>
      <focalLength>0.0</focalLength>
      <hackBaseline>0.0</hackBaseline>
    </plugin>
  </sensor>
</gazebo>
```

### IMU Simulation

Inertial Measurement Units measure orientation, velocity, and gravitational forces:

```xml
<!-- Example IMU configuration -->
<gazebo reference="imu_link">
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <visualize>false</visualize>
    <imu>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
          </noise>
        </z>
      </angular_velocity>
      <linear_acceleration>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
          </noise>
        </z>
      </linear_acceleration>
    </imu>
  </sensor>
</gazebo>
```

---

## 2.4 Gazebo vs. Unity for Robotics

### Gazebo Strengths

1. **Physics Accuracy**: Highly accurate physics simulation using ODE, Bullet, or Simbody
2. **ROS Integration**: Native ROS/ROS 2 integration through Gazebo ROS packages
3. **Robot Models**: Extensive library of robot models and environments
4. **Sensor Simulation**: Realistic simulation of various robot sensors
5. **Open Source**: Free and open-source with a large community

### Unity Strengths

1. **Visual Fidelity**: High-quality graphics for photorealistic environments
2. **Interactive Environments**: Game engine capabilities for complex interactions
3. **User Interface**: Robust tooling for creating and editing environments
4. **Perception Simulation**: Advanced rendering for computer vision applications
5. **Cross-platform**: Deployable across multiple platforms

### Choosing the Right Tool

Consider Gazebo when:
- Physics accuracy is paramount
- Working with ROS/ROS 2 extensively
- Need realistic sensor simulation
- Working with standard robot models

Consider Unity when:
- High visual fidelity is required
- Creating complex interactive environments
- Developing perception algorithms
- Need game-like interactions or VR/AR capabilities

---

## 2.5 Human-Robot Interaction Visualization

### Visualization Tools in Simulation

Simulation environments provide powerful tools for visualizing:

1. **Robot State Visualization**: Joint positions, velocities, and forces
2. **Sensor Data Overlay**: Displaying LiDAR scans, camera feeds, etc.
3. **Trajectory Planning**: Path visualization and planning feedback
4. **Collision Detection**: Visual indicators for collisions and contacts

### Developing Human-Robot Interfaces

Creating effective human-robot interaction requires:
- **Intuitive Visualization**: Clear representation of robot state and intentions
- **Safety Indicators**: Visual warnings and safety zones
- **Communication Channels**: Clear communication between human and robot
- **Debugging Tools**: Visualization of internal robot state for developers

---

<EducationalBox type="summary">

This module introduced the concept of digital twins in robotics, focusing on physics simulation using Gazebo and Unity. You learned about creating realistic environments, simulating various sensors, and the trade-offs between different simulation platforms. The module also covered visualization techniques that are essential for human-robot interaction.

The next module will explore the AI components that give robots their "brain" - perception, navigation, and learning capabilities using NVIDIA Isaac.

</EducationalBox>

<EducationalBox type="quiz">

1. What are the main differences between Gazebo and Unity for robotics simulation?
2. Name three different types of sensors that can be simulated in robotics environments.
3. Why are digital twins important in robotics development?

</EducationalBox>