FROM ubuntu:22.04
USER root
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /data/jupyter

# 安装基础依赖
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Miniconda
RUN wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh &&\
    chmod 777 Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm -f Miniconda3-latest-Linux-x86_64.sh

# 设置环境变量
ENV PATH="/opt/miniconda/bin:$PATH"
RUN echo 'export PATH="/opt/miniconda/bin:$PATH"' >> ~/.bashrc

# 配置 conda 镜像并安装 jupyter
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ &&\
    conda config --set show_channel_urls yes &&\
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main &&\
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r &&\
    conda install jupyter notebook -y && \
    jupyter notebook --generate-config

# 复制配置文件
COPY conf/pip.conf /root/.pip/pip.conf
COPY conf/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
COPY shell/start.sh /usr/local/bin/start.sh
RUN chmod 777 /usr/local/bin/start.sh

# 下载 tini (如果需要)
# RUN wget -q https://github.com/krallin/tini/releases/download/v0.19.0/tini-static -O /tini && chmod +x /tini

VOLUME [ "/data" ]

EXPOSE 8888

CMD ["/bin/sh", "-c", "export PATH=/opt/miniconda/bin:$PATH && jupyter notebook --ip=0.0.0.0"]