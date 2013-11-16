octopus
=======

[![Build Status](https://travis-ci.org/heynemann/octopus.png?branch=master)](https://travis-ci.org/heynemann/octopus)
[![PyPi version](https://pypip.in/v/octopus-http/badge.png)](https://crate.io/packages/octopus-http/)
[![PyPi downloads](https://pypip.in/d/octopus-http/badge.png)](https://crate.io/packages/octopus-http/)
[![Coverage Status](https://coveralls.io/repos/heynemann/octopus/badge.png?branch=master)](https://coveralls.io/r/heynemann/octopus?branch=master)

`octopus` is a library to use threads to concurrently retrieve and report on the completion of http requests

Installing
==========

Installing `octopus` is really easy:

    $ pip install octopus-http

The reason for the name of the package is that a package called `octopus` was already registered at the Python Package Index.

Using
=====

Using `octopus` is pretty simple:

    # this Octopus instance we'll run 4 threads,
    # automatically start listening to the queue and
    # we'll in-memory cache responses for 10 seconds.
    otto = Octopus(concurrency=4, auto_start=True, cache=True, expiration_in_seconds=10)

    def handle_url_response(url, response):
        # do something with response

    otto.enqueue('http://www.google.com', handle_url_response)
    otto.enqueue('http://www.facebook.com', handle_url_response)
    otto.enqueue('http://www.yahoo.com', handle_url_response)
    otto.enqueue('http://www.google.com', handle_url_response)  # will come from the cache

    otto.wait()  # waits until queue is empty or timeout is ellapsed

API Reference
=============

Octopus Class
-------------

This is the main unit of work in `octopus`. To enqueue new urls you need to have an `Octopus` instance:

    from octopus import Octopus

    otto = Octopus()

The constructor for `Octopus` takes several configuration options:

* `concurrency`: number of threads to use to retrieve URLs (defaults to 10 threads);
* `auto_start`: Indicates whether threads should be started automatically (defaults to False);
* `cache`: If set to `True`, responses will be cached for the number of seconds specified in `expiration_in_seconds` (defaults to False);
* `expiration_in_seconds`: The number of seconds to keep url responses in the local cache (defaults to 30).

Octopus.start()
---------------

If `auto_start` is set to `False`, this method must be called to start retrieving URLs. This is a **non-blocking** method.

Octopus.enqueue(url, handler)
-----------------------------

This is the main method in the `Octopus` class. This method is used to enqueue new URLs. The handler argument specifies the method to be called when the response is available.

The handler takes the form `handler(url, response)`. The response argument is a [Response](http://www.python-requests.org/en/latest/api/#requests.Response) instance.

This is a **non-blocking** method.

Octopus.queue_size
------------------

This property returns the approximate number of URLs still in the queue (not retrieved yet).

Octopus.is_empty
----------------

This property returns if the URL queue is empty.

Octopus.wait(timeout=10)
------------------------

If you want to wait for all the URLs in the queue to finish loading, just call this method.

If you specify a `timeout` of `0`, `octopus` will wait until the queue is empty, no matter how long it takes.

If a timeout occurs, this method raises `Octopus.TimeoutError`.

This is a **blocking** method.

Benchmark
=========

In order to decide whether `octopus` really was worth using, it features a benchmark test in it's codebase.

If you want to run it yourself (which is highly encouraged), just clone `octopus` repository and run this command:

    $ python benchmark/test_octopus.py 200 100

The first argument is the number of URLs to retrieve. The seconds argument means how many threads will be used by `octopus` to get the urls.

The test is pretty simple. Time how long it takes for requests to get the URLs sequentially and for `octopus` to get them concurrently.

The results for retrieving 2000 urls with 200 threads is as follows:

    =======
    RESULTS
    =======

    [requests] Retrieving 2000 urls took 2692.66 seconds meaning 0.74 urls/second.

    [octopus] Retrieving 2000 urls took 33.56 seconds meaning 59.59 urls/second.

    [octopus] Retrieving 2000 urls with local in-memory caching took 2.43 seconds meaning 821.95 urls/second.

    Overall, octopus was more than 80.00 times faster than sequential requests.
