# Use a Rust base image
FROM rust:1.77-slim-bookworm as builder

# Set the working directory
WORKDIR /app

# Copy Cargo.toml and Cargo.lock to leverage Docker cache
COPY Cargo.toml Cargo.lock ./

# Build dummy project to cache dependencies
RUN mkdir src && echo "fn main() {}\n" > src/main.rs && \
    cargo build --release && rm -rf src

# Copy the source code
COPY src ./src

# Build the release binary
RUN cargo build --release

# Use a minimal base image for the final stage
FROM debian:bookworm-slim

# Set the working directory
WORKDIR /app

# Copy the built binary from the builder stage
COPY --from=builder /app/target/release/execution-engine .

# Copy the .env file from the root of the project (assuming it's in the same context as docker-compose.yml)
# This assumes the .env file is at the root of the sensex-scalper-supabase directory


# Run the application
CMD ["./execution-engine"]