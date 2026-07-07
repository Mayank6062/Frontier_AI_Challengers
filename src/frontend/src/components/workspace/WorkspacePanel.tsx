import React from 'react';
import { useWorkspace } from '../../hooks/useWorkspace';
import { Tabs } from '../shared/Tabs';
import styles from './WorkspacePanel.module.css';

/**
 * WorkspacePanel - Displays engagement artifacts and workspace views
 */
export const WorkspacePanel: React.FC = () => {
  const { activeTab, sections } = useWorkspace();

  const tabs = [
    {
      id: 'requirements',
      label: 'Requirements',
      content: (
        <div className={styles.section}>
          <h3>Requirements</h3>
          <p>
            {sections.requirements?.status === 'loading'
              ? 'Loading...'
              : (String(sections.requirements?.content) || 'No requirements available')}
          </p>
        </div>
      ),
    },
    {
      id: 'architecture',
      label: 'Architecture',
      content: (
        <div className={styles.section}>
          <h3>Architecture Design</h3>
          <p>
            {sections.architecture?.status === 'loading'
              ? 'Loading...'
              : (String(sections.architecture?.content) || 'No architecture available')}
          </p>
        </div>
      ),
    },
    {
      id: 'validation',
      label: 'Validation',
      content: (
        <div className={styles.section}>
          <h3>Validation Results</h3>
          <p>
            {sections.validation?.status === 'loading'
              ? 'Loading...'
              : (String(sections.validation?.content) || 'No validation data available')}
          </p>
        </div>
      ),
    },
    {
      id: 'review',
      label: 'Review',
      content: (
        <div className={styles.section}>
          <h3>Review Gate</h3>
          <p>
            {sections.review?.status === 'loading'
              ? 'Loading...'
              : (String(sections.review?.content) || 'No review data available')}
          </p>
        </div>
      ),
    },
    {
      id: 'outputs',
      label: 'Outputs',
      content: (
        <div className={styles.section}>
          <h3>Generated Outputs</h3>
          <p>
            {sections.outputs?.status === 'loading'
              ? 'Loading...'
              : (String(sections.outputs?.content) || 'No outputs generated')}
          </p>
        </div>
      ),
    },
  ];

  return (
    <div className={styles.panel}>
      <Tabs
        tabs={tabs}
        defaultTab={activeTab || 'requirements'}
      />
    </div>
  );
};

export default WorkspacePanel;
