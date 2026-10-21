FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3001

# Set port for React dev server
ENV PORT=3001

# Start development server
CMD ["npm", "start"]
