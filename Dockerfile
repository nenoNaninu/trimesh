FROM python:3.9-slim-bullseye
LABEL maintainer="mikedh@kerfed.com"
ARG TRIMESH_PATH=/opt/trimesh

# Required for Python to be able to find libembree.
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Create a local non-root user.
RUN useradd -m -s /bin/bash user

# Install binary APT dependencies.
COPY docker/builds/apt.bash /tmp/
RUN bash /tmp/apt.bash

# Install various custom utilities and libraries.
COPY docker/builds/draco.bash /tmp/
RUN bash /tmp/draco.bash

COPY docker/builds/embree.bash /tmp/
RUN bash /tmp/embree.bash

# XVFB runs in the background if you start supervisor.
COPY docker/config/xvfb.supervisord.conf /etc/supervisor/conf.d/

# Copy local trimesh installation.
COPY --chown=user:user . "${TRIMESH_PATH}"

# Include all soft dependencies.
RUN pip install --no-cache-dir -e "${TRIMESH_PATH}[all,test]" pyassimp==4.1.3

# Switch to non-root user.
USER user

# Set environment variables for software rendering.
ENV XVFB_WHD="1920x1080x24"\
    DISPLAY=":99" \
    LIBGL_ALWAYS_SOFTWARE="1" \
    GALLIUM_DRIVER="llvmpipe"
