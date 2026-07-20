import json
import os
from datasets import load_dataset

print("Loading Ground Truth...")
dataset = load_dataset("TuwaiqAcademy/AISA-ArabicFC", split="dev")

def evaluate_submission(pred_file, track_name):
    if not os.path.exists(pred_file):
        print(f"File not found: {pred_file}")
        return

    preds = {}
    with open(pred_file, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line.strip())
            # In some cases the id is numeric in dataset but string in prediction or vice versa. Convert both to str.
            preds[str(p["id"])] = p

    fn_correct = 0
    arg_correct = 0
    total = len(dataset)

    for i, sample in enumerate(dataset):
        gold_tool = "none"
        gold_args_clean = {}

        # استخراج الإجابة النموذجية بشكل صحيح من السيرفر
        for msg in sample.get("messages", []):
            if msg.get("role") == "assistant":
                if "tool_calls" in msg and msg["tool_calls"]:
                    tool_call = msg["tool_calls"][0]
                    if "function" in tool_call:
                        gold_tool = tool_call["function"].get("name", "none")
                        raw_args = tool_call["function"].get("arguments", {})
                        if isinstance(raw_args, dict):
                            gold_args_clean = {k: v for k, v in raw_args.items() if v is not None}
                break

        # ID can be from `id` field in dataset if exists, otherwise index i
        sample_id = str(sample.get("id", i))
        pred = preds.get(sample_id, {})
        pred_tool = pred.get("tool_called", "none")
        pred_args = pred.get("arguments", {})

        if pred_tool == gold_tool:
            fn_correct += 1
            if pred_args == gold_args_clean:
                arg_correct += 1

    fn_acc = fn_correct / total
    arg_em = arg_correct / total

    print(f"\n=== Results for {track_name} ===")
    print(f"FnAcc:  {fn_acc:.4f}  ({fn_correct}/{total})")
    print(f"ArgEM:   {arg_em:.4f}  ({arg_correct}/{total})")

base_path = os.path.join("aisa-arabicfc-solution_download", "submissions")
print("\n--- RAW PREDICTIONS ---")
evaluate_submission(os.path.join(base_path, "track_a_public_dev_candidate.jsonl"), "Track A - Core (RAW)")

print("\n--- OPTIMIZED PREDICTIONS (WINNER) ---")
evaluate_submission(os.path.join(base_path, "track_a_WINNER.jsonl"), "Track A - Core (WINNER)")
evaluate_submission(os.path.join(base_path, "track_b_WINNER.jsonl"), "Track B - Reasoning (WINNER)")
