from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import sqlite3
from datetime import datetime
from PIL import Image
from werkzeug.utils import secure_filename
import uuid 

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = load_model('petri_dish_classifier (1).h5')

# Configuration
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create SQLite DB if it doesn't exist
def init_db():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            prediction TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/test_result')
def test_result():
    return render_template('result.html', filename='test.jpg', prediction='Bacterium Green')

# Check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Preprocess uploaded image for prediction
def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((150, 150))  # Ensure this matches your model input size
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Prediction handler
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part in the request."

    file = request.files['file']

    if file.filename == '':
        return "No file selected."

    if file and allowed_file(file.filename):
        # Secure and make filename unique
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(filepath)

        # Preprocess and predict
        img_array = preprocess_image(filepath)
        prediction = model.predict(img_array)
        predicted_class_index = np.argmax(prediction, axis=1)[0]

        # Match with class labels (based on your folders)
        class_labels = ['Bacterium Green', 'Bacterium Yellow', 'Both Bacterium', 'Clean']
        predicted_label = class_labels[predicted_class_index]

        # Save to SQLite DB
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        c.execute("INSERT INTO predictions (filename, prediction, timestamp) VALUES (?, ?, ?)", 
                  (unique_filename, predicted_label, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        return render_template('result.html', filename=unique_filename, prediction=predicted_label)

    return "Invalid file type."

# Result page (in case someone accesses directly)
@app.route('/result')
def result():
    return render_template('result.html')

# History page
@app.route('/history')
def history():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM predictions")
    data = c.fetchall()
    conn.close()
    return render_template('history.html', data=data)

# Run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
