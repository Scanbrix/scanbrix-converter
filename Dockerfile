# Use a Node.js base image
FROM node:18-bullseye

# Install Blender and system dependencies
# Added wget as it's more reliable for GitHub downloads
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install the SketchUp Importer Plugin using wget
RUN mkdir -p /root/.config/blender/2.83/scripts/addons && \
    wget --no-check-certificate https://github.com/Space-Design/SketchUp_Importer/archive/refs/heads/master.zip -O /tmp/skp_importer.zip && \
    unzip /tmp/skp_importer.zip -d /tmp && \
    mv /tmp/SketchUp_Importer-master/SketchUp_Importer /root/.config/blender/2.83/scripts/addons/ && \
    rm -rf /tmp/skp_importer.zip /tmp/SketchUp_Importer-master

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your code
COPY . .

EXPOSE 10000

CMD ["npm", "start"]
