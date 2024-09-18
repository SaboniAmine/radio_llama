# Use the official Node.js image.
FROM node:22-alpine

# Set the working directory.
WORKDIR /app

# Copy the package.json and package-lock.json files.
COPY package*.json ./

# Install dependencies.
RUN npm install

# Copy the rest of the application.
COPY . .

# Expose the port that the app runs on.
EXPOSE 3000

# Command to run the application.
CMD ["npm", "run", "dev"]
