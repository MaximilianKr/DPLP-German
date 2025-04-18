import os
import argparse
import subprocess


def run_local_preprocessing(input_path):
    os.system(f"python3 ger_3_ner.py {input_path}")
    os.system(f"python3 ger_4_txt2parse.py {input_path}")
    os.system(f"python3 ger_5_txt2conll.py {input_path}")


def run_docker_segmenter(input_path, datapath="data/de"):
    print("Running segmentation in Docker (Python 2)")
    subprocess.run([
        "docker", "run", "-it", "--rm",
        "-v", os.getcwd() + ":/home/DPLP",
        "-w", "/home/DPLP",
        "mohamadisara20/dplp-env:ger",
        "python2", "discoseg/ger_segmenter.py", input_path, "-d", datapath
    ])


def extract_edus(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for fname in os.listdir(input_dir):
        if fname.endswith('.merge'):
            edus = []
            with open(
                os.path.join(input_dir, fname), 'r', encoding='utf8'
            ) as f:
                lines = f.readlines()

            prev_edu = -1
            tokens = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                cols = line.split('\t')
                token = cols[2]
                edu_num = int(cols[-1])
                if edu_num != prev_edu and prev_edu != -1:
                    edus.append(' '.join(tokens))
                    tokens = []
                tokens.append(token)
                prev_edu = edu_num
            if tokens:
                edus.append(' '.join(tokens))

            out_file = os.path.join(
                output_dir, fname.replace(".merge", "_edus.txt")
            )
            with open(out_file, 'w', encoding='utf8') as f:
                for edu in edus:
                    f.write(edu.strip() + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("-o", "--output_path", required=True)
    args = parser.parse_args()

    run_local_preprocessing(args.input_path)
    run_docker_segmenter(args.input_path)
    extract_edus(args.input_path, args.output_path)
    print(f"Finished! EDU .txt files are in: {args.output_path}")
