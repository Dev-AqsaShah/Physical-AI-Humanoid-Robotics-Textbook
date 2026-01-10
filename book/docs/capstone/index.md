---
sidebar_position: 1
title: "Capstone: Voice-Controlled Humanoid"
description: Build an autonomous humanoid robot that responds to voice commands
---

# Capstone: The Autonomous Humanoid

*Integrate everything you've learned into a complete voice-controlled robot system*

## Project Overview

In this capstone project, you'll build a simulated humanoid robot that can:

1. **Receive voice commands** using speech recognition
2. **Navigate autonomously** using Nav2 path planning
3. **Avoid obstacles** in its environment
4. **Identify objects** using computer vision
5. **Manipulate objects** through grasping actions

## Prerequisites

:::info Complete All Modules First
This capstone project requires knowledge from all four modules:
- **Module 1**: ROS 2, URDF, rclpy
- **Module 2**: Gazebo simulation, sensors
- **Module 3**: Isaac Sim, Nav2, VSLAM
- **Module 4**: VLA, Whisper, LLM parsing
:::

## Chapters

1. [Project Overview](./cap-1-project-overview) - Scope and architecture
2. [System Architecture](./cap-2-system-architecture) - Full system design
3. [Voice Input](./cap-3-voice-input) - Whisper + LLM integration
4. [Navigation](./cap-4-navigation) - Nav2 path planning
5. [Vision](./cap-5-vision) - Object detection
6. [Manipulation](./cap-6-manipulation) - Grasping and interaction
7. [Integration](./cap-7-integration) - Connecting all components
8. [Conclusion](./cap-8-conclusion) - Next steps and extensions

## Estimated Time

6-8 hours for complete capstone project

## What You'll Build

```
┌─────────────────────────────────────────────────────────────┐
│                   VOICE-CONTROLLED HUMANOID                  │
├─────────────────────────────────────────────────────────────┤
│  USER: "Go to the kitchen and pick up the red cup"          │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ Whisper │───▶│   LLM   │───▶│  Nav2   │───▶│  Arm    │  │
│  │ (ASR)   │    │ Parser  │    │ Planner │    │ Control │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ROBOT: Navigates to kitchen, identifies cup, grasps it     │
└─────────────────────────────────────────────────────────────┘
```
