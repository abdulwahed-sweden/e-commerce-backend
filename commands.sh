tree -I '.git|__pycache__|.venv|venv|.mypy_cache|.pytest_cache' -a -L 3 > STRUCTURE.txt

cat STRUCTURE.txt



curl -X 'POST' \
  'http://localhost:8000/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "admin@company.se",
  "password": "SecureAdmin123"
}'