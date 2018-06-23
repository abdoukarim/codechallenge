FROM python:3.6.2

MAINTAINER karim_155@hotmail.com

RUN mkdir -p /usr/src/app
ENV APP_HOME=/usr/src/app
WORKDIR $APP_HOME

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application sources.
COPY . $APP_HOME

# Expose port 8888 to the Docker host, so we can access it from the outside.
EXPOSE 8888

# The main command to run when the container starts.
CMD ["python", "home.py"]
