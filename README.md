# How to run source
# 1. Install python: https://www.python.org/downloads/
<img width="1906" height="987" alt="image" src="https://github.com/user-attachments/assets/a68a2ef4-b25d-4040-bb66-3010dd225bd0" />

# 2. Open Terminal: ```Window -> Type Terminal -> Enter```
# 3. Clone repo: ```git clone https://github.com/tricaodev/crawl-data.git```
# 4. Go to working directory: ```cd crawl-data```
<img width="1417" height="328" alt="image" src="https://github.com/user-attachments/assets/5c062566-e17f-4cd0-a34e-a561998effbd" />

# 5. Create virtual environment: ```python -m venv .venv```
# 6. Active virtual environment
* Window: ```./.venv/Scripts/activate```
* MacOS: ```source ./.venv/bin/activate```
<img width="1602" height="181" alt="image" src="https://github.com/user-attachments/assets/29950c93-5d23-432b-8c7b-80dec4e3c0d1" />

# 7. Install python package: ```pip install -r .\requirements.txt```
<img width="1596" height="454" alt="image" src="https://github.com/user-attachments/assets/549d68c4-d4b1-4e01-87f5-bccf953ff1bf" />

# 9. Run crawler:
* ```python main.py --page travis_perkins --mode retail``` -> Crawl data from Travis Perkins without login to get retail price
<img width="1827" height="339" alt="image" src="https://github.com/user-attachments/assets/af5ddcae-22ee-42fb-8d79-9053083a6d06" />

* ```python main.py --page travis_perkins --mode trade``` -> Login before crawl data from Travis Perkins to get trade price
<img width="1828" height="344" alt="image" src="https://github.com/user-attachments/assets/9390c285-2a4a-4730-9812-7469bfa5147d" />
