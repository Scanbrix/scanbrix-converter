FROM node:18-bullseye

# Install Blender
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy everything including the sketchup_importer folder
COPY . .

# Install Node dependencies
RUN npm install

EXPOSE 10000
CMD ["npm", "start"]
