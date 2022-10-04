FROM kayvan/stockfish:latest as stockfish

FROM python:3.10

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100


WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY --from=stockfish /usr/local/bin/stockfish /usr/local/bin/stockfish

COPY src /code

EXPOSE 8000
CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "main:app"]
