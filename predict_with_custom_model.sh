#!/bin/bash
set -e

# This script runs the DPLP German RST parser on a directory of .txt files using a custom trained model.
# It leverages the pre-built Docker container to ensure the correct environment, including Python 2 dependencies.

# --- Configuration ---
# The parent directory of your custom corpus (e.g., 'pcc' which contains 'model', 'train', 'test', etc.)
CORPUS_NAME="pcc"

# --- Argument Validation ---
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <input_directory> <output_directory>"
  echo "Example: $0 data/pcc/test_input data/pcc/test_output"
  exit 1
fi
INPUT_DIR="$1"
OUTPUT_DIR="$2"

# --- Path Definitions ---
# These paths are relative to the project root and will be used inside the Docker container.
MODEL_DIR="data/$CORPUS_NAME/model"
MODEL_FILE="$MODEL_DIR/model.pickle.gz"
PROJMAT_FILE="$MODEL_DIR/projmat.pickle.gz"
RELATION_MAP="data/$CORPUS_NAME/${CORPUS_NAME}_rel_mapping.json"
DATAPATH="data/$CORPUS_NAME" # Path for vocabs etc.

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
# The following scripts use Stanza and will leverage the local GPU if available.
echo "Running Stanza preprocessing on the host machine..."
python3 run_stanza_preprocessing.py "$INPUT_DIR"

echo "Running BerkeleyParser on the host machine..."
python3 ger_4_txt2parse.py "$INPUT_DIR"

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