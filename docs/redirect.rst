How to configure redirects
==========================

Redirect from www. and http to https:
-------------------------------------

To configure proper redirects on your nginx server::

    server {
        listen 80;
        server_name www.example.com;
        return 301 https://example.com#request_uri;
    }

    server {
        listen 80;
        server_name example.com;
        return 301 https://example.com#request_uri;
    }
