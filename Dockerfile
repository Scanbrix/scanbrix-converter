FROM node:18-bullseye

# Install Blender and the missing C-library helpers
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    libgomp1 \
    libfreeimage3 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy Cython

WORKDIR /app
COPY . .

# Link the libraries so the SketchUp brain can find its muscles
ENV LD_LIBRARY_PATH=/app/sketchup_importer/slapi:$LD_LIBRARY_PATH

RUN npm install
EXPOSE 10000
CMD ["npm", "start"]
