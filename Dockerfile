# Dockerfile — Policy+FX Trust Layer v0.1
# Build: docker build -t policyfx-trust .
# Run: docker run -p 8080:80 policyfx-trust

FROM nginx:alpine

# Copy static assets
COPY ui/ /usr/share/nginx/html/
COPY data/ /usr/share/nginx/html/data/
COPY lib/ /usr/share/nginx/html/lib/
COPY alerts/ /usr/share/nginx/html/alerts/
COPY docs/ /usr/share/nginx/html/docs/

# Add minimal cron for auto-refresh
RUN apk add --no-cache cron && \
    echo "*/30 * * * * /usr/bin/python3 /usr/share/nginx/html/lib/fetcher.py --url https://api.exchangerate-api.com/v4/latest/USD --cache-ttl 1800 --output /usr/share/nginx/html/data/fx/latest.json >> /var/log/cron.log 2>&1" | crontab - && \
    echo "*/30 * * * * /usr/bin/python3 /usr/share/nginx/html/lib/fetcher.py --url https://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html --cache-ttl 7200 --output /usr/share/nginx/html/data/policy/latest.json >> /var/log/cron.log 2>&1" | crontab -

# Start cron + nginx
CMD ["sh", "-c", "crond -l 2 & nginx -g 'daemon off;'"]