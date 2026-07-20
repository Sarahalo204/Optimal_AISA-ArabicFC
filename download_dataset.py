from huggingface_hub import snapshot_download

try:
    print("Downloading dataset...")
    path = snapshot_download(
        repo_id="arabic-aisa/aisa-arabicfc-solution",
        repo_type="dataset",
        token="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",
        local_dir="aisa-arabicfc-solution_download"
    )
    print("Downloaded to:", path)
except Exception as e:
    print("Error:", e)
