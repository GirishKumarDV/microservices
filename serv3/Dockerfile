FROM python:3
WORKDIR /login
COPY . /login
RUN pip install -r requirements.txt
EXPOSE 5000
CMD flask run --host 0.0.0.0