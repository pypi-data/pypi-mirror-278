#!/bin/sh

echo "*****     Starting CBR NGINX API Gateway: $FASTAPI_APP_HOST"
# Substitute environment variables in the template and create the final nginx.conf
#envsubst '${FLASK_APP_HOST} ${FASTAPI_APP_HOST}' < ./nginx.template.conf > /etc/nginx/nginx.conf

cp ./nginx.conf /etc/nginx/nginx.conf
# Start NGINX

nginx -g 'daemon off;'

