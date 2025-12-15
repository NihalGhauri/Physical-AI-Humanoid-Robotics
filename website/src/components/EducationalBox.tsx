import React from 'react';
import clsx from 'clsx';
import styles from './EducationalBox.module.css';

type EducationalBoxProps = {
  children: React.ReactNode;
  type?: 'objective' | 'quiz' | 'summary' | 'note' | 'example' | 'warning';
  title?: string;
};

const EducationalBox: React.FC<EducationalBoxProps> = ({ 
  children, 
  type = 'note',
  title 
}) => {
  const cssClass = clsx(
    styles.box,
    styles[`box--${type}`]
  );

  const defaultTitles = {
    objective: 'Learning Objectives',
    quiz: 'Knowledge Check',
    summary: 'Module Summary',
    note: 'Note',
    example: 'Example',
    warning: 'Important'
  };

  const displayTitle = title || defaultTitles[type] || 'Note';

  return (
    <div className={cssClass}>
      <div className={styles.header}>
        <h3 className={styles.title}>{displayTitle}</h3>
      </div>
      <div className={styles.content}>
        {children}
      </div>
    </div>
  );
};

export default EducationalBox;