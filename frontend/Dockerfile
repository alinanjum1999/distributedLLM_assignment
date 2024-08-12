# Use the official Node.js image as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the React app
RUN npm run build

# Install `serve` to serve the build directory
RUN npm install -g serve

# Expose the port that the app will run on
EXPOSE 3000

# Serve the app using `serve` (use the build directory)
CMD ["serve", "-s", "build", "-l", "8080"]
