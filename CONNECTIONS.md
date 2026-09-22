# Connection and engine requirements

This is a setup/verification matrix, not a list of bundled SDK implementations.
No account, credential, local model, GPU runtime or application is included.
Use the exact current tool schema and official provider documentation at setup time.
Names in source examples do not establish availability or authorization.

## What Codex does when a dependency is missing

1. Identify the selected workflow and exact requested operation.
2. Check the host for that capability, not merely a similarly named plugin.
3. Prefer the native connector or installed project runtime; read its current instructions.
4. State one exact missing dependency. Installation, data upload and paid calls need their own authorization.
5. Verify a read-only capability first, then perform only the requested operation and check its real result.
6. If unavailable, deliver any independent local work and clearly mark the blocked portion.

Provider-neutral documents/images/research use native capabilities without needing every historical service.
An explicit provider request must not silently become a different provider.
CLI-only hosts do not automatically have Desktop browser, media, documents or task-management tools.

## Optional local engines

Nine specialized workflows now use shipped executable adapters rather than this
connection-only fallback. Engine/model installation remains optional and selected
per device/task. See [OPTIONAL-ADAPTERS.md](native/OPTIONAL-ADAPTERS.md) for the exact
implemented operations, JSON requests, official setup sources and test boundaries.
No generic image instruction is treated as a substitute for CAD, OCR or local PII filtering.

## Per-service contracts

| Service group | Entries | Required capability |
|---|---:|---|
| anthropic | 4 | The explicitly requested Anthropic API, Claude Design or official Claude CLI connection; never reuse subscription tokens as generic API credentials. |
| google-ai | 3 | Authorized Google AI capability for the requested text, image, speech or grounding action; current model availability must be discovered. |
| openai-api | 1 | Current native OpenAI capability or an explicitly authorized API connection. Native subscribed tools are not generic API billing credentials. |
| deepseek | 1 | Authorized DeepSeek text/reasoning capability and a currently supported model. |
| kimi | 3 | Authorized Moonshot/Kimi capability when that provider is explicitly requested; generic reasoning can run natively without claiming a Kimi call. |
| multi-model | 3 | Explicitly authorized independent evaluators/providers with a bounded manifest, current models, cost controls and observed outputs; no fabricated cross-model consensus. |
| google-workspace | 11 | The specific Google Workspace service connector and requested read/write scope for the user's selected account. One working Google connection does not prove every API is authorized. |
| google-cloud | 1 | Authorized Google Cloud project/bucket connection and exact storage operation; inspect IAM and destination before mutation. |
| google-analytics-ads | 3 | Authorized Ads, Analytics or Search Console connector for the selected account/property, with actual operation-specific scope. |
| microsoft-mail | 1 | Authorized native Microsoft mail connector; explicit desktop COM requests additionally require the user's local Outlook profile and supported Windows runtime. |
| mail-protocols | 1 | User-selected mailbox/server with approved IMAP read or SMTP send access, TLS and a secure credential mechanism; no default recipient/account. |
| deepgram | 2 | Authorized Deepgram transcription capability and permission to upload the selected audio; verify actual transcript, timings and speaker labels. |
| deepl | 2 | Authorized DeepL text/document translation connection and applicable account endpoint, glossary and language scope. |
| elevenlabs | 1 | Authorized ElevenLabs speech/audio capability and permission to use the selected voice; no baked-in voice identity. |
| d-id | 2 | Authorized D-ID presenter-generation capability, permitted portrait/audio and real job completion. |
| heygen | 1 | Authorized HeyGen avatar/video capability and permission for the chosen identity/voice. |
| gamma | 1 | Authorized Gamma generation/export capability. A local presentation is not proof of a Gamma operation. |
| manus | 4 | Authorized Manus task or slide-generation connection when the provider is explicit. Generic slides use native presentations without claiming Manus execution. |
| figma | 3 | Native Figma connection for actual file/frame reads, export or the requested supported write operation; API read access does not imply arbitrary canvas editing. |
| miro | 1 | Authorized Miro board connection with the exact requested read/write operation and selected board. |
| notebooklm | 1 | An available authorized NotebookLM capability or the user's normal interactive browser flow; no cookie extraction or private undocumented session API. |
| perplexity | 1 | Authorized Perplexity search/research capability when explicitly requested; generic research uses native web with sources. |
| serpapi | 1 | Authorized SerpAPI search capability with selected engine/locale and observed result metadata. |
| similarweb | 1 | Authorized Similarweb data access for the selected domain/period; do not fabricate unavailable traffic estimates. |
| apify | 3 | Authorized selected scraping/ad-library/intelligence capability, lawful target scope, bounded dataset/job and verified source timestamps. |
| maps | 1 | Available map/place/geocoding capability for the selected region and task; respect provider attribution/rate rules and verify live places. |
| pinecone | 1 | Authorized Pinecone index/namespace connection, embedding dimension/model compatibility and exact data-sharing scope. |
| n8n | 3 | User-selected n8n/automation instance and authorized connector. Validate a workflow against actual nodes/credentials before activation; raw sample exports were deliberately omitted. |
| social-publishing | 12 | An authorized connector for the exact platform/account and action, plus verified destination, visibility and readback. Do not silently switch publishing providers. |
| telegram | 1 | Authorized Telegram bot or user-account transport appropriate to the requested action, explicit destination and actual readback; no copied session file. |
| youtube | 3 | The specific YouTube transcript/analytics/upload capability. Public transcripts may not need account access; analytics/upload requires the selected authorized channel and action. |
| zoom | 1 | Authorized Zoom meeting/recording capability for the selected account and explicit operation; recording contents are private inputs. |
| twilio | 1 | Authorized Twilio account/sender and permitted recipient, exact message/cost authorization, and delivery status; credentials alone do not provision a sender. |
| yandex | 1 | The selected Yandex Disk/Metrika/mail/calendar capability. Public-link retrieval is separate from account OAuth or write access. |
| tilda-crm | 2 | Authorized selected Tilda project and CRM connection; read/rehearse before publishing or submitting real lead forms and verify end-to-end readback. |
| home-assistant | 1 | User-selected Home Assistant instance and explicit device/action authorization; reading state does not authorize physical control. |
| apple-developer | 1 | Authorized Apple Developer identity/certificates and supported signing/notarization runtime or approved CI; no certificates or signing keys are included. |
| deployment | 5 | Explicit deployment/registry/DNS/Git remote target, authorized credentials, rollback and real service verification; never infer a server from author-specific defaults. |
| task-manager | 2 | Authorized actual task/calendar connector for the selected account, or user-supplied exported tasks for local planning. Scheduling/sending requires exact intent. |
| external-media | 3 | Authorized exact media provider and supported current operation/model, permitted inputs, cost boundary and completed output validation. |
| ai-detectors | 1 | Explicit authorization to share the text with selected detector providers; scores are detector observations, not proof of authorship. |
| course-submission | 1 | The user-selected course submission service and their authorized account. Never infer the destination from the pack author; submit only the explicit assignment/artifact and verify its actual status. |

The exact skill/command/agent membership is in [native/connection-contracts.json](native/connection-contracts.json).
The execution protocol is [native/recipes/service.md](native/recipes/service.md).
Connection presence is evaluated per user and per host; the public pack contains no author-specific connection state.
