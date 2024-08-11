# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory inside the frontend folder in the container
WORKDIR /app/frontend

# Copy the package.json and package-lock.json files to the working directory
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY frontend/ ./

# Build the app
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
