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

# Install the SketchUp Importer Plugin for Blender 2.83
# Using the specific release tag URL for better stability
RUN mkdir -p /root/.config/blender/2.83/scripts/addons && \
    curl -L https://github.com/Space-Design/SketchUp_Importer/archive/refs/tags/v0.23.0.zip -o /tmp/skp_importer.zip && \
    unzip /tmp/skp_importer.zip -d /tmp && \
    mv /tmp/SketchUp_Importer-0.23.0/SketchUp_Importer /root/.config/blender/2.83/scripts/addons/ && \
    rm -rf /tmp/skp_importer.zip /tmp/SketchUp_Importer-0.23.0

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your code
COPY . .

EXPOSE 10000

CMD ["npm", "start"]
