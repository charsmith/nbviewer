#-----------------------------------------------------------------------------
#  Copyright (C) 2013 The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

import json
import os

try: # py3
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient, HTTPError
from tornado.httputil import url_concat
from tornado.log import app_log

from .utils import url_path_join, quote, response_text

#-----------------------------------------------------------------------------
# Async Stash Client
#-----------------------------------------------------------------------------

class AsyncStashClient(object):
    """AsyncHTTPClient wrapper with methods for common requests"""
    stash_api_url = 'https://{}/rest/api/1.0/'.format(os.environ.get('STASH_HOSTNAME'))
    auth = None
    
    def __init__(self, client=None):
        self.client = client or AsyncHTTPClient()
    

    def fetch(self, url, callback=None, params=None, **kwargs):
        future = self.client.fetch(url, callback, **kwargs)
        return future

    def stash_api_request(self, path, callback=None, **kwargs):
        """Make a Stash API request to URL
        
        URL is constructed from url and params, if specified.
        callback and **kwargs are passed to client.fetch unmodified.
        """
        url = url_path_join(self.stash_api_url, path)
        return self.fetch(url, callback, **kwargs)

    
    def get_contents(self, project, repo, path, callback=None, **kwargs):
        """Make contents API request - either file contents or directory listing"""
        path = quote(u'projects/{project}/repos/{repo}/browse/{path}'.format(
            **locals()
        ))
        return self.stash_api_request(path, callback, **kwargs)
    
    
