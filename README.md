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