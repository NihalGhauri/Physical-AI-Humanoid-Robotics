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
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
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
    </header>
  );
}

function TextbookIntro() {
  return (
    <section className={styles.textbookIntro}>
      <div className="container">
        <Heading as="h2" className="text--center margin-bottom--lg">
          About This Textbook
        </Heading>
        <p className="text--center">
          This comprehensive textbook on Physical AI & Humanoid Robotics covers the design, simulation,
          and deployment of intelligent robots that interact with the physical world. Drawing from state-of-the-art
          technologies including ROS 2, NVIDIA Isaac, Gazebo, and Unity, this resource prepares you to build
          next-generation embodied AI systems.
        </p>
      </div>
    </section>
  );
}

function FeaturedModules() {
  const modules = [
    {
      title: "ROS 2 Fundamentals",
      description: "Learn the Robot Operating System 2 architecture, nodes, topics, services, and actions.",
      icon: "🤖"
    },
    {
      title: "Simulation & Digital Twins",
      description: "Master physics simulation with Gazebo and Unity for safe robot testing and validation.",
      icon: "🎮"
    },
    {
      title: "AI & Perception",
      description: "Implement perception, navigation, and learning with NVIDIA Isaac and Vision-Language-Action systems.",
      icon: "🧠"
    }
  ];

  return (
    <section className={styles.featuredModulesSection}>
      <div className="container">
        <div className="row">
          <div className="col col--12 text--center margin-bottom--lg">
            <Heading as="h2">Core Learning Modules</Heading>
            <p>Explore the fundamental concepts of physical AI and humanoid robotics</p>
          </div>
        </div>
        <div className="row">
          {modules.map((module, idx) => (
            <div key={idx} className="col col--4 margin-bottom--lg">
              <div className={clsx('padding-horiz--md', styles.robotCard)}>
                <div style={{fontSize: '2rem', textAlign: 'center', marginBottom: '1rem'}}>{module.icon}</div>
                <Heading as="h3">{module.title}</Heading>
                <p>{module.description}</p>
                <Link
                  to={idx === 0 ? `/docs/module-1-robotic-nervous-system/intro` :
                      idx === 1 ? `/docs/module-2-digital-twin/intro` :
                      `/docs/module-3-ai-robot-brain/intro`}
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
    <section className="container padding-vert--xl text--center">
      <div className="row">
        <div className="col col--8 col--offset-2">
          <Heading as="h2">Ready to Start Learning?</Heading>
          <p className="padding-vert--md">
            Begin your journey into Physical AI & Humanoid Robotics with our comprehensive textbook.
            Whether you're a student, researcher, or engineer, this resource will guide you through
            the fundamentals to advanced concepts in embodied AI.
          </p>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Get Started Now
          </Link>
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
        <FeaturedModules />
        <CTASection />
      </main>
    </Layout>
  );
}
