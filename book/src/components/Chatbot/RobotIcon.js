import React from 'react';
import styles from './RobotIcon.module.css';

/**
 * Animated humanoid robot face icon
 * Features smooth, human-like eye movement animation
 */
export default function RobotIcon({ size = 48, isOpen = false }) {
  return (
    <div className={styles.robotContainer} style={{ width: size, height: size }}>
      <svg
        viewBox="0 0 100 100"
        className={styles.robotSvg}
        aria-hidden="true"
      >
        {/* Definitions for gradients and filters */}
        <defs>
          {/* Glow effect filter */}
          <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="1.5" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Face gradient */}
          <linearGradient id="faceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#3d4555" />
            <stop offset="50%" stopColor="#2a2f3a" />
            <stop offset="100%" stopColor="#1a1d24" />
          </linearGradient>

          {/* Visor/eye area gradient */}
          <linearGradient id="visorGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#0a0d12" />
            <stop offset="100%" stopColor="#12161d" />
          </linearGradient>

          {/* Human-like eye white gradient */}
          <radialGradient id="eyeWhiteGradient" cx="50%" cy="45%" r="55%">
            <stop offset="0%" stopColor="#f0f4f8" />
            <stop offset="70%" stopColor="#d8dce3" />
            <stop offset="100%" stopColor="#b8bcc5" />
          </radialGradient>

          {/* Iris gradient - cyan/blue AI color */}
          <radialGradient id="irisGradient" cx="45%" cy="40%" r="50%">
            <stop offset="0%" stopColor="#00e5ff" />
            <stop offset="40%" stopColor="#00bcd4" />
            <stop offset="100%" stopColor="#0097a7" />
          </radialGradient>

          {/* Pupil gradient */}
          <radialGradient id="pupilGradient" cx="40%" cy="35%" r="60%">
            <stop offset="0%" stopColor="#1a1a2e" />
            <stop offset="100%" stopColor="#0a0a15" />
          </radialGradient>

          {/* Eye shadow for depth */}
          <filter id="eyeShadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="1" stdDeviation="1" floodColor="#000" floodOpacity="0.3"/>
          </filter>
        </defs>

        {/* Robot head outer shell */}
        <rect
          x="12"
          y="10"
          width="76"
          height="80"
          rx="18"
          ry="18"
          fill="url(#faceGradient)"
          stroke="#4a5568"
          strokeWidth="1"
        />

        {/* Head highlight edge */}
        <path
          d="M 22 12 Q 50 6 78 12"
          fill="none"
          stroke="#5a6577"
          strokeWidth="1"
          opacity="0.5"
        />

        {/* Antenna base */}
        <rect x="44" y="2" width="12" height="10" rx="3" fill="#2d3748" />

        {/* Antenna light */}
        <circle
          cx="50"
          cy="5"
          r="3"
          fill="#00f5ff"
          filter="url(#softGlow)"
          className={styles.antennaLight}
        />

        {/* Visor / Eye area background */}
        <rect
          x="20"
          y="26"
          width="60"
          height="34"
          rx="10"
          fill="url(#visorGradient)"
          stroke="#2d3748"
          strokeWidth="0.5"
        />

        {/* Visor inner highlight */}
        <rect
          x="22"
          y="28"
          width="56"
          height="30"
          rx="8"
          fill="none"
          stroke="#3d4555"
          strokeWidth="0.5"
          opacity="0.4"
        />

        {/* ===== LEFT EYE ===== */}
        <g className={styles.eyeGroup}>
          {/* Eye socket shadow */}
          <ellipse
            cx="35"
            cy="43"
            rx="11"
            ry="10"
            fill="#050608"
          />

          {/* Eye white (sclera) - human-like almond shape */}
          <ellipse
            cx="35"
            cy="43"
            rx="10"
            ry="9"
            fill="url(#eyeWhiteGradient)"
            filter="url(#eyeShadow)"
          />

          {/* Iris - animated part */}
          <g className={styles.irisGroup}>
            <circle
              cx="35"
              cy="43"
              r="5.5"
              fill="url(#irisGradient)"
            />

            {/* Pupil */}
            <circle
              cx="35"
              cy="43"
              r="2.5"
              fill="url(#pupilGradient)"
            />

            {/* Pupil light reflection - main */}
            <ellipse
              cx="33.5"
              cy="41.5"
              rx="1.2"
              ry="0.9"
              fill="#ffffff"
              opacity="0.9"
            />

            {/* Pupil light reflection - secondary */}
            <circle
              cx="36.5"
              cy="44.5"
              r="0.5"
              fill="#ffffff"
              opacity="0.5"
            />
          </g>

          {/* Upper eyelid shadow hint */}
          <ellipse
            cx="35"
            cy="36"
            rx="8"
            ry="3"
            fill="#0a0d12"
            opacity="0.3"
          />
        </g>

        {/* ===== RIGHT EYE ===== */}
        <g className={styles.eyeGroup}>
          {/* Eye socket shadow */}
          <ellipse
            cx="65"
            cy="43"
            rx="11"
            ry="10"
            fill="#050608"
          />

          {/* Eye white (sclera) - human-like almond shape */}
          <ellipse
            cx="65"
            cy="43"
            rx="10"
            ry="9"
            fill="url(#eyeWhiteGradient)"
            filter="url(#eyeShadow)"
          />

          {/* Iris - animated part */}
          <g className={styles.irisGroup}>
            <circle
              cx="65"
              cy="43"
              r="5.5"
              fill="url(#irisGradient)"
            />

            {/* Pupil */}
            <circle
              cx="65"
              cy="43"
              r="2.5"
              fill="url(#pupilGradient)"
            />

            {/* Pupil light reflection - main */}
            <ellipse
              cx="63.5"
              cy="41.5"
              rx="1.2"
              ry="0.9"
              fill="#ffffff"
              opacity="0.9"
            />

            {/* Pupil light reflection - secondary */}
            <circle
              cx="66.5"
              cy="44.5"
              r="0.5"
              fill="#ffffff"
              opacity="0.5"
            />
          </g>

          {/* Upper eyelid shadow hint */}
          <ellipse
            cx="65"
            cy="36"
            rx="8"
            ry="3"
            fill="#0a0d12"
            opacity="0.3"
          />
        </g>

        {/* Nose bridge hint */}
        <line
          x1="50"
          y1="48"
          x2="50"
          y2="56"
          stroke="#3d4555"
          strokeWidth="1"
          opacity="0.3"
        />

        {/* Mouth / Speaker grille area */}
        <rect x="32" y="66" width="36" height="14" rx="5" fill="#0d1117" />

        {/* Speaker lines - voice indicator */}
        <g className={styles.speakerLines} opacity="0.6">
          <line x1="38" y1="69" x2="38" y2="77" stroke="#00f5ff" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="44" y1="69" x2="44" y2="77" stroke="#00f5ff" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="50" y1="69" x2="50" y2="77" stroke="#00f5ff" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="56" y1="69" x2="56" y2="77" stroke="#00f5ff" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="62" y1="69" x2="62" y2="77" stroke="#00f5ff" strokeWidth="1.5" strokeLinecap="round" />
        </g>

        {/* Side panel accents - left */}
        <rect x="14" y="48" width="3" height="10" rx="1.5" fill="#00f5ff" opacity="0.25" />

        {/* Side panel accents - right */}
        <rect x="83" y="48" width="3" height="10" rx="1.5" fill="#00f5ff" opacity="0.25" />

        {/* Ear pieces */}
        <rect x="5" y="36" width="8" height="22" rx="4" fill="#2d3748" stroke="#3d4555" strokeWidth="0.5" />
        <rect x="87" y="36" width="8" height="22" rx="4" fill="#2d3748" stroke="#3d4555" strokeWidth="0.5" />

        {/* Ear piece lights */}
        <circle cx="9" cy="47" r="2" fill="#00f5ff" opacity="0.4" />
        <circle cx="91" cy="47" r="2" fill="#00f5ff" opacity="0.4" />
      </svg>
    </div>
  );
}
