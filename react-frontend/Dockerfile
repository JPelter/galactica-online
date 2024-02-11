FROM --platform=linux/amd64 node:20 AS builder
COPY . .
RUN npm install
RUN npm run build

# NOW BUILD THE ACTUAL NGINX SERVER!
FROM --platform=linux/amd64 nginx:1.25.2
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder build /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]