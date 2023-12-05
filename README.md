[![Documentation Status](https://readthedocs.org/projects/webwasp/badge/?version=latest)](https://webwasp.readthedocs.io/en/latest/?badge=latest)

```
 __        __   _      __        __              
 \ \      / /__| |__   \ \      / /_ _ ___ _ __  
  \ \ /\ / / _ \ '_ \   \ \ /\ / / _` / __| '_ \ 
   \ V  V /  __/ |_) |   \ V  V / (_| \__ \ |_) |
    \_/\_/ \___|_.__/     \_/\_/ \__,_|___/ .__/ 
      Get Stinging                        |_|
                              Author: Mike Rosinsky 
```
---

WebWasp is a multi-purpose pentesting tool for websites through an all-in-one command line suite.

Primary features include:

- GET and POST request crafting
- Built-in response scraping tools
- Cookie manipulation
- Packet header manipulation
- File downloading

## Installation

WebWasp can be installed using the `pip` package manager...

```bash
pip install webwasp
```

... and can be run by calling the module directly:

```bash
python3 -m webwasp
```

That should get us started, and will drop us into the WebWasp command line!

```
 __        __   _      __        __              
 \ \      / /__| |__   \ \      / /_ _ ___ _ __  
  \ \ /\ / / _ \ '_ \   \ \ /\ / / _` / __| '_ \ 
   \ V  V /  __/ |_) |   \ V  V / (_| \__ \ |_) |
    \_/\_/ \___|_.__/     \_/\_/ \__,_|___/ .__/ 
      Get Stinging                        |_|
                              Author: Mike Rosinsky 
    
[🐝] Running WebWasp version 0.1a...
> 
```

## Quick Start Guide

It's recommended to read the full [documentation](#3-documentation) to get a feel for all WebWasp has to offer, but here's a few things to get you started!

### GET Requests

Making an HTTP GET request is as easy! Here's a simple get request to google:

```
> get google.com
```

WebWasp will automatically fill in the URL scheme and make the request for you!

You should see the following output:

```
> get google.com
[🐝] Sending GET request to http://google.com/...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

### Viewing the Response

To view the response of the request we just made, we can use the ```response show``` command:

```
> response show  
[🐝] Summary of captured response:

Response url:
   http://www.google.com/
Response date/time:
   12/05/2023   00:51:33
Status code:
   200 (OK)
Encoding:
   ISO-8859-1

Re-run 'response show text' to show response text
```

This gives us a quick summary about the response we just made.

If we want to see the actual source code of the response, we can use the ```text``` argument:

```HTML
> response show text
<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en"><head><meta content="Search the world's information, ...
```

## Documentation

The full WebWasp documentation along with some walkthroughs that demonstrate WebWasp's capabilities can be found here:

> [ReadTheDocs](https://webwasp.readthedocs.io/en/latest/)

## Contributors

WebWasp is completely open-source, and anyone willing to make improvements or additions to the project is encouraged to submit a PR!

Any bugs, issues, requests, etc can be submitted as an issue:

https://github.com/m-rosinsky/WebWasp/issues
