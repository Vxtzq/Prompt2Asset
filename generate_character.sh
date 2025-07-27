#!/bin/bash

# Default values
RIG_ARG=""
PROMPT_ARG=""
POSE_ARG=""
NEG_PROMPT_ARG=""
USE_POSE_ARG=""
BASE_IMAGE_ARG=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --rig)
      RIG_ARG="--rig"
      shift
      ;;
    --pose_image)
      POSE_ARG="$2"
      shift 2
      ;;
    --negative_prompt)
      NEG_PROMPT_ARG="$2"
      shift 2
      ;;
    --use_pose)
      USE_POSE_ARG="--use_pose"
      shift
      ;;
    --base_image)
      BASE_IMAGE_ARG="$2"
      shift 2
      ;;
    *)
      # Everything else is considered the prompt
      PROMPT_ARG="$*"
      break
      ;;
  esac
done

# Run core setup
python3 download_model.py
mkdir -p sprite
mkdir -p sprite_output
mkdir -p mesh_output

# Use base image if provided
if [[ -n "$BASE_IMAGE_ARG" ]]; then
  if [[ ! -f "$BASE_IMAGE_ARG" ]]; then
    echo "Error: base image '$BASE_IMAGE_ARG' not found."
    exit 1
  fi

  echo "Using base image: $BASE_IMAGE_ARG"
  cp "$BASE_IMAGE_ARG" sprite/sprite.png
else
  # Run character generation
  CMD="python3 character_gen.py"

  if [[ -n "$POSE_ARG" ]]; then
    if [[ ! -f "$POSE_ARG" ]]; then
      echo "Error: pose image '$POSE_ARG' not found."
      echo "Please provide a valid path using --pose_image <path>."
      exit 1
    fi
    CMD+=" --pose_image \"$POSE_ARG\""
  fi

  if [[ -n "$USE_POSE_ARG" ]]; then
    CMD+=" $USE_POSE_ARG"
  fi

  if [[ -n "$PROMPT_ARG" ]]; then
    CMD+=" --prompt \"$PROMPT_ARG\""
  fi

  if [[ -n "$NEG_PROMPT_ARG" ]]; then
    CMD+=" --negative_prompt \"$NEG_PROMPT_ARG\""
  fi

  echo "Running character generation..."
  eval $CMD
fi

# Continue pipeline
python3 IS-Net/Inference.py
python3 inference.py

# Optional rigging step
if [[ "$RIG_ARG" == "--rig" ]]; then
  cd UniRig

  bash launch/inference/generate_skeleton.sh --input ../mesh_output/mesh.glb --output ../results/rigged_mesh.fbx
  bash launch/inference/generate_skin.sh --input ../results/rigged_mesh.fbx --output ../results/rigged_mesh.fbx
  bash launch/inference/merge.sh --source ../results/rigged_mesh.fbx --target ../mesh_output/mesh.glb --output ../results/mesh_final.glb

  rm -rf mesh_output tmp
  cd ..
fi
