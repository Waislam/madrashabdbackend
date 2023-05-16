upstream core {
    server web:8000;
}

server {
    listen 80;

    server_name ${DOMAIN} www.${DOMAIN};

    # server logs
    access_log  /var/log/nginx/access_log.log;
    error_log /var/log/nginx/error_log.log;


    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }


    location / {        
        proxy_redirect     off;
        proxy_pass   http://core;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }
}
