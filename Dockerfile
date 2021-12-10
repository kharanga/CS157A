FROM python:3

RUN useradd --create-home --shell /bin/bash app_user

WORKDIR /home/app_user

USER app_user

COPY ./ .

RUN pip3 install mysql-connector-python
RUN pip3 install tabulate

CMD ["bash"]