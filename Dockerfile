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

# Install the SketchUp Importer - Flattening the folder structure
RUN mkdir -p /root/.config/blender/2.83/scripts/addons/Sketchup_Importer && \
    wget --no-check-certificate https://github.com/RedHaloStudio/Sketchup_Importer/archive/refs/tags/0.22.1.zip -O /tmp/plugin.zip && \
    unzip /tmp/plugin.zip -d /tmp/plugin_extracted && \
    # This specifically moves the contents of the internal folder to our target
    cp -v -r /tmp/plugin_extracted/Sketchup_Importer-0.22.1/Sketchup_Importer/* /root/.config/blender/2.83/scripts/addons/Sketchup_Importer/ && \
    rm -rf /tmp/plugin.zip /tmp/plugin_extracted

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your code
COPY . .

EXPOSE 10000

CMD ["npm", "start"]
