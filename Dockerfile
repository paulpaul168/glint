FROM amd64/fedora
LABEL maintainer="paulpaul168"
COPY . .
RUN chmod +x install && ./install.sh
CMD ["./run.sh"]