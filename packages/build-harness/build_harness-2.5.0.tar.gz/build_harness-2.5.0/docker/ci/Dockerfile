# python:3.8-slim
FROM python@sha256:f8a12edddd4fb9c9fd38cd7147c5861a596dee5a4852b6bded3d1d6e2c8987bd as pyenv

ARG requirements_lock=/tmp/apt_requirements.lock

COPY docker/ci/apt1_requirements.lock "${requirements_lock}"

# Acquire pyenv installer
RUN /bin/bash -c  \
  "set -x; \
  apt-get update; \
  xargs -a \"${requirements_lock}\" \
    apt-get install \
      -y \
      --no-install-recommends; \
  /usr/bin/curl -L \
    https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer \
    > /pyenv-installer"


# python:3.8-slim
FROM python@sha256:f8a12edddd4fb9c9fd38cd7147c5861a596dee5a4852b6bded3d1d6e2c8987bd

ARG init_pyenv=/tmp/initialize_pyenv.sh
ARG project_dir=/tmp
ARG python_version
ARG requirements_lock=/tmp/apt_requirements.lock
ARG venv_path

COPY docker/ci/apt2_requirements.lock "${requirements_lock}"

COPY --from=pyenv /pyenv-installer /pyenv-installer
COPY docker/ci/pyenv-python-versions /pyenv-python-versions

ENV PYENV_ROOT="/root/.pyenv"

COPY . ${project_dir}/
COPY docker/ci/initialize_pyenv.sh "${init_pyenv}"

RUN set -ex \
    && chmod +x "${init_pyenv}" \
    && "${init_pyenv}"
