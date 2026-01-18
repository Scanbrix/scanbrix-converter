FROM node:18-bullseye

# Install Blender and system dependencies
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 1. Create the SYSTEM addon directory (this is where Blender 2.83 on Debian lives)
RUN mkdir -p /usr/share/blender/scripts/addons/sketchup_importer

# 2. Copy the folder from your repo into the SYSTEM folder
COPY sketchup_importer/ /usr/share/blender/scripts/addons/sketchup_importer/

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 10000
CMD ["npm", "start"]
