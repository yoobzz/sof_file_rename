from flask import Flask, render_template, request, jsonify, send_file, session, url_for
from werkzeug.utils import secure_filename
import os
import json
import uuid
from datetime import datetime
import re
from pathlib import Path
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow nie jest dostępne - konwersja do PDF będzie wyłączona")
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import ImageReader
import io
import PyPDF2

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
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except Exception as e:
    print(f"Nie można utworzyć folderu uploads: {e}")

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

def convert_images_to_pdf(image_paths, output_path, page_size=A4):
    """Konwertuje obrazy do PDF"""
    try:
        c = canvas.Canvas(output_path, pagesize=page_size)
        width, height = page_size
        
        for i, image_path in enumerate(image_paths):
            if i > 0:  # Nowa strona dla każdego obrazu oprócz pierwszego
                c.showPage()
            
            try:
                # Otwórz obraz
                img = Image.open(image_path)
                
                # Oblicz rozmiary zachowując proporcje
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height
                
                # Dostosuj rozmiar do strony
                if aspect_ratio > width / height:
                    # Obraz szerszy niż strona
                    new_width = width - 40  # margines 20px z każdej strony
                    new_height = new_width / aspect_ratio
                else:
                    # Obraz wyższy niż strona
                    new_height = height - 40
                    new_width = new_height * aspect_ratio
                
                # Wyśrodkuj obraz
                x = (width - new_width) / 2
                y = (height - new_height) / 2
                
                # Dodaj obraz do PDF
                c.drawImage(image_path, x, y, width=new_width, height=new_height)
                
            except Exception as e:
                print(f"Błąd podczas przetwarzania obrazu {image_path}: {e}")
                continue
        
        c.save()
    except Exception as e:
        print(f"Błąd podczas tworzenia PDF: {e}")
        raise

def convert_single_image_to_pdf(image_path, output_path, page_size=A4):
    """Konwertuje pojedynczy obraz do PDF"""
    convert_images_to_pdf([image_path], output_path, page_size)

def compress_pdf(input_path, output_path):
    """Kompresuje PDF używając PyPDF2"""
    try:
        with open(input_path, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            pdf_writer = PyPDF2.PdfWriter()
            
            # Kopiuj wszystkie strony z kompresją
            for page in pdf_reader.pages:
                page.compress_content_streams()
                pdf_writer.add_page(page)
            
            # Zapisz skompresowany PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Błąd podczas kompresji PDF: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Sprawdź czy są pliki
        if 'files' not in request.files and 'file' not in request.files:
            return jsonify({'error': 'Brak plików'}), 400
        
        # Pobierz pliki (może być jeden lub wiele)
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            # Fallback na pojedynczy plik
            files = [request.files['file']]
            if files[0].filename == '':
                return jsonify({'error': 'Nie wybrano plików'}), 400
        
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
        
        # Pobierz opcje konwersji
        convert_to_pdf = request.form.get('convertToPdf') == 'on'
        should_compress_pdf = request.form.get('compressPdf') == 'on'
        
        # Stwórz pełną nazwę ćwiczenia
        exercise_name = ''
        if subject and subject != 'custom':
            exercise_name = subject
        elif custom_subject:
            exercise_name = custom_subject
        
        if project_name:
            exercise_name += f'_{project_name}' if exercise_name else project_name
        
        if not first_name or not last_name:
            return jsonify({'error': 'Imię i nazwisko są wymagane. Skonfiguruj je w ustawieniach.'}), 400
        
        # Sprawdź czy wszystkie pliki są dozwolone
        for file in files:
            if not allowed_file(file.filename):
                return jsonify({'error': f'Nieprawidłowy typ pliku: {file.filename}'}), 400
        
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
        
        saved_files = []
        
        if convert_to_pdf:
            # Sprawdź czy PIL jest dostępne
            if not PIL_AVAILABLE:
                return jsonify({'error': 'Konwersja do PDF nie jest dostępna na tym serwerze. Spróbuj bez konwersji.'}), 400
            
            # Konwersja do PDF
            image_paths = []
            
            # Zapisz wszystkie obrazy tymczasowo
            for file in files:
                if file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    try:
                        temp_filename = secure_filename(file.filename)
                        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{temp_filename}")
                        file.save(temp_path)
                        image_paths.append(temp_path)
                    except Exception as e:
                        print(f"Błąd podczas zapisywania obrazu {file.filename}: {e}")
                        continue
            
            if image_paths:
                # Wygeneruj nazwę PDF
                pdf_filename = generate_filename("combined.pdf", first_name, last_name, exercise_name)
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                compressed_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"compressed_{pdf_filename}")
                
                # Konwertuj obrazy do PDF
                convert_images_to_pdf(image_paths, pdf_path)
                
                # Kompresuj PDF tylko jeśli zaznaczono
                if should_compress_pdf:
                    if compress_pdf(pdf_path, compressed_pdf_path):
                        # Usuń niekompresowany PDF i zmień nazwę skompresowanego
                        os.remove(pdf_path)
                        os.rename(compressed_pdf_path, pdf_path)
                        print(f"PDF skompresowany: {pdf_filename}")
                    else:
                        print(f"Nie udało się skompresować PDF: {pdf_filename}")
                else:
                    print(f"PDF utworzony bez kompresji: {pdf_filename}")
                
                # Usuń tymczasowe pliki
                for temp_path in image_paths:
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                
                saved_files.append({
                    'filename': pdf_filename,
                    'filePath': pdf_filename,
                    'type': 'pdf'
                })
            else:
                return jsonify({'error': 'Brak obrazów do konwersji. Upewnij się, że przesłałeś pliki PNG, JPG, JPEG lub GIF.'}), 400
        else:
            # Normalne zapisywanie plików
            for file in files:
                try:
                    new_filename = generate_filename(file.filename, first_name, last_name, exercise_name)
                    filename = secure_filename(new_filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    saved_files.append({
                        'filename': new_filename,
                        'filePath': filename,
                        'type': 'original'
                    })
                except Exception as e:
                    print(f"Błąd podczas zapisywania pliku {file.filename}: {e}")
                    return jsonify({'error': f'Błąd podczas zapisywania pliku {file.filename}: {str(e)}'}), 500
        
        return jsonify({
            'success': True,
            'files': saved_files,
            'message': f'{"Pliki zostały" if len(saved_files) > 1 else "Plik został"} przesłane pomyślnie!'
        })
    except Exception as e:
        print(f"Błąd podczas przesyłania pliku: {e}")
        return jsonify({'error': f'wystąpił błąd podczas przesyłania pliku (spróbuj jeszcze raz, może tym razem się uda): {str(e)}'}), 500

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


@app.route('/upload_to_drive', methods=['POST'])
def upload_to_drive():
    return jsonify({'error': 'Funkcja Google Drive będzie dostępna wkrótce!'}), 501

@app.route('/send_email', methods=['POST'])
def send_email():
    return jsonify({'error': 'Funkcja email będzie dostępna wkrótce!'}), 501

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        app.run(debug=debug, host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Błąd uruchamiania aplikacji: {e}")
        raise
