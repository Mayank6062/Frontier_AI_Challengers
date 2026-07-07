import React from 'react';

interface CommandPaletteProps {
  isOpen?: boolean;
  onClose?: () => void;
  commands?: Array<{ label: string; action: () => void }>;
}

/**
 * CommandPalette - Command palette component
 */
export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  commands = [],
}) => {
  if (!isOpen) return null;

  return (
    <div className="command-palette">
      <div className="commands">
        {commands.map((cmd) => (
          <button key={cmd.label} onClick={cmd.action}>
            {cmd.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CommandPalette;
