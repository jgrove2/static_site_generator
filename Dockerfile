# Use Python 3.11 slim image for building
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY static_site_generator.py .
COPY templates/ ./templates/

# Copy markdown files
COPY markdown/ ./markdown/

# Generate static HTML
RUN python static_site_generator.py --input-dir ./markdown --output-dir ./html

# Use nginx to serve static files
FROM nginx:alpine

# Copy generated HTML files to nginx
COPY --from=builder /app/html /usr/share/nginx/html

# Copy custom nginx configuration (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 