FROM python:{PYTHON_VERSION}-alpine3.9

ADD . .
RUN pip install -e . && pip install $FLAKE8_VERSION$
RUN python setup.py test
RUN flake8 tests/issues
