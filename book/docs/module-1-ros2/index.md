---
sidebar_position: 1
title: "Module 1: ROS 2 Foundations"
description: Learn the middleware that powers modern robotics - nodes, topics, services, and robot description
---

# Module 1: The Robotic Nervous System

*Master the communication infrastructure that enables robots to perceive, think, and act*

## Why ROS 2?

Just as the human nervous system coordinates signals between brain, sensors, and muscles, ROS 2 (Robot Operating System 2) coordinates communication between software components in a robot. It's not an operating system in the traditional sense - it's **middleware** that provides:

- **Communication patterns** for components to exchange data
- **Tools** for visualization, debugging, and development
- **Ecosystem** of reusable packages for common robotics tasks
- **Hardware abstraction** so software works across different robots

Nearly every major robotics company and research institution uses ROS. Learning ROS 2 opens doors to a vast ecosystem of tools, libraries, and community knowledge.

## Learning Objectives

By the end of this module, you will be able to:

- Explain ROS 2's role as robotics middleware and its architecture
- Create and manage ROS 2 nodes that publish and subscribe to topics
- Implement services for synchronous request-response communication
- Write Python programs using the rclpy client library
- Describe robot structure using URDF (Unified Robot Description Format)
- Build and visualize a complete humanoid robot model

## Prerequisites

Before starting, you should have:

- **Python**: Functions, classes, decorators, context managers
- **Command Line**: Navigation, running scripts, environment variables
- **Ubuntu 22.04**: Fresh installation or virtual machine (WSL2 works)

## What You'll Build

By the end of this module, you'll have created:

1. A **publisher node** that sends sensor data
2. A **subscriber node** that processes messages
3. A **service** that responds to requests
4. A complete **humanoid robot URDF** ready for simulation

## Chapters

| Chapter | Topic | Key Concepts |
|---------|-------|--------------|
| 1.1 | [Introduction to ROS 2](./1-1-introduction) | History, architecture overview, installation |
| 1.2 | [ROS 2 Architecture](./1-2-architecture) | Nodes, topics, services, actions |
| 1.3 | [Python with rclpy](./1-3-rclpy-basics) | Publishers, subscribers, timers |
| 1.4 | [URDF Fundamentals](./1-4-urdf-fundamentals) | Links, joints, visual geometry |
| 1.5 | [Building a Humanoid](./1-5-humanoid-model) | Complete robot model |
| 1.6 | [Summary](./1-6-summary) | Review and next steps |

## Estimated Time

**4-6 hours** for complete module with hands-on exercises

## Environment Setup

Before proceeding, verify your ROS 2 installation:

```bash
# Check ROS 2 is installed
ros2 --version

# Expected output: ros2 humble
```

If not installed, follow the [official ROS 2 Humble installation guide](https://docs.ros.org/en/humble/Installation.html).

---

Ready to begin? Start with [Chapter 1.1: Introduction to ROS 2](./1-1-introduction).
