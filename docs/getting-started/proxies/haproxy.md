# Using HAPROXY as Reverse Proxy

!!! quote ""
    Help improve this page! You can contribute by clicking :material-pencil: to send a pull request with your changes.

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

