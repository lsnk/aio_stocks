FROM rust:1-buster

WORKDIR /app

COPY src/ src
COPY Cargo.lock .
COPY Cargo.toml .

RUN RUSTFLAGS="-C target-cpu=native" cargo build --release

EXPOSE 8002

CMD "./target/release/aio_stocks"
