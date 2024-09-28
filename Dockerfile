FROM python

WORKDIR /app
COPY . /app

# install geckodriver and firefox
RUN apt-get update && apt-get install -y curl wget jq

RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r '.tag_name') && \
    echo "Geckodriver version: $GECKODRIVER_VERSION" && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN tar -zxf geckodriver-*.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-*.tar.gz


RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP



# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install -r requirements.txt

# ENTRYPOINT [ "Python3", "like_comments_i3.py" ]