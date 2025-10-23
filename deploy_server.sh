#!/bin/bash

echo "🚀 Deploy aplikacji Student Files na własny serwer"
echo "================================================="

# Sprawdź czy jesteś w odpowiednim folderze
if [ ! -f "app.py" ]; then
    echo "❌ Błąd: Uruchom skrypt z folderu file_renamer_app"
    exit 1
fi

# Sprawdź czy git jest zainicjowany
if [ ! -d ".git" ]; then
    echo "📦 Inicjalizacja Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Student Files App"
fi

echo "📋 Instrukcje deploy na własny serwer:"
echo ""
echo "1. 📁 Skopiuj pliki na serwer:"
echo "   scp -r . user@twoja-domena.com:/var/www/files/"
echo ""
echo "2. 🔧 Zaloguj się na serwer:"
echo "   ssh user@twoja-domena.com"
echo ""
echo "3. 📦 Zainstaluj zależności:"
echo "   cd /var/www/files"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo ""
echo "4. 🔧 Skonfiguruj nginx (plik /etc/nginx/sites-available/files):"
echo "   server {"
echo "       listen 80;"
echo "       server_name files.twoja-domena.com;"
echo "       location / {"
echo "           proxy_pass http://127.0.0.1:5000;"
echo "           proxy_set_header Host \$host;"
echo "           proxy_set_header X-Real-IP \$remote_addr;"
echo "       }"
echo "   }"
echo ""
echo "5. 🔗 Włącz konfigurację nginx:"
echo "   sudo ln -s /etc/nginx/sites-available/files /etc/nginx/sites-enabled/"
echo "   sudo nginx -t"
echo "   sudo systemctl reload nginx"
echo ""
echo "6. 🔒 Skonfiguruj SSL (Certbot):"
echo "   sudo certbot --nginx -d files.twoja-domena.com"
echo ""
echo "7. 🚀 Uruchom aplikację:"
echo "   cd /var/www/files"
echo "   source venv/bin/activate"
echo "   nohup python app.py > app.log 2>&1 &"
echo ""
echo "8. 🔄 Skonfiguruj systemd service (opcjonalnie):"
echo "   sudo nano /etc/systemd/system/files-app.service"
echo ""
echo "✅ Gotowe! Aplikacja będzie dostępna pod:"
echo "   https://files.twoja-domena.com"
echo ""
echo "📖 Więcej szczegółów w DEPLOY_SERVER.md"
