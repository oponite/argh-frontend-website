Run frontend with Gunicorn:

`BACKEND_URL=http://127.0.0.1:8000 /home/ubuntu/argh-frontend/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5010 app:app`

The frontend proxies projection requests to `POST $BACKEND_URL/api/basketball/projection`.
