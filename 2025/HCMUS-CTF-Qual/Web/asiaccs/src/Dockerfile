FROM tiangolo/uwsgi-nginx-flask:python3.12

# Update system packages and install Python packages
RUN apt update && apt install -y --no-install-recommends \
    && pip install Flask \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN adduser --disabled-password --gecos "" hello

# Set working directory
WORKDIR /app

# Copy application files
COPY main .

# Initialize the database
RUN python3 init_db.py

# Set ownership and permissions
RUN chown -R root:hello /app \
    && chmod 444 /app/database.db
