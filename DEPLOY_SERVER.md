# 🚀 Deploy na Własny Serwer - Student Files

## 📋 Wymagania

- Serwer z Ubuntu/Debian
- SSH dostęp
- Python 3.14+
- Nginx
- Certbot (dla SSL)

## 🔧 Krok po kroku

### 1. Przygotowanie plików

```bash
# Sklonuj repo na serwer
git clone https://github.com/yoobzz/sof_file_rename.git
cd sof_file_rename
```

### 2. Instalacja zależności

```bash
# Zainstaluj Python i pip
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Stwórz środowisko wirtualne
python3 -m venv venv
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt
```

### 3. Konfiguracja Nginx

Stwórz plik `/etc/nginx/sites-available/files`:

```nginx
server {
    listen 80;
    server_name files.twoja-domena.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Bezpieczeństwo
    client_max_body_size 20M;
}
```

Włącz konfigu replikację:

```bash
sudo ln -s /etc/nginx/sites-available/files /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Konfiguracja SSL

```bash
# Zainstaluj Certbot
sudo apt install certbot python3-certbot-nginx

# Skonfiguruj SSL
sudo certbot --nginx -d files.twoja-domena.com
```

### 5. Uruchomienie aplikacji

```bash
cd /path/to/your/app
source venv/bin/activate
python app.py
```

### 6. Systemd Service (opcjonalnie)

Stwórz plik `/etc/systemd/system/files-app.service`:

```ini
[Unit]
Description=Student Files App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/files
Environment=PATH=/var/www/files/venv/bin
ExecStart=/var/www/files/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Włącz service:

```bash
sudo systemctl enable files-app
sudo systemctl start files-app
sudo systemctl status files-app
```

## 🔒 Bezpieczeństwo

### Firewall

```bash
# UFW
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Uprawnienia

```bash
# Ustaw właściwe uprawnienia
sudo chown -R www-data:www-data /var/www/files
sudo chmod -R 755 /var/www/files
```

## 📁 Struktura katalogów

```
/var/www/files/
├── app.py
├── requirements.txt
├── venv/
├── uploads/
├── users_data.json
└── templates/
```

## 🔧 Konfiguracja aplikacji

### Zmienne środowiskowe

Stwórz plik `.env`:

```env
SECRET_KEY=twoj-bardzo-bezpieczny-klucz
FLASK_ENV=production
```

### Konfiguracja w app.py

```python
# Zmień SECRET_KEY na silny klucz
SECRET_KEY = os.environ.get('SECRET_KEY') or 'zmien-na-silny-klucz'
```

## 📊 Monitoring

### Logi aplikacji

```bash
# Sprawdź logi
tail -f /var/www/files/app.log

# Logi systemd
sudo journalctl -u files-app -f
```

### Logi Nginx

```bash
# Logi dostępu
sudo tail -f /var/log/nginx/access.log

# Logi błędów
sudo tail -f /var/log/nginx/error.log
```

## 🔄 Aktualizacje

```bash
# Pobierz najnowsze zmiany
git pull origin main

# Restart aplikacji
sudo systemctl restart files-app
```

## 🚨 Troubleshooting

### Problem z portem 5000

```bash
# Sprawdź co używa portu
sudo lsof -i :5000

# Zabij pierwszą aplikację
sudo kill -9 PID
```

### Problem z uprawnieniami

```bash
# Napraw uprawnienia
sudo chown -R www-data:www-data /var/www/files
sudo chmod -R 755 /var/www/files
```

### Problem z SSL

```bash
# Odnów certyfikat
sudo certbot renew --dry-run
```

## ✅ Testowanie

Po deploy sprawdź:

1. **Strona główna**: `https://files.twoja-domena.com`
2. **Upload pliku**: Prześlij testowy plik
3. **Download**: Pobierz plik ze zmienioną nazwą
4. **Konwersja PDF**: Prześlij obrazy i skonwertuj do PDF
5. **SSL**: Sprawdź czy certyfikat jest ważny

## 🎯 Rezultat

Aplikacja będzie dostępna pod adresem:
- `https://files.twoja-domena.com`

Z pełną funkcjonalnością:
- ✅ Upload plików
- ✅ Zmiana nazw
- ✅ Konwersja do PDF
- ✅ Download plików
- ✅ SSL/HTTPS
- ✅ Responsywny design
