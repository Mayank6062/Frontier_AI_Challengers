import React from 'react';
import styles from './ThreePanelLayout.module.css';

interface ThreePanelLayoutProps {
  leftPanel: React.ReactNode;
  centerPanel: React.ReactNode;
  rightPanel: React.ReactNode;
  leftWidth?: number; // percentage
  rightWidth?: number; // percentage
}

/**
 * ThreePanelLayout - Resizable three-panel layout for workspace
 */
export const ThreePanelLayout: React.FC<ThreePanelLayoutProps> = ({
  leftPanel,
  centerPanel,
  rightPanel,
  leftWidth = 20,
  rightWidth = 30,
}) => {
  return (
    <div className={styles.container}>
      <div
        className={styles.leftPanel}
        style={{ width: `${leftWidth}%` }}
      >
        {leftPanel}
      </div>

      <div
        className={styles.centerPanel}
        style={{ width: `${100 - leftWidth - rightWidth}%` }}
      >
        {centerPanel}
      </div>

      <div
        className={styles.rightPanel}
        style={{ width: `${rightWidth}%` }}
      >
        {rightPanel}
      </div>
    </div>
  );
};

export default ThreePanelLayout;
