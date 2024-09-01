# Use the latest Ubuntu image
FROM ubuntu:latest

# Set up a working directory
WORKDIR /usr/src/app

# Update the package list and install basic dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    curl \
    wget \
    python3 \
    python3-pip \
    python3-tk \
    graphviz \
    x11-apps \
    git \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install ANTLR
RUN mkdir /usr/local/lib/antlr && \
    curl -o /usr/local/lib/antlr/antlr-4.13.2-complete.jar https://www.antlr.org/download/antlr-4.13.2-complete.jar

# Set up ANTLR in the CLASSPATH
ENV CLASSPATH="/usr/local/lib/antlr/antlr-4.13.2-complete.jar"

# Set up aliases for ANTLR Tool and TestRig
RUN echo 'export CLASSPATH="/usr/local/lib/antlr/antlr-4.13.2-complete.jar:$CLASSPATH"' >> ~/.bashrc && \
    echo 'alias antlr4="java -jar /usr/local/lib/antlr/antlr-4.13.2-complete.jar"' >> ~/.bashrc && \
    echo 'alias grun="java org.antlr.v4.gui.TestRig"' >> ~/.bashrc

# Create a virtual environment and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install antlr4-python3-runtime graphviz

# Allow the container to use the host's display for Tkinter windows
ENV XDG_RUNTIME_DIR=/tmp