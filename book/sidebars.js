// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Physical AI & Humanoid Robotics Book Sidebar Configuration
 *
 * Structure:
 * - Introduction
 * - Module 1: ROS 2 (6 chapters)
 * - Module 2: Simulation (7 chapters)
 * - Module 3: NVIDIA Isaac (7 chapters)
 * - Module 4: VLA (6 chapters)
 * - Capstone Project (8 chapters)
 *
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  bookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: ROS 2 Foundations',
      link: {
        type: 'doc',
        id: 'module-1-ros2/index',
      },
      items: [
        'module-1-ros2/1-1-introduction',
        'module-1-ros2/1-2-architecture',
        'module-1-ros2/1-3-rclpy-basics',
        'module-1-ros2/1-4-urdf-fundamentals',
        'module-1-ros2/1-5-humanoid-model',
        'module-1-ros2/1-6-summary',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Robot Simulation',
      link: {
        type: 'doc',
        id: 'module-2-simulation/index',
      },
      items: [
        'module-2-simulation/2-1-simulation-concepts',
        'module-2-simulation/2-2-gazebo-setup',
        'module-2-simulation/2-3-physics-simulation',
        'module-2-simulation/2-4-sensor-simulation',
        'module-2-simulation/2-5-unity-introduction',
        'module-2-simulation/2-6-urdf-to-gazebo',
        'module-2-simulation/2-7-summary',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac & Navigation',
      link: {
        type: 'doc',
        id: 'module-3-isaac/index',
      },
      items: [
        'module-3-isaac/3-1-isaac-sim-overview',
        'module-3-isaac/3-2-setup-prerequisites',
        'module-3-isaac/3-3-synthetic-data',
        'module-3-isaac/3-4-isaac-ros-integration',
        'module-3-isaac/3-5-vslam',
        'module-3-isaac/3-6-nav2-planning',
        'module-3-isaac/3-7-summary',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      link: {
        type: 'doc',
        id: 'module-4-vla/index',
      },
      items: [
        'module-4-vla/4-1-embodied-ai',
        'module-4-vla/4-2-speech-recognition',
        'module-4-vla/4-3-llm-command-parsing',
        'module-4-vla/4-4-ros2-actions',
        'module-4-vla/4-5-end-to-end-pipeline',
        'module-4-vla/4-6-summary',
      ],
    },
    {
      type: 'category',
      label: 'Capstone: Voice-Controlled Assistant',
      link: {
        type: 'doc',
        id: 'capstone/index',
      },
      items: [
        'capstone/cap-1-project-overview',
        'capstone/cap-2-system-architecture',
        'capstone/cap-3-voice-input',
        'capstone/cap-4-navigation',
        'capstone/cap-5-vision',
        'capstone/cap-6-manipulation',
        'capstone/cap-7-integration',
        'capstone/cap-8-conclusion',
      ],
    },
  ],
};

export default sidebars;
