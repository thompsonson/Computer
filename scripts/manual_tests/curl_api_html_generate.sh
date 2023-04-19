curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"message": "Generate a website that acts as an index page for information on AI capability and AI alignment. 
     The pages should include images that are generated from Dalle, please include the prompts for these. 
     The tone should be informative and fun, with a serious note around the Alignment."}' \
http://localhost:8080/api/html/generate | jq

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"message": "Generate a website that acts as an index page for information on AI capability and AI alignment."}' \
http://localhost:8080/api/html/generate 