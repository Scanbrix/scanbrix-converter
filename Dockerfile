# Use a Node.js base image
FROM node:18-bullseye

# Install Blender and system dependencies
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install the SketchUp Importer Plugin for Blender
# We download the latest stable release from GitHub
RUN mkdir -p /root/.config/blender/3.4/scripts/addons && \
    curl -L https://github.com/Space-Design/SketchUp_Importer/releases/download/v0.23.0/SketchUp_Importer.zip -o /tmp/skp_importer.zip && \
    unzip /tmp/skp_importer.zip -d /root/.config/blender/3.4/scripts/addons && \
    rm /tmp/skp_importer.zip

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your code
COPY . .

EXPOSE 10000

CMD ["npm", "start"]
