#!/bin/bash
# Simple bash script to test the API using curl

API_URL="http://localhost:8000"

echo "============================================================"
echo "Testing Backend API with curl"
echo "============================================================"

echo -e "\n1. Health Check:"
echo "------------------------------------------------------------"
curl -s -X GET "$API_URL/health" | python3 -m json.tool

echo -e "\n\n2. JavaScript Analysis:"
echo "------------------------------------------------------------"
curl -s -X POST "$API_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "const x = \"hello\";\nconst y = x.length();",
    "error_message": "TypeError: x.length is not a function",
    "language": "javascript"
  }' | python3 -m json.tool

echo -e "\n\n3. JavaScript Undefined Error:"
echo "------------------------------------------------------------"
curl -s -X POST "$API_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "const arr = undefined;\nconst result = arr.map(x => x * 2);",
    "error_message": "TypeError: Cannot read property '\''map'\'' of undefined",
    "language": "javascript"
  }' | python3 -m json.tool

echo -e "\n\nDone!"

