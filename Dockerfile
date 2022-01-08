FROM amd64/fedora
LABEL maintainer="paulpaul168"

COPY . .
RUN chmod +x install.sh && chmod +x run.sh && ./install.sh

# Frontend and backend ports respecitvly 
EXPOSE 3000
EXPOSE 5000
ENTRYPOINT [ "bin/bash", "run.sh" ] 