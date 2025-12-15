<!--
Sync Impact Report:
- Version change: N/A -> 1.0.0
- Added sections: Core Principles (6), Technology Stack, Development Workflow, Success Criteria
- Removed sections: None (new constitution)
- Templates requiring updates: All templates checked and compatible
- Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### Syllabus Fidelity
All course content and implementations MUST follow the specified syllabus exactly without omissions or reinterpretations. Modifications to the curriculum require explicit approval and documentation.

### Deterministic, Grounded AI Output
AI-generated content MUST be deterministic and grounded in the textbook material with no hallucinations. All responses must trace back to specific content in the textbook with citations.

### Spec-First Development
All features and implementations MUST be fully specified before any coding begins. Specifications must include user stories, requirements, success criteria, and technical architecture.

### Reproducibility
All experiments, simulations, and demonstrations MUST be reproducible with documented steps and configurations. Claims and results must be traceable to specific code, data, or experiments.

### Educational Focus
All code and implementations MUST maintain an educational focus rather than production-grade robotics code. Clarity and learning value take precedence over performance optimizations.

### Free-Tier Compliance
All technology choices and implementations MUST operate within free-tier service limitations. No paid services may be required for basic functionality and deployment.

## Technology Stack Constraints

### Platform & Framework Requirements
- Frontend: Docusaurus v3+ deployed on GitHub Pages
- Backend: FastAPI for API services
- Vector Database: Qdrant Cloud (free tier only)
- Metadata Database: Neon Postgres (free tier only)
- AI Services: Claude Code / Gemini free tier
- Build & Deployment: Vercel (frontend), Railway (backend)

### Hardware Requirements
- Minimum GPU: NVIDIA RTX 4070 Ti (12GB) for simulation workstation
- Minimum CPU: Intel i7 (13th gen) or Ryzen 9
- Minimum RAM: 64 GB (32 GB absolute minimum)
- OS: Ubuntu 22.04 LTS preferred
- Edge AI: Jetson Orin Nano (8GB) or Orin NX (16GB)

### Simulation Frameworks
- ROS 2 for robotic nervous system
- Gazebo and Unity for digital twin simulation
- NVIDIA Isaac for AI-robot brain
- VSLAM and Nav2 for navigation

## Development Workflow

### Feature Implementation
- Each feature MUST begin with a detailed specification document
- Specifications MUST include user stories with clear acceptance criteria
- Development follows the Spec-Kit Plus lifecycle: spec → plan → tasks → implementation
- All code changes MUST pass through pull request review process

### Testing Protocol
- Unit tests for all core functionality
- Integration tests for module interactions
- End-to-end tests for complete user journeys
- Automated checks for syllabus coverage completeness

### Quality Assurance
- Code reviews MUST validate compliance with all principles
- All technical claims REQUIRE citations to textbook content
- Performance benchmarks MUST meet specified constraints
- Demo recordings MUST complete within 90-second limit

## Success Criteria

### Completeness Requirements
- 100% syllabus coverage VERIFIED through automated checks
- All chapters accessible and readable in under 45 minutes total
- Complete RAG functionality with grounded, cited responses

### User Experience Standards
- Fast load times and mobile-friendly interface
- Clear navigation and minimal cognitive load
- Accurate Urdu translations for all content
- Functional chatbot with reliable responses

### Deployment Compliance
- Frontend deployed successfully on GitHub Pages
- Backend operational on Railway
- Vector DB and metadata DB connected and functional
- All constraints operate within free-tier limits

## Governance

This constitution governs all development activities for the Physical AI & Humanoid Robotics Textbook project. All contributors MUST abide by these principles, with compliance verified during code reviews and PR merges. Amendments to this constitution require explicit project leadership approval and must be documented in a version change. All development workflows, code reviews, and quality gates must reference this document to ensure consistent application of project principles.

**Version**: 1.0.0 | **Ratified**: 2025-01-14 | **Last Amended**: 2025-01-14
