FROM centos:7
USER root
ENV ROOT_DIR /root/docker
WORKDIR ${ROOT_DIR}
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN yum update -y && \
    yum upgrade -y && \
    yum install -y \
    sudo \
    git \
    wget && \
    yum clean all && rm -rf /var/lib/apt/lists/*

COPY tini ${ROOT_DIR}/tini
RUN cp ${ROOT_DIR}/tini /tini && chmod +x /tini

RUN wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh &&\
    chmod 777 Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -f -p ${ROOT_DIR}/miniconda3 && \
    rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PATH=${ROOT_DIR}/miniconda3/bin:${PATH}
CMD tail -f /dev/null
COPY shell ${ROOT_DIR}
RUN cat ${ROOT_DIR}/miniconda.bashrc >> ~/.bashrc && source ~/.bashrc && bash shell/env.sh
ENTRYPOINT ["/tini", "--"] CMD