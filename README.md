# How to run source
# 1. Install python: https://www.python.org/downloads/
<img width="1906" height="987" alt="image" src="https://github.com/user-attachments/assets/a68a2ef4-b25d-4040-bb66-3010dd225bd0" />

# 2. Open Terminal: ```Window -> Type Terminal -> Enter```
# 3. Clone repo: ```git clone https://github.com/tricaodev/crawl-data.git```
# 4. Go to working directory: ```cd crawl-data```
<img width="1097" height="255" alt="image" src="https://github.com/user-attachments/assets/d9a3f0bb-5f20-4ec8-beb4-e77f5bd6f5a0" />

# 5. Create virtual environment: ```python -m venv .venv```
# 6. Active virtual environment
* Window: ```./.venv/Scripts/activate```
* MacOS: ```source ./.venv/bin/activate```
<img width="1829" height="341" alt="image" src="https://github.com/user-attachments/assets/e9abb8cf-9973-4de4-8ca1-29585b1566a2" />

# 7. Install python package: ```pip install -r .\requirements.txt```
<img width="1831" height="336" alt="image" src="https://github.com/user-attachments/assets/d725f73f-4a9f-4137-a1d5-d8438e9be7b9" />

# 9. Run crawler:
* ```python main.py --page travis_perkins --mode retail``` -> Crawl data from Travis Perkins without login to get retail price
<img width="1827" height="339" alt="image" src="https://github.com/user-attachments/assets/af5ddcae-22ee-42fb-8d79-9053083a6d06" />

* ```python main.py --page travis_perkins --mode trade``` -> Login before crawl data from Travis Perkins to get trade price
<img width="1828" height="344" alt="image" src="https://github.com/user-attachments/assets/9390c285-2a4a-4730-9812-7469bfa5147d" />
