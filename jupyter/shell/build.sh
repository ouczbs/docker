mkdir /data/jupyter
yum update -y && \
    yum upgrade -y && \
    yum install -y \
    sudo \
    wget && \
    yum clean all && rm -rf /var/lib/apt/lists/*
    
cat ./config/miniconda.bashrc >> /root/.bashrc
wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh &&\
    chmod 777 Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -f && \
    rm -f Miniconda3-latest-Linux-x86_64.sh && \
    source ~/.bashrc
    
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/  &&\
    conda config --set show\_channel\_urls yes &&\
    conda install jupyter notebook -y &&  jupyter notebook --generate-config
    
cp ./config/pip.conf /root/.pip/pip.conf
cp ./config/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
cp ./config/jupyter.service /etc/systemd/system/jupyter.service

systemctl enable jupyter.service
systemctl start jupyter.service