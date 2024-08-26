# How to use:
# 1- execute directly with: python3 ger_rest_api.py
# 2- or as a docker container with:
#    docker run -d -p 5000:5000 -v $(pwd):/home/DPLP -w /home/DPLP mohamadisara20/dplp-env python3 ger_rest_api.py
#    Check for errors with: docker logs
# 3- send a POST request with a `text` arg, like: {text: 'I am mat. I am sad'}
# you can send the request from terminal:
#        curl -d '{"text":"baeldung"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/dplp
 

from flask import Flask, request, jsonify
import uuid 
import os
import argparse

root_path = './rstout'
download_base_url = 'rstout'
file_name = 'document'
args = {}

app = Flask(__name__)

def initialize_files(uid, text):
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    
    path = f'{root_path}/{uid}'
    if not os.path.exists(path):
        os.mkdir(path)
    
    with open(f'{path}/{file_name}.txt', 'w') as f:
        f.write(text)
    
    return path

@app.post("/dplp")
def dplp():
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415

    uid = uuid.uuid4()
    req = request.get_json()
    text = req["text"]
    
    path = initialize_files(uid, text)
    os.system(f'python3 ger_predict_dis_from_txt.py {path} -o {path} -p {args.fprojmat} -m {args.fmodel} -d {args.datapath}')
    
    response = {"uid": uid}
    response['dis_url'] = f'{download_base_url}/{uid}/{file_name}.dis'
    dis_file = f'{path}/{file_name}.dis'
    if os.path.exists(dis_file):
        with open(dis_file, 'r') as f:
            response["dis"] = f.read()
    
        rs3_file = f'{path}/{file_name}.rs3'
        if os.path.exists(rs3_file):
            with open(rs3_file, 'r') as f:
                response["rs3"] = f.read()
            response['rs3_url'] = f'{download_base_url}/{uid}/{file_name}.rs3'

    
    return response, 201

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog= os.path.basename(__file__),
        description='A RESTful API endpoint for RST parser, listening on port 5000 by default.',
    )

    parser.add_argument("-p", "--fprojmat", type=str, default='data/de/model/projmat.pickle.gz', help="The projection matrix pickle file.")
    parser.add_argument("-m", "--fmodel", type=str, default='data/de/model/model.pickle.gz', help="The trained model file.")
    parser.add_argument("-d", "--datapath", type=str, default='data/de', help="Path to the training data files (vocabs, ...)")
    parser.add_argument("-o", "--outpath", type=str, help="The path of the output dis and rs3 files.")
    parser.add_argument("-r", "--port", type=int, help="The endpoint's port number.")
    # TODO: add argument for segmenter model
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)

