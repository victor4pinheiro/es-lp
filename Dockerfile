# Stage 1: Build environment
FROM rust:1.75.0-slim-bookworm AS builder

WORKDIR /app

# Copy project files
COPY . .

# Build the application with sccache caching
RUN cargo build --release

# Stage 2: Runtime environment
FROM debian:bookworm-slim AS runner

WORKDIR /app

# Copy the built binary from the previous stage
COPY --from=builder /app/target/release/learning-elasticsearch /app

# Expose the ports
EXPOSE 8000

# Run the application
CMD ["./learning-elasticsearch"]
