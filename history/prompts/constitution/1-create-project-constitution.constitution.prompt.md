---
id: "1"
title: "Create Project Constitution"
stage: "constitution"
date_iso: "2025-01-14"
surface: "agent"
model: "Claude Sonnet 4"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution Project: Physical AI & Humanoid Robotics Textbook"
labels: ["constitution", "specification", "governance"]
spec: null
ticket: null
adr: null
pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
links: []

outcome: "Successfully created the project constitution for the Physical AI & Humanoid Robotics Textbook project based on the provided specifications. The constitution establishes six core principles along with technology stack constraints, development workflow, success criteria, and governance guidelines."
evaluation: "The constitution aligns with all specified requirements and provides a solid foundation for the project governance. All placeholder values were properly replaced with project-specific content."

prompt_text: |
  /sp.constitution Project: Physical AI & Humanoid Robotics Textbook

  Core principles:

  * Syllabus fidelity (no omissions or reinterpretation)
  * Deterministic, grounded AI output (no hallucinations)
  * Spec-first development (no implementation before specs)
  * Reproducibility (all claims traceable)

  Key standards:

  * Full syllabus implemented verbatim
  * Spec-Kit Plus lifecycle enforced
  * RAG answers sourced only from textbook content
  * Citations required for all technical claims
  * Free-tier tooling only

  Constraints:

  * Platform: Docusaurus v3+ on GitHub Pages
  * Backend: FastAPI
  * Vector DB: Qdrant Cloud (free tier)
  * Metadata DB: Neon Postgres
  * AI: Claude Code / Gemini free tier
  * Demo length: ≤ 90 seconds (auto-stop at 85s)

  Success criteria:

  * Book live on GitHub Pages
  * 100% syllabus coverage verified
  * RAG answers include clickable citations
  * Demo completes within time limit
  * Zero plagiarism detected

  ---

  ## Book Content Specification

  ### Course Identity

  * Course Name: Physical AI & Humanoid Robotics
  * Theme: Embodied intelligence and AI systems in the physical world
  * Goal: Control humanoid robots in simulated and real environments using AI

  ### Quarter Scope

  * Design, simulate, and deploy humanoid robots
  * Tools: ROS 2, Gazebo, Unity, NVIDIA Isaac
  * Emphasis: Physical laws, sensors, perception, action

  ### Modules (Mandatory)

  **Module 1: Robotic Nervous System (ROS 2)**

  * ROS 2 architecture
  * Nodes, topics, services, actions
  * Python control with rclpy
  * URDF for humanoid modeling

  **Module 2: Digital Twin (Gazebo & Unity)**

  * Physics simulation (gravity, collisions)
  * Environment modeling
  * Sensor simulation: LiDAR, depth cameras, IMUs
  * Human-robot interaction visualization

  **Module 3: AI-Robot Brain (NVIDIA Isaac)**

  * Isaac Sim
  * Synthetic data generation
  * Isaac ROS
  * VSLAM and navigation (Nav2)
  * Reinforcement learning basics

  **Module 4: Vision-Language-Action (VLA)**

  * Voice input using Whisper
  * LLM-based task planning
  * Natural language to ROS action pipelines

  **Capstone Project**

  * Simulated humanoid robot
  * Voice command input
  * Path planning and obstacle avoidance
  * Object detection and manipulation

  ### Learning Outcomes

  * Apply Physical AI and embodied intelligence concepts
  * Build and control robots using ROS 2
  * Simulate robots in Gazebo and Unity
  * Use NVIDIA Isaac for perception and navigation
  * Integrate LLMs for conversational robotics

  ### Weekly Structure

  * Weeks 1–2: Physical AI foundations and sensors
  * Weeks 3–5: ROS 2 fundamentals
  * Weeks 6–7: Simulation with Gazebo and Unity
  * Weeks 8–10: NVIDIA Isaac platform
  * Weeks 11–12: Humanoid locomotion and manipulation
  * Week 13: Conversational robotics

  ### Assessments

  * ROS 2 package project
  * Gazebo simulation project
  * Isaac perception pipeline
  * Capstone humanoid demo

  ### Hardware Requirements (Minimum)

  **Simulation Workstation**

  * GPU: NVIDIA RTX 4070 Ti (12GB) minimum
  * CPU: Intel i7 (13th gen) or Ryzen 9
  * RAM: 64 GB (32 GB minimum)
  * OS: Ubuntu 22.04 LTS

  **Edge AI Kit**

  * Jetson Orin Nano (8GB) or Orin NX (16GB)
  * Intel RealSense D435i or D455
  * USB microphone for voice input

  **Robot Options**

  * Proxy robot: Unitree Go2 or robotic arm
  * Mini humanoid: Unitree G1 or equivalent

  ### Cloud Alternative

  * GPU instances (AWS g5 or equivalent)
  * Local Jetson required for deployment
  * Cloud used for training only

  ---

  ---

  ## Product Features & User Experience

  ### Core Features (Mandatory)

  * User authentication using Better-Auth (signup/login)
  * Personalized chapter content based on learner background
  * One-click Urdu translation for every chapter
  * Auto-generated summaries, quizzes, and learning boosters

  ---

  ## Success Criteria

  * Clean UI, fast load times, mobile-friendly
  * Entire book readable in under 45 minutes
  * RAG answers accurate, cited, and grounded in book content
  * Personalization produces visibly different text
  * Urdu translation is clear, accurate, and fast
  * Full deployment completed:

    * Frontend: Vercel
    * Backend: Railway
    * Vector DB: Qdrant (free tier)
    * Database: Neon (free tier)

  ---

  ## Non-Goals

  * No unnecessary animations
  * No long or verbose chapters
  * No production-grade robotics code; educational focus only

  ---

  ## Architecture Principles

  * Frontend must be minimal and readable
  * Backend must be modular (FastAPI with services and routes)
  * Persistent data stored only in Neon and Qdrant
  * Required folder structure:

    * `/backend`
    * `/website`
    * `/rag`
    * `/agents`
  * Reusable agent skills required for bonus scoring

  ---

  ## User Stories (Priority Order)

  1. Learner reads the textbook smoothly
  2. Learner asks questions via chatbot
  3. Learner receives personalized content
  4. Learner translates content to Urdu
  5. Learner accesses summaries and quizzes
  6. Admin maintains clean architecture and deployment

  ---

  ## Operational Constraints

  * Must operate entirely on free tiers
  * Demo recording limited to 90 seconds
  * Must support low-end and mobile devices
  * Avoid heavy dependencies and unnecessary complexity

  ---

  ## Risks & Mitigation

  * RAG accuracy risk: use chunking and efficient embeddings
  * High token usage: phased implementation
  * User confusion: minimal UI and clear navigation
  * Backend instability: health checks and structured logging

  ---

  ## Definition of Done

  * All chapters accessible and readable
  * Chatbot functional with grounded responses
  * Authentication, personalization, and translation operational

response_text: |
  I've successfully updated the project constitution based on the specifications provided. The new constitution establishes six core principles derived from the provided specifications:
  
  1. Syllabus Fidelity - Following the syllabus exactly without omissions
  2. Deterministic, Grounded AI Output - No hallucinations, with citations to textbook
  3. Spec-First Development - Specification before coding
  4. Reproducibility - Documented and traceable results
  5. Educational Focus - Prioritizing learning value over production optimizations
  6. Free-Tier Compliance - Operating within free service limits
  
  The constitution also includes sections on:
  - Technology Stack Constraints (platforms, hardware, frameworks)
  - Development Workflow (implementation, testing, QA)
  - Success Criteria (completeness, UX, deployment)
  - Governance guidelines
  
  The document is now fully customized for the Physical AI & Humanoid Robotics Textbook project and includes an initial version (1.0.0) with the required information.
---
