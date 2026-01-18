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

# Install the RedHaloStudio SketchUp Importer for Blender 2.83
# We use the v0.22.1 release which specifically supports Blender 2.80+
RUN mkdir -p /root/.config/blender/2.83/scripts/addons && \
    wget --no-check-certificate https://github.com/RedHaloStudio/Sketchup_Importer/releases/download/0.22.1/Sketchup_Importer.zip -O /tmp/skp_importer.zip && \
    unzip /tmp/skp_importer.zip -d /root/.config/blender/2.83/scripts/addons && \
    rm -rf /tmp/skp_importer.zip

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your code
COPY . .

EXPOSE 10000

CMD ["npm", "start"]
