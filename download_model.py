from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="Vxtzq/Is-Net",
    filename="isnet-general-use.pth",
    local_dir="./",  # or use any specific folder path
    local_dir_use_symlinks=False  # ensures the file is copied, not symlinked
)

print("Model downloaded to:", model_path)
