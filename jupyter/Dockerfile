FROM almalinux:8 as jupyter
USER root
ENV ROOT_DIR /root/docker
WORKDIR /data/jupyter
COPY --from=ouczbs:miniconda ${ROOT_DIR} ${ROOT_DIR}
RUN cat ${ROOT_DIR}/miniconda.bashrc >> /root/.bashrc && rm ${ROOT_DIR}/miniconda.bashrc &&\
    source ~/.bashrc && mv ${ROOT_DIR}/tini /tini && chmod +x /tini

RUN source ~/.bashrc && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/  &&\
    conda config --set show\_channel\_urls yes &&\
    conda install jupyter notebook -y &&  jupyter notebook --generate-config

VOLUME [ "/data" ]
COPY conf/pip.conf /root/.pip/pip.conf
COPY conf/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
COPY shell/start.sh /usr/local/bin/start.sh
RUN chmod 777 /usr/local/bin/start.sh

EXPOSE 8888
CMD bash /usr/local/bin/start.sh
ENTRYPOINT ["/tini", "--"] CMD

