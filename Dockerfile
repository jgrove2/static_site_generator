# Stage 1: Build static site
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and assets
COPY main.py .
COPY src/ ./src/
COPY templates/ ./templates/
COPY content/ ./content/

# Generate static HTML into /app/output
RUN python main.py

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy generated site into Nginx's html directory
COPY --from=builder app/dist /usr/share/nginx/html

# Expose port 80 (default for Nginx)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]