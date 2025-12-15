# Physical AI & Humanoid Robotics Textbook

An interactive educational platform featuring a comprehensive textbook on Physical AI and Humanoid Robotics with RAG-powered question answering, personalization, and Urdu translation.

## Overview

This project implements a web-based textbook for Physical AI & Humanoid Robotics following the Spec-Kit Plus methodology. The platform includes:

- Complete curriculum covering ROS 2, Gazebo, Unity, NVIDIA Isaac, and VLA systems
- Interactive RAG (Retrieval Augmented Generation) chatbot for question answering
- Personalized content based on learner background
- One-click Urdu translation for all content
- Auto-generated summaries and quizzes
- Simulation framework integration with ROS 2, Gazebo, and NVIDIA Isaac

## Architecture

The system is structured as a multi-service application:

- **Backend**: FastAPI application handling business logic and APIs
- **Website**: Docusaurus-based frontend for textbook consumption
- **RAG**: Retrieval Augmented Generation services for question answering
- **Agents**: Reusable AI skills and agent implementations with modular design

## Technologies

- **Frontend**: Docusaurus v3+, deployed on GitHub Pages
- **Backend**: FastAPI
- **Database**: Neon Postgres (metadata), Qdrant Cloud (embeddings)
- **Authentication**: Better-Auth
- **Simulation**: ROS 2, Gazebo, Unity, NVIDIA Isaac
- **AI/ML**: RAG with vector embeddings for question answering
- **Translation**: Urdu translation service integration

## Getting Started

For development setup instructions, see the [Quickstart Guide](specs/master/quickstart.md).

## Project Status

All features are planned according to the [tasks](specs/master/tasks.md) with implementation organized by user story priority:

1. Textbook content access and navigation
2. Question answering via RAG
3. Personalized content
4. Urdu translation
5. Summaries and quizzes
6. Operational concerns

## Contributing

This project follows the Spec-Driven Development methodology with all changes guided by specifications in the `/specs` directory. New features or changes should begin with a specification document before implementation.