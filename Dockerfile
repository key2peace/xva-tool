# ==============================================================================
#                      XVATOOL ENTERPRISE DOCKER CONTAINER
# ==============================================================================
FROM debian:stretch-slim

# Maintainer metadata properties mapping alignment
LABEL maintainer="Alexander Maassen <outsider@cuci.nl>"
LABEL description="Advanced Zero-Copy Streaming Core Engine for Citrix XenServer"

# Enforce non-interactive frontend during package build execution phase
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal production system dependencies (Python 2.7 standard libraries runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
	python2.7 \
	python-minimal \
	&& rm -rf /var/lib/apt/lists/*

# Fix python binary alias path mappings to target standard python runtime environment
RUN ln -s /usr/bin/python2.7 /usr/bin/python

# Allocate framework runtime orchestration directory structures
WORKDIR /app

# Clone active core executable bundles and templates into the system container path
COPY xva-tool /usr/local/bin/xva-tool
COPY xvapkg /usr/local/bin/xvapkg
COPY xva-tool.conf.example /etc/xva-tool/conf-available/global.conf
RUN chmod +x /usr/local/bin/xva-tool /usr/local/bin/xvapkg

# Establish internal shared bind mountpoints for localized volume storage array access
VOLUME ["/data", "/etc/xva-tool", "/var/log"]

# Set the standalone core script engine as the immutable execution entrypoint
ENTRYPOINT ["/usr/local/bin/xva-tool"]
