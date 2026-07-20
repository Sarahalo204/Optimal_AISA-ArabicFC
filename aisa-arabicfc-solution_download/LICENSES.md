# License And Provenance Inventory

Dataset revision: `1a5e5f8a9eeadd996118a8a86f72c4285047a00e`
Evaluator revision: `f73d1f95d2ccd3219e01cf2aa68173018acd9e0d`

This file records the licenses visible from Hugging Face metadata on
2026-06-19. It is a solution-package inventory, not legal advice.

| Artifact | Source | Revision or SHA | License metadata | Notes |
| --- | --- | --- | --- | --- |
| Base model | `Qwen/Qwen2.5-7B-Instruct` | `a09a35458c702b33eeacc393d103063234e8bc28` | `apache-2.0` | License link in model card: `https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/blob/main/LICENSE`. |
| Selected private adapter | `arabic-aisa/arabicfc-7b` | `57aa2ab514e8fca42a5643df3fec8b0157b5437d` | not declared in HF metadata | Private PEFT adapter for the selected G0 solution artifact. |
| Dataset | `TuwaiqAcademy/AISA-ArabicFC` | `1a5e5f8a9eeadd996118a8a86f72c4285047a00e` | `apache-2.0` | Pinned v1.2-equivalent dataset revision used for internal splits. |
| Shared-task page | `TuwaiqAcademy/AISA-ArabicFC-Shared-Task` | `23afc7694a2eea290736ed8f29bed71d6c97a63b` | `apache-2.0` | Task-facing Hugging Face Space metadata. |
| Evaluator / leaderboard | `TuwaiqAcademy/AISA-ArabicFC-SharedTask-Leaderboard` | `f73d1f95d2ccd3219e01cf2aa68173018acd9e0d` | `apache-2.0` | Pinned evaluator revision used by local scoring. |
| Local repo code | this repository | current working tree | not declared in `pyproject.toml` | Add an explicit project license before public release. |

Candidate models such as `ALLaM-AI/ALLaM-7B-Instruct-preview` are not included
in this inventory until they produce accepted finalist artifacts. Before any
public release, add an explicit project/model license and update this inventory.
