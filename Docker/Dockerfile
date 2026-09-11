FROM nginx:alpine

# Remove a configuracao padrao do Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copia configuracao com proxy reverso para /api/
COPY Docker/nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos estaticos do frontend
COPY frontend/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
