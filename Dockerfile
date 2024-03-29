FROM python:3.11-alpine
WORKDIR /app
COPY . /app

RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirement.txt

CMD ["python", "-m", "bot"]
