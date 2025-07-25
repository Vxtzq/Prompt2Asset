#!/bin/bash

# The first argument could be --rig or something else
# The second argument is the prompt string (optional)

RIG_ARG=""
PROMPT_ARG=""

# Check for --rig flag in first argument
if [[ "$1" == "--rig" ]]; then
  RIG_ARG="--rig"
  PROMPT_ARG="$2"
else
  PROMPT_ARG="$1"
fi

# Run core setup
python3 download_model.py
mkdir -p sprite
mkdir -p sprite_output
mkdir -p mesh_output

# Pass prompt argument to character_gen.py if present
if [[ -z "$PROMPT_ARG" ]]; then
  python3 character_gen.py
else
  python3 character_gen.py --prompt "$PROMPT_ARG"
fi

python3 IS-Net/Inference.py
python3 inference.py

if [[ "$RIG_ARG" == "--rig" ]]; then
  cd UniRig

  bash launch/inference/generate_skeleton.sh --input ../mesh_output/mesh.glb --output ../results/rigged_mesh.fbx
  bash launch/inference/generate_skin.sh --input ../results/rigged_mesh.fbx --output ../results/rigged_mesh.fbx
  bash launch/inference/merge.sh --source ../results/rigged_mesh.fbx --target ../mesh_output/mesh.glb --output ../results/mesh_final.glb
  rm -rf mesh_output tmp
  cd ..
fi
