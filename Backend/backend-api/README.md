# API Backend

## Developing

Creating an PostgreeSQL database

```terminal
./run-postgree-docker.sh
```

Installing python requirements

```terminal
pip install -r requirements.txt
```

Running

- In Windows

```terminal
python app.py
```

- In Linux

```terminal
python3 app.py
```

## Config

- PORT: Set server port (default: 8080)
- JWT_KEY: Set jwt private key (default: 'secret_key')
- STORAGE_PATH: Set directory application will use to store image files (default: './data')
- LOAD_TEST_DATA: If True, loads an test recycler to database with name='TestRecycler' (default: True)