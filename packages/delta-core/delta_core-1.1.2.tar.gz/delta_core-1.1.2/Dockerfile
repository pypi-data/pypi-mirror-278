FROM python:3.11-slim
EXPOSE 8000
COPY delta /delta/app/delta
COPY gael.delta /delta/app/gael.delta
COPY alembic.ini log_config.json /delta/app/
COPY requirements.txt /delta/app/requirements.txt
WORKDIR /delta/app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["/bin/bash", "-c", "python -m delta.run.api.api"]
