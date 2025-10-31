FROM python:3.12-slim

RUN useradd -m myuser

WORKDIR /new_chat_app_backend

COPY /new_chat_app_backend/requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./new_chat_app_backend .

RUN chown -R myuser:myuser /new_chat_app_backend

USER myuser

CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]

EXPOSE 8000