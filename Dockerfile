FROM python:3.11-slim

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root
COPY  smart_vendor ./smart_vendor

COPY . .

COPY .env .env

COPY entrypoint.sh code/entrypoint.sh

RUN chmod +x code/entrypoint.sh

EXPOSE 80

ENTRYPOINT [ "/code/entrypoint.sh" ]

