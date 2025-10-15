#!/bin/bash

# Skrypt uruchamiający aplikację w środowisku dziubek

echo "🚀 Uruchamianie aplikacji Student Files..."

# Aktywuj środowisko dziubek
source ../dziubek/bin/activate

# Zainstaluj zależności jeśli potrzeba
echo "📦 Sprawdzanie zależności..."
pip install -r requirements.txt

# Uruchom aplikację
echo "🌐 Uruchamianie serwera..."
echo "Aplikacja będzie dostępna pod: http://localhost:5000"
echo "Naciśnij Ctrl+C aby zatrzymać"
echo ""

python app.py
