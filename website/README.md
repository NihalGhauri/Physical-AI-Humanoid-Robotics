# Physical AI & Humanoid Robotics Textbook Website

This Docusaurus-based website hosts the comprehensive textbook on Physical AI & Humanoid Robotics. The content covers ROS 2, simulation environments, AI-powered robotics systems, and Vision-Language-Action interfaces.

## Installation

```bash
npm install
```

## Local Development

```bash
npm start
```

This command starts a local development server and opens the website in your default browser with live reload functionality.

## Build

```bash
npm run build
```

This command generates static content in the `build` directory, ready for deployment to any static hosting service.

## Deployment

The site is designed for deployment to GitHub Pages. The build output in the `build` directory can be served from the `gh-pages` branch.

## Directory Structure

- `/docs`: Contains all textbook content organized by modules
- `/blog`: Contains additional articles and updates related to the textbook
- `/src`: Contains custom React components and pages
  - `/src/components`: Custom reusable components (e.g., EducationalBox)
  - `/src/css`: Custom styling for enhanced UI/UX
  - `/src/pages`: Custom page layouts
- `/static`: Contains static assets like images and favicons

## Content Organization

The textbook content is organized into modules:

1. **Module 1**: Robotic Nervous System (ROS 2)
2. **Module 2**: Digital Twin (Gazebo & Unity)
3. **Module 3**: AI-Robot Brain (NVIDIA Isaac)
4. **Module 4**: Vision-Language-Action (VLA)
5. **Capstone Project**: Complete humanoid robot implementation

## UI/UX Improvements

The website includes several UI/UX enhancements for better educational experience:

- **Custom Educational Components**: 
  - Learning Objectives boxes with clear visual indicators
  - Knowledge Check (quiz) sections with distinct styling
  - Module Summary sections for reinforcement
  - Note, Warning, and Example boxes for special content

- **Enhanced Homepage**:
  - Interactive module cards with hover effects
  - Clear call-to-action buttons
  - Visual icons for each module
  - Improved typography and spacing

- **Improved Readability**:
  - Better typography hierarchy with proper heading sizes
  - Enhanced code block styling with syntax highlighting
  - Improved table formatting with hover effects
  - Better spacing and padding throughout

- **Responsive Design**:
  - Mobile-friendly layout adjustments
  - Proper font sizing for different screen sizes
  - Touch-friendly interactive elements

- **Accessibility Improvements**:
  - Proper focus states for keyboard navigation
  - Sufficient color contrast
  - Semantic HTML structure

## Custom Components

- **EducationalBox Component**: Reusable component for educational elements like objectives, quizzes, and summaries
- **Enhanced CSS styling**: Custom styles in `/src/css/custom.css` for textbook-specific visual design
- **Custom homepage layout**: Enhanced in `/src/pages/index.tsx` with interactive elements
- **Module organization**: Improved structure in `/sidebars.ts`

## Internationalization

The website supports English and Urdu (Ur) for broader accessibility. Content translation is handled through Docusaurus i18n system.