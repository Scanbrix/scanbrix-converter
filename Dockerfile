# Use a Node.js base image
FROM node:18-bullseye

# Install Blender, Git, and system dependencies
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install the SketchUp Importer Plugin using Git Clone
RUN mkdir -p /root/.config/blender/2.83/scripts/addons && \
    git clone https://github.com/Space-Design/SketchUp_Importer.git /tmp/skp_repo && \
    mv /tmp/skp_repo/SketchUp_Importer /root/.config/blender/2.83/scripts/addons/ && \
    rm -rf /tmp/skp_repo

WORKDIR /app

# Install Node dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your code
COPY . .

EXPOSE 10000

CMD ["npm", "start"]
