# edit-banana: Codex execution

Image to editable DrawIO using the user-selected configured engine. Review local models and external-provider settings; validate editable cells and required OCR text, then visually compare.

1. Read `${CODEX_PACK_ROOT}/native/OPTIONAL-ADAPTERS.md`, the **edit-banana** section and shared execution/setup contract. Only read the relevant section plus the shared boundaries.
2. Preserve domain methodology from `library/skills/edit-banana/SKILL.md` and its explicitly needed references through `catalog.py --read-reference`. Historical tool calls, provider defaults and `.source` files are not executable.
3. Select the correct reviewed operation, check its optional dependencies without importing/downloading engines, then prepare a task-specific JSON request in the explicit workspace.
4. Run the installed adapter using the selected interpreter and workspace. Do not stop after showing a catalog result or command for the user to run. If a dependency is absent, offer the exact isolated setup and obtain installation/data-sharing approval; do not install every engine or mislabel the code as unfinished.
5. Verify actual output artifacts, inspect domain quality and report any remaining manual review. Creation is separate from upload/publication. Do not claim unavailable engine inference was live-tested.

```text
python "${CODEX_PACK_ROOT}/scripts/optional_adapter.py" check <operation>
python "${CODEX_PACK_ROOT}/scripts/optional_adapter.py" run --workspace "${CODEX_WORKSPACE}" --request "job.json"
```
