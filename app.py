# app.py
"""
Emotion Detection Web Application
Flask-based web app for detecting emotions from facial images
"""

# Set Keras backend to JAX (compatible with Python 3.14)
import os
os.environ['KERAS_BACKEND'] = 'jax'

from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Emotion labels (must match training order)
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load model
print("🔄 Loading emotion detection model...")
try:
    model = load_model('face_emotionModel.h5')
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create table with more fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotion TEXT NOT NULL,
            confidence REAL,
            filename TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    try:
        # Load image in grayscale
        img = image.load_img(img_path, target_size=(48, 48), color_mode='grayscale')
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def save_to_database(emotion, confidence, filename):
    """Save prediction result to database"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emotions (emotion, confidence, filename) VALUES (?, ?, ?)",
            (emotion, confidence, filename)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False

@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle emotion prediction from uploaded image"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please ensure face_emotionModel.h5 exists.'
            }), 500

        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file with secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess image
        img_array = preprocess_image(filepath)
        if img_array is None:
            return jsonify({
                'success': False,
                'error': 'Error processing image'
            }), 500

        # Make prediction
        prediction = model.predict(img_array, verbose=0)
        emotion_idx = np.argmax(prediction[0])
        emotion = EMOTIONS[emotion_idx]
        confidence = float(prediction[0][emotion_idx]) * 100

        # Get all emotion probabilities
        all_emotions = {
            EMOTIONS[i]: float(prediction[0][i]) * 100
            for i in range(len(EMOTIONS))
        }

        # Save to database
        save_to_database(emotion, confidence, filename)

        # Return result
        return jsonify({
            'success': True,
            'emotion': emotion,
            'confidence': round(confidence, 2),
            'all_emotions': {k: round(v, 2) for k, v in all_emotions.items()},
            'image_url': f'/static/uploads/{filename}'
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/history')
def history():
    """Get prediction history from database"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emotion, confidence, filename, timestamp FROM emotions ORDER BY timestamp DESC LIMIT 50"
        )
        rows = cursor.fetchall()
        conn.close()

        history_data = [
            {
                'emotion': row[0],
                'confidence': row[1],
                'filename': row[2],
                'timestamp': row[3]
            }
            for row in rows
        ]

        return jsonify({
            'success': True,
            'history': history_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stats')
def stats():
    """Get emotion statistics"""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emotion, COUNT(*) as count FROM emotions GROUP BY emotion ORDER BY count DESC"
        )
        rows = cursor.fetchall()
        conn.close()

        stats_data = {row[0]: row[1] for row in rows}

        return jsonify({
            'success': True,
            'stats': stats_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/uploads', exist_ok=True)

    # Initialize database
    init_db()

    # Run app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
