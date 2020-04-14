FROM python:3.7-alpine
WORKDIR /mysymp
COPY . /mysymp
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "symp.py"]

