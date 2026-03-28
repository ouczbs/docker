FROM python:3.10-slim
WORKDIR /app/anki
COPY anki-env /app/anki
ENV XDG_CONFIG_HOME=/data/anki
RUN cd /app/anki/shell/ && chmod 777 build.sh && chmod 777 start.sh
RUN /app/anki/shell/build.sh
COPY anki-sync-server /app/anki/anki-sync-server
CMD /app/anki/shell/start.sh
EXPOSE 27701
#CMD tail -f /dev/null