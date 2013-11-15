#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preggy import expect

from octopus import Octopus
from tests import TestCase


class TestOctopus(TestCase):
    def test_can_create_octopus(self):
        otto = Octopus(concurrency=20)
        expect(otto.concurrency).to_equal(20)
        expect(otto.auto_start).to_be_false()

    def test_has_default_concurrency(self):
        otto = Octopus()
        expect(otto.concurrency).to_equal(10)

    def test_queue_is_empty(self):
        otto = Octopus()
        expect(otto.is_empty).to_be_true()

    def test_can_enqueue_url(self):
        otto = Octopus()

        otto.enqueue('http://www.google.com', None)

        expect(otto.queue_size).to_equal(1)

    def test_can_get_after_started(self):
        otto = Octopus(concurrency=1)

        self.response = None

        def handle_url_response(url, response):
            self.response = response

        otto.enqueue('http://www.google.com', handle_url_response)
        otto.start()

        otto.wait()

        expect(self.response).not_to_be_null()
        expect(self.response.status_code).to_equal(200)

    def test_can_handle_more_urls_concurrently(self):
        urls = [
            'http://www.google.com',
            'http://www.globo.com',
            'http://www.cnn.com',
            'http://www.bbc.com'
        ]
        otto = Octopus(concurrency=4)

        self.responses = {}

        def handle_url_response(url, response):
            self.responses[url] = response

        for url in urls:
            otto.enqueue(url, handle_url_response)

        otto.start()

        otto.wait()

        expect(self.responses).to_length(4)

        for url in urls:
            expect(self.responses).to_include(url)
            expect(self.responses[url].status_code).to_equal(200)
