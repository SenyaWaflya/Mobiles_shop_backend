FROM python:3.13-alpine

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

CMD ["uv", "run", "uvicorn", "--host", "0.0.0.0", "main:app", "--reload"]
