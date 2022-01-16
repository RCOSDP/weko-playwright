# weko-playwright

## how to run sample/test_helloworld.py

check the python version.

```
$ python --version
Python 3.7.12
```

### clone this repository

```
git clone https://github.com/RCOSDP/weko-playwright.git
cd weko-playwright
```

### make a virtual environment

```
python -m venv venv
source venv/bin/activate
```

### install playwright and pytest-playwright

```
pip install playwright
python -m playwright install
python -m playwright install-deps
pip install pytest-playwright
```

### run sample/test_helloworld.py

```
pytest sample/test_helloworld.py
```

### check a result of sample test

```
$ pytest sample/test_helloworld.py
============================= test session starts ==============================
platform linux -- Python 3.7.12, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/vagrant/weko-playwright
plugins: base-url-1.4.2, playwright-0.2.2
collected 1 item

sample/test_helloworld.py .                                              [100%]

============================== 1 passed in 3.61s ===============================
```

screen shots:

```
$ ls images/
chromium.png
```

capture videos:

```
$ ls videos/
c548abea4ba9143cd395003a83565bfd.webm
```

### remove the result

```
rm -rvf images/
rm -rvf videos/
```

### deactivate a virtual environment

```
deactivate
```

### remove a virtual environment

```
rm -rvf venv
```