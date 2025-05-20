web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker fastapi_wrapper:app --host 0.0.0.0 --port $PORT
