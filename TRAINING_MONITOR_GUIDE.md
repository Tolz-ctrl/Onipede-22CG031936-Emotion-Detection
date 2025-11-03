# 🎭 Training Monitor Dashboard - User Guide

## Overview

The **Training Monitor Dashboard** is an interactive web page that displays real-time progress of your emotion detection model training. It automatically updates every 30 seconds to show the latest metrics, charts, and estimates.

## How to Access

### Option 1: Direct File Access
Open the file in your browser:
```
file:///C:/Users/User/Desktop/School Assignments/Onipede-22CG031936/training_monitor.html
```

### Option 2: Double-click
Simply double-click `training_monitor.html` in your project folder.

### Option 3: Local Server (Recommended for best experience)
```bash
# Navigate to project directory
cd "C:\Users\User\Desktop\School Assignments\Onipede-22CG031936"

# Start a simple HTTP server
python -m http.server 8000

# Open in browser
http://localhost:8000/training_monitor.html
```

## Dashboard Features

### 1. **Status Badge** (Top Center)
- 🔄 **Training in Progress**: Yellow badge with pulsing animation
- ✅ **Training Completed**: Green badge when training finishes
- Shows current training state at a glance

### 2. **Current Progress Card**
- **Epoch Counter**: Shows current epoch out of total (e.g., "5 / 20")
- **Progress Bar**: Visual representation of training completion percentage
- Updates after each epoch completes

### 3. **Validation Accuracy Card**
- **Latest Validation Accuracy**: Main metric for model performance
- **Training Accuracy**: Comparison metric
- Color-coded:
  - 🟢 Green: ≥60% (Good)
  - 🟡 Orange: 40-59% (Warning)
  - 🔴 Red: <40% (Needs improvement)

### 4. **Loss Metrics Card**
- **Validation Loss**: How well model performs on unseen data
- **Training Loss**: How well model fits training data
- Lower values are better
- Ideally, both should decrease over time

### 5. **Time Estimates Card**
- **Elapsed Time**: Total time since training started
- **Estimated Remaining**: Calculated based on average epoch time
- Format: Hours, minutes, seconds (e.g., "2h 15m 30s")

### 6. **Accuracy Trends Chart**
- Line graph showing accuracy over epochs
- Blue line: Training accuracy
- Green line: Validation accuracy
- Hover over points to see exact values
- Helps identify overfitting (training >> validation)

### 7. **Loss Trends Chart**
- Line graph showing loss over epochs
- Orange line: Training loss
- Red line: Validation loss
- Both should trend downward
- Helps monitor convergence

### 8. **Model Information Panel**
- **Total Parameters**: 6,003,143 (model complexity)
- **Model Size**: 22.9 MB (file size when saved)
- **Training Samples**: 5,236 images
- **Validation Samples**: 1,311 images
- **Batch Size**: 64 images per batch
- **Image Size**: 48x48 pixels
- **Emotion Classes**: 7 emotions (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral)

### 9. **Final Results Panel** (Shown when complete)
- Displays final validation accuracy
- **Download Trained Model** button: Downloads `face_emotionModel.h5`
- **Test Model** button: Opens the main app to test predictions

## Auto-Refresh

The dashboard automatically refreshes every **30 seconds** to fetch the latest training data from `training_progress.json`. You'll see the last update time at the bottom of the page.

## Understanding the Metrics

### What is Good Performance?

| Metric | Target | Excellent | Good | Needs Work |
|--------|--------|-----------|------|------------|
| Validation Accuracy | 60-70% | >70% | 50-70% | <50% |
| Validation Loss | <1.0 | <0.5 | 0.5-1.5 | >1.5 |
| Training Time | 3-5 hours | <3 hours | 3-5 hours | >5 hours |

### Signs of Good Training

✅ **Validation accuracy increasing** over epochs  
✅ **Both losses decreasing** steadily  
✅ **Training and validation metrics close** (not overfitting)  
✅ **Learning rate adjustments** when plateau detected  

### Warning Signs

⚠️ **Validation accuracy stuck** at same value  
⚠️ **Training accuracy >> Validation accuracy** (overfitting)  
⚠️ **Losses increasing** instead of decreasing  
⚠️ **Very slow progress** (may need more epochs)  

## Training Process

### Current Configuration
- **Total Epochs**: 20 (maximum)
- **Early Stopping**: Stops if no improvement for 10 epochs
- **Learning Rate Reduction**: Reduces LR by 50% if no improvement for 5 epochs
- **Backend**: Keras 3.12.0 with JAX (Python 3.14 compatible)

### Expected Timeline
- **Epoch Duration**: ~13-15 minutes per epoch
- **Total Training Time**: 3-5 hours (may stop early)
- **Data Loading**: ~5 minutes (one-time at start)
- **Model Building**: ~1 minute (one-time at start)

## Troubleshooting

### Dashboard shows "Unable to load training data"
**Cause**: `training_progress.json` file not found or training not started  
**Solution**: 
1. Make sure training script is running
2. Check that `training_progress.json` exists in project folder
3. Refresh the page manually

### Metrics not updating
**Cause**: Training may have stopped or crashed  
**Solution**:
1. Check if Python process is still running: `Get-Process python`
2. Check terminal output for errors
3. Restart training if needed

### Charts not displaying
**Cause**: No epoch data yet (training just started)  
**Solution**: Wait for first epoch to complete (~15 minutes)

### Page shows old data
**Cause**: Browser cache  
**Solution**: Hard refresh (Ctrl + F5) or clear browser cache

## Files Involved

| File | Purpose |
|------|---------|
| `training_monitor.html` | Main dashboard web page |
| `training_progress.json` | Real-time training data (auto-updated) |
| `model_training_simple.py` | Training script with monitoring callback |
| `face_emotionModel.h5` | Trained model (created when complete) |

## Tips for Best Experience

1. **Keep the page open** during training to monitor progress
2. **Check periodically** rather than constantly (auto-refresh handles updates)
3. **Use a local server** for better file access (avoids CORS issues)
4. **Don't close the terminal** running the training script
5. **Bookmark the page** for easy access

## What to Do When Training Completes

1. ✅ **Check Final Accuracy**: Should be 60-70% or higher
2. 📥 **Download Model**: Click "Download Trained Model" button
3. 🧪 **Test Model**: Click "Test Model" to try predictions
4. 📊 **Review Charts**: Analyze training progression
5. 💾 **Commit to GitHub**: Add and push the trained model

## Next Steps After Training

```bash
# Verify model file exists and check size
dir face_emotionModel.h5

# Test the Flask application
python app.py

# Commit trained model to GitHub
git add face_emotionModel.h5 training_progress.json
git commit -m "Add trained emotion detection model with XX% validation accuracy"
git push origin main
```

## Support

If you encounter issues:
1. Check the terminal running `model_training_simple.py` for error messages
2. Verify all required packages are installed in virtual environment
3. Ensure sufficient disk space for model file (~25 MB)
4. Check that no other process is using port 5000 (for Flask app)

---

**Happy Training! 🚀**

The dashboard will automatically update as your model learns to detect emotions from facial expressions.

