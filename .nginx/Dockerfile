FROM nginx

RUN rm -rf /usr/share/nginx/html/*


COPY nginx.conf /etc/nginx/nginx.conf


EXPOSE 1111

CMD ["nginx", "-g", "daemon off;" ]