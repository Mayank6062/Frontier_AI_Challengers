/**
 * Diagram Renderer Utility
 * Handles Mermaid and Graphviz diagram rendering
 */

export interface DiagramConfig {
  theme?: 'light' | 'dark';
  scale?: number;
  width?: number;
  height?: number;
}

/**
 * Render Mermaid diagram
 */
export const renderMermaidDiagram = async (
  content: string,
  config: DiagramConfig = {}
): Promise<string> => {
  try {
    // Import mermaid dynamically to avoid bundle size issues
    // @ts-expect-error - mermaid is optional dependency
    const { default: mermaid } = await import('mermaid');

    const id = `mermaid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const theme = config.theme || 'light';

    mermaid.initialize({ startOnLoad: false, theme });

    const { svg } = await mermaid.render(id, content);
    return svg;
  } catch (error) {
    console.error('Failed to render Mermaid diagram:', error);
    return '<div class="error">Failed to render diagram</div>';
  }
};

/**
 * Render Graphviz diagram (via Mermaid's graphviz support or external service)
 */
export const renderGraphvizDiagram = async (
  dotContent: string,
  config: DiagramConfig = {}
): Promise<string> => {
  try {
    // For now, we'll use a placeholder
    // In production, this would use a Graphviz-to-SVG service
    const svgWrapper = document.createElement('div');
    svgWrapper.className = 'graphviz-diagram';
    svgWrapper.style.width = `${config.width || 400}px`;
    svgWrapper.style.height = `${config.height || 300}px`;
    svgWrapper.innerHTML = '<p>Graphviz rendering requires server support</p>';

    return svgWrapper.outerHTML;
  } catch (error) {
    console.error('Failed to render Graphviz diagram:', error);
    return '<div class="error">Failed to render diagram</div>';
  }
};

/**
 * Detect diagram type from content
 */
export const detectDiagramType = (content: string): 'mermaid' | 'graphviz' | 'unknown' => {
  if (content.trim().startsWith('graph ') || content.trim().startsWith('digraph ')) {
    return 'graphviz';
  }

  const mermaidKeywords = [
    'graph ',
    'flowchart ',
    'sequence ',
    'state ',
    'class ',
    'er ',
    'journey ',
    'requirement ',
  ];
  if (mermaidKeywords.some((keyword) => content.includes(keyword))) {
    return 'mermaid';
  }

  return 'unknown';
};

/**
 * Render diagram based on detected type
 */
export const renderDiagram = async (
  content: string,
  config: DiagramConfig = {}
): Promise<string> => {
  const type = detectDiagramType(content);

  switch (type) {
    case 'mermaid':
      return renderMermaidDiagram(content, config);
    case 'graphviz':
      return renderGraphvizDiagram(content, config);
    default:
      return '<div class="error">Unknown diagram format</div>';
  }
};

/**
 * Sanitize diagram content
 */
export const sanitizeDiagramContent = (content: string): string => {
  // Remove potentially dangerous scripts or injections
  let sanitized = content;

  // Remove script tags
  sanitized = sanitized.replace(/<script[^>]*>.*?<\/script>/gs, '');

  // Remove event handlers
  sanitized = sanitized.replace(/on\w+\s*=\s*["'][^"']*["']/gi, '');

  // Remove data URIs with potential issues
  sanitized = sanitized.replace(/data:text\/html/gi, '');

  return sanitized;
};
