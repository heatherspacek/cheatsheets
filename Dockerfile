FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY uv.lock pyproject.toml .
RUN uv sync --locked

ADD . /
WORKDIR /src

CMD ["uv", "run", "python", "frontend.py"]