# How to run source
# 1. Install python: https://www.python.org/downloads/
<img width="1906" height="987" alt="image" src="https://github.com/user-attachments/assets/a68a2ef4-b25d-4040-bb66-3010dd225bd0" />

# 2. Open Terminal: ```Window -> Type Terminal -> Enter```
# 3. Clone repo: ```git clone https://github.com/tricaodev/travis-perkins-crawler.git```
# 4. Go to working directory: ```cd travis-perkins-crawler```
<img width="1417" height="328" alt="image" src="https://github.com/user-attachments/assets/5c062566-e17f-4cd0-a34e-a561998effbd" />

# 5. Create virtual environment: ```python -m venv .venv```
# 6. Active virtual environment (on Window): ```./.venv/Scripts/activate```
<img width="1602" height="181" alt="image" src="https://github.com/user-attachments/assets/29950c93-5d23-432b-8c7b-80dec4e3c0d1" />

# 7. Install python package: ```pip install -r .\requirements.txt```
<img width="1596" height="454" alt="image" src="https://github.com/user-attachments/assets/549d68c4-d4b1-4e01-87f5-bccf953ff1bf" />

# 8. Run crawler:
* ```python main.py``` -> Crawl data without login to get retail price
<img width="1614" height="146" alt="image" src="https://github.com/user-attachments/assets/1aa92ebb-b1b1-4e2f-936a-5f797c0d1409" />

* ```python main.py --mode trade``` -> Login before crawl data to get trade price
<img width="1614" height="146" alt="image" src="https://github.com/user-attachments/assets/4ad2d1c6-38dc-4223-9394-32c0a0c1f106" />
