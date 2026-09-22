# Native image workflow

For provider-neutral image creation/editing, discover and use the current native
image-generation capability and its documented interface. Do not use legacy DALL-E
IDs, a Google API wrapper or an external paid image endpoint by default.

Use the selected source guide's composition, lighting, typography and quality criteria
where they fit the user's request. Inspect local references before editing; pass only
the reference mechanism supported by the native tool. Never substitute a guessed
portrait/logo/product for a supplied reference. Preserve explicit user/provider choices.

Return the generated media through the host's supported image/artifact mechanism.
If saving a result, check magic/MIME before choosing an extension. Do not claim a
specific native model identifier unless the current host actually exposes it.

Deterministic resizing/upscaling, OCR reconstruction, transparent cutouts, segmentation
and editable vector conversion are separate operations. Native generation does not
prove those constraints are met. Use an actual matching local/native tool, validate
dimensions, alpha or editable objects, and explain a missing specialized capability.
