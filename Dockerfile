FROM python:3-slim AS base

FROM base AS build

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y build-essential \
    python3 libpython3-dev python3-venv \
    libssl-dev libffi-dev cargo

RUN pip3 install -U pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt -t /app
RUN find . -name __pycache__ -exec rm -rf -v {} +
COPY . .

FROM base

WORKDIR /app
COPY --from=build /app .

CMD ["python","-u","main.py"]
