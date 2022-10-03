Варіан: Python 3.7 + venv + requirements.txt

To install and boot this service you would need the following:

    Python 3.7.*
    Flask 2.2.2
    waitress 2.1.2

  
Boot it via waitress with the command below

    waitress-serve --port=5000 --call "app.app:app"
