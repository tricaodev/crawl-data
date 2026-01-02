# How to run source
# 1. Clone repo: ```git clone https://github.com/tricaodev/travis-perkins-crawler.git```
# 2. Open Terminal: ```Window -> Type Terminal -> Enter```
# 3. Go to working directory: ```cd travis-perkins-crawler```
# 4. Create virtual environment: ```python -m venv .venv```
# 5. Active virtual environment (on Window): ```./.venv/Scripts/activate```
# 6. Install python package: ```pip install -r .\requirements.txt```
# 4. Run crawler:
* ```python main.py``` -> Crawl data without login to get retail price
* ```python main.py --mode trade``` -> Login before crawl data to get trade price