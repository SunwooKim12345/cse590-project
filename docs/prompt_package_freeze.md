# Prompt Package Freeze

## Status
- package_id: `prompt_package_locked`
- status: `frozen`
- active prompt_ids: `s1_prompt`, `s2_prompt`

## Frozen source of truth
Use only files under `prompts/frozen/` for data collection runs.

Included files:
- `prompts/frozen/scenario1_multiturn_template.md`
- `prompts/frozen/scenario1_persona_scripts.csv`
- `prompts/frozen/scenario2_singleturn_template.md`
- `prompts/frozen/prompt_log.md`

Integrity files:
- `prompts/frozen/prompt_package_manifest.json`
- `prompts/frozen/checksums.sha256`

## Verification command (PowerShell)
```powershell
$root='c:\Users\USER\study\CSE590_group_project'
Get-Content "$root\prompts\frozen\checksums.sha256" | ForEach-Object {
  $parts = $_ -split "\s+", 2
  $expected = $parts[0].Trim()
  $rel = $parts[1].Trim()
  $actual = (Get-FileHash -Path (Join-Path $root $rel) -Algorithm SHA256).Hash.ToLower()
  if ($actual -ne $expected) { Write-Output "MISMATCH: $rel" }
}
```

## Freeze rule
1. Do not edit files under `prompts/frozen/`.
2. If prompts must change, edit files under `prompts/`, then re-freeze and regenerate manifest/checksums.
3. Log any freeze replacement in project notes before running new experiments.
