
# Instructions copied from - https://hub.docker.com/_/python/
FROM python:3.10-alpine

COPY . /app/
WORKDIR /app/

#COPY requirements.txt /
#RUN pip install -r /requirements.txt
RUN pip install -r requirements.txt

# tell the port number the container should expose
#EXPOSE 6027

#RUN python3 -m pytest .

# run the command
# CMD ["gunicorn", "-b", "0.0.0.0:6027", "-t", "600", "app_flask:create_app()"]
# CMD ["python3", "app_flask.py", "-d", "True"]
#CMD ["gunicorn", "-b", "0.0.0.0:6027", "--log-level=debug", "-t", "600", "--worker-class", "uvicorn.workers.UvicornWorker", "app_fastapi:create_app()"]
# CMD ["python3", "app_flask.py", "-d", "True"]
CMD ["fastapi", "run", "app/app_fastapi.py", "--proxy-headers", "--port", "80"]
#CMD uvicorn app.app_fastapi:app --reload --host 0.0.0.0 --port 8000
# RUN apk add --no-cache bash
