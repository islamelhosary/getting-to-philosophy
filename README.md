# Getting-to-Philosophy
Welcome to Wikipedia Jumper. It has the ability to instantly transport itself to the first link in Wikipedia page till it reaches https://en.wikipedia.org/wiki/Philosophy


## Install
```sh
$ sudo apt-get install libxml2-dev libxslt-dev python-dev
$ pip install -r requirements.txt
```

## Run
Before running anything, source environment variables.
```sh
$ source .env
```
Run the main script and pass the page name as an argument.
```
$ python DeathStar.py Yoda
```

## Contributing
Please make sure you read [contributing guidelines](CONTRIBUTING.md) before making any change.


## Limitations
It is working only on Wikipedia English 

## TODO
Tests!
More Error handling!