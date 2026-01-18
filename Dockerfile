FROM node:18-bullseye

# Install Blender and system dependencies
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Create the addon directory
RUN mkdir -p /root/.config/blender/2.83/scripts/addons

# COPY the folder from your GitHub repo into the Blender addons path
# Use lowercase 'sketchup_importer' to match your screenshot
COPY sketchup_importer/ /root/.config/blender/2.83/scripts/addons/sketchup_importer/

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 10000
CMD ["npm", "start"]
