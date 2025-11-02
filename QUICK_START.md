# Quick Start Guide - Emotion Detection App

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Get the Dataset (1 minute)

You need the FER2013 emotion dataset. Download it from:
- [Kaggle FER2013](https://www.kaggle.com/datasets/msambare/fer2013)
- Or use any emotion dataset in CSV format

Place the CSV file at: `data/data/emotions.csv`

**CSV Format Required:**
```csv
emotion,pixels
0,70 80 82 72 58 58 60 63...
1,151 150 147 155 148 133...
```

Where:
- `emotion`: 0-6 (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral)
- `pixels`: Space-separated pixel values (48x48 = 2304 values)

### Step 3: Train the Model (10-30 minutes)

```bash
python model_training.py
```

This will:
- Load the dataset
- Train a CNN model
- Save `face_emotionModel.h5`

**Note**: Training time depends on your hardware:
- With GPU: 10-15 minutes
- CPU only: 30-60 minutes

### Step 4: Run the App (30 seconds)

```bash
python app.py
```

Open your browser to: `http://localhost:5000`

### Step 5: Test It!

1. Upload a facial image
2. Click "Analyze Emotion"
3. See the results!

## 📁 Project Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Flask web server |
| `model_training.py` | Trains the ML model |
| `face_emotionModel.h5` | Trained model (created after training) |
| `templates/index.html` | Web interface |
| `requirements.txt` | Python dependencies |
| `database.db` | Stores prediction history |
| `Procfile` | Render deployment config |
| `runtime.txt` | Python version for deployment |

## 🎯 What Each File Does

### `model_training.py`
- Loads emotion dataset from CSV
- Builds a CNN with 3 convolutional blocks
- Trains for up to 50 epochs (with early stopping)
- Saves the trained model

### `app.py`
- Loads the trained model
- Provides web interface
- Handles image uploads
- Makes predictions
- Stores results in database
- Provides API endpoints

### `templates/index.html`
- Modern, responsive UI
- Drag-and-drop file upload
- Real-time preview
- Animated result display
- Shows all emotion probabilities

## 🔧 Common Issues & Solutions

### Issue: "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### Issue: "CSV file not found"
Download the FER2013 dataset and place it at `data/data/emotions.csv`

### Issue: "Model file not found"
Run `python model_training.py` first to create the model.

### Issue: Training is too slow
- Use a smaller dataset for testing
- Reduce epochs in `model_training.py` (line 197: change `epochs=50` to `epochs=10`)
- Use Google Colab for free GPU access

## 📊 API Usage

### Predict Emotion (POST)
```bash
curl -X POST -F "file=@face.jpg" http://localhost:5000/predict
```

Response:
```json
{
  "success": true,
  "emotion": "Happy",
  "confidence": 95.5,
  "all_emotions": {
    "Happy": 95.5,
    "Neutral": 2.3,
    "Surprise": 1.2,
    "Sad": 0.5,
    "Angry": 0.3,
    "Fear": 0.1,
    "Disgust": 0.1
  },
  "image_url": "/static/uploads/20231102_143022_face.jpg"
}
```

### Get History (GET)
```bash
curl http://localhost:5000/history
```

### Get Statistics (GET)
```bash
curl http://localhost:5000/stats
```

### Health Check (GET)
```bash
curl http://localhost:5000/health
```

## 🎨 Customization Ideas

### Change Emotions
Edit the `EMOTIONS` list in both files:
- `model_training.py` (line 17)
- `app.py` (line 24)

### Adjust Model Architecture
In `model_training.py`, modify the `build_model()` function (line 103)

### Customize UI
Edit `templates/index.html` - change colors, layout, etc.

### Add Features
- Webcam support
- Batch processing
- Export results to CSV
- User authentication
- Emotion trends over time

## 📦 Deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

Quick deploy to Render:
1. Push to GitHub
2. Connect to Render
3. Deploy!

## 🧪 Testing

Test with sample images:
- Download test faces from [Unsplash](https://unsplash.com/s/photos/face-emotion)
- Use your own photos
- Try different emotions

## 📈 Performance Tips

### Improve Accuracy
- Use more training data
- Train for more epochs
- Add data augmentation (already included)
- Use transfer learning (VGG16, ResNet)

### Speed Up Inference
- Use TensorFlow Lite
- Quantize the model
- Use smaller image size

### Reduce File Size
- Quantize model weights
- Use model pruning
- Remove unnecessary layers

## 🎓 Learning Resources

- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Emotion Recognition Papers](https://paperswithcode.com/task/facial-expression-recognition)

## 💡 Tips

1. **Start Small**: Test with a small dataset first
2. **Monitor Training**: Watch the accuracy/loss curves
3. **Save Checkpoints**: Model saves automatically
4. **Test Locally**: Before deploying, test thoroughly
5. **Use Version Control**: Commit changes regularly

## 🆘 Need Help?

1. Check the error message carefully
2. Review the logs in terminal
3. Verify file paths are correct
4. Ensure all dependencies are installed
5. Check Python version (3.11+ recommended)

## ✅ Checklist

Before deployment:
- [ ] Dataset downloaded and placed correctly
- [ ] Model trained successfully
- [ ] App runs locally without errors
- [ ] Tested with multiple images
- [ ] All files committed to git
- [ ] README updated with your info

## 🎉 You're Ready!

Your emotion detection app is ready to use. Have fun experimenting with it!

---

**Next Steps:**
1. Train the model with your dataset
2. Test locally
3. Deploy to Render/Vercel
4. Share with friends!

