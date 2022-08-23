FROM nginx:1.23-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
#COPY web.cert /etc/ssl/
#COPY web.key /etc/ssl/
#COPY cf.pem /etc/ssl/
