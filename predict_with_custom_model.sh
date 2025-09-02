#!/bin/bash
set -e

# This script runs the DPLP German RST parser on a directory of .txt files using a custom trained model.
# It leverages the pre-built Docker container to ensure the correct environment, including Python 2 dependencies.

# --- Argument Validation ---
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: $0 <corpus_base_path> <input_directory> <output_directory>"
  echo "Example: $0 data/pcc data/pcc/test_input data/pcc/test_output"
  exit 1
fi
CORPUS_BASE_PATH="$1"
INPUT_DIR="$2"
OUTPUT_DIR="$3"

# --- Path Definitions ---
# These paths are relative to the project root and will be used inside the Docker container.
CORPUS_NAME=$(basename "$CORPUS_BASE_PATH")
MODEL_DIR="$CORPUS_BASE_PATH/model"
MODEL_FILE="$MODEL_DIR/model.pickle.gz"
PROJMAT_FILE="$MODEL_DIR/projmat.pickle.gz"

# Handle different relation map naming conventions (custom vs. default)
CUSTOM_REL_MAP="$CORPUS_BASE_PATH/${CORPUS_NAME}_rel_mapping.json"
DEFAULT_REL_MAP="$CORPUS_BASE_PATH/rel_mapping.json"
if [ -f "$CUSTOM_REL_MAP" ]; then
  RELATION_MAP="$CUSTOM_REL_MAP"
elif [ -f "$DEFAULT_REL_MAP" ]; then
  RELATION_MAP="$DEFAULT_REL_MAP"
else
  echo "Warning: No relation map file found. Proceeding without one."
  RELATION_MAP=""
fi

DATAPATH="$CORPUS_BASE_PATH" # Path for vocabs etc.

# --- Pre-flight Checks ---
if ! command -v docker &> /dev/null; then
    echo "Error: Docker command not found. Please install Docker to run this script."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running or not accessible."
    echo "Please start the Docker service. On many systems, the command is: sudo systemctl start docker"
    exit 1
fi

if [ ! -f "$MODEL_FILE" ]; then
    echo "Error: Model file not found at $MODEL_FILE"
    exit 1
fi

if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory not found at $INPUT_DIR"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# --- Local Preprocessing ---
# The following script uses Stanza and will leverage the local GPU if available.
echo "Running unified Stanza preprocessing on the host machine..."
python3 run_stanza_preprocessing.py "$INPUT_DIR"

# --- Docker Execution ---
# We mount the entire project directory into the container at /home/DPLP.
# The container's working directory is set to /home/DPLP, so all paths are relative to the project root.
echo "Running segmentation, parsing, and conversion inside Docker container..."
docker run --rm -v "$(pwd)":/home/DPLP -w /home/DPLP mohamadisara20/dplp-env:latest \
  python3 ger_predict_dis_from_txt.py "$INPUT_DIR" \
    -m "$MODEL_FILE" \
    -p "$PROJMAT_FILE" \
    -d "$DATAPATH" \
    -o "$OUTPUT_DIR" \
    -rm "$RELATION_MAP" \
    --no-pre


echo "Processing complete. Output files are in $OUTPUT_DIR"