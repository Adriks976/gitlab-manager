FROM python:3.7-alpine
RUN pip install -r requirements.txt
ENTRYPOINT ["./gitlab-manager.py", "-h"] 
