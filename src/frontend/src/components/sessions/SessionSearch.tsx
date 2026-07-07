import React, { useState } from 'react';
import { Input } from '../shared/Input';
import styles from './SessionSearch.module.css';

interface SessionSearchProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

/**
 * SessionSearch - Search sessions by name
 */
export const SessionSearch: React.FC<SessionSearchProps> = ({
  onSearch,
  placeholder = 'Search sessions...',
}) => {
  const [query, setQuery] = useState('');

  const handleChange = (value: string) => {
    setQuery(value);
    onSearch(value);
  };

  return (
    <div className={styles.container}>
      <Input
        type="text"
        placeholder={placeholder}
        value={query}
        onChange={(e) => handleChange(e.target.value)}
        className={styles.input}
      />
    </div>
  );
};

export default SessionSearch;
