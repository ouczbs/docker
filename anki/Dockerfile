FROM python:3.10-slim
WORKDIR /app/anki
COPY anki-env /app/anki/anki-env
ENV XDG_CONFIG_HOME=/data/anki
RUN chmod +x /app/anki/anki-env/shell/build.sh /app/anki/anki-env/shell/start.sh && \
    cd /app/anki/anki-env && pip install -r conf/requirements.txt && pip install pyzstd
COPY anki-sync-server /app/anki/anki-sync-server
CMD /app/anki/anki-env/shell/start.sh
EXPOSE 27001