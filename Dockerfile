FROM python:3.14-slim
ENV APP_FOLDER="/app"
ENV PYTHONPATH=${PYTHONPATH:-}:${APP_FOLDER}:.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_ROOT_USER_ACTION="ignore"
ENV PATH="/root/.local/bin:$PATH"
ENV PATH="${APP_FOLDER}/.venv/bin:$PATH"

WORKDIR ${APP_FOLDER}
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv
ADD pyproject.toml uv.lock ./
RUN uv sync --all-extras --frozen
ADD . ${APP_FOLDER}
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]