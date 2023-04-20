curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer token1" \
     -d '{"message": "Sample message for evaluation."}' \
http://localhost:8080/api/eithicalai/evaluate_message | jq
