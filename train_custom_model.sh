#!/bin/bash

# This script trains a new DPLP model for German.

# Prerequisites:
# 1. Docker is installed and running.
# 2. The DPLP-German docker image is available (mohamadisara20/dplp-env:ger).
# 3. Your training data is prepared in the required format.

# Instructions:
# 1. Set the BASE_DIR variable below to the absolute path of your corpus directory.
#    This directory must contain 'training', 'dev', and 'test' subdirectories
#    filled with your .rs3 files.
# 2. Make sure your parsing_eval_metrics/rel_mapping.json file is up-to-date
#    with all the relations in your corpus.
# 3. Run this script from the root of the DPLP-German project directory:
#    bash train_custom_model.sh

# --- Configuration ---
# Change this to the relative path of the data directory from the project root.
BASE_DIR="data/pcc"
REL_MAP_FILE="${BASE_DIR}/pcc_rel_mapping.json"

# --- Script ---

# Check if the base directory exists
if [ ! -d "$BASE_DIR" ]; then
  echo "Error: Base directory '$BASE_DIR' not found."
  echo "Please create it and organize your data in 'training', 'dev', and 'test' subdirectories."
  exit 1
fi

echo "--- Step 1: Generating custom relation map ---"
python3 scripts/generate_relation_map.py "${BASE_DIR}/training" "${REL_MAP_FILE}"
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate relation map. Aborting."
    exit 1
fi

echo "--- Step 2: Starting training process ---"
echo "Using base directory: $BASE_DIR"
echo "Using relation map: $REL_MAP_FILE"

# Run the training command inside the Docker container
docker run --rm -it \
  -v "$(pwd)":/home/DPLP \
  -w /home/DPLP \
  mohamadisara20/dplp-env:ger \
  python3 ger_train.py "$BASE_DIR" -rm "$REL_MAP_FILE"

echo "Training finished."
echo "Your new model is located in: $BASE_DIR/model/"
echo "Training results are in: $BASE_DIR/result.txt"
