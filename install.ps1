param(
    [switch]$DryRun,
    [switch]$WithAgents,
    [switch]$Uninstall,
    [string]$Target
)
$ErrorActionPreference = 'Stop'
$cliArgs = @('-I', '-X', 'utf8', '-B', (Join-Path $PSScriptRoot 'install.py'))
if ($DryRun) { $cliArgs += '--dry-run' }
if ($WithAgents) { $cliArgs += '--with-agents' }
if ($Uninstall) { $cliArgs += '--uninstall' }
if ($Target) { $cliArgs += @('--target', $Target) }
& python @cliArgs
exit $LASTEXITCODE
