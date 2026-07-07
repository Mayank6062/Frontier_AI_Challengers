/**
 * Markdown Renderer Utility
 * Safe markdown rendering with sanitization
 */

/**
 * Basic markdown to HTML conversion with safety checks
 * Does NOT execute scripts or support raw HTML
 */
export const renderMarkdown = (markdown: string): string => {
  let html = markdown;

  // Headers
  html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');

  // Italic
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/_(.*?)_/g, '<em>$1</em>');

  // Code blocks
  html = html.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');

  // Inline code
  html = html.replace(/`(.*?)`/g, '<code>$1</code>');

  // Links
  html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

  // Unordered lists
  html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*?<\/li>)/s, '<ul>$1</ul>');

  // Ordered lists
  html = html.replace(/^\d+\. (.*?)$/gm, '<li>$1</li>');

  // Line breaks
  html = html.replace(/\n\n/g, '</p><p>');
  html = html.replace(/\n/g, '<br>');

  // Wrap in paragraphs
  html = html.replace(/^(?!<)([^<].*)$/gm, '<p>$1</p>');

  return html;
};

/**
 * Escape HTML special characters
 */
export const escapeHtml = (text: string): string => {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
};

/**
 * Extract plain text from markdown (strips formatting)
 */
export const extractPlainText = (markdown: string): string => {
  let text = markdown;

  // Remove headers
  text = text.replace(/^#+\s+/gm, '');

  // Remove bold/italic
  text = text.replace(/[*_]/g, '');

  // Remove code blocks
  text = text.replace(/```[\s\S]*?```/g, '');

  // Remove inline code
  text = text.replace(/`[^`]*`/g, '');

  // Remove links
  text = text.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1');

  // Remove list markers
  text = text.replace(/^[*\-+]\s+/gm, '');
  text = text.replace(/^\d+\.\s+/gm, '');

  return text.trim();
};

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text: string, maxLength: number, suffix = '...'): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - suffix.length) + suffix;
};

/**
 * Highlight search terms in text
 */
export const highlightSearchTerms = (text: string, terms: string[]): string => {
  if (!terms || terms.length === 0) return escapeHtml(text);

  let result = escapeHtml(text);
  terms.forEach((term) => {
    const regex = new RegExp(`(${escapeRegex(term)})`, 'gi');
    result = result.replace(regex, '<mark>$1</mark>');
  });

  return result;
};

/**
 * Escape regex special characters
 */
const escapeRegex = (str: string): string => {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
};
