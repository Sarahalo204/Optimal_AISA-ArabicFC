import json
from datasets import load_dataset

dataset = load_dataset("TuwaiqAcademy/AISA-ArabicFC", split="dev")

def load_preds(path):
    preds = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            p = json.loads(line.strip())
            preds[str(p["id"])] = p
    return preds

winner_preds = load_preds(r"C:\Users\Lenovo\OneDrive\Desktop\AISA_ArabicFC\aisa-arabicfc-solution_download\submissions\track_a_WINNER.jsonl")

out_f = open("remaining_errors.txt", "w", encoding="utf-8")
errors_count = 0

for i, sample in enumerate(dataset):
    gold_tool = "none"
    gold_args_clean = {}

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

    q_text = ""
    for msg in sample.get("messages", []):
        if msg.get("role") == "user":
            q_text = msg.get("content", "")
            break

    sample_id = str(sample.get("id", i))
    
    win_p = winner_preds.get(sample_id, {})
    win_tool = win_p.get("tool_called", "none")
    win_args = win_p.get("arguments", {})
    win_correct = (win_tool == gold_tool and win_args == gold_args_clean)
    
    if not win_correct:
        errors_count += 1
        out_f.write(f"\n--- ERROR {errors_count} | Sample ID: {sample_id} ---\n")
        out_f.write(f"Question: {q_text}\n")
        out_f.write(f"Tool: Pred={win_tool} | GT={gold_tool}\n")
        
        # Only print keys that are different or missing
        all_keys = set(win_args.keys()).union(set(gold_args_clean.keys()))
        for k in all_keys:
            v_pred = win_args.get(k, "<MISSING>")
            v_gt = gold_args_clean.get(k, "<MISSING>")
            if v_pred != v_gt:
                out_f.write(f"Mismatch [{k}]: Pred={repr(v_pred)} | GT={repr(v_gt)}\n")

out_f.write(f"\nTotal Errors: {errors_count}\n")
out_f.close()
