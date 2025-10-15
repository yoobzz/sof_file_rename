# 🚀 Deploy Strony Internetowej - Student Files

## Opcja 1: Vercel (ZALECANE - Darmowe i proste)

### Kroki deploy:

1. **Zarejestruj się na Vercel:**
   - Idź na [vercel.com](https://vercel.com)
   - Zaloguj się przez GitHub

2. **Przygotuj repozytorium:**
   ```bash
   cd file_renamer_app
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Push na GitHub:**
   ```bash
   git remote add origin https://github.com/twoj-username/student-files.git
   git push -u origin main
   ```

4. **Deploy na Vercel:**
   - W Vercel kliknij "New Project"
   - Importuj swoje repo z GitHub
   - Vercel automatycznie wykryje Python
   - Kliknij "Deploy"

5. **Konfiguracja zmiennych środowiskowych:**
   - W Vercel Dashboard > Settings > Environment Variables
   - Dodaj:
     ```
     SECRET_KEY=twoj-bezpieczny-klucz
     SENDGRID_API_KEY=twoj-sendgrid-klucz
     FROM_EMAIL=twoj@email.com
     ```

### ✅ Rezultat:
- Twoja strona będzie dostępna pod: `https://twoj-projekt.vercel.app`
- Automatyczne HTTPS
- Darmowy hosting
- Automatyczne redeploy przy push na GitHub

---

## Opcja 2: Heroku (Alternatywa)

### Kroki deploy:

1. **Zainstaluj Heroku CLI:**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows - pobierz z heroku.com
   ```

2. **Zaloguj się:**
   ```bash
   heroku login
   ```

3. **Stwórz aplikację:**
   ```bash
   heroku create student-files-app
   ```

4. **Dodaj zmienne środowiskowe:**
   ```bash
   heroku config:set SECRET_KEY=twoj-klucz
   heroku config:set SENDGRID_API_KEY=twoj-klucz
   heroku config:set FROM_EMAIL=twoj@email.com
   ```

5. **Deploy:**
   ```bash
   git push heroku main
   ```

### ✅ Rezultat:
- Strona dostępna pod: `https://student-files-app.herokuapp.com`

---

## Opcja 3: Railway (Nowoczesny hosting)

### Kroki deploy:

1. **Zarejestruj się na [railway.app](https://railway.app)**
2. **Połącz GitHub repo**
3. **Railway automatycznie wykryje Python**
4. **Dodaj zmienne środowiskowe w dashboard**
5. **Deploy automatyczny**

### ✅ Rezultat:
- Strona dostępna pod domeną Railway
- Darmowy plan dostępny

---

## 🌐 Konfiguracja Domeny Własnej

### Vercel:
1. W Settings > Domains dodaj swoją domenę
2. Skonfiguruj DNS u dostawcy domeny
3. Automatyczne SSL

### Heroku:
1. W Settings > Domains dodaj domenę
2. Skonfiguruj DNS
3. SSL automatyczny (Heroku SSL)

---

## 🔧 Konfiguracja Produkcyjna

### Wymagane zmienne środowiskowe:
```env
SECRET_KEY=twoj-bardzo-bezpieczny-klucz
SENDGRID_API_KEY=twoj-sendgrid-klucz
FROM_EMAIL=noreply@twoja-domena.com
FLASK_ENV=production
```

### Opcjonalne (Google Drive):
```env
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
GOOGLE_DRIVE_TOKEN_FILE=token.pickle
```

---

## 📱 Testowanie Strony

Po deploy:
1. Otwórz stronę w przeglądarce
2. Przetestuj upload pliku
3. Sprawdź czy nazwy się zmieniają
4. Przetestuj na telefonie
5. Sprawdź funkcje Google Drive/Email

---

## 🚨 Ważne Uwagi

### Bezpieczeństwo:
- ✅ Używaj silnego SECRET_KEY
- ✅ Nie commituj credentials.json
- ✅ Używaj HTTPS (automatyczny)
- ✅ Ogranicz rozmiar plików

### Performance:
- ✅ Vercel/Railway mają automatyczne CDN
- ✅ Heroku może wymagać upgrade dla większego ruchu
- ✅ Rozważ caching dla dużych plików

### Monitoring:
- ✅ Sprawdź logi w dashboard hostingu
- ✅ Monitoruj użycie zasobów
- ✅ Ustaw alerty dla błędów

---

## 🎯 Rekomendacja

**Dla początkujących: Vercel**
- Najłatwiejszy setup
- Darmowy
- Automatyczny HTTPS
- Dobra dokumentacja

**Dla zaawansowanych: Railway**
- Nowoczesny stack
- Łatwy deploy
- Dobra integracja z GitHub

**Dla enterprise: Heroku**
- Sprawdzone rozwiązanie
- Wiele opcji skalowania
- Dobra dokumentacja
