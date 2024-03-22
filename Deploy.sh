
source config/config.cfg

uvicorn app.main:app --host $host --port $port --workers $workers
