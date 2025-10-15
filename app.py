from flask import Flask, render_template, request, jsonify, send_file, session, url_for
from werkzeug.utils import secure_filename
import os
import json
import uuid
from datetime import datetime
import re
from pathlib import Path

app = Flask(__name__)

# Konfiguracja
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
USERS_FILE = 'users_data.json'
SECRET_KEY = 'dev-secret-key-change-in-production'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['SECRET_KEY'] = SECRET_KEY

# Stwórz folder uploads jeśli nie istnieje
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users_data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(original_name, first_name, last_name, exercise_name=None):
    """Generuje nową nazwę pliku w formacie: Imię_Nazwisko_[Ćwiczenie]"""
    
    # Pobierz rozszerzenie pliku
    file_ext = Path(original_name).suffix
    
    # Stwórz podstawową nazwę
    base_name = f"{first_name}_{last_name}"
    
    # Dodaj nazwę ćwiczenia jeśli podana
    if exercise_name and exercise_name.strip():
        exercise_clean = re.sub(r'[^\w\s-]', '', exercise_name.strip())
        exercise_clean = re.sub(r'\s+', '_', exercise_clean)
        base_name += f"_{exercise_clean}"
    
    return f"{base_name}{file_ext}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Brak pliku'}), 400
    
    file = request.files['file']
    
    # Pobierz dane z formularza lub z sesji
    user_id = session.get('user_id')
    users_data = load_users()
    user_data = users_data.get(user_id, {}) if user_id else {}
    
    first_name = request.form.get('firstName', '').strip() or user_data.get('firstName', '')
    last_name = request.form.get('lastName', '').strip() or user_data.get('lastName', '')
    
    # Pobierz przedmiot i projekt
    subject = request.form.get('subjectSelect', '').strip()
    custom_subject = request.form.get('customSubject', '').strip()
    project_name = request.form.get('projectName', '').strip()
    
    # Stwórz pełną nazwę ćwiczenia
    exercise_name = ''
    if subject and subject != 'custom':
        exercise_name = subject
    elif custom_subject:
        exercise_name = custom_subject
    
    if project_name:
        exercise_name += f'_{project_name}' if exercise_name else project_name
    
    if file.filename == '':
        return jsonify({'error': 'Nie wybrano pliku'}), 400
    
    if not first_name or not last_name:
        return jsonify({'error': 'Imię i nazwisko są wymagane. Skonfiguruj je w ustawieniach.'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Nieprawidłowy typ pliku'}), 400
    
    # Zapisz dane użytkownika w sesji
    session['firstName'] = first_name
    session['lastName'] = last_name
    session['exerciseName'] = exercise_name
    
    # Zapisz dane użytkownika w pliku
    users_data = load_users()
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    
    users_data[user_id] = {
        'firstName': first_name,
        'lastName': last_name,
        'lastExercise': exercise_name,
        'lastLogin': datetime.now().isoformat()
    }
    save_users(users_data)
    
    # Wygeneruj nową nazwę pliku
    new_filename = generate_filename(file.filename, first_name, last_name, exercise_name)
    
    # Zapisz plik
    filename = secure_filename(new_filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    return jsonify({
        'success': True,
        'newFilename': new_filename,
        'filePath': filename,
        'message': 'Plik został przesłany pomyślnie!'
    })

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'Plik nie został znaleziony'}), 404

@app.route('/get_user_data')
def get_user_data():
    user_id = session.get('user_id')
    if user_id:
        users_data = load_users()
        return jsonify(users_data.get(user_id, {}))
    return jsonify({})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
