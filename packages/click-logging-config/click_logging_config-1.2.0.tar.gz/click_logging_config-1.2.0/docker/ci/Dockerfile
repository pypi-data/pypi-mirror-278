# python:3.8-slim
FROM python@sha256:f8a12edddd4fb9c9fd38cd7147c5861a596dee5a4852b6bded3d1d6e2c8987bd AS venv

ARG project_dir=/tmp
ARG project_name
ARG venv_path

COPY . ${project_dir}/

# build-harness uses click-logging-config so have to take care of a potential
# circular dependency here that can causes pipeline issues.
RUN set -ex \
 && python3 -m venv ${venv_path} \
 && ${venv_path}/bin/pip install "${project_dir}[doc,test]" \
 && ${venv_path}/bin/pip uninstall -y ${project_name} \
 && ${venv_path}/bin/pip install -r "${project_dir}/docker/ci/requirements-dev.txt"


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

ARG python_version
ARG requirements_lock=/tmp/apt_requirements.lock
ARG venv_path

COPY docker/ci/apt2_requirements.lock "${requirements_lock}"

COPY --from=pyenv /pyenv-installer /pyenv-installer
COPY docker/ci/pyenv-python-versions /pyenv-python-versions

ENV PYENV_ROOT="/root/.pyenv"

RUN /bin/bash -c \
  "set -ex; \
  apt-get update; \
  xargs -a \"${requirements_lock}\" \
    apt-get install \
      -y \
      --no-install-recommends; \
  rm -rf /var/lib/apt/lists/*; \
  git config --global user.email \"you@example.com\"; \
  git config --global user.name \"Your Name\"; \
  source /pyenv-installer; \
  command -v pyenv >/dev/null || export PATH=\"\${PYENV_ROOT}/bin:\${PATH}\"; \
  for x in \$(cat /pyenv-python-versions | grep \"${python_version}\"); do \
    pyenv install \${x}; \
  done"

COPY --from=venv "${venv_path}" "${venv_path}"
