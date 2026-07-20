# Training And Reproduction

Dataset revision: `1a5e5f8a9eeadd996118a8a86f72c4285047a00e`
Evaluator revision: `f73d1f95d2ccd3219e01cf2aa68173018acd9e0d`

This file explains the solution in the simplest reproducible way.

## What Was Trained

We trained a LoRA adapter on top of `Qwen/Qwen2.5-7B-Instruct`.

The model sees:

1. the Arabic user request;
2. the four candidate tools;
3. the required answer format.

It learns to output:

```json
{"tool_called": "tool_name", "arguments": {"key": "value"}}
```

The main lesson was simple: tool choice became easy, but exact argument values
were hard. Training for three epochs helped. Bigger models, broad synthetic
data, and constrained decoding did not beat the selected setup.

## Environment

Use Python 3.11 or 3.12 with a CUDA GPU. A 16 GB T4 can run 4-bit QLoRA; a
24 GB 4090 is more comfortable.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pip install transformers peft bitsandbytes accelerate trl sentencepiece tiktoken safetensors
```

The exact local orchestration environment is recorded in
`manifests/environment.lock`.

Log into Hugging Face before using the private adapter:

```bash
huggingface-cli login
```

## Recreate The Internal Split

This split is only for honest local selection. It uses the official train split,
not public dev.

```bash
PYTHONPATH=src .venv/bin/python scripts/make_splits.py \
  --out manifests/splits-v12-20260618.jsonl \
  --summary-out manifests/splits-v12-20260618.summary.json
```

For finalist Track C analysis, also create five grouped out-of-fold manifests.
Each utterance group is held out exactly once, so dialect robustness is measured
on train data without relying on the tiny public-dev Maghrebi slice:

```bash
PYTHONPATH=src .venv/bin/python scripts/make_oof_folds.py \
  --out manifests/oof-folds-v12-20260618.jsonl \
  --summary-out manifests/oof-folds-v12-20260618.summary.json
```

## Train The Same Method

The exact delivered adapter is already frozen at `arabic-aisa/arabicfc-7b`.

A fresh run should be treated as method reproduction and extension work, not as
a promise of byte-identical weights. Train only on the internal `train` split
when selecting new ideas:

```bash
PYTHONPATH=src .venv/bin/python -m arabicfc.train.sft \
  --model Qwen/Qwen2.5-7B-Instruct \
  --track A \
  --full-lm \
  --epochs 3 \
  --data-split train \
  --split-manifest manifests/splits-v12-20260618.jsonl \
  --internal-split train \
  --batch 8 \
  --grad-accum 2 \
  --max-seq 512 \
  --lr 2e-4 \
  --seed 20260618 \
  --out runs/g0-qwen7b-3ep
```

Important details:

- `--full-lm` trains on the whole prompt and answer. Completion-only masking was worse.
- `--epochs 3` was the useful training lever.
- `--internal-split train` protects tune and lockbox from training leakage.
- `--max-seq 512` is enough for the compact prompt.
- The training script uses 4-bit QLoRA on CUDA by default.

## Score For Selection

First score internal tune. This is the score used to decide whether a new idea
is worth keeping:

```bash
PYTHONPATH=src .venv/bin/python scripts/predict.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapter runs/g0-qwen7b-3ep \
  --split train \
  --split-manifest manifests/splits-v12-20260618.jsonl \
  --internal-split tune \
  --batch 16 \
  --out runs/g0-qwen7b-3ep/tune_pred_raw.jsonl \
  --score-out runs/g0-qwen7b-3ep/tune_score_raw.json
```

Apply the clean default ruleset:

```bash
PYTHONPATH=src .venv/bin/python scripts/postprocess_predictions.py \
  --pred runs/g0-qwen7b-3ep/tune_pred_raw.jsonl \
  --split train \
  --split-manifest manifests/splits-v12-20260618.jsonl \
  --internal-split tune \
  --track A \
  --ruleset accepted \
  --out runs/g0-qwen7b-3ep/tune_pred_accepted.jsonl \
  --score-out runs/g0-qwen7b-3ep/tune_score_accepted.json
```

Repeat the same two commands with `--internal-split lockbox` before promoting a
new run. Do not use public dev to choose between experiments.

For Track C, train one model per fold on the fold complement, predict only that
fold's held-out rows, concatenate those held-out predictions, then build the
dialect report:

```bash
mkdir -p runs/finalist
: > runs/finalist/train_oof_pred.jsonl
for fold in 0 1 2 3 4; do
  PYTHONPATH=src .venv/bin/python -m arabicfc.train.sft \
    --model Qwen/Qwen2.5-7B-Instruct \
    --track A \
    --full-lm \
    --epochs 3 \
    --data-split train \
    --split-manifest manifests/oof-folds-v12-20260618.jsonl \
    --fold "${fold}" \
    --fold-role train \
    --batch 8 \
    --grad-accum 2 \
    --max-seq 512 \
    --lr 2e-4 \
    --seed 20260618 \
    --out "runs/finalist/fold_${fold}"

  PYTHONPATH=src .venv/bin/python scripts/predict.py \
    --model Qwen/Qwen2.5-7B-Instruct \
    --adapter "runs/finalist/fold_${fold}" \
    --split train \
    --split-manifest manifests/oof-folds-v12-20260618.jsonl \
    --fold "${fold}" \
    --fold-role heldout \
    --batch 16 \
    --postprocess \
    --postprocess-ruleset accepted \
    --out "runs/finalist/fold_${fold}/heldout_pred.jsonl" \
    --score-out "runs/finalist/fold_${fold}/heldout_score.json"

  cat "runs/finalist/fold_${fold}/heldout_pred.jsonl" >> runs/finalist/train_oof_pred.jsonl
done
```

```bash
PYTHONPATH=src .venv/bin/python scripts/track_c_report.py \
  --pred runs/finalist/train_oof_pred.jsonl \
  --split train \
  --out runs/finalist/track_c_oof_report.json
```

The report includes per-dialect `n`, positive `n`, FnAcc, ArgEM, bootstrap
intervals, deltas from MSA, macro dialect scores, worst dialect, and official
max-minus-min gaps.

## Reproduce The Public-Dev Candidate

Use public dev only after the method is frozen. Generate raw public-dev
predictions:

```bash
PYTHONPATH=src .venv/bin/python scripts/predict.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapter runs/g0-qwen7b-3ep \
  --split dev \
  --batch 16 \
  --out runs/g0-qwen7b-3ep/dev_pred_raw.jsonl \
  --score-out runs/g0-qwen7b-3ep/dev_score_raw.json
```

Apply the public-dev candidate ruleset:

```bash
PYTHONPATH=src .venv/bin/python scripts/postprocess_predictions.py \
  --pred runs/g0-qwen7b-3ep/dev_pred_raw.jsonl \
  --split dev \
  --track A \
  --ruleset surface_v2 \
  --out runs/g0-qwen7b-3ep/dev_pred_surface_v2.jsonl \
  --score-out runs/g0-qwen7b-3ep/score_surface_v2.json
```

Track B uses the same function-call predictions and adds a short non-empty
Arabic `think` field:

```bash
PYTHONPATH=src .venv/bin/python scripts/postprocess_predictions.py \
  --pred runs/g0-qwen7b-3ep/dev_pred_raw.jsonl \
  --split dev \
  --track B \
  --ruleset surface_v2 \
  --out runs/g0-qwen7b-3ep/dev_pred_surface_v2_b.jsonl \
  --score-out runs/g0-qwen7b-3ep/score_surface_v2_b.json
```

## Reproduce The Frozen Artifact Directly

If the goal is to reproduce the delivered package rather than retrain, use the
private adapter directly:

```bash
PYTHONPATH=src .venv/bin/python scripts/predict.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapter arabic-aisa/arabicfc-7b \
  --split dev \
  --batch 16 \
  --out runs/frozen/dev_pred_raw.jsonl \
  --score-out runs/frozen/score_raw.json
```

Then apply either `accepted` or `surface_v2` exactly as above.

## Which Result To Use

- Use `accepted` to explain the clean method. It is backed by train/schema
  evidence and improves internal lockbox.
- Use `surface_v2` to reproduce the public-dev leaderboard candidate. It scores
  higher on public dev but is more likely to contain leaderboard-specific
  calibration.

Do not train on public dev. Do not add a postprocess rule just because it helps
public dev unless it also has train/internal evidence.
