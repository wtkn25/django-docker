FROM python:3.9-slim-buster

# 各パッケージインストール
RUN apt-get update && \
    apt-get -y install gcc libmariadb-dev

# Poetryを導入
RUN pip install poetry

# 仮想環境の作成を無効化
RUN poetry config virtualenvs.create false

# ワーキングディレクトリ
RUN mkdir /app
WORKDIR /app

# pyproject.tomlとpoetry.lockを読む
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

# 
RUN poetry install


