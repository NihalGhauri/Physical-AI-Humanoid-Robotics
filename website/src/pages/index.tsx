import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <div className="text--center margin-bottom--xl">
              <div className="avatar avatar--xxl margin-bottom--sm">
                {/* <img  src="img/pngwing.com.png" alt="nihal" /> */}
              </div>
            </div>
            <Heading as="h1" className="hero__title text--center">
              {siteConfig.title}
            </Heading>
            <p className="hero__subtitle text--center text--large">
              {siteConfig.tagline}
            </p>
            <div className={styles.buttons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro">
                Start Reading - Textbook Introduction
              </Link>
              <Link
                className="button button--primary button--lg"
                to="/docs/module-1-robotic-nervous-system/intro">
                Begin with Module 1
              </Link>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function TextbookIntro() {
  return (
    <section className={styles.textbookIntro}>
      <div className="container">
        <div className="row">
          <div className="col col--10 col--offset-1">
            <Heading as="h2" className="text--center margin-bottom--lg">
              About This Textbook
            </Heading>
            <p className="text--center">
              This comprehensive textbook on Physical AI & Humanoid Robotics covers the design, simulation,
              and deployment of intelligent robots that interact with the physical world. Drawing from state-of-the-art
              technologies including ROS 2, NVIDIA Isaac, Gazebo, and Unity, this resource prepares you to build
              next-generation embodied AI systems.
            </p>
            <div className="row margin-top--lg">
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <div className="avatar avatar--lg margin-bottom--sm">
                    <div className="avatar__intro">
                      <div className="avatar__name">ROS 2</div>
                    </div>
                  </div>
                  <p>Robotic Operating System for communication and control</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <div className="avatar avatar--lg margin-bottom--sm">
                    <div className="avatar__intro">
                      <div className="avatar__name">NVIDIA Isaac</div>
                    </div>
                  </div>
                  <p>AI-powered perception and navigation systems</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <div className="avatar avatar--lg margin-bottom--sm">
                    <div className="avatar__intro">
                      <div className="avatar__name">VLA Systems</div>
                    </div>
                  </div>
                  <p>Vision-Language-Action interfaces for human-robot interaction</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function FeaturedModules() {
  const modules = [
    {
      title: "Robotic Nervous System (ROS 2)",
      description: "Learn the Robot Operating System 2 architecture, nodes, topics, services, and actions.",
      icon: "🤖",
      path: "/docs/module-1-robotic-nervous-system/intro"
    },
    {
      title: "Digital Twin (Gazebo & Unity)",
      description: "Master physics simulation with Gazebo and Unity for safe robot testing and validation.",
      icon: "🎮",
      path: "/docs/module-2-digital-twin/intro"
    },
    {
      title: "AI-Robot Brain (NVIDIA Isaac)",
      description: "Implement perception, navigation, and learning with NVIDIA Isaac and Vision-Language-Action systems.",
      icon: "🧠",
      path: "/docs/module-3-ai-robot-brain/intro"
    },
    {
      title: "Vision-Language-Action (VLA)",
      description: "Create conversational robots that understand natural language commands and execute them.",
      icon: "💬",
      path: "/docs/module-4-vision-language-action/intro"
    },
    {
      title: "Capstone Project",
      description: "Integrate all concepts to develop a complete simulated humanoid robot system.",
      icon: "🎓",
      path: "/docs/capstone-project/intro"
    },
    {
      title: "Advanced Applications",
      description: "Explore real-world implementations and cutting-edge applications of humanoid robotics.",
      icon: "🚀",
      path: "/docs/intro"
    }
  ];

  return (
    <section className={styles.featuredModulesSection}>
      <div className="container">
        <div className="row">
          <div className="col col--10 col--offset-1 text--center margin-bottom--xl">
            <Heading as="h2">Learning Modules</Heading>
            <p className="text--large">Explore the fundamental concepts of physical AI and humanoid robotics</p>
          </div>
        </div>
        <div className="row">
          {modules.map((module, idx) => (
            <div key={idx} className="col col--4 margin-bottom--lg">
              <div className={clsx('padding-horiz--md', styles.robotCard)}>
                <div style={{fontSize: '2.5rem', textAlign: 'center', marginBottom: '1rem'}}>{module.icon}</div>
                <Heading as="h3">{module.title}</Heading>
                <p>{module.description}</p>
                <Link
                  to={module.path}
                  className="button button--outline button--secondary"
                >
                  Explore Module
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <Heading as="h2">Ready to Start Learning?</Heading>
            <p className="padding-vert--md">
              Begin your journey into Physical AI & Humanoid Robotics with our comprehensive textbook.
              Whether you're a student, researcher, or engineer, this resource will guide you through
              the fundamentals to advanced concepts in embodied AI.
            </p>
            <div className="margin-top--lg">
              <Link
                className="button button--primary button--lg margin-right--md"
                to="/docs/intro">
                Get Started Now
              </Link>
              <Link
                className="button button--secondary button--lg"
                to="/docs/module-1-robotic-nervous-system/intro">
                Begin with Module 1
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function StatsSection() {
  return (
    <section className="padding-vert--lg">
      <div className="container">
        <div className="row text--center">
          <div className="col col--3 col--offset-1">
            <h2 className="text--center padding-top--sm">6</h2>
            <p className="text--large">Learning Modules</p>
          </div>
          <div className="col col--3">
            <h2 className="text--center padding-top--sm">50+</h2>
            <p className="text--large">Concepts & Techniques</p>
          </div>
          <div className="col col--3">
            <h2 className="text--center padding-top--sm">100+</h2>
            <p className="text--large">Pages of Content</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics`}
      description="Comprehensive textbook on embodied intelligence and AI systems in the physical world">
      <HomepageHeader />
      <main>
        <TextbookIntro />
        <StatsSection />
        <FeaturedModules />
        <CTASection />
      </main>
    </Layout>
  );
}
