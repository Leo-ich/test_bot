# python (Debian)
FROM python:3.5-slim as base

LABEL "description"="Telegram bot"

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

#----------------------------------------------------------
FROM base AS python-deps

RUN apt-get update
#    && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /venv
COPY requirements.txt ./
RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install -r requirements.txt

#----------------------------------------------------------
FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /venv /venv
ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
USER appuser

WORKDIR /home/appuser/app

# Install application into container
COPY --chown=appuser ./ ./

# Run the application
ENTRYPOINT ["gunicorn", "app:app"]
CMD ["--workers", "1", "--log-file", "-"]
#CMD ["/usr/bin/env", "bash"]