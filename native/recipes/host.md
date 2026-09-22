# Native Codex host configuration and task operations

Discover the actual host capability before acting. For skills/agents, use the native
skill creator or supported Codex configuration schema and current project conventions;
preserve the selected historical guide's useful design methodology, not its Claude
frontmatter, hook payloads, CLI aliases or global installation paths.

For task list/read/rename/continuation, use native task tools with the exact user-selected
task. For scheduled work/reminders use the native automation mechanism only when the
user asks for later/recurring work. A source JSONL edit, Markdown note or shell loop is
not an equivalent host action. Do not inspect or mutate private session databases.

For bounded headless Codex work explicitly requested by the user, inspect the installed
CLI's help and official current documentation, pass an explicit workspace and output
path, inherit allowed models/permissions, bound concurrency/retries and retain a job
manifest. Do not create an OpenAI-compatible proxy from subscription credentials,
reuse OAuth tokens outside supported clients or expose a listening service by default.

For third-party agent/skill managers such as beads or gstack, keep an explicit provider
request intact. Inspect the user's chosen project installation before using its CLI.
Install/update requires a concrete approved source, package/license review, isolated
state and rollback; the copied source installer is not a Codex updater.

If the requested operation has no native equivalent in this host, state that exact
limitation rather than changing task/model/scheduler state by undocumented means.
Verify effective configuration or actual task state after an authorized change; new
configuration may require a fresh task/app reload and may not affect the current one.
