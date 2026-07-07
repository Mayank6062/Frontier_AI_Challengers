const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', 'src', 'frontend', 'src');
const EXCLUDE = [
  'src/shared/theme',
  'src/shared/theme/tokens.css',
  'src/shared/theme/tokens.ts'
];
const HEX_RE = /#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})/;
const PX_RE = /\b\d+px\b/;

let violations = [];

function walk(dir) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const full = path.join(dir, file);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      // skip theme token folder
      const rel = path.relative(path.join(__dirname, '..', 'src', 'frontend'), full).replace(/\\/g, '/');
      if (EXCLUDE.some(e => rel.startsWith(e))) continue;
      walk(full);
    } else if (/\.(ts|tsx|js|jsx|css)$/.test(full)) {
      const rel = path.relative(path.join(__dirname, '..', 'src', 'frontend'), full).replace(/\\/g, '/');
      if (EXCLUDE.some(e => rel === e || rel.startsWith(e + '/'))) return;
      const content = fs.readFileSync(full, 'utf8');
      const lines = content.split('\n');
      lines.forEach((ln, idx) => {
        if (HEX_RE.test(ln) || PX_RE.test(ln)) {
          violations.push({ file: full, line: idx + 1, text: ln.trim() });
        }
      });
    }
  }
}

walk(ROOT);

if (violations.length) {
  console.error('Hardcoded value violations found:');
  violations.slice(0, 50).forEach(v => console.error(`${v.file}:${v.line} -> ${v.text}`));
  process.exit(2);
} else {
  console.log('No hardcoded hex/px violations found.');
}
