FROM python
COPY ./app /app
RUN pip3 install -r /app/requirements.txt
CMD ["python3", "/app/app.py"]
