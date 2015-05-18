

# General #

## What is Libforensics? ##

LibForensics is a Python library, used to build digital forensics tools.

## Why Python? ##

LibForensics has actually had several incarnations, in different programming languages, including Java, C, C++, and Python.  I eventually settled on Python for a few reasons:
  * Python runs on Windows, Mac OS X, and Linux
  * Python has a fairly "c-like" feel to it
  * Python is fairly easy to learn
  * Writing code in Python is usually a lot quicker than in C or Java

## Isn't Python slow? ##

This really depends on your definition of "slow".  Many people place Python in similar categories as PERL.  However, there are some architectural differences that make Python out perform PERL (at least for our uses).  Notably, Python (unlike PERL) is compiled into byte code (.pyc files) and run through a Python virtual machine.  This is similar to how Java works, except the end user doesn't have to manually compile the code (it is done behind the scenes automatically).

There are several "tricks" we can do to speed up the Python code, including moving some of the work into the C modules that are included in the Python standard library.  On top of this, there is work such as [Unladen Swallow](http://code.google.com/p/unladen-swallow), and [Psyco](http://psyco.sourceforge.net) which can help speed up the process.

Ultimately however, a tight loop in C runs faster than a tight loop in Python.  Once we get to the point where the Python code is the bottle neck, I'll look at moving the responsible code into C modules.

## How is Libforensics different than other frameworks/tools? ##

LibForensics is meant to provide a full "forensic stack".  Providing tools to do everything from location, to extraction, decoding, and interpretation.  For instance, data structures are first class objects (see the lf.datatype package).

If you have a part of a data structure (e.g. part of a directory entry) LibForensics can be used to process the part of the data structure that you do have.

In addition, LibForensics provides all of the unit tests used during development and testing.  This follows from the "open testing" ideology for forensic tools.

# Installation #

## What platforms does Libforensics run on? ##

I've tested LibForensics on Linux, Mac OS X, and Windows.  In theory, it should be able to run on any platform that supports Python 3.1.

## What other packages are required? ##

Right now, LibForensics doesn't have any external dependencies (other than a full Python standard library).  I'm trying to keep external dependencies low, to minimize the extra work to install LibForensics.

# Usage #

## Why aren't there any modules for user interfaces? ##

LibForensics is aiming to handle only the "forensic processing" aspect of digital forensics tools.

## Where is the documentation? ##

This is a work in progress.  At the moment, all of the objects (and most of the modules) have documentation (in restructured text format) in the docstrings.