FROM node:18-bullseye

RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Create the target directory
RUN mkdir -p /usr/share/blender/scripts/addons/sketchup_importer

# Copy EVERYTHING from your local folder into the Blender path
# We use . to mean "everything inside the current directory's sketchup_importer folder"
COPY sketchup_importer/. /usr/share/blender/scripts/addons/sketchup_importer/

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 10000
CMD ["npm", "start"]
