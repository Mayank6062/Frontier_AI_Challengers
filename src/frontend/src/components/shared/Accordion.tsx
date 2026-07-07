import React, { useState } from 'react';
import styles from './Accordion.module.css';

export interface AccordionItem {
  id: string;
  title: string;
  content: React.ReactNode;
}

interface AccordionProps {
  items: AccordionItem[];
  allowMultiple?: boolean;
}

/**
 * Accordion - Expandable content sections
 */
export const Accordion: React.FC<AccordionProps> = ({
  items,
  allowMultiple = false,
}) => {
  const [expandedIds, setExpandedIds] = useState<Set<string>>(
    new Set()
  );

  const toggle = (id: string) => {
    const newExpanded = new Set(expandedIds);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      if (!allowMultiple) {
        newExpanded.clear();
      }
      newExpanded.add(id);
    }
    setExpandedIds(newExpanded);
  };

  return (
    <div className={styles.container}>
      {items.map((item) => (
        <div key={item.id} className={styles.item}>
          <button
            className={styles.trigger}
            onClick={() => toggle(item.id)}
            aria-expanded={expandedIds.has(item.id)}
          >
            <span className={styles.title}>{item.title}</span>
            <span
              className={`${styles.icon} ${
                expandedIds.has(item.id) ? styles.expanded : ''
              }`}
            >
              ▼
            </span>
          </button>

          {expandedIds.has(item.id) && (
            <div className={styles.content}>{item.content}</div>
          )}
        </div>
      ))}
    </div>
  );
};

export default Accordion;
