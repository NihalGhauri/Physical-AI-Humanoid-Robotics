import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar structure for the Physical AI & Humanoid Robotics textbook
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'intro',
      ],
      link: {
        type: 'doc',
        id: 'intro',
      }
    },
    {
      type: 'category',
      label: 'Module 1: Robotic Nervous System (ROS 2)',
      items: [
        'module-1-robotic-nervous-system/intro',
      ],
      link: {
        type: 'doc',
        id: 'module-1-robotic-nervous-system/intro',
      }
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/intro',
      ],
      link: {
        type: 'doc',
        id: 'module-2-digital-twin/intro',
      }
    },
    {
      type: 'category',
      label: 'Module 3: AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-3-ai-robot-brain/intro',
      ],
      link: {
        type: 'doc',
        id: 'module-3-ai-robot-brain/intro',
      }
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vision-language-action/intro',
      ],
      link: {
        type: 'doc',
        id: 'module-4-vision-language-action/intro',
      }
    },
    {
      type: 'category',
      label: 'Capstone Project: Simulated Humanoid Robot',
      items: [
        'capstone-project/intro',
      ],
      link: {
        type: 'doc',
        id: 'capstone-project/intro',
      }
    }
  ],
};

export default sidebars;
