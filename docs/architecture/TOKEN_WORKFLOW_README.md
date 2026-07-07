Token workflow
=================

This folder contains the canonical tokens (`config/styles/tokens.yaml`), a JSON Schema (`tokens.schema.json`), and build scripts to generate theme CSS files used by the frontend.

How it works:
- `.tools/token_build.py` validates `tokens.yaml` against the schema and emits `config/styles/build/tokens.<theme>.css` and `diagram-tokens.yaml`.
- `src/backend/output_generation/portal/token_embedder.py` reads the built CSS and inlines it into portal HTML at build time.
- `.tools/generate_tokens_ts.py` generates `src/frontend/src/shared/theme/tokens.ts` for TypeScript consumers.

Developer commands:
```powershell
python .tools/token_build.py
python .tools/generate_tokens_ts.py
pytest -q
```
