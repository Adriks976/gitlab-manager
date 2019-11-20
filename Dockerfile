FROM python:3.7-alpine
COPY requirements.txt /requirements.txt
COPY gitlab-manager /usr/bin/gitlab-manager
RUN pip install -r requirements.txt
ENTRYPOINT ["gitlab-manager"]
CMD [gitlab-manager] 
