# Development Dockerfile for GeoStory Frontend
# For production, consider multi-stage builds and optimized image sizes

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
# Copying these first allows Docker to cache npm install layer
COPY package.json package-lock.json ./

# Install dependencies
# Using ci for clean install from package-lock.json
RUN npm ci

# Copy application source
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start Vite dev server with host binding for Docker
# --host 0.0.0.0 allows external connections
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
