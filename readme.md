# RedpointsGit

RedpointsGit is a Github web crawler that utilizes Python3.

### Tech

RedpointsGit uses :

* [Scrapy] - An open source and collaborative framework for extracting the data you need from websites.

### Installation

RedpointsGit requires [Python3](https://www.python.org/download/releases/3.0/) and [Scrapy] to run.

Download from git:

```sh
$ git clone https://github.com/TugberkArkose/RedpointsGit.git
```

Installing dependicies can be done 2 ways.

Through pipenv already configured in the directory:
```sh
$ cd RedpointsGit
$ pipenv shell
```

Or by installing Scrapy with Pip3.

```sh
$ pip3 install scrapy
```

### Running

```sh
$ cd RedpointsGit/RedpointsGit
$ python git_spider_process.py -i input.json -o result.json
```

Where input.json has the following format:

```
{
  "keywords": [
    "python",
    "django-rest-framework",
    "jwt"
  ],
  "proxies": [
    "194.126.37.94:8080",
    "13.78.125.167:8080"
  ],
  "type": "Repositories"
}
```

```
keywords: a list of keywords to be used as search terms (unicode characters supported)
proxies: one of them selected and used randomly to perform all the HTTP requests.
type: the type of object we are searching for (Repositories, Issues and Wikis supported)
```

### Testing

RedpointsGit is covered with unit tests. Dedicated unit tests checks input, crawling and output processes.

To execute the tests

```sh
$ cd RedpointsGit/RedpointsGit/tests
$ python -m unittest git_spider_process_test.py
```


### Todos

 - Dynamic Proxy configuration with crawling https://free-proxy-list.net/
 - Add integration tests



[Scrapy]: <https://scrapy.org/>

