## 📖 About 

Sitemappy (or sitemap-py 😉) is a crawler that produces a sitemap for a given website.

Sitemappy is a command-line application, and also provides Python interfaces for use as a library.

### Features

- [x] Print the URL for a given website when visited
- [x] Print the links for a given webpage
- [x] Visit the links for a given webpage
- [x] Limit the links to follow on a webpage to the same single subdomain
- [x] Concurrency (`asyncio`, `multithreading`, `multiprocessing`)
- [x] Output crawling results to file by default (results too long for console)
- [x] Modify number of async crawler workers
- [x] Specify crawling depth
- [x] Crawling politeness argument
- [ ] Follow HTTP redirect responses
- [ ] HTTP error response handling
- [ ] Add DEBUG, INFO and ERROR logging
- [ ] Adhere to a website's `robots.txt`
- [ ] "Spider Trap" resilience
- [ ] Introduce `multiprocessing`
- [ ] Distributed multiprocessing
- [x] Publish to PyPi 🚀
- [x] GitHub Workflows (deploy)
- [ ] GitHub Workflows (linting, unit testing, dev deployments)

## 🚀 Usage

Generate a sitemap (`./results.json`):

```shell
sitemappy-cli https://monzo.com/
```

### Help

```shell
$ sitemappy-cli --help
usage: sitemappy-cli [-h] BASE_URL

Sitemappy is a CLI tool to crawl a website and create a sitemap.
For more information about the tool go to https://github.com/dan-wilton/sitemappy/

Arguments:
  BASE_URL              a valid website URL to sitemap [required]

Options:
  --workers           INTEGER     Number of workers to asynchronously 
                                  make web requests [default: 10]
  
  --crawl-depth       INTEGER     Depth of links from base URL to follow
                                  [default: 0 - unlimited]
  
  --politeness-delay  INTEGER     Delay between each request to the website
                                  [default: 0 - none]
  
  --enable-cmd-out                Print output to cmd
  
  --help                          show this help message and exit
```


## 🎒 Requirements 

[Python](https://www.python.org/downloads/) `3.12+`


### Development 

[PDM](https://pdm-project.org/en/latest/)


## 💻 Installation

To use the sitemappy CLI:

```shell
pip install --user -U sitemappy-cli
```

### Local Development / Contributing

```shell
pdm install
```

Run the tests with:

```shell
pytest -v
```

### Python Library

Use sitemappy in your project with one of the following:

with **pip**:

```bash
pip install -U sitemappy-cli
```

with **PDM**:

```bash
pdm add sitemappy-cli
```

with **Poetry** >= 1.2.0:

```bash
poetry add sitemappy-cli
```

### macOS

> **_NOTE:_** This is not yet enabled 😢

via [homebrew](#macos):

```bash
brew install sitemappy-cli
```
