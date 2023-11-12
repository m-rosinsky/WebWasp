.. _documentation:

WebWasp Documentation
=====================

`WebWasp <https://github.com/m-rosinsky/WebWasp/>`_ is a multi-purpose pentesting tool for websites through an all-in-one command line suite.

Primary features include:

* GET and POST request crafting
* Built-in response scraping tools
* Cookie manipulation
* Packet header manipulation
* File downloading

Getting Started
===============

Installation
------------

WebWasp has yet to be packaged, so it will need to be cloned from source:

.. code-block:: rst

  git clone https://github.com/m-rosinsky/WebWasp.git

.. code-block:: rst

  cd WebWasp

Ensure at least Python3.7 is installed:

.. code-block:: rst

  python3 --version

Install the ``pip`` dependencies:

.. code-block:: rst

  python3 -m pip install -r requirements.txt

and then...

.. code-block:: rst

  python3 webwasp.py

That should get us started, and will drop us into the WebWasp command line!

.. code-block::

   __        __   _      __        __              
   \ \      / /__| |__   \ \      / /_ _ ___ _ __  
    \ \ /\ / / _ \ '_ \   \ \ /\ / / _` / __| '_ \ 
     \ V  V /  __/ |_) |   \ V  V / (_| \__ \ |_) |
      \_/\_/ \___|_.__/     \_/\_/ \__,_|___/ .__/ 
        Get Stinging                        |_|
                                Author: Mike Rosinsky 
      
  [🐝] Running WebWasp version 0.1a...
  > 

Quick Start
-----------

GET Requests
~~~~~~~~~~~~

Making an HTTP GET request is easy! Here's a simple GET request to google:

.. code-block::

  > get google.com

WebWasp will automatically fill in the URL scheme and make the request for you!

You should see the following output:

.. code-block::

  > get google.com
  [🐝] Sending GET request to http://google.com/...
  [🐝] GET request completed. Status code: 200 (OK)
  [🐝] Response captured! Type 'response show' for summary

Responses
~~~~~~~~~

To view the response of the request we just made, we can use the ``response show`` command:

.. code-block::

  > response show
  [🐝] Summary of captured response:
  
  Response url:
     http://www.google.com/
  Response date/time:
     11/09/2023   11:30:05
  Status code:
     200 (OK)
  
  Re-run 'response show' with '-t' option to show response text

This gives us a quick summary about the response we just received.

If we want to see the actual source code of the response, we can use the ``-t`` or ``--text`` option:

.. code-block::

  > response show -t
  <!doctype html>
  --truncated--

Commands and the Console
========================

TODO

Variables
=========

TODO

Response Parsing
================

TODO

Headers
=======

TODO

Parameters and POST Requests
============================

TODO

Cookies
=======

TODO

Planned Features
================

TODO

Contributors
============

TODO
