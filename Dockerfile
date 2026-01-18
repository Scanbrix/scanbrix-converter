FROM node:18-bullseye

# Install Blender and Linux system dependencies
RUN apt-get update && apt-get install -y \
    blender \
    libglu1-mesa \
    libxi6 \
    libxrender1 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Cython to help Python read the 3D geometry files
RUN pip3 install Cython

WORKDIR /app

# Copy the entire repository into /app
COPY . .

# Install Node.js dependencies
RUN npm install

EXPOSE 10000

CMD ["npm", "start"]
