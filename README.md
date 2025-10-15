# 📝 Aplikacja do Zmiany Nazw Plików - Student Files

Aplikacja webowa dla studentów do automatycznego formatowania nazw plików z integracją Google Drive i email.

## ✨ Funkcje

- **Automatyczna zmiana nazw plików** w formacie: `Imię_Nazwisko_[Ćwiczenie]_timestamp`
- **Responsywny design** - działa na telefonach i komputerach
- **Drag & Drop** upload plików
- **Zapamiętywanie danych** użytkownika (imię, nazwisko, ostatnie ćwiczenie)
- **Integracja z Google Drive** - automatyczne zapisywanie plików
- **Wysyłanie email** z linkiem do pobrania lub załącznikiem
- **Wsparcie dla różnych formatów**: PNG, JPG, PDF, DOC, DOCX

## 🚀 Instalacja i Deploy

### 🌐 Opcja 1: Deploy na Vercel (ZALECANE - Strona Internetowa)

**Szybki deploy:**
```bash
cd file_renamer_app
./deploy_vercel.sh
```

**Lub ręcznie:**
1. Zarejestruj się na [vercel.com](https://vercel.com)
2. Połącz z GitHub
3. Importuj repozytorium
4. Deploy automatyczny!

**Rezultat:** Twoja strona będzie dostępna online pod adresem `https://twoj-projekt.vercel.app`

### 💻 Opcja 2: Uruchomienie Lokalne

```bash
cd file_renamer_app
source ../dziubek/bin/activate  # lub twoje środowisko Python
pip install -r requirements.txt
python app.py
```

Aplikacja będzie dostępna pod adresem: http://localhost:5000

### ⚙️ Konfiguracja

**Dla deploy online (Vercel):**
- Dodaj zmienne środowiskowe w Vercel Dashboard
- `SECRET_KEY=twoj-bezpieczny-klucz`
- `SENDGRID_API_KEY=twoj-sendgrid-klucz` (opcjonalne)

**Dla uruchomienia lokalnego:**
```bash
cp env_example.txt .env
# Edytuj .env z odpowiednimi wartościami
```

### 📖 Szczegółowe Instrukcje Deploy

Zobacz [DEPLOY.md](DEPLOY.md) dla szczegółowych instrukcji deploy na:
- Vercel (zalecane)
- Heroku
- Railway
- Konfiguracja własnej domeny

## 📱 Użycie

### Podstawowe użycie:
1. Otwórz aplikację w przeglądarce
2. Wpisz imię i nazwisko
3. Opcjonalnie dodaj nazwę ćwiczenia
4. Wybierz plik (lub przeciągnij)
5. Kliknij "Prześlij i Zmień Nazwę"

### Dodatkowe opcje:
- **Pobierz plik** - bezpośrednie pobranie ze zmienioną nazwą
- **Zapisz na Google Drive** - automatyczny upload do chmury
- **Wyślij emailem** - wysyłka z linkiem lub załącznikiem

## 🔧 Konfiguracja Email

### SendGrid (zalecane):
1. Zarejestruj się na [SendGrid](https://sendgrid.com/)
2. Stwórz API Key
3. Dodaj do `.env`: `SENDGRID_API_KEY=twoj-klucz`

### SMTP (alternatywnie):
Dodaj do `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=twoj@gmail.com
SMTP_PASSWORD=twoje-haslo-aplikacji
```

## 📁 Struktura Projektu

```
file_renamer_app/
├── app.py                 # Główna aplikacja Flask
├── config.py             # Konfiguracja
├── google_drive_service.py # Integracja z Google Drive
├── email_service.py      # Integracja z email
├── requirements.txt      # Zależności Python
├── templates/
│   └── index.html        # Frontend
├── uploads/              # Przesłane pliki
├── users_data.json       # Dane użytkowników
└── README.md            # Ta dokumentacja
```

## 🛠️ Rozwój

### Dodanie nowych formatów plików:
Edytuj `config.py`:
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}
```

### Zmiana formatu nazw:
Edytuj funkcję `generate_filename()` w `app.py`

## 🔒 Bezpieczeństwo

- Używaj silnego `SECRET_KEY` w produkcji
- Nie commituj plików `.env` i `credentials.json`
- Ogranicz rozmiar uploadowanych plików
- Używaj HTTPS w produkcji

## 📞 Wsparcie

W przypadku problemów sprawdź:
1. Czy wszystkie zależności są zainstalowane
2. Czy pliki konfiguracyjne są poprawne
3. Czy port 5000 jest wolny
4. Logi aplikacji w konsoli

## 🎯 Przykłady Nazw

**Przed:**
- `IMG_20231201_143022.jpg`
- `zadanie_matematyka.pdf`
- `scan_dokumentu.png`

**Po:**
- `Jan_Kowalski_Zadanie_1_20231201_143022.jpg`
- `Anna_Nowak_Test_koncowy_20231201_143022.pdf`
- `Piotr_Wisniewski_20231201_143022.png`
