FROM python:3.10-slim-buster

WORKDIR /root
ENV PYTHONPATH /root
RUN apt-get update && apt-get install -y git curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN pip install -U pandas numpy maturin "git+https://github.com/flyteorg/flytekit.git@master"

ENV PATH="/root/.cargo/bin:${PATH}"

COPY . /root/rustfs
RUN cd rustfs && maturin build && pip install target/wheels/rustfs*.whl
RUN rm -rf /root/rustfs  # Clean up

ENV FLYTE_SDK_RICH_TRACEBACKS 0
ENV RUST_BACKTRACE 1