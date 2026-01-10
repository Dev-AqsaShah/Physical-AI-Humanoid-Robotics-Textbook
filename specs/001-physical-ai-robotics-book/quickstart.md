# Quickstart: Physical AI & Humanoid Robotics Book

**Feature Branch**: `001-physical-ai-robotics-book`
**Date**: 2026-01-09

## Reader Prerequisites

Before starting this book, readers should have:

### Required Knowledge
- [ ] Basic Python programming (functions, classes, file I/O)
- [ ] Familiarity with command line / terminal
- [ ] Understanding of basic AI/ML concepts (models, training, inference)
- [ ] Basic linear algebra (vectors, matrices, transformations)

### Recommended (but not required)
- [ ] Linux/Ubuntu experience
- [ ] Git version control basics
- [ ] Docker familiarity

---

## Environment Setup

### Option A: Ubuntu Native (Recommended)

**Operating System**: Ubuntu 22.04 LTS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3 python3-pip python3-venv -y

# Install ROS 2 Humble
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-humble-desktop -y

# Source ROS 2
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Option B: Docker Container

```bash
# Pull ROS 2 Humble image
docker pull ros:humble

# Run interactive container
docker run -it --rm \
  --name ros2-dev \
  -v ~/robotics-book:/workspace \
  ros:humble \
  bash
```

### Option C: WSL2 (Windows Users)

1. Install WSL2 with Ubuntu 22.04
2. Follow Option A instructions inside WSL2
3. Install VcXsrv for GUI applications

---

## Module-Specific Setup

### Module 1: ROS 2

```bash
# Install additional ROS 2 packages
sudo apt install ros-humble-rclpy ros-humble-std-msgs -y

# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash

# Verify installation
ros2 run demo_nodes_cpp talker
# In another terminal:
ros2 run demo_nodes_cpp listener
```

**Verification**: You should see "Hello World" messages being published and received.

### Module 2: Gazebo Fortress

```bash
# Install Gazebo Fortress
sudo apt install ros-humble-ros-gz -y

# Install additional tools
sudo apt install ros-humble-robot-state-publisher \
                 ros-humble-joint-state-publisher-gui -y

# Test Gazebo
gz sim
```

**Verification**: Gazebo window opens with empty world.

### Module 3: NVIDIA Isaac Sim

**Hardware Requirements**:
- NVIDIA GPU: RTX 2070 or better
- VRAM: 8GB minimum (16GB recommended)
- RAM: 32GB recommended
- Storage: 50GB free space

```bash
# Install NVIDIA drivers (if not already installed)
sudo apt install nvidia-driver-535 -y

# Download Isaac Sim from NVIDIA Omniverse Launcher
# https://developer.nvidia.com/isaac-sim

# Install Isaac ROS packages
mkdir -p ~/isaac_ros_ws/src
cd ~/isaac_ros_ws/src
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git
cd ..
colcon build
```

**Verification**: Isaac Sim launches and shows sample scene.

### Module 4: VLA (Voice-Language-Action)

```bash
# Create Python virtual environment
python3 -m venv ~/vla_env
source ~/vla_env/bin/activate

# Install Whisper
pip install openai-whisper

# Install LLM tools (choose one)
# Option A: Ollama (local)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3

# Option B: OpenAI API
pip install openai
# Set OPENAI_API_KEY environment variable

# Test Whisper
whisper --help
```

**Verification**: `whisper --help` shows usage information.

---

## Book Content Development Setup

For contributors working on book content:

```bash
# Clone repository
git clone <repository-url>
cd physical-ai-robotics-book

# Install Node.js (for Docusaurus)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install dependencies
npm install

# Start development server
npm run start

# Build for production
npm run build
```

**Verification**: Browser opens to `http://localhost:3000` showing book.

---

## Validation Checklist

Use this checklist to verify your environment is ready:

### Module 1 Ready
- [ ] `ros2 --version` returns version info
- [ ] `ros2 topic list` shows /rosout
- [ ] Python imports work: `python3 -c "import rclpy; print('OK')"`

### Module 2 Ready
- [ ] `gz sim --version` returns version info
- [ ] Gazebo launches without errors
- [ ] `ros2 pkg list | grep robot_state_publisher` returns result

### Module 3 Ready
- [ ] `nvidia-smi` shows GPU info
- [ ] Isaac Sim launches successfully
- [ ] Isaac ROS packages built without errors

### Module 4 Ready
- [ ] `whisper --help` shows usage
- [ ] LLM responds to test prompt
- [ ] Audio recording works on system

---

## Troubleshooting

### Common Issues

**Issue**: ROS 2 commands not found
```bash
# Solution: Source ROS 2 setup
source /opt/ros/humble/setup.bash
```

**Issue**: Gazebo crashes on startup
```bash
# Solution: Check graphics driver
glxinfo | grep "OpenGL version"
# Should show OpenGL 4.x or higher
```

**Issue**: Isaac Sim won't launch
```bash
# Solution: Check NVIDIA driver
nvidia-smi
# Ensure driver version >= 525
```

**Issue**: Whisper model download fails
```bash
# Solution: Set cache directory
export WHISPER_CACHE_DIR=~/.cache/whisper
whisper --model tiny test.wav
```

---

## Learning Path

### Sequential (Recommended for Beginners)

```
Week 1-2: Module 1 (ROS 2)
    └── Complete all chapters, run all examples

Week 3-4: Module 2 (Simulation)
    └── Build on Module 1 knowledge

Week 5-6: Module 3 (NVIDIA Isaac)
    └── Requires GPU, can skip if unavailable

Week 7-8: Module 4 (VLA)
    └── Builds on all previous modules

Week 9-10: Capstone
    └── Integrate everything
```

### Reference (For Experienced Users)

Jump directly to the module you need:
- **Need ROS 2?** → Module 1
- **Need simulation?** → Module 2
- **Need Isaac/Nav2?** → Module 3
- **Need voice/LLM?** → Module 4

---

## Support Resources

- **Official ROS 2 Documentation**: https://docs.ros.org/en/humble/
- **Gazebo Documentation**: https://gazebosim.org/docs/fortress/
- **NVIDIA Isaac Documentation**: https://docs.omniverse.nvidia.com/isaacsim/
- **Nav2 Documentation**: https://navigation.ros.org/
- **Whisper GitHub**: https://github.com/openai/whisper

---

**Quickstart Version**: 1.0.0
**Last Updated**: 2026-01-09
