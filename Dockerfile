# Run German RST parser's restful API in a Docker container:  docker run -d -p 5000:5000 -v $(pwd):/home/DPLP -w /home/DPLP mohamadisara20/dplp-env:latest python3 ger_rest_api.py
# It loads a web server listening to port 5000 and accepts json requests on path `./dplp` with the form {"text": "Some German Test"}
# 
# It can be tested from terminal with: curl -X POST http://127.0.0.1:5000/dplp -H 'Content-Type: application/json' -d '{"text": "How do you do"}' 

FROM mohamadisara20/dplp-env:latest

