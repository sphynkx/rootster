# ADMINKA


# Initial Setup

## App Install

```
cd /var/www
git clone https://github.com/sphynkx/rootster
cd rootster
chmod +x app.py
pip install -r install/requirements.txt
cp install/config.py-sample config.py
```
Set necessary params at `config.py`.

run:
```
./app.py
```

## Admin Users Configuration
Create hash for user's password:
```
echo -n 'adminpass' | md5sum
```
Create SQL-script from example:
```
cp install/add_admins.sql-sample install/add_admins.sql
```
Edit `install/add_admins.sql` set your own params in the VALUES. Also set password hash prepared above. Run:
```
mysql -u korneslov -p korneslov < add_admins.sql
```


## Systemd Setup
Create `/etc/systemd/system/rootster.service`:
```
[Unit]
Description=Rootster Flask Admin Panel
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/var/www/rootster
ExecStart=/usr/bin/python3 /var/www/rootster/app.py
Restart=always
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```
Next:
```
systemctl daemon-reload
systemctl start rootster
systemctl enable rootster
```


## Internal Nginx configuration
If hosting and app are on the same server..

....



## External Nginx configuration
Optionally, if hosting is not same with app.. No need to configure internal nginx (as above). Proxying will be directly. Create `/etc/nginx/conf.d/rootster.conf `:
```
    server {
        server_name  rootster.sphynkx.org.ua;
        listen       80;
        access_log   /var/log/nginx/rootster-access.log  main;
        error_log   /var/log/nginx/rootster-error.log;
        location / {
        proxy_pass      http://192.168.7.27:5000;
        proxy_connect_timeout       600;
        proxy_send_timeout          600;
        proxy_read_timeout          600;
        send_timeout                600;
        }

}
```
Next:
```
letsencrypt

```
Choose your subdomain, press `Enter`. Choose **option 2** (Redirect). Reload nginx.




