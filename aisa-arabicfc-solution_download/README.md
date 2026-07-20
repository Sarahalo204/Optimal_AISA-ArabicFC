---
pretty_name: AISA ArabicFC Solution Package
tags:
  - arabic
  - function-calling
  - shared-task
  - private-solution
---

# AISA-ArabicFC Solution Package

This is the private, reproducible solution package for the AISA-ArabicFC shared
task. It is prepared against dataset revision
`1a5e5f8a9eeadd996118a8a86f72c4285047a00e` and evaluator revision
`f73d1f95d2ccd3219e01cf2aa68173018acd9e0d`.

Private Hugging Face solution dataset: `arabic-aisa/aisa-arabicfc-solution`.

## Selected Artifact

- Base: `Qwen/Qwen2.5-7B-Instruct`
- Adapter: `arabic-aisa/arabicfc-7b`
- Default ruleset: `accepted`
- Public-dev candidate ruleset: `surface_v2`

Exact revisions are recorded in `model/HF_POINTER.json` and
`manifests/hf_repos.json`.

The adapter lives in a private Hugging Face model repository. Grant authorized
recipients read access before they run the configs.

## Contents

- `configs/track_a.yaml`: default Track A config using the accepted ruleset.
- `configs/track_b.yaml`: default Track B config using the accepted ruleset.
- `configs/track_a_public_dev.yaml`: public-dev leaderboard calibration config.
- `configs/track_b_public_dev.yaml`: public-dev leaderboard Track B wrapper.
- `TRAINING.md`: simple training and scoring reproduction guide.
- `METHODS.md`: concise strategy and rejected directions.
- `RESULTS.md`: score table and accepted/public-dev split.
- `model/HF_POINTER.json`: selected private adapter pointer.
- `postprocess/rules.yaml`: documented rulesets.
- `submissions/`: ready-to-upload public-dev JSONL candidates.
- `manifests/`: dataset, experiment registry, environment, and HF provenance.
- `LICENSES.md`: license and provenance inventory.

## Reproduce

```bash
python -m arabicfc.prepare --dataset-revision 1a5e5f8a9eeadd996118a8a86f72c4285047a00e --output data/processed
python -m arabicfc.predict --config handoff/configs/track_a.yaml --input data/dev.jsonl --output outputs/track_a.jsonl
python -m arabicfc.validate --input data/dev.jsonl --predictions outputs/track_a.jsonl
python -m arabicfc.evaluate --gold data/dev.jsonl --predictions outputs/track_a.jsonl --evaluator-revision f73d1f95d2ccd3219e01cf2aa68173018acd9e0d
python scripts/validate_experiment_registry.py handoff/manifests/experiment_registry.json --repo-root handoff
```

Use `track_a_public_dev.yaml` or `track_b_public_dev.yaml` only to reproduce the
public-dev leaderboard-calibrated result. The default accepted
configs are the cleaner strategy to learn from because those rules are justified
from train/schema/internal evidence.

For the live development leaderboard, upload the matching file from
`submissions/` directly. Track A uses
`track_a_public_dev_candidate.jsonl`; Track B uses
`track_b_public_dev_candidate.jsonl`.

This package is private solution material, not a public model release or a
submission by the local operator. Before public release, choose and record an
explicit project/model license.
