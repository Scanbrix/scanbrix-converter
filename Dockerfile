# Use a Node.js base image
FROM node:18-bullseye

# Install Blender and system dependencies
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install the SketchUp Importer
# We unzip to a temp folder, find the actual addon folder, and move it
RUN mkdir -p /root/.config/blender/2.83/scripts/addons && \
    wget --no-check-certificate https://github.com/RedHaloStudio/Sketchup_Importer/archive/refs/tags/0.22.1.zip -O /tmp/plugin.zip && \
    unzip /tmp/plugin.zip -d /tmp/plugin_extracted && \
    mv /tmp/plugin_extracted/Sketchup_Importer-0.22.1/Sketchup_Importer /root/.config/blender/2.83/scripts/addons/ && \
    rm -rf /tmp/plugin.zip /tmp/plugin_extracted

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your code
COPY . .

EXPOSE 10000

CMD ["npm", "start"]
