# 🚀 Szybki Deploy na PythonAnywhere

## ⚡ Kroki (5 minut)

### 1. **Zarejestruj się na pythonanywhere.com**

### 2. **W Console wykonaj:**
```bash
git clone https://github.com/yoobzz/sof_file_rename.git
cd sof_file_rename
mkdir uploads
chmod 755 uploads
pip3.10 install --user -r requirements.txt
```

### 3. **Napraw ścieżki w app.py:**
```bash
# Zamień 'username' na swój username w app.py
sed -i 's/username/your_username/g' app.py
```

### 4. **W Web tab:**
- Kliknij "Add a new web app"
- Wybierz "Flask"
- Wybierz Python 3.10
- Ścieżka: `/home/your_username/sof_file_rename/app.py`

### 5. **Kliknij "Reload"**

## ✅ Gotowe!

Aplikacja będzie dostępna pod:
`your_username.pythonanywhere.com`

## 🔧 Jeśli są błędy:

### Problem z uprawnieniami:
```bash
chmod 755 uploads/
chmod 644 *.py
```

### Problem z miejscem:
```bash
# Sprawdź użycie
df -h
du -sh uploads/
```

### Problem z zależnościami:
```bash
pip3.10 install --user --upgrade -r requirements.txt
```

## 📊 Limity darmowego planu:
- 512MB miejsca
- 100 sekund CPU/dzień
- 1 aplikacja

## 💡 Wskazówki:
- Usuwaj stare pliki regularnie
- Używaj małych plików do testów
- Upgrade do płatnego planu jeśli potrzeba
