import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

// Icons as inline SVGs for the pillars
const PhysicalAIIcon = () => (
  <svg className={styles.pillarIcon} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M24 4L4 14v20l20 10 20-10V14L24 4z" stroke="currentColor" strokeWidth="2" fill="none"/>
    <circle cx="24" cy="24" r="8" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M24 16v-6M24 38v-6M16 24h-6M38 24h-6" stroke="currentColor" strokeWidth="2"/>
    <circle cx="24" cy="24" r="3" fill="currentColor"/>
  </svg>
);

const HumanoidIcon = () => (
  <svg className={styles.pillarIcon} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="24" cy="10" r="6" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M24 16v8" stroke="currentColor" strokeWidth="2"/>
    <path d="M16 20h16" stroke="currentColor" strokeWidth="2"/>
    <path d="M16 20v12" stroke="currentColor" strokeWidth="2"/>
    <path d="M32 20v12" stroke="currentColor" strokeWidth="2"/>
    <path d="M20 24h8v10H20z" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M20 34v10M28 34v10" stroke="currentColor" strokeWidth="2"/>
    <circle cx="24" cy="10" r="2" fill="currentColor"/>
  </svg>
);

const EmbodiedIcon = () => (
  <svg className={styles.pillarIcon} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="8" y="8" width="32" height="32" rx="4" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M16 20h16M16 28h10" stroke="currentColor" strokeWidth="2"/>
    <circle cx="36" cy="36" r="8" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M36 32v4h4" stroke="currentColor" strokeWidth="2"/>
    <path d="M8 16h4M8 24h4M8 32h4" stroke="currentColor" strokeWidth="2"/>
  </svg>
);

// Arrow icon for buttons
const ArrowRight = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Hero Section
function HeroSection() {
  return (
    <section className={styles.hero}>
      <div className={styles.heroBackground}>
        <div className={`${styles.heroGlow} ${styles.heroGlowPrimary}`} />
        <div className={`${styles.heroGlow} ${styles.heroGlowSecondary}`} />
        <div className={styles.heroGrid} />
      </div>

      <div className={styles.heroContainer}>
        <div className={styles.heroContent}>
          <div className={styles.heroTagline}>
            <span className={styles.heroTaglineDot} />
            The Future of Intelligent Machines
          </div>

          <h1 className={styles.heroTitle}>
            Physical AI &<br />
            <span className={styles.heroTitleGradient}>Humanoid Robotics</span>
          </h1>

          <p className={styles.heroSubtitle}>
            Master the technologies powering the next generation of intelligent robots.
            From ROS 2 foundations to embodied AI systems that perceive, reason, and act
            in the physical world.
          </p>

          <div className={styles.heroButtons}>
            <Link to="/docs/intro" className={styles.heroPrimary}>
              Start Learning <ArrowRight />
            </Link>
            <Link to="/docs/module-1-ros2" className={styles.heroSecondary}>
              View Modules
            </Link>
          </div>
        </div>

        <div className={styles.heroVisual}>
          <div className={styles.robotContainer}>
            <div className={styles.robotGlow} />
            <HumanoidRobotIllustration />
          </div>
        </div>
      </div>
    </section>
  );
}

// Humanoid Robot SVG Illustration
function HumanoidRobotIllustration() {
  return (
    <svg
      className={styles.robotImage}
      viewBox="0 0 400 500"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Background glow effect */}
      <defs>
        <radialGradient id="glowGradient" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#00d4ff" stopOpacity="0.35" />
          <stop offset="100%" stopColor="#00d4ff" stopOpacity="0" />
        </radialGradient>
        <linearGradient id="bodyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#2a2a38" />
          <stop offset="100%" stopColor="#1e1e28" />
        </linearGradient>
        <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#00e5ff" />
          <stop offset="100%" stopColor="#a78bfa" />
        </linearGradient>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="4" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Ambient glow */}
      <ellipse cx="200" cy="250" rx="150" ry="200" fill="url(#glowGradient)" />

      {/* Base/Feet */}
      <ellipse cx="200" cy="480" rx="80" ry="15" fill="#12121a" stroke="#3a3a4a" strokeWidth="2" />

      {/* Left Leg */}
      <path
        d="M160 380 L150 460 Q150 475 160 475 L170 475 Q180 475 180 460 L175 380"
        fill="url(#bodyGradient)"
        stroke="#3a3a4a"
        strokeWidth="2"
      />
      <rect x="155" y="400" width="20" height="4" rx="2" fill="url(#accentGradient)" filter="url(#glow)" />

      {/* Right Leg */}
      <path
        d="M240 380 L250 460 Q250 475 240 475 L230 475 Q220 475 220 460 L225 380"
        fill="url(#bodyGradient)"
        stroke="#3a3a4a"
        strokeWidth="2"
      />
      <rect x="225" y="400" width="20" height="4" rx="2" fill="url(#accentGradient)" filter="url(#glow)" />

      {/* Pelvis */}
      <path
        d="M150 350 Q150 385 200 385 Q250 385 250 350 L240 320 L160 320 Z"
        fill="url(#bodyGradient)"
        stroke="#3a3a4a"
        strokeWidth="2"
      />
      <circle cx="200" cy="360" r="8" fill="url(#accentGradient)" filter="url(#glow)" />

      {/* Torso */}
      <path
        d="M155 200 L145 320 L255 320 L245 200 Q245 180 200 180 Q155 180 155 200"
        fill="url(#bodyGradient)"
        stroke="#3a3a4a"
        strokeWidth="2"
      />

      {/* Chest details */}
      <path
        d="M170 220 L180 280 L220 280 L230 220 Q230 200 200 200 Q170 200 170 220"
        fill="#1a1a24"
        stroke="#3a3a4a"
        strokeWidth="1"
      />
      <rect x="185" y="230" width="30" height="40" rx="4" fill="#12121a" stroke="#00e5ff" strokeWidth="1" />
      <circle cx="200" cy="250" r="10" fill="none" stroke="url(#accentGradient)" strokeWidth="2" filter="url(#glow)" />
      <circle cx="200" cy="250" r="4" fill="#00e5ff" filter="url(#glow)" />

      {/* Energy lines on torso */}
      <path d="M160 240 L145 240" stroke="#00e5ff" strokeWidth="2" opacity="0.5" />
      <path d="M240 240 L255 240" stroke="#00e5ff" strokeWidth="2" opacity="0.5" />
      <path d="M160 260 L140 260" stroke="#8b5cf6" strokeWidth="2" opacity="0.5" />
      <path d="M240 260 L260 260" stroke="#8b5cf6" strokeWidth="2" opacity="0.5" />

      {/* Left Arm */}
      <path
        d="M145 200 L115 210 L100 280 L95 340 Q90 355 105 355 L115 355 Q130 355 125 340 L120 280 L130 220"
        fill="url(#bodyGradient)"
        stroke="#3a3a4a"
        strokeWidth="2"
      />
      <circle cx="115" cy="210" r="12" fill="url(#bodyGradient)" stroke="#3a3a4a" strokeWidth="2" />
      <rect x="97" y="300" width="20" height="4" rx="2" fill="url(#accentGradient)" filter="url(#glow)" />

      {/* Right Arm */}
      <path
        d="M255 200 L285 210 L300 280 L305 340 Q310 355 295 355 L285 355 Q270 355 275 340 L280 280 L270 220"
        fill="url(#bodyGradient)"
        stroke="#3a3a4a"
        strokeWidth="2"
      />
      <circle cx="285" cy="210" r="12" fill="url(#bodyGradient)" stroke="#3a3a4a" strokeWidth="2" />
      <rect x="283" y="300" width="20" height="4" rx="2" fill="url(#accentGradient)" filter="url(#glow)" />

      {/* Neck */}
      <rect x="185" y="155" width="30" height="30" rx="4" fill="url(#bodyGradient)" stroke="#3a3a4a" strokeWidth="2" />
      <rect x="190" y="165" width="20" height="3" rx="1" fill="#00e5ff" opacity="0.5" />

      {/* Head */}
      <path
        d="M155 80 Q155 40 200 40 Q245 40 245 80 L245 140 Q245 160 200 160 Q155 160 155 140 Z"
        fill="url(#bodyGradient)"
        stroke="#3a3a4a"
        strokeWidth="2"
      />

      {/* Face plate */}
      <path
        d="M165 75 Q165 55 200 55 Q235 55 235 75 L235 130 Q235 145 200 145 Q165 145 165 130 Z"
        fill="#0a0a0f"
        stroke="#3a3a4a"
        strokeWidth="1"
      />

      {/* Eyes */}
      <ellipse cx="180" cy="95" rx="15" ry="10" fill="#12121a" stroke="#00e5ff" strokeWidth="2" />
      <ellipse cx="220" cy="95" rx="15" ry="10" fill="#12121a" stroke="#00e5ff" strokeWidth="2" />
      <ellipse cx="180" cy="95" rx="8" ry="5" fill="#00e5ff" filter="url(#glow)">
        <animate attributeName="opacity" values="1;0.5;1" dur="3s" repeatCount="indefinite" />
      </ellipse>
      <ellipse cx="220" cy="95" rx="8" ry="5" fill="#00e5ff" filter="url(#glow)">
        <animate attributeName="opacity" values="1;0.5;1" dur="3s" repeatCount="indefinite" />
      </ellipse>

      {/* Visor line */}
      <path d="M165 95 L235 95" stroke="url(#accentGradient)" strokeWidth="1" opacity="0.3" />

      {/* Mouth/Speaker */}
      <rect x="185" y="115" width="30" height="8" rx="2" fill="#12121a" stroke="#3a3a4a" strokeWidth="1" />
      <line x1="190" y1="119" x2="195" y2="119" stroke="#00e5ff" strokeWidth="2" opacity="0.7" />
      <line x1="198" y1="119" x2="202" y2="119" stroke="#00e5ff" strokeWidth="2" opacity="0.7" />
      <line x1="205" y1="119" x2="210" y2="119" stroke="#00e5ff" strokeWidth="2" opacity="0.7" />

      {/* Head antenna/sensor */}
      <circle cx="200" cy="35" r="6" fill="url(#bodyGradient)" stroke="#3a3a4a" strokeWidth="2" />
      <circle cx="200" cy="35" r="3" fill="#00e5ff" filter="url(#glow)">
        <animate attributeName="r" values="3;4;3" dur="2s" repeatCount="indefinite" />
      </circle>
      <line x1="200" y1="41" x2="200" y2="55" stroke="#3a3a4a" strokeWidth="2" />

      {/* Side head details */}
      <rect x="150" y="85" width="8" height="20" rx="2" fill="url(#bodyGradient)" stroke="#3a3a4a" strokeWidth="1" />
      <rect x="242" y="85" width="8" height="20" rx="2" fill="url(#bodyGradient)" stroke="#3a3a4a" strokeWidth="1" />
    </svg>
  );
}

// Pillars Section
function PillarsSection() {
  const pillars = [
    {
      Icon: PhysicalAIIcon,
      title: 'Physical AI',
      description:
        'Learn how artificial intelligence extends beyond software into the physical realm, enabling machines to perceive and interact with their environment.',
    },
    {
      Icon: HumanoidIcon,
      title: 'Humanoid Robotics',
      description:
        'Build robots with human-like form factors using ROS 2, URDF modeling, and advanced control systems for natural movement and manipulation.',
    },
    {
      Icon: EmbodiedIcon,
      title: 'Embodied Intelligence',
      description:
        'Integrate vision, language, and action through Vision-Language-Action models that enable robots to understand and execute complex tasks.',
    },
  ];

  return (
    <section className={styles.pillars}>
      <div className={styles.pillarsContainer}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionLabel}>Core Concepts</span>
          <h2 className={styles.sectionTitle}>AI Systems in the Physical World</h2>
          <p className={styles.sectionSubtitle}>
            Explore the three pillars of modern robotics that are transforming how
            machines interact with the real world.
          </p>
        </div>

        <div className={styles.pillarsGrid}>
          {pillars.map((pillar, idx) => (
            <div key={idx} className={styles.pillarCard}>
              <pillar.Icon />
              <h3 className={styles.pillarTitle}>{pillar.title}</h3>
              <p className={styles.pillarDescription}>{pillar.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// Modules Section
function ModulesSection() {
  const modules = [
    {
      number: '1',
      title: 'ROS 2 Foundations',
      description: 'Master Robot Operating System 2, from architecture to building your first humanoid robot model.',
      chapters: '6 chapters',
      link: '/docs/module-1-ros2',
    },
    {
      number: '2',
      title: 'Simulation Environments',
      description: 'Set up physics simulations with Gazebo and Unity for safe robot development and testing.',
      chapters: '7 chapters',
      link: '/docs/module-2-simulation',
    },
    {
      number: '3',
      title: 'NVIDIA Isaac Platform',
      description: 'Leverage Isaac Sim for synthetic data, perception, and navigation with GPU acceleration.',
      chapters: '7 chapters',
      link: '/docs/module-3-isaac',
    },
    {
      number: '4',
      title: 'Vision-Language-Action',
      description: 'Build end-to-end pipelines connecting speech, LLMs, and robot actions for intelligent control.',
      chapters: '6 chapters',
      link: '/docs/module-4-vla',
    },
  ];

  return (
    <section className={styles.modules}>
      <div className={styles.modulesContainer}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionLabel}>Curriculum</span>
          <h2 className={styles.sectionTitle}>Learning Path</h2>
          <p className={styles.sectionSubtitle}>
            A structured journey from robotics fundamentals to cutting-edge AI integration.
          </p>
        </div>

        <div className={styles.modulesGrid}>
          {modules.map((module) => (
            <Link key={module.number} to={module.link} className={styles.moduleCard}>
              <div className={styles.moduleNumber}>{module.number}</div>
              <div className={styles.moduleContent}>
                <h3 className={styles.moduleTitle}>{module.title}</h3>
                <p className={styles.moduleDescription}>{module.description}</p>
                <span className={styles.moduleChapters}>{module.chapters}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

// CTA Section
function CTASection() {
  return (
    <section className={styles.cta}>
      <div className={styles.ctaContainer}>
        <div className={styles.ctaGlow} />
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaTitle}>Ready to Build the Future?</h2>
          <p className={styles.ctaDescription}>
            Complete the capstone project and build a fully integrated humanoid robot system
            with voice control, navigation, and manipulation capabilities.
          </p>
          <Link to="/docs/capstone" className={styles.heroPrimary}>
            Start Capstone Project <ArrowRight />
          </Link>
        </div>
      </div>
    </section>
  );
}

// Main Home Component
export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title="Physical AI & Humanoid Robotics"
      description="Master the technologies powering the next generation of intelligent robots. From ROS 2 foundations to embodied AI systems."
    >
      <HeroSection />
      <PillarsSection />
      <ModulesSection />
      <CTASection />
    </Layout>
  );
}
