# Emotion Detection Web Application

A machine learning-powered web application that detects emotions from facial expressions using deep learning.

## 🎯 Features

- **Real-time Emotion Detection**: Upload facial images to detect 7 different emotions
- **Deep Learning Model**: CNN-based model trained on facial expression data
- **Interactive Web Interface**: Modern, responsive UI with drag-and-drop support
- **Confidence Scores**: View detailed probability scores for all emotions
- **History Tracking**: SQLite database stores all predictions with timestamps
- **REST API**: JSON-based API endpoints for integration

## 😊 Supported Emotions

1. Happy
2. Sad
3. Angry
4. Surprise
5. Fear
6. Disgust
7. Neutral

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **ML Framework**: TensorFlow/Keras
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Deployment**: Render/Vercel

## 📁 Project Structure

```
Onipede-22CG031936/
│
├── app.py                      # Flask web application
├── model_training.py           # ML model training script
├── requirements.txt            # Python dependencies
├── database.db                 # SQLite database
├── face_emotionModel.h5        # Trained model file
├── link_web_app.txt           # Deployed app URL
├── Procfile                    # Render deployment config
├── runtime.txt                 # Python version specification
│
├── data/
│   └── data/
│       └── emotions.csv        # Training dataset
│
├── templates/
│   └── index.html             # Web interface
│
└── static/
    └── uploads/               # Uploaded images storage
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Onipede-22CG031936
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the model (optional)**
   ```bash
   python model_training.py
   ```
   Note: This requires the dataset in `data/data/emotions.csv`

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the app**
   Open your browser and navigate to `http://localhost:5000`

## 📊 API Endpoints

### 1. Home Page
- **URL**: `/`
- **Method**: GET
- **Description**: Renders the main web interface

### 2. Predict Emotion
- **URL**: `/predict`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**: 
  - `file`: Image file (JPG, PNG, GIF, BMP)
- **Response**:
  ```json
  {
    "success": true,
    "emotion": "Happy",
    "confidence": 95.5,
    "all_emotions": {
      "Happy": 95.5,
      "Neutral": 2.3,
      "Surprise": 1.2,
      ...
    },
    "image_url": "/static/uploads/image.jpg"
  }
  ```

### 3. Prediction History
- **URL**: `/history`
- **Method**: GET
- **Description**: Returns last 50 predictions

### 4. Statistics
- **URL**: `/stats`
- **Method**: GET
- **Description**: Returns emotion distribution statistics

### 5. Health Check
- **URL**: `/health`
- **Method**: GET
- **Description**: API health status

## 🎓 Model Architecture

The emotion detection model uses a Convolutional Neural Network (CNN) with:
- 3 Convolutional blocks with BatchNormalization
- MaxPooling and Dropout layers for regularization
- Dense layers for classification
- Softmax activation for 7-class output

**Input**: 48x48 grayscale images  
**Output**: 7 emotion probabilities

## 📦 Deployment

### Deploy to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Render will automatically detect the `Procfile`
4. Set environment variables if needed
5. Deploy!

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts
4. Your app will be deployed!

## 🗄️ Database Schema

```sql
CREATE TABLE emotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion TEXT NOT NULL,
    confidence REAL,
    filename TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 📝 Usage Example

```python
import requests

# Upload image for prediction
url = "http://localhost:5000/predict"
files = {'file': open('face.jpg', 'rb')}
response = requests.post(url, files=files)
result = response.json()

print(f"Emotion: {result['emotion']}")
print(f"Confidence: {result['confidence']}%")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Onipede** - Matric Number: 22CG031936

## 🙏 Acknowledgments

- FER2013 dataset for emotion recognition
- TensorFlow/Keras team for the ML framework
- Flask team for the web framework

## 📞 Contact

For questions or support, please open an issue in the repository.

---

**Note**: Make sure to have the trained model file (`face_emotionModel.h5`) in the root directory before running the application. If you don't have it, run `model_training.py` first with the appropriate dataset.

