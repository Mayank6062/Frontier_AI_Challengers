import React, { useEffect, useRef, useState } from "react";

export const CommandPalette: React.FC<{ commands: { id: string; label: string }[] }> = ({ commands }) => {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((v) => !v);
        setTimeout(() => inputRef.current?.focus(), 0);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const filtered = commands.filter((c) => c.label.toLowerCase().includes(query.toLowerCase()));

  useEffect(() => setIndex(0), [query]);

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") setIndex((i) => Math.min(filtered.length - 1, i + 1));
    if (e.key === "ArrowUp") setIndex((i) => Math.max(0, i - 1));
    if (e.key === "Enter") {
      const cmd = filtered[index];
      if (cmd) {
        // emit custom event
        window.dispatchEvent(new CustomEvent("og2:command", { detail: cmd }));
        setOpen(false);
      }
    }
    if (e.key === "Escape") setOpen(false);
  };

  if (!open) return null;

  return (
    <div role="dialog" aria-modal="true" style={{ position: "fixed", inset: 0, display: "flex", alignItems: "flex-start", justifyContent: "center", paddingTop: "10vh" }}>
      <div style={{ width: '90%', background: 'var(--og2-semantic-bg-primary-light)', borderRadius: 'var(--og2-components-radii-radius-2)', boxShadow: 'var(--og2-components-shadow-elevation-2)', overflow: 'hidden' }}>
        <div style={{ padding: 'var(--og2-components-spacing-space-3)' }}>
          <input ref={inputRef} value={query} onChange={(e) => setQuery(e.target.value)} onKeyDown={onKey} aria-label="Command Palette" style={{ width: '100%', padding: 'var(--og2-components-spacing-space-2)', fontSize: 'var(--og2-components-typography-size-md)' }} />
        </div>
        <ul role="listbox" aria-activedescendant={filtered[index]?.id} style={{ maxHeight: 320, overflow: "auto", margin: 0, padding: 0, listStyle: "none" }}>
          {filtered.map((c, i) => (
            <li key={c.id} id={c.id} role="option" aria-selected={i === index} style={{ padding: "var(--og2-components-spacing-space-2)", background: i === index ? "var(--og2-components-shadow-elevation-1)" : "transparent" }}>
              {c.label}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default CommandPalette;
