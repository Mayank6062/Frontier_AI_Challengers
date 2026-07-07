import React from "react";

export const Modal: React.FC<{ open: boolean; onClose?: () => void; children?: React.ReactNode }> = ({ open, onClose, children }) => {
  if (!open) return null;

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === "Escape" && onClose) onClose();
  };

  return (
    <div
      role="dialog"
      aria-label="Dialog"
      aria-modal="true"
      onKeyDown={onKey}
      tabIndex={-1}
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--og2-backdrop, rgba(0,0,0,0.4))",
      }}
    >
      <div style={{ background: 'var(--og2-semantic-bg-primary-light)', padding: 'var(--og2-components-spacing-space-5)', borderRadius: 'var(--og2-components-radii-radius-2)' }}>
        {children}
      </div>
    </div>
  );
};

export default Modal;
