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
  Encoding:
      utf-8
  
  Re-run 'response show text' to show response text

This gives us a quick summary about the response we just received.

If we want to see the actual source code of the response, we can use the ``text`` subcommand:

.. code-block::

  > response show text
  <!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="en"><head>...

Commands and the Console
========================

WebWasp's command line comes with numerous quality-of-life features to
support ease of use and speed in entering commands. It is meant to resemble
the bash command line to make users feel right at home, with some improvements
to allow easy integration into WebWasp's functionality.

Basic Features
--------------

The command line has most of the basic features that bash users are familiar with.

These include:

* Command history seeking with up and down arrows
* Enhanced tab completions
* Command shortening
* Session persistence
* Session context management

Getting Help
------------

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

The ``positional arguments`` are ones required for the command, while the ``optional arguments`` are of course optional.

Command Shortening
-------------------

WebWasp's command line offers an optional technique for entering commands,
known as *command shortening*.

This means that when entering a command, we need only to provide enough
characters so that it is unambiguous which command we are
referring to.

For example, in this version of WebWasp, the only command that begins with
the letter ``t`` is ``timeout``, meaning we only need to supply
a single letter to be unambiguous:

.. code-block::

  > timeout 2.0
  [🐝] Timeout -> 2.0 seconds

.. code-block::

  > t 2.0
  [🐝] Timeout -> 2.0 seconds

Command shortening can be used at any stage of the command as well:

.. code-block::

  > response show text

is equivalent to:

.. code-block::

  > r s t

Easy right?

If there is ambiguity between two commands, the console will let us know the options:

.. code-block::

  > he
  [🛑] Ambiguous command: 'he'. Potential matches:
      help
      headers

Enhanced Tab Completions
------------------------

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

Variables allow us to store pieces of text so we don't have to worry about remembering them, or copy-pasting them all the time.

We can add a variable with the ``var add`` command, for example, an address to our local server:

.. code-block::

  > var add "local" "http://localhost:8000"
  [🐝] Added variable:
    $local -> 'http://localhost:8000'

The quotes are optional unless there is a space in the name.

To use the variable later, we just prefix the name with a ``$``:

.. code-block::

  > get $local
  [🐝] Sending GET request to http://localhost:8000/...

We can remove variables with the ``remove`` subcommand:

.. code-block::

  > var remove local
  [🐝] Removed variable:
    $local

And we can remove all variables with the ``clear`` subcommand:

.. code-block::

  > var clear
  [🐝] All variables cleared

Variables are saved to whatever session they were created in. See the next section for more on sessions.

Console Sessions
================

By default, WebWasp will create a session for us called ``default`` to work in.

We can list the existing sessions by using the ``list`` subcommand:

.. code-block::

  > console session list        
  [🐝] Console session list:
    default *

Our active session will be highlighted green and have an ``*`` next to it.

All things we create will be saved under the active session.

To create a new blank session, we can use the ``new`` subcommand:

.. code-block::

  > console session new "my_session"
  [🐝] Created and switched to new session: 'my_session'

Running ``list`` again, we can see our session has been created, and is now active:

.. code-block::

  > console session list
  [🐝] Console session list:
    default
    my_session *

Any variables, headers, parameters, etc. will be saved within the ``default`` session, and not transferred to our new session.

This is useful if we want to start an unrelated task to what we were working on before, without deleting our data.

We can always switch back to a different session by using the ``load`` subcommand:

.. code-block::

  > console session load default
  [🐝] Switched to session 'default'

If we want to copy our active session into another session, we can use the ``copy`` subcommand:

.. code-block::

  > console session copy my_session
  [🐝] Copied data from session 'default' to 'my_session'
  [🐝] Switched to session 'my_session'

In this example, we were in session ``default``, and copied our session data to the existing session named ``my_session``.

If the target session already exists, as in this example, the data currently in that session will be overwritten, so use with caution.

If the target session does not exist, it will be created and the data will be copied into it, as shown here:

.. code-block::

  > console session copy default2  
  [🐝] Copied data from session 'default' to 'default2'
  [🐝] Switched to session 'default2'
  > console session list
  [🐝] Console session list:
    default
    default2 *
    my_session

We can reset our session data by using the ``reset`` subcommand. This effectively erases any session data we currently have:

.. code-block::

  > console session reset
  [🐝] Resetting data for session 'default'

We can also delete sessions using the ``delete`` subcommand:

.. code-block::

  > console session delete my_session
  [🐝] Deleted session 'my_session'

If we delete our current session, it will switch us back to ``default``:

.. code-block::

  > console session delete default2
  [🐝] Deleted session 'default2'
  [🐝] Switched to session 'default'

If we delete the ``default`` session, it will be recreated with blank data.

When starting a new task within WebWasp, it's a good practice to create a new session for it.

Response Parsing
================

WebWasp offers a wide variety of tools for viewing, searching, and parsing response data.

All of these features fall under the ``response`` command.

For this example, we'll use this sample html doc:

.. code-block:: html

  <!DOCTYPE html>
  <html>
  <head>
      <title>My Sample Page</title>
  </head>
  <body>
      <h1>Welcome to my page!</h1>
      <a href="file1.txt">File1</a>
      <a href="file2.txt">File2</a>
      <a href="file3.txt">File3</a>
  </body>
  </html>

Let's stand up a local server using python's built-in http server:

.. code-block::

  $ python3 -m http.server


Now let's fire up WebWasp and make a request to it:

.. code-block:: 

  > get localhost:8000/sample.html
  [🐝] Sending GET request to http://localhost:8000/sample.html...
  [🐝] GET request completed. Status code: 200 (OK)
  [🐝] Response captured! Type 'response show' for summary

Success! Let's take a look at a summary of the response:

.. code-block:: 

  > response show
  [🐝] Summary of captured response:

  Response url:
    http://localhost:8000/sample.html
  Response date/time:
    11/19/2023   21:19:49
  Status code:
    200 (OK)
  Encoding:
    ISO-8859-1

This shows us some basic information about the request. If we want to take a look at the headers, a technique commonly referred to as *banner grabbing*, we can specify the ``headers`` argument:

.. code-block::

  > response show headers
  [🐝] Response headers:
    Server:         SimpleHTTP/0.6 Python/3.8.10
    Date:           Sun, 19 Nov 2023 21:19:49 GMT
    Content-type:   text/html
    Content-Length: 229
    Last-Modified:  Sun, 19 Nov 2023 21:17:42 GMT

If we want to see the actual source, we can use ``text`` instead:

.. code-block:: html

  > response show text
  <!DOCTYPE html>
  <html>
  <head>
      <title>My Sample Page</title>
  </head>
  <body>
      <h1>Welcome to my page!</h1>
      <a href="file1.txt">File1</a>
      <a href="file2.txt">File2</a>
      <a href="file3.txt">File3</a>
  </body>
  </html>

And there's our sample source that WebWasp retrieved for us!

Response Grep
-------------

We can perform grep-like searches on our response text using the ``response grep`` command!

In the above example, if we wanted to find all lines with the word ``file`` in it:

.. code-block:: html

  > response grep file
  [🐝] Search results for pattern 'file':
        <a href="file1.txt">File1</a>
        <a href="file2.txt">File2</a>
        <a href="file3.txt">File3</a>

``response grep`` also supports regular expressions. It's good practice to always wrap regex in quotes:

.. code-block:: html

  > response grep 'href="([^"]*)"'
  [🐝] Search results for pattern 'href="([^"]*)"':
        <a href="file1.txt">File1</a>
        <a href="file2.txt">File2</a>
        <a href="file3.txt">File3</a>

Response Find
-------------

The ``response`` find command performs actual html parsing behind the scenes, rather than just acting on raw text like ``grep`` does.

For example, if we wanted to find all ``a`` tags within the response, we can use:

.. code-block:: html

  > response find --tag a
  [🐝] Find results:
  <a href="file1.txt">File1</a>
  <a href="file2.txt">File2</a>
  <a href="file3.txt">File3</a>

We can also specify the ``--strip`` option to only see *inside* the tags:

.. code-block::

  > response find --tag a --strip
  [🐝] Find results:
  File1
  File2
  File3

``--tag`` is just one of several find options. Run ``response find -h`` to see a full list!

Syntax Highlighting
-------------------

By default, when we run ``response show text``, WebWasp will attempt to use HTML syntax highlighting.

WebWasp has built-in support for both PHP and Javascript as well!

We can specify the ``--syntax [language]`` option to change the highlighting method.

Here's an example with some sample PHP code:

.. code-block::

  > get localhost:8000/sample.php
  [🐝] Sending GET request to http://localhost:8000/sample.php...
  [🐝] GET request completed. Status code: 200 (OK)
  [🐝] Response captured! Type 'response show' for summary

.. code-block:: php

  > response show text --syntax php
  <?php
  // Sample PHP code
  $greeting = "Hello, PHP!";
  echo "<h1>$greeting</h1>";

  // Simple loop
  for ($i = 1; $i <= 5; $i++) {
      echo "Iteration $i<br>";
  }

  // Associative array
  $person = array(
      "name" => "John",
      "age" => 30,
      "city" => "New York"
  );

  // Accessing array elements
  echo "<p>{$person['name']} is {$person['age']} years old and lives in {$person['city']}.</p>";
  ?>

Response Beautify
-----------------

WebWasp comes with functionality to decode any HTML entities that are in their encoded state when sent by the server.

Some examples of these entities are the ``&gt;`` for ``>`` and ``&nbsp;`` for a non-break space.

If the response has some of these entities in it, we can run ``response beautify`` to perform decoding.

This command will also format the HTML source into a more readable format:

.. code-block::

  > get localhost:8000/sample.html
  [🐝] Sending GET request to http://localhost:8000/sample.html...
  [🐝] GET request completed. Status code: 200 (OK)
  [🐝] Response captured! Type 'response show' for summary

.. code-block:: html

  -- truncated --
  <ul>
    <li>&lt;p&gt; represents &lt;paragraph&gt;</li>
    <li>&amp;copy; represents the copyright symbol &copy;</li>
    <li>&amp;trade; represents the trademark symbol &trade;</li>
    <li>&lt;br&gt; represents a line break <br></li>
    <li>&amp;lt; represents the less-than symbol &lt;</li>
    <li>&amp;gt; represents the greater-than symbol &gt;</li>
  </ul>
  -- truncated --

.. code-block:: 

  > response beautify 
  [🐝] Beautifying response text...
    Ran prettify.
    Made 13 entity decodes.

.. code-block:: html

  <ul>
   <li>
    <p> represents <paragraph>
   </li>
   <li>
    &copy; represents the copyright symbol ©
   </li>
   <li>
    &trade; represents the trademark symbol ™
   </li>
   <li>
    <br> represents a line break
    <br/>
   </li>
   <li>
    &lt; represents the less-than symbol <
   </li>
   <li>
    &gt; represents the greater-than symbol >
   </li>
  </ul>

Exporting Responses
===================

To export responses we gather to a file, we can use the ``response export`` command.

If we don't provide a path, it will auto-configure a name for us and save it within the current directory.

.. code-block:: 

  > response export sample.html
  [🐝] Exported response to file 'sample.html'
  >
  > response export
  [🐝] Exported response to file 'webwasp11_21_2023_10_37_10'

Headers
=======

HTTP headers can be ``set`` and ``unset`` on a per-session basis.

To see a list of headers that can be configured and sent, run ``headers``:

.. code-block:: 

  > headers
  [🐝] Current header fields:
    auth-pass    : ''
    auth-user    : ''
    referer      : ''
    user-agent   : ''
    -- truncated --

When we set a field with the ``set`` command, it will be displayed here:

.. code-block::

  > headers set referer "myreferringsite.com"
  [🐝] Set header field:
    referer : 'myreferringsite.com'

We can use ``headers unset`` to unset specific header fields, or ``headers clear`` to unset *all* header fields.

When a request is made within this session now, any header fields that have been set will automatically be shipped with it.

Checkout the Natas OverTheWire WebWasp walkthrough `level 4 <https://github.com/m-rosinsky/WebWasp/blob/main/docs/natas.md#level-4>`_ to see this in a practical example.

HTTP Authorization
------------------

The ``auth-user`` and ``auth-pass`` headers have to do with HTTP authorization. If you're getting a ``401 Unauthorized`` error, you may need to set these fields and try the request again.

All levels of the Natas walkthrough deal with these fields, for an example.

Headers and Sessions
--------------------

As mentioned above, header fields (just like variables, parameters, etc), are saved on a per-session basis.

This means if we move to a new session, the headers we created won't be there (unless we copied this session).

This allows freedom to work on other tasks without having to delete any header fields we've configured.

Parameters and POST Requests
============================

Parameters with GET Requests
----------------------------

Parameters are used to send data as part of the URL query string.

We can add a new parameter using the ``params add`` command:

.. code-block:: 

  > params add key1 value1
  [🐝] Added param:
    'key1' : 'value1'

And we can list all currently stored parameters for the session with just the ``params`` command:

.. code-block::

  > params
  [🐝] Current stored parameters:
    'key1' : 'value1'

Now when we send a GET request, the parameters, similar to the headers, will automatically be sent with it:

.. code-block:: 

  > get localhost:8000
  [🐝] Sending GET request to http://localhost:8000/?key1=value1...

We can see in the first line of the feedback there that our parameter was automatically added onto the URL.

If we don't wish to send our parameters, we can specify the ``--no-params`` option:

.. code-block::

  > get localhost:8000 --no-params
  [🐝] Sending GET request to http://localhost:8000/...

Parameters with POST Requests
-----------------------------

POST requests can be sent using WebWasp's ``post`` command.

In order to send encoded data with our POST requests, we need to first create specific parameters with the ``params`` command, then pass these to the POST request:

Let's create the params first:

.. code-block::

  > params add key1 value1
  [🐝] Added param:
    'key1' : 'value1'
  > params add key2 value2
  [🐝] Added param:
    'key2' : 'value2

Then we can perform a POST request with the parameters we made:

.. code-block::

  > post https://httpbin.org/post key1 key2
  [🐝] Sending POST request to https://httpbin.org/post...
  POST request made with parameters:
    'key1' : 'value1'
    'key2' : 'value2'
    -- truncated --

.. code-block::

  > response show text
  -- truncated --
  "form": {
    "key1": "value1", 
    "key2": "value2"
  },
  -- truncated --

Cookies
=======

Response Cookies
----------------

When we make a request, we can see the cookies that a site returns by using the ``response show cookies`` command:

Here's an example from the Natas walkthrough `level 5 <https://github.com/m-rosinsky/WebWasp/blob/main/docs/natas.md#level-5>`_:

.. code-block::

  > response show cookies
  [🍪] Response cookies:
    loggedin     : 0

Request Cookies
---------------

If we want to send cookie values within our requests, we can use the ``cookies`` command.

It operates nearly identically to the ``params`` command, for ``add``, ``remove`` and ``clear`` subcommands.

.. code-block::

  > cookies add loggedin '1'
  [🍪] Added cookie:
    'loggedin' : '1'

Also similar to the ``params`` command, any cookies we have stored are automatically shipped along with requests we make.

.. code-block::

  > get https://httpbin.org/get
  [🐝] Sending GET request to https://httpbin.org/get...
  [🐝] GET request completed. Status code: 200 (OK)
  [🐝] Response captured! Type 'response show' for summary
  > 
  > response show text
  {
    "args": {}, 
    "headers": {
      "Accept": "*/*", 
      "Accept-Encoding": "gzip, deflate", 
      "Cookie": "loggedin=1",
  -- truncated --

Timeouts
========

We can set the timeout value for requests with the ``timeout`` command.

.. code-block::

  > timeout 0.5
  [🐝] Timeout -> 0.5 seconds

The timeout value is saved on a per-session basis.

The default timeout value is 2.0 seconds.

If we set the timeout to 0, or a negative number, the timeout will set to ``None``, and there will be no timeout.

.. code-block::

  > timeout 0
  [🐝] Timeout -> None

This is **NOT** recommended, since it can cause the program to hang indefinitely if the request does not complete.

Planned Features
================

WebWasp is very much still in development, but here's a sneak preview of the features I plan to add:

- Directory brute-forcing, similar to gobuster
- WebSocket support
- Further syntax highlighting
- GUI interface alternative

Contributors
============

If you've been brushing up on your Python and want to do some open-source contributing, WebWasp would love to have you!

Check out the `Contribution Guide (LINK PENDING)`_ to get started! 🐝
