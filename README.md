## ⚙️ How to install chrome and chrome driver

### Install Google Chrome

1. Curl downloads the google-chrome binary.
2. Rename google-chrome-stable to google-chrome (webdriver will find the "google-chrome")
3. Print google-chrome version
```bash
curl https://intoli.com/install-google-chrome.sh | bash
mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
google-chrome --version
```

### Install ChromeDriver

1. Navigating to the `/tmp/`
2. Download the chrome driver that match the version of google-chrome binary (already installed above)
    
    - You can find the chrome driver [this](https://chromedriver.chromium.org/downloads)
3. Unzip the zip file
4. Move chromedriver to `/usr/bin/`
5. Check chromedriver version

```bash
cd /tmp/
wget https://chromedriver.storage.googleapis.com/[Version]/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chromedriver --version
```


## ⚙️ Enviroment setting

```bash
cd genie_crawler
conda init
(base) . ~/.bashrc
(base) conda create -n crawling python=3.10 -y
(base) conda activate crawling
(crawling) pip install -r requirements.txt

```


## 🔨 How to set pre-commit config

```bash
pip install pre-commit
# Used in case of locale related errors
# apt install locales locales-all 
pre-commit install
```


## 💡 How to run

```bash
python main.py
```