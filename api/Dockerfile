FROM python:3

WORKDIR /api

COPY requirements.txt /api
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /api

CMD ["python3", "app.py"]
