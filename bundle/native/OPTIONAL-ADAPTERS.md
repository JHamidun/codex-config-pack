# Optional engine adapters

These are executable Codex-owned adapters, not renamed historical scripts. Engines,
weights and accounts are user-side prerequisites, not missing adapter implementation.
Do not install all of them. Select the requested operation and check only its needs.

## Execution

The agent writes a UTF-8 JSON request in the selected workspace, then executes:

```text
python "${CODEX_PACK_ROOT}/scripts/optional_adapter.py" check <operation>
python "${CODEX_PACK_ROOT}/scripts/optional_adapter.py" run --workspace "<project>" --request "job.json"
```

Use the interpreter of the selected isolated engine environment when applicable.
`check` inspects module availability, without importing engines, connecting, installing
packages or downloading weights. It is not a successful engine test. The agent should
resolve prerequisites and execute, not tell the user to manually reproduce a CLI.

Every request requires `operation` and a **new** workspace-relative `output` directory.
Inputs are explicit workspace-relative paths with forward slashes. Existing outputs,
protected source trees and links/junctions are refused. Explicit engine executable,
model and installation paths may be outside the workspace, but not in protected
source trees. Resolve package-manager launcher links to their actual executable.
Only trusted, user-selected engines are permitted; this wrapper is not their sandbox.

Output is staged and published only on successful validation. Failed local runs do
not replace existing work. A remote submission may already exist after a connection
failure: **never blindly retry a submit**. Errors do not print provider payloads or
document contents. For diagnosis run the engine's own smoke test on synthetic input.

No operation publishes/uploads a sticker pack, modifies an existing drawing, loads
the author's credentials, or silently changes provider. Publishing uses an available
authorized connector separately and requires a destination readback.

## Implemented operations and request fields

### Music: `ace-submit`, `ace-fetch`

Requires a separately running [official ACE-Step REST server](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md).
This replaces the fragile Gradio positional-call wrapper. It does not start a server.

```json
{"operation":"ace-submit","endpoint":"http://127.0.0.1:8001","output":"music-submit","parameters":{"prompt":"Instrumental acoustic guitar","lyrics":"[Instrumental]","audio_duration":30,"thinking":false,"batch_size":1}}
```

Allowed parameters: `prompt`, `lyrics`, `thinking`, `vocal_language`, `sample_query`,
`use_format`, `model`, `bpm`, `key_scale`, `time_signature`, `audio_duration` (10–600),
`inference_steps` (1–200), `seed`, `use_random_seed`, `batch_size` (1–8). Choose model
from the actual server, not an old recipe. Output format is WAV for content validation.

```json
{"operation":"ace-fetch","input":"music-submit/task.json","output":"music-result"}
```

Fetch never resubmits. Pending status means wait, then fetch into a new output directory.
Completed WAV files are checked by signature, decoder and duration. For an explicitly
authorized remote server set `allow_remote:true` on both operations; HTTPS is mandatory.
Optional `ACESTEP_API_KEY` is read only from the process environment, never JSON. No
redirect, proxy or cross-origin audio download is followed. No provider cancellation
endpoint is assumed; stopping local polling does not cancel a server job.

### CAD: `cad-inspect`, `cad-create`

Requires Windows, `pywin32`, and a running AutoCAD-compatible COM application.
`cad-inspect` reports connection/document count only. It never launches an application.

```json
{"operation":"cad-create","output":"drawing-result","units":4,"entities":[{"type":"line","start":[0,0,0],"end":[100,0,0]},{"type":"circle","center":[50,50,0],"radius":20}]}
```

Creates/saves/closes **only a new document**. Existing drawings are not modified.
`units` is the application's INSUNITS enumeration, explicitly selected (4 = millimeters
in AutoCAD). Optional `progid` selects AutoCAD/GstarCAD/ZWCAD/BricsCAD/nanoCAD.
Points have 3 finite coordinates. Types:

- `line`: `start`, `end`.
- `circle`: `center`, positive `radius`.
- `arc`: `center`, `radius`, `start_angle`, `end_angle` in radians.
- `text`: `text`, `point`, positive `height`.
- `box`: `center`, positive `length`, `width`, `height`.
- `cylinder`: `center`, positive `radius`, `height`.
- `dimension`: `start`, `end`, `location`, optional entity-level `scale`.

Entity handles/count are read back and DWG existence checked. Inspect and measure in
the actual application before delivery; file existence does not establish engineering
correctness. Advanced CAD work uses the native model plus reviewed project code based
on preserved methodology, never imported historical `.source` or arbitrary SendCommand.

### Diagram OCR/segmentation: `edit-banana`

Requires a configured [Edit-Banana installation](https://github.com/BIT-DataLab/Edit-Banana),
its interpreter, local SAM3/OCR models and any explicitly chosen provider authorization.

```json
{"operation":"edit-banana","input":"diagram.png","output":"diagram-result","engine":"<installed-engine-directory>","python":"<engine-python-executable>","engine_config_reviewed":true,"require_text":true}
```

Review engine config, local checkpoints, caching and data-sharing before setting the
acknowledgment. The adapter calls `main.py -i <absolute-input> -o <isolated-output>`;
it does not copy input into the engine tree or trust exit code alone. Editable mxCells
and an OCR text layer are required. `require_text:false` is only for a genuinely
text-free diagram. Inspect the rendered result against the original. This engine may
use services configured by its owner; the pack does not enable or authorize them.

### Enhancement: `enhance`, `upscale`

`enhance` requires Pillow and performs deterministic, non-generative transformations:

```json
{"operation":"enhance","input":"photo.png","output":"enhanced","scale":2,"contrast":1.1,"brightness":1,"color":1,"sharpness":1.2,"denoise":false}
```

Scale 1–4, enhancement factors 0–3, at most 16 million output pixels. EXIF orientation
is applied and metadata stripped; alpha is retained. `denoise` is a 3×3 median filter,
not AI restoration. For exact AI upscaling use `upscale`, `executable` = a trusted
[Real-ESRGAN NCNN](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) executable,
`models` = existing model directory, `model` = its basename, `scale` = integer 2–4.
Both `.bin`/`.param` must exist. No downloads or guessed model selection occur.
For creative retouching use native image tools, not a falsely labeled deterministic filter.

### OCR restoration: `ocr-extract`, `ocr-restore`

`ocr-extract` uses an explicit installed [Tesseract](https://github.com/tesseract-ocr/tesseract)
executable with `input`, `language` (default `eng`), `psm` (3–13). It emits both text
and TSV coordinates/confidence; language data belongs to the user's engine installation.

```json
{"operation":"ocr-restore","input":"scan-text.txt","output":"restored","corrections":[{"old":"known OCR error","new":"verified correction","count":1}]}
```

Safe cleanup removes control/BOM/soft-hyphen artifacts. No guessed dictionary changes,
historical spelling modernization or factual rewrites are applied automatically.
Use preserved tiered restoration methodology: inspect scan/block coordinates, fix
only evidenced corruption, preserve headings/tables/footnotes, mark illegible content.
Codex can reason over difficult blocks with available native vision, then apply explicit
occurrence-count-checked corrections. `review.json` never claims factual verification.

### Local privacy: `privacy-redact`, `privacy-restore`

Requires the [official OpenAI Privacy Filter](https://github.com/openai/privacy-filter)
installed in an isolated interpreter and an **existing explicit checkpoint directory**.
No default checkpoint/model download is used. CPU is the default; set `device:"cuda"`
only on suitable hardware. Windows uses the non-Triton fallback unless explicitly set.

```json
{"operation":"privacy-redact","input":"document.txt","output":"redaction","checkpoint":"<local-model-directory>","device":"cpu"}
```

Read `redacted.txt` **locally** and review missed entities before any authorized upload.
Model detection is probabilistic, especially outside its evaluated language/domain.
`private/restore-map.json` contains real private data. It has a local ignore file and
restrictive POSIX mode, but Windows requires appropriate user ACLs; neither is encryption.
Never upload the directory, restore map, original input, or restored output by default.
Repeated identical entities keep the same token. Overlapping/mismatched offsets or a
tokenizer round-trip change fail closed instead of silently leaking unredacted spans.

```json
{"operation":"privacy-restore","input":"model-answer.txt","map":"redaction/private/restore-map.json","output":"local-restored"}
```

Restore uses no model; replacements happen in one pass, with unknown-token detection.
Keep placeholders exact when asking a model to transform already-reviewed redacted text.

### Slack GIF: `gif`

```json
{"operation":"gif","frames":["frame1.png","frame2.png"],"output":"slack-gif","fps":10,"emoji":true}
```

Pillow builds a looping GIF, preserving binary transparency and verifying animation.
Emoji preset: 128×128, at most 64 KiB; message preset: 480×480, at most 2 MiB.
These are conservative pack budgets, not a promise of every Slack workspace limit.
At most 100 frames/5 seconds; the adapter refuses an oversized file rather than silently
truncating frames. Compose movement/phase/easing in Codex using native tools or reviewed
project code; preserved templates are reference only. Check actual workspace acceptance
before upload. Do not claim that an output file has already been uploaded.

### Stickers: `segment`, `sticker-static`, `sticker-video`

Generate source art with native images when appropriate. For supplied RGBA, skip
segmentation. For local background removal, `segment` requires Pillow and
rembg and an explicit trusted **U2Net-compatible ONNX** checkpoint:

```json
{"operation":"segment","input":"character.png","output":"cutout","rembg_checkpoint":"<u2net-onnx-file>","white_background":false}
```

No implicit model fallback or weight download. For a sequence, replace `input` with
`frames:[...]` and provide `sam2_checkpoint`, `sam2_config` (installed configuration
such as `configs/sam2.1/sam2.1_hiera_s.yaml`) and `device` (`cpu`/`cuda`). Requires
[official SAM2](https://github.com/facebookresearch/sam2) and matching Torch runtime.
The first rembg mask seeds SAM2 propagation. Only for an actual white background use
`white_background:true`, optional `white_threshold` (default 215): mask/chromakey union,
5×5 closing and 60/180 rethreshold retain flying props and reduce halos. Review masks;
do not assume that every white background or character shares one optimal threshold.

```json
{"operation":"sticker-static","input":"cutout/frame-0000.png","output":"static-sticker","emoji":false}
```

Produces lossless transparent WebP, 512×512 (100×100 for `emoji:true`), at most 512 KiB.
The shared crop has a transparent margin, so cropping cannot accidentally remove alpha.

```json
{"operation":"sticker-video","frames":["frame1.png","frame2.png"],"output":"video-sticker","fps":30,"emoji":false,"ffmpeg":"<actual-ffmpeg-executable>","ffprobe":"<actual-ffprobe-executable>"}
```

Requires alpha-capable libvpx-vp9 in FFmpeg. Uses a stable union crop; verifies single
VP9/no-audio, dimensions, size, duration, actual decoded frame count and alpha error
against source frames. **The old claim that FFmpeg always loses alpha is not treated
as fact**: this adapter tests the result. A build that loses alpha fails validation.
No automatic custom-encoder build/WSL install. [Telegram's format contract](https://core.telegram.org/stickers/webm-vp9-encoding)
sets 30 FPS/3 seconds/256 KiB; the helper enforces these bounds. Publishing/pack mutation
uses an authorized connector or normal @Stickers workflow with state readback. Map
stickers by normalized emoji, not unstable list position; never copy session databases.

### Web assets: `web-assets`

```json
{"operation":"web-assets","input":"logo.png","social_input":"approved-banner.png","output":"web-assets"}
```

Pillow generates PNG sizes 16–512, true multi-size ICO, Apple touch icon, icon manifest
and link markup. Optional `social_input` yields 1200×630 and 1200×600 canvases without
distorting the artwork. For a branded banner first render the preserved HTML design
with available native browser tooling; inspect typography and image rights. Background
removal can use `segment`. No fictitious social preview is generated from a missing brief.

## Setup policy and evidence

- Core pack/installer remains Python-standard-library-only. For image artifacts use
  an isolated environment with Pillow. Test environments use `requirements-test-media.txt`.
- Install only the selected engine using its linked official instructions, after the
  user authorizes downloads and any costs/data sharing. Hardware-specific Torch/CUDA
  wheels, desktop applications and model license acceptance cannot be one universal lockfile.
- Synthetic local tests exercise output bytes, rollback, request validation and known
  engine contracts. Unavailable GPU, CAD, OPF and Edit-Banana inference is **not** labeled
  live-verified. See `VALIDATION.md` in the repository for the executed test matrix.
- A missing engine produces an actionable prerequisite, not a claim that the adapter
  is missing, and not permission to replace the task with an unrelated tool.
