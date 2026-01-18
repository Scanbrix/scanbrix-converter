FROM node:18-bullseye

# Install Blender and Linux system dependencies
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the entire repository (including sketchup_importer folder) into /app
COPY . .

# Install Node.js dependencies for the server
RUN npm install

EXPOSE 10000

# Start the Node.js server
CMD ["npm", "start"]
