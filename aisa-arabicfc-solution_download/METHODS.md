# Methods

Dataset revision: `1a5e5f8a9eeadd996118a8a86f72c4285047a00e`
Evaluator revision: `f73d1f95d2ccd3219e01cf2aa68173018acd9e0d`

## Framing

ArabicFC is mostly an exact argument-surface task once tool selection is solved.
The score weights argument exact match more heavily than function accuracy, and
small value-form mismatches lose the whole argument component for that example.

## Selected System

The selected system is Qwen2.5-7B-Instruct with a 3-epoch QLoRA adapter. The
main useful training lever was epochs. Bigger model scale, rank increases,
synthetic augmentation, completion masking, constrained decoding, ensembles, and
DPO did not produce a better accepted result.

## Rulesets

`accepted` is the default ruleset. It contains only train/schema-backed rules:
trap-tool suppression, one customs category surface fix, and one explicit
diabetes-medication phrase fix. It improves internal tune and lockbox.

`surface_v2` is the public-dev candidate. It adds narrow compare-price
surface-form repairs and gives the strongest public-dev score, but it regresses
internal lockbox, so it is packaged separately and clearly labeled.

## What To Learn From This

The strategy is proper for a scrappy shared-task attempt:

- vendor and pin the official scorer first;
- create a train-only internal tune/lockbox split;
- use grouped five-fold out-of-fold predictions for Track C finalist reports;
- change one factor at a time;
- reject attractive ideas when the scorer says they do not help;
- keep public-dev calibration separate from the hidden-test-safe default.

The result is not a blind-test guarantee. It is a clean, reproducible, strong
attempt with a clear audit trail.
