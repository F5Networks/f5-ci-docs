# Format: FROM    repository[:version]
FROM       ubuntu:latest

# Usage:
# docker run -it -v <your directory>:/documents/

ENV DEBIAN_FRONTEND noninteractive

# Update apt-get sources AND install stuff
RUN apt-get update && apt-get install -y -q \
    build-essential \
    git \
    openssh-server \
    pandoc \
    python-pip \
    python-sphinx \
    texlive \
    texlive-latex-extra




CMD ["/bin/bash"]
