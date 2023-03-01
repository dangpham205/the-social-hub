ARG NGINX_VERSION
FROM nginx:${NGINX_VERSION}
#WORKDIR '/var/www/html/user_be'
#RUN rm /etc/nginx/conf.d/default.conf
#COPY ./docker/nginx/conf.d/user.nginx.conf /etc/nginx/conf.d/
ARG NGINX_PORT
ENV REDIS_PORT ${NGINX_PORT}\
EXPOSE ${NGINX_PORT}
CMD ["nginx", "-g", "daemon off;"]
#RUN echo "upstream php-upstream { server php-fpm:9000; }" > /etc/nginx/conf.d/upstream.conf