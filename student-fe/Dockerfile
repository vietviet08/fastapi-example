# Multi-stage build for Vue.js frontend
FROM node:18-alpine as build-stage

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage

# Copy built assets from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx configuration (optional, for SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
