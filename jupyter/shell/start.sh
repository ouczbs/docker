#!/bin/sh
source ~/.bashrc
echo "start success jupyter-notebook"
#nohub jupyter notebook --allow-root > /data/jupyter.log 2>&1
jupyter notebook
echo "exist jupyter-notebook ? why?"