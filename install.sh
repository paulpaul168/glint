#!/bin/bash
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    OS=$DISTRIB_ID
    VER=$DISTRIB_RELEASE
elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    OS=Debian
    VER=$(cat /etc/debian_version)
elif [ -f /etc/SuSe-release ]; then
    # Older SuSE/etc.
    ...
elif [ -f /etc/redhat-release ]; then
    # Older Red Hat, CentOS, etc.
    ...
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
    VER=$(uname -r)
fi

install_fedora(){
    echo "Welcome to the dark side. Starting Installation...";
    sudo dnf -y install python3.9 python3-pip python3-gunicorn python3-toml python3-flask\
                golang-go golang-honnef-tools \
                php-cli \
                nodejs \
                cargo rust clippy

    sudo chmod +x run.sh
    cd backend
    python3.9 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    go install github.com/securego/gosec/v2/cmd/gosec@latest
    npm install eslint --save-dev

    cd ../frontend
    npm install

    NODE_VER=$(node --version)
    if [ "17" = ${NODE_VER:1:2} ]; then
        echo "Node version is $NODE_VER (major version = 17) -> applying fix: See this git issue (https://github.com/webpack/webpack/issues/14532) for info"
        export NODE_OPTIONS=--openssl-legacy-provider
    fi
    npm install -g serve
    npm run build

}

install_ubuntu(){
    echo "Why would you use Ubuntu? Whatever! Starting Installation...";
    sudo apt -y install python3.9 python3-pip python3-venv python3-gunicorn python3-toml python3-flask\
                        golang-go golang-golang-x-tools-dev \
                        php-cli \
                        nodejs \
                        cargo


    sudo chmod +x run.sh
    cd backend
    python3.9 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    go install github.com/securego/gosec/v2/cmd/gosec@latest
    npm install eslint --save-dev
    #rustup component add clippy

    cd ../frontend
    npm install
    NODE_VER=$(node --version)
    if [ "17" = ${NODE_VER:1:2} ]; then
        echo "Node version is $NODE_VER (major version = 17) -> applying fix: See this git issue (https://github.com/webpack/webpack/issues/14532) for info"
        export NODE_OPTIONS=--openssl-legacy-provider
    fi
    npm install -g serve
    npm run build
}

SUPPORTED_OS="Fedora Linux"
SECOND_SUPPORTED_OS="Ubuntu"

#echo $OS;
#echo $VER;

if [ "$OS" = "$SUPPORTED_OS" ]; then
    install_fedora
elif [ "$OS" = "$SECOND_SUPPORTED_OS" ]; then   
    install_ubuntu
else
    echo "Sorry. We are racist and only support Fedora or Ubuntu.";
fi


