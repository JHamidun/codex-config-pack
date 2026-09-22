# Native connected-service workflow

This is a connector procedure, not an executable port of the historical SDK/scripts.
The selected contract lists the exact service and task scope. Resolve that capability
from the current host's callable tools, installed skills or explicitly configured CLI.
Names found in source examples, environment variables or a plugin catalog do not
prove a connection exists. Do not pretend an absent connector is an adapter.

## One-time connection

1. Check current tool inventory for the selected service and required action. Load
   only its native instructions/schema. Prefer a first-party/official connector.
2. If it is absent, use the host's supported plugin/MCP setup only when that install
   is explicitly requested and offered by the host. Otherwise give the user the exact
   missing service/action and its official connection documentation. Never auto-enable
   all integrations, all scopes, background services or paid providers.
3. Authenticate through the connector's normal authorization flow. For an explicit
   API workflow use only the named environment variables from the current official
   documentation, injected by the user's approved secret mechanism. Do not read or
   copy a master credential file, save keys in the pack, extract cookies, or log values.
4. Inspect a read-only account/workspace/capability response. Record the selected
   account, permitted operation and missing scopes without exposing private contents.
   Installed package or key presence alone is not authentication or action support.

## Execute the user task

Use the selected source guide only for domain inputs, output requirements and relevant
provider concepts. Its command lines, model IDs and endpoint payloads are historical;
use the live native schema or current official provider API documentation instead.
Do not run `.source`, import a missing home-directory module, or silently switch provider.

Confirm the intended account/destination and exact mutating action unless already
explicit. Pass the actual authorized inputs, inspect structured errors, and verify a
real artifact/readback or job completion. A queued job is not a finished output.
For idempotent retries preserve the operation ID; do not blindly repeat sends,
publishes, charges, deletes or deployments. Stop on authorization/cost boundaries.

If only draft/analysis is requested, complete it without connecting unrelated services.
If the actual service action is unavailable, report the precise blocker and return
any independently complete local artifact. A native generic alternative is acceptable
only if it preserves the user's request; never label it as the selected provider.

## Portability boundary

No accounts, tokens, OAuth grants, purchased services or host-specific tools ship in
this public pack. `connection-required` means the procedure is defined but its remote
operation cannot run until a matching live capability is connected and verified.
It is not a claim of provider integration testing. No legacy API proxy, session token
reuse or subscription-to-API bridge is enabled as a fallback.
