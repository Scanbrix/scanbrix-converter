FROM node:18-bullseye

RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy Cython

WORKDIR /app
COPY . .

# --- CRITICAL: LINK THE C-LIBRARIES ---
# This tells Linux to look inside your slapi folder for the SketchUp engine
ENV LD_LIBRARY_PATH=/app/sketchup_importer/slapi:$LD_LIBRARY_PATH

RUN npm install
EXPOSE 10000
CMD ["npm", "start"]
