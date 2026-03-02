FROM ubuntu:latest

RUN apt-get update \  
    && apt-get install -y \
        curl \  
        git \  
        build-essential \  
        python3 \  
        python3-pip \  
    && rm -rf /var/lib/apt/lists/* 

CMD ["/bin/bash"]