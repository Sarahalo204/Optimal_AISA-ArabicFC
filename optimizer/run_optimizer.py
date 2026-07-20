import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from repair import Coordinator

def load_jsonl(file_path):
    if not os.path.exists(file_path):
        return None
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def save_jsonl(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def run_pipeline():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Attempt to load questions from multiple possible paths
    gold_paths = [
        os.path.join(project_root, "gold_ground_truth.jsonl"),
        os.path.join(project_root, "data", "dev.jsonl"),
        "/content/handoff/data/dev.jsonl",
        "/content/handoff/gold_ground_truth.jsonl"
    ]
    
    questions_map = {}
    for p in gold_paths:
        data = load_jsonl(p)
        if data:
            for item in data:
                q_text = ""
                if "messages" in item:
                    for msg in item["messages"]:
                        if msg.get("role") == "user":
                            q_text = msg.get("content", "")
                            break
                if not q_text:
                    q_text = item.get("query", item.get("question", item.get("text", "")))
                questions_map[str(item.get("id"))] = q_text
            print(f"Loaded {len(questions_map)} questions from {p} for logical inference.")
            break

    search_paths = [
        project_root,
        os.path.join(project_root, "outputs"),
        os.path.join(project_root, "submissions"),
        os.path.join(project_root, "aisa-arabicfc-solution_download", "submissions"),
        "/content/handoff/submissions"
    ]
    
    tracks = [
        ("track_a_public_dev_candidate.jsonl", "track_a_WINNER.jsonl"),
        ("track_b_public_dev_candidate.jsonl", "track_b_WINNER.jsonl"),
        ("track_a.jsonl", "track_a_optimized.jsonl"),
        ("track_b.jsonl", "track_b_optimized.jsonl")
    ]
    
    coordinator = Coordinator()

    files_processed = 0
    for base_path in search_paths:
        for in_name, out_name in tracks:
            input_path = os.path.join(base_path, in_name)
            if not os.path.exists(input_path):
                continue
                
            output_result_path = os.path.join(base_path, out_name)
            print(f"Processing {input_path}...")
            
            preds = load_jsonl(input_path)
            optimized = []
            for p in preds:
                q_text = questions_map.get(str(p.get("id")), "")
                opt_p = coordinator.coordinate(p, q_text)
                optimized.append(opt_p)
                
            save_jsonl(optimized, output_result_path)
            print(f"Saved optimized results to: {output_result_path}")
            files_processed += 1
            
    if files_processed == 0:
        print("No input files found. Make sure prediction files exist in the correct paths.")

if __name__ == "__main__":
    run_pipeline()
