# Using HAPROXY as Reverse Proxy

!!! tldr ""
    Should you experience problems with Haproxy, we recommend that you ask the Haproxy community for advice, as we cannot provide support for third-party software and services.

```bigquery
#frontend connection handling
#'photo' is the name of the subdomain
acl photo hdr(host) -i photo.example.com
use_backend be_photo_ipvANY if photo aclcrt_fe_http

#backend config
#be_photo is the name of the backend
backend be_photo_ipvANY
mode http
id 112
log global
timeout connect 30000
timeout server 30000
retries 3
load-server-state-from-file global
timeout queue 5s
timeout tunnel 2m
option redispatch

mode http
option forwardfor
no option httpclose

http-request set-header Host photo.example.com
http-request del-header  X-Frame-Options
http-request del-header  Connection
http-request add-header  X-Frame-Options SAMEORIGIN
http-request add-header  Connection Upgrade
             # Websocket configuration
             acl is_websocket hdr(Upgrade) -i WebSocket
acl is_websocket hdr_beg(Host) -i ws
             # photoprism ip address and port
server photo x.x.x.x:2342 id 106  
```

## Why Use a Proxy? ##

If you install PhotoPrism on a public server outside your home network, **always run it behind a secure
HTTPS reverse proxy**. Your files and passwords will otherwise be transmitted in clear text and can be intercepted
by anyone, including your provider, hackers, and governments. Backup tools and file sync apps may refuse to
connect as well.

![](https://dl.photoprism.app/img/diagrams/reverse-proxy.svg){ class="w100" }

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
