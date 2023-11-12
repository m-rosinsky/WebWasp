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

WebWasp's command line comes with numerous quality-of-life features to
support ease of use and speed in entering commands. It is meant to resemble
the bash command line to make users feel right at home, with some improvements
to allow easy integration into WebWasp's functionality.

Basic Features
~~~~~~~~~~~~~~

The command line has most of the basic features that bash users are familiar with.

These include:

* Command history seeking with up and down arrows
* Enhanced tab completions
* Command shortening
* Session persistence

Getting Help
~~~~~~~~~~~~

Getting suggestions for commands is fully integrated into WebWasp's command line.

To get basic help, we can utilize the built-in ``help`` command:

.. code-block::

    > help
    clear           Clear the screen
    cookies         Modify the cookies for requests
    get             Send an HTTP 1.1 GET request to a server/url
    -- truncated --

We can also utilize the ``-h`` option at any stage of a command.

For example, if we wanted to see the syntax of a ``get`` command, we
can use do the following:

.. code-block::

    > get -h
    usage: get [-h] [--no-params] [--no-cookies] url

    Send an HTTP 1.1 GET request to a server/url

    positional arguments:
    url           The url to make a request to

    optional arguments:
    -h, --help    Show this help message
    --no-params   Perform request without stored parameters in url
    --no-cookies  Perform request without stored cookies

The ``positional arguments`` are ones required for the command, and the ``optional arguments`` are of course optional.

Command Shortnening
~~~~~~~~~~~~~~~~~~~

WebWasp's command line offers an optional technique for entering commands, called _command shortening_.

This means that when entering a command, we need only to provide enough
characters in the command so that it is unambiguous which command we are
referring to.

For example, in this version of WebWasp, the only command that begins with
the letter ``t`` is the ``timeout`` command, meaning we only need to supply
a single letter to be unambiguous!

This means that these two commands are exactly the same:

.. code-block::

    > timeout 2.0
    [🐝] Timeout -> 2.0 seconds

and

.. code-block::

    > t 2.0
    [🐝] Timeout -> 2.0 seconds

Command shortening can be used at any stage of the command as well:

.. code-block::

    > response show -t

is equivalent to:

.. code-block::

    > r s -t

If there is ambiguity between two commands, the console will let us know the options:

.. code-block::

    > he
    [🛑] Ambiguous command: 'he'. Potential matches:
       help
       headers

Enhanced Tab Completions
~~~~~~~~~~~~~~~~~~~~~~~~

Instead of using command shortening, we can use tab completions to autofill commands.

For example if we type:

.. code-block::

    > headers set r

and press ``TAB``:

.. code-block::

    > headers set referer 

WebWasp will autofill the rest of the command, since ``referer`` was the only
option for completion given the partial command ``r``.

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
