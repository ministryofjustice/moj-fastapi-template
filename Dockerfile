ARG BASE_IMAGE=python:3.12-slim
FROM $BASE_IMAGE AS base

ARG REQUIREMENTS=requirements-production.txt

# Create a non-root user
RUN adduser --disabled-password app -u 1000 && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime

RUN mkdir /home/app/moj-fastapi-skeleton
WORKDIR /home/app/moj-fastapi-skeleton

COPY requirements/generated/$REQUIREMENTS requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app ./app
COPY bin ./bin
COPY alembic.ini ./alembic.ini

# Change ownership of the working directory to the non-root user
RUN chown -R app:app /home/app

# Cleanup container
RUN rm -rf /var/lib/apt/lists/*

# Switch to the non-root user
USER app

# Expose the fast api port
EXPOSE 8027

CMD ["uvicorn", "app:api", "--port",  "8027", "--host", "0.0.0.0"]
