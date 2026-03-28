FROM --platform=linux/amd64 rust:1.65.0

# System packages 
ENV ROOT_DIR /root/docker
COPY --from=ouczbs:miniconda ${ROOT_DIR}/miniconda3 ${ROOT_DIR}/miniconda3

# configure & update conda
USER root
ENV PATH=${ROOT_DIR}/miniconda3/bin:${PATH}
COPY conf/pip.conf root/pip.conf 
RUN conda init bash && \
    conda update -y conda && \
    conda install -c anaconda cmake -y && \
    conda install -y nb_conda_kernels jupyterlab

# install evcxr_jupyter
## by setting GIT_FETCH_WITH_CLI option,
## Cargo will use the git executable to fetch registry indexes and git dependencies
COPY conf/config.conf root/.cargo/config 
#RUN cargo install evcxr_jupyter && evcxr_jupyter --install
#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8899", "--notebook-dir=/opt/notebooks", "--allow-root", "--no-browser"]
CMD tail -f /dev/null