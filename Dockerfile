FROM python:3.7-alpine
RUN cd /home/runner/work/gitlab-manager/gitlab-manager && ls -la
RUN pip install -r requirements.txt
ENTRYPOINT ["./gitlab-manager.py", "-h"] 
