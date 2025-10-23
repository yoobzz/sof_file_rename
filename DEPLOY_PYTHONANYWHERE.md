# 🚀 Deploy na PythonAnywhere - Student Files

## 📋 Wymagania

- Konto PythonAnywhere (darmowe lub płatne)
- Aplikacja gotowa do deploy

## 🔧 Krok po kroku

### 1. Przygotowanie aplikacji

```bash
# Sklonuj repo lokalnie
git clone https://github.com/yoobzz/sof_file_rename.git
cd sof_file_rename
```

### 2. PythonAnywhere Setup

1. **Zarejestruj się na [pythonanywhere.com](https://pythonanywhere.com)**
2. **Wybierz plan:**
   - Darmowy: 512MB, 1 aplikacja
   - Płatny: $5/miesiąc, 3GB, więcej aplikacji

### 3. Upload plików

**Opcja A: Git (zalecane)**
```bash
# W PythonAnywhere Console
git clone https://github.com/yoobzz/sof_file_rename.git
cd sof_file_rename
```

**Opcja B: Upload plików**
1. Idź do **Files** w PythonAnywhere
2. Upload wszystkich plików z repo

### 4. Instalacja zależności

```bash
# W PythonAnywhere Console
pip3.10 install --user -r requirements.txt
```

### 5. Konfiguracja aplikacji

1. **Idź do Web tab**
2. **Kliknij "Add a new web app"**
3. **Wybierz "Flask"**
4. **Wybierz Python 3.10**
5. **Ścieżka do kodu:** `/home/username/sof_file_rename/app.py`

### 6. Konfiguracja WSGI

W pliku WSGI (`/var/www/username_pythonanywhere_com_wsgi.py`):

```python
import sys
path = '/home/username/sof_file_rename'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 7. Konfiguracja domeny

**Opcja A: Subdomena PythonAnywhere**
- `username.pythonanywhere.com/files`

**Opcja B: Własna domena**
1. W **Web tab** → **Domains**
2. Dodaj `files.twoja-domena.com`
3. Skonfiguruj DNS w Vercel:
   ```
   files.twoja-domena.com → username.pythonanywhere.com
   ```

### 8. Uruchomienie

1. **Kliknij "Reload"** w Web tab
2. **Sprawdź logi** w **Web tab** → **Error log**

## 🔧 Konfiguracja aplikacji

### Zmienne środowiskowe

W pliku `app.py` zmień:

```python
# Zmień na silny klucz
SECRET_KEY = 'twoj-bardzo-bezpieczny-klucz-12345'

# Konfiguracja dla PythonAnywhere
UPLOAD_FOLDER = '/home/username/sof_file_rename/uploads'
```

### Uprawnienia

```bash
# Stwórz folder uploads
mkdir uploads
chmod 755 uploads
```

## 📊 Monitoring

### Sprawdź użycie miejsca

```bash
# W Console
df -h
du -sh uploads/
```

### Logi aplikacji

- **Error log:** Web tab → Error log
- **Server log:** Web tab → Server log

## 🔄 Aktualizacje

```bash
# W Console
cd sof_file_rename
git pull origin main
# Reload w Web tab
```

## 🚨 Troubleshooting

### Problem z miejscem

```bash
# Usuń stare pliki
find uploads/ -type f -mtime +7 -delete
```

### Problem z uprawnieniami

```bash
chmod 755 uploads/
chmod 644 *.py
```

### Problem z zależnościami

```bash
pip3.10 install --user --upgrade -r requirements.txt
```

## 💰 Limity darmowego planu

- **512MB miejsca**
- **1 aplikacja**
- **100 sekund CPU/dzień**
- **Brak własnej domeny**

## ✅ Testowanie

Po deploy sprawdź:

1. **Strona główna:** `username.pythonanywhere.com`
2. **Upload pliku:** Prześlij testowy plik
3. **Download:** Pobierz plik ze zmienioną nazwą
4. **Konwersja PDF:** Prześlij obrazy i skonwertuj

## 🎯 Rezultat

Aplikacja będzie dostępna pod:
- `username.pythonanywhere.com` (darmowy plan)
- `files.twoja-domena.com` (z własną domeną)

Z pełną funkcjonalnością:
- ✅ Upload plików
- ✅ Zmiana nazw
- ✅ Konwersja do PDF
- ✅ Download plików
- ✅ SSL/HTTPS
