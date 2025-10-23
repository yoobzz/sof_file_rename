#!/usr/bin/env python3
"""
Skrypt konfiguracyjny dla PythonAnywhere
Uruchom ten skrypt w PythonAnywhere Console po sklonowaniu repo
"""

import os
import subprocess
import sys

def setup_pythonanywhere():
    """Konfiguruje aplikację dla PythonAnywhere"""
    
    print("🚀 Konfiguracja aplikacji dla PythonAnywhere")
    print("=" * 50)
    
    # Pobierz username
    username = os.environ.get('USER', 'username')
    print(f"👤 Username: {username}")
    
    # Ścieżki
    app_path = f"/home/{username}/sof_file_rename"
    uploads_path = f"{app_path}/uploads"
    
    print(f"📁 Ścieżka aplikacji: {app_path}")
    print(f"📁 Folder uploads: {uploads_path}")
    
    # Stwórz folder uploads
    try:
        os.makedirs(uploads_path, exist_ok=True)
        print("✅ Folder uploads utworzony")
    except Exception as e:
        print(f"❌ Błąd tworzenia folderu uploads: {e}")
        return False
    
    # Ustaw uprawnienia
    try:
        os.chmod(uploads_path, 0o755)
        print("✅ Uprawnienia ustawione")
    except Exception as e:
        print(f"❌ Błąd ustawiania uprawnień: {e}")
        return False
    
    # Zainstaluj zależności
    try:
        print("📦 Instalacja zależności...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"], 
                      check=True, cwd=app_path)
        print("✅ Zależności zainstalowane")
    except Exception as e:
        print(f"❌ Błąd instalacji zależności: {e}")
        return False
    
    # Aktualizuj app.py z prawidłowymi ścieżkami
    app_py_path = f"{app_path}/app.py"
    try:
        with open(app_py_path, 'r') as f:
            content = f.read()
        
        # Zamień username w ścieżkach
        content = content.replace('/home/username/', f'/home/{username}/')
        
        with open(app_py_path, 'w') as f:
            f.write(content)
        
        print("✅ app.py zaktualizowany z prawidłowymi ścieżkami")
    except Exception as e:
        print(f"❌ Błąd aktualizacji app.py: {e}")
        return False
    
    print("\n🎉 Konfiguracja zakończona!")
    print("\n📋 Następne kroki:")
    print("1. Idź do Web tab w PythonAnywhere")
    print("2. Kliknij 'Add a new web app'")
    print("3. Wybierz 'Flask'")
    print("4. Wybierz Python 3.10")
    print(f"5. Ścieżka do kodu: {app_py_path}")
    print("6. Kliknij 'Reload'")
    
    return True

if __name__ == "__main__":
    setup_pythonanywhere()
