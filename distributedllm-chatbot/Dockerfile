# Use an official Node.js runtime as a parent image
FROM node:16

# Install Python 3.7 and required libraries
RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip build-essential libyaml-dev && \
    apt-get clean

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Install a specific version of pyyaml
RUN pip3 install pyyaml==5.4.1

# Install other Python dependencies
RUN pip3 install --no-cache-dir panel ctransformers

# Copy the rest of the application code
COPY . .


# Expose the port that Panel will serve the app on
EXPOSE 5006
# Set the environment variable for Bokeh WebSocket origin
ENV BOKEH_ALLOW_WS_ORIGIN=localhost:5007

# Start the app with npm start, which runs `panel serve chatbot.py`
CMD [ "npm", "start" ]

