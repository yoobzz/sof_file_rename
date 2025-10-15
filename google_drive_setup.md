# 🔧 Konfiguracja Google Drive API

## Krok 1: Stworzenie projektu w Google Cloud Console

1. Idź do [Google Cloud Console](https://console.cloud.google.com/)
2. Kliknij "Select a project" i "New Project"
3. Nadaj nazwę projektowi (np. "Student Files App")
4. Kliknij "Create"

## Krok 2: Włączenie Google Drive API

1. W menu po lewej wybierz "APIs & Services" > "Library"
2. Wyszukaj "Google Drive API"
3. Kliknij na "Google Drive API"
4. Kliknij "Enable"

## Krok 3: Tworzenie credentials

1. Idź do "APIs & Services" > "Credentials"
2. Kliknij "Create Credentials" > "OAuth client ID"
3. Jeśli to pierwszy raz, skonfiguruj OAuth consent screen:
   - User Type: External
   - App name: "Student Files App"
   - User support email: twój email
   - Developer contact: twój email
   - Dodaj swój email w "Test users"

## Krok 4: Konfiguracja OAuth Client

1. Application type: "Desktop application"
2. Name: "Student Files Desktop Client"
3. Kliknij "Create"
4. Pobierz plik JSON (credentials.json)
5. Umieść plik w folderze aplikacji

## Krok 5: Pierwsze uruchomienie

1. Uruchom aplikację: `python app.py`
2. Kliknij "Zapisz na Google Drive" w aplikacji
3. Otworzy się przeglądarka z autoryzacją Google
4. Zaloguj się i kliknij "Allow"
5. Aplikacja automatycznie zapisze token w pliku `token.pickle`

## Krok 6: Sprawdzenie

Po pierwszej autoryzacji:
- Plik `token.pickle` zostanie utworzony
- Kolejne użycie nie będzie wymagało ponownej autoryzacji
- Pliki będą zapisywane w folderze "Student Files" na Twoim Google Drive

## 🔒 Bezpieczeństwo

- **NIE** commituj pliku `credentials.json` do repozytorium
- **NIE** commituj pliku `token.pickle` do repozytorium
- Dodaj te pliki do `.gitignore`
- W przypadku kompromitacji - usuń credentials w Google Cloud Console

## ❗ Troubleshooting

**Błąd "Invalid credentials":**
- Usuń plik `token.pickle`
- Uruchom ponownie i przejdź przez autoryzację

**Błąd "Access blocked":**
- Sprawdź czy aplikacja jest w trybie testowym
- Dodaj swój email w "Test users" w OAuth consent screen

**Błąd "Quota exceeded":**
- Sprawdź limity API w Google Cloud Console
- Rozważ upgrade do płatnego planu
