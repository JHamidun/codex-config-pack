# Codex configuration pack development

- This repository is a portable derivative of a public configuration pack, not a personal home-directory backup.
- Keep all source inputs read-only. Never run upstream installers, hooks, or scripts against their original defaults.
- Do not import personal configuration, credentials, transcripts, memory, machine paths, or session files.
- Adapt capabilities, not product names. Keep unsupported runtime dependencies explicit.
- Do not enable external services, paid providers, broad permissions, or background processes during installation.
- Only delegate when the user or applicable instructions explicitly request delegation.
- Validate Python syntax, rebuild the bundle, validate its manifest, then run tests.
- Keep installers additive, idempotent, symlink-safe, and reversible without deleting user changes.
- Do not publish, push, or deploy without the owner's explicit request.
