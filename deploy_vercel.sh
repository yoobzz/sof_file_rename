#!/bin/bash

echo "🚀 Deploy aplikacji Student Files na Vercel"
echo "=========================================="

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

# Sprawdź czy Vercel CLI jest zainstalowany
if ! command -v vercel &> /dev/null; then
    echo "📥 Instalacja Vercel CLI..."
    npm install -g vercel
fi

echo "🌐 Logowanie do Vercel..."
vercel login

echo "🚀 Deploy aplikacji..."
vercel --prod

echo ""
echo "✅ Deploy zakończony!"
echo "🌐 Twoja strona jest teraz dostępna online!"
echo ""
echo "📝 Następne kroki:"
echo "1. Dodaj zmienne środowiskowe w Vercel Dashboard"
echo "2. Skonfiguruj Google Drive API (opcjonalnie)"
echo "3. Skonfiguruj SendGrid (opcjonalnie)"
echo "4. Przetestuj wszystkie funkcje"
echo ""
echo "📖 Więcej informacji w DEPLOY.md"
