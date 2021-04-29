from python:3.9.4-slim


# set work dir
WORKDIR /app

# prepare environment [copy dependencies files, install all dependencies]
COPY requirements.txt Pipfile Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --system --deploy

# copy all project
COPY . .

# set command for running
CMD ["python", "tg_note_bot/__main__.py"]