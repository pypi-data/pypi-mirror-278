from finter.settings import logger
import os


def prepare_docker_submit_files(model_name):
    """
    Copy the poetry.lock and pyproject.toml files to the model directory.
    """

    os.system(f"cp poetry.lock pyproject.toml {model_name}")
    logger.info("Moved poetry.lock and pyproject.toml to model directory.")


    run_docker_script = """
from am import Alpha
import os

KEY = os.environ.get("KEY")
SECRET = os.environ.get("SECRET")
REGION = os.environ.get("REGION")
NAME = os.environ.get("NAME")

start = os.environ.get("START")
end = os.environ.get("END")

storage_options = {
    "key": KEY,
    "secret": SECRET,
    "client_kwargs": {
        "region_name": REGION
    }
}

alpha = Alpha().get(int(start), int(end))

alpha.to_parquet(f"s3://finter-parquet-temp/{NAME}.parquet", engine="pyarrow", storage_options=storage_options)
"""

    filename = "run.py"

    full_path = os.path.join(model_name, filename)

    with open(full_path, "w") as file:
        file.write(run_docker_script)

    logger.info(f"{filename} saved to {full_path}")


    dockerfile = """
ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim as builder

COPY . /app

WORKDIR /app

RUN pip install poetry==1.8.3

RUN python -m poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root


CMD ["python", "run.py"]
"""

    filename = "Dockerfile"

    full_path = os.path.join(model_name, filename)

    with open(full_path, "w") as file:
        file.write(dockerfile)

    logger.info(f"{filename} saved to {full_path}")
