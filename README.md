Run frontend with Gunicorn:

`/home/ubuntu/argh-frontend-website/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5010 app:app`
