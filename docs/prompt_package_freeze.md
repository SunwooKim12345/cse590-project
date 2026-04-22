# Prompt Package Freeze

## Status
- package_id: `prompt_package_locked`
- status: `mixed_s1_adaptive_s2_frozen`
- active prompt_ids: `s1_prompt`, `s2_prompt`

## Source of truth

Scenario 1 is adaptive multi-turn collection. Its baseline files are kept under `prompts/frozen/`, but they are not checksum-locked because the actual next prompt may vary slightly based on prior model responses. For S1, the source of truth is the logged `input_prompt` value in each response CSV row.

Scenario 2 is fixed single-turn collection. Use only the frozen S2 files under `prompts/frozen/` for data collection runs.

S1 adaptive baseline files:
- `prompts/frozen/scenario1_multiturn_template.md`
- `prompts/frozen/scenario1_persona_scripts.csv`

S2 checksum-locked files:
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
1. Do not edit checksum-locked S2 files under `prompts/frozen/` during a run.
2. If S2 prompts must change, edit files under `prompts/`, then re-freeze and regenerate manifest/checksums.
3. S1 turns may be adapted during collection when needed to follow model responses; record the actual sent text in `input_prompt`.
4. Log any freeze replacement or S1 protocol change in project notes before running new experiments.
