FROM python:3.7-alpine
COPY requirements.txt /requirements.txt
COPY gitlab-manager.py /usr/bin/gitlab-manager.py
RUN pip install -r requirements.txt
ENTRYPOINT ["gitlab-manager.py", "-h"] 
