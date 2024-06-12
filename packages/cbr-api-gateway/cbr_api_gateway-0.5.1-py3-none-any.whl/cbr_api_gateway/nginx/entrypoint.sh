#!/bin/sh

echo "Starting CBR NGINX API Gateway..."
# Substitute environment variables in the template and create the final nginx.conf
envsubst '${FLASK_APP_HOST} ${FASTAPI_APP_HOST}' < ./nginx.conf.template > /etc/nginx/nginx.conf

# Start NGINX
cat /etc/nginx/nginx.conf
nginx -g 'daemon off;'

