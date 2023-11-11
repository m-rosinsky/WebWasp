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

# Contents

1. [Installation](#1-installation)
2. [Quick Start Guide](#2-quick-start-guide)
    - a. [GET Requests](#2a-get-requests)
    - b. [Viewing the Response](#2b-viewing-the-response)
3. [Documentation](#3-documentation)
4. [Planned Features](#4-planned-features)
5. [Contributors](#5-contributors)

## 1. Installation

WebWasp has yet to be packaged, since it is still in its alpha stages.

Therefore, we will need to clone from source:

```bash
git clone https://github.com/m-rosinsky/WebWasp.git
```

```bash
cd WebWasp
```

Ensure we have at least Python3.7 installed:

```bash
python3 --version
```

Install the ```pip``` dependencies:

```bash
python3 -m pip install -r requirements.txt
```

and then...

```bash
python3 webwasp.py
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

## 2. Quick Start Guide

It's recommended to read the full [documentation](#3-documentation) to get a feel for all WebWasp has to offer, but here's a few things to get you started!

### 2.a. GET Requests

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

### 2.b. Viewing the Response

To view the response of the request we just made, we can use the ```response show``` command:

```
> response show
[🐝] Summary of captured response:

Response url:
   http://www.google.com/
Response date/time:
   11/09/2023   11:30:05
Status code:
   200 (OK)

Re-run 'response show' with '-t' option to show response text
```

This gives us a quick summary about the response we just made.

If we want to see the actual source code of the response, we can use the ```-t```, or ```--text``` option:

```
> response show -t
<!doctype html>... (truncated google.com's source code is long)
```

## 3. Documentation

The full WebWasp documentation along with some walkthroughs that demonstrate WebWasp's capabilities can be found here:

```
link
```

## 4. Planned Features

- Directory bruteforcing, similar to dirbuster
- Response syntax highlighting

## 5. Contributors

TODO
