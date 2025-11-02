# Model Training Instructions

## ⚠️ Important: Python Installation Required

Python is not currently installed on your system. You need to install it before training the model.

---

## Step 1: Install Python

### Option A: Install from Microsoft Store (Easiest)
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Get" or "Install"
4. Wait for installation to complete

### Option B: Install from Python.org
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 for Windows
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Wait for installation to complete

### Verify Installation
Open a new PowerShell window and run:
```powershell
python --version
```

You should see: `Python 3.11.x` or `Python 3.12.x`

---

## Step 2: Set Up Virtual Environment

```powershell
# Navigate to project directory
cd "C:\Users\User\Desktop\School Assignments\Onipede-22CG031936"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**Note**: If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Step 3: Install Dependencies

With the virtual environment activated:

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- TensorFlow (ML framework) - ~500MB
- Flask (web framework)
- NumPy, Pandas (data processing)
- Pillow (image processing)
- And other dependencies

**Note**: This may take 10-20 minutes depending on your internet speed.

---

## Step 4: Train the Model

### Quick Training (For Testing - 10 epochs)

Edit `model_training.py` line 197 and change:
```python
epochs=50  # Change to 10 for quick testing
```

Then run:
```powershell
python model_training.py
```

### Full Training (Recommended - 50 epochs)

Just run:
```powershell
python model_training.py
```

### What to Expect

**Training Output:**
```
🚀 Starting Emotion Detection Model Training...
TensorFlow Version: 2.15.0

📂 Loading data from directories...
Found 28709 images belonging to 7 classes.
Found 7178 images belonging to 7 classes.

🏗️  Building CNN model...
✅ Model built successfully!

📋 Model Summary:
...

🎯 Starting training...
Epoch 1/50
448/448 [==============================] - 120s 267ms/step - loss: 1.7234 - accuracy: 0.3456 - val_loss: 1.5432 - val_accuracy: 0.4123
Epoch 2/50
448/448 [==============================] - 115s 257ms/step - loss: 1.5123 - accuracy: 0.4234 - val_loss: 1.4321 - val_accuracy: 0.4567
...
```

**Training Time:**
- **With GPU**: 10-20 minutes
- **CPU only**: 30-90 minutes

**Expected Accuracy:**
- After 10 epochs: 50-60%
- After 50 epochs: 60-70%

### Monitor Progress

The training will show:
- Current epoch number
- Training loss and accuracy
- Validation loss and accuracy
- Time per epoch

### Early Stopping

The model uses early stopping, so if validation loss doesn't improve for 10 epochs, training will stop automatically.

---

## Step 5: Verify Model Creation

After training completes, check:

```powershell
dir face_emotionModel.h5
```

You should see a file sized **10-50 MB** (not 0 bytes).

---

## Step 6: Test the Model Locally

```powershell
# Make sure virtual environment is activated
python app.py
```

Open browser to: `http://localhost:5000`

Test with a facial image to verify predictions work.

---

## Step 7: Push to GitHub

### Commit the Trained Model

```powershell
git add face_emotionModel.h5
git add model_training.py
git commit -m "Add trained emotion detection model"
```

### Push to GitHub

```powershell
# Set branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note**: The first push may take a while due to the large model file (10-50 MB).

---

## Troubleshooting

### Issue: "Python not found"
**Solution**: Install Python (see Step 1) and make sure "Add to PATH" was checked.

### Issue: "Cannot activate virtual environment"
**Solution**: Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "pip install fails"
**Solution**: 
```powershell
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

### Issue: "TensorFlow installation fails"
**Solution**: Make sure you have:
- Python 3.11 or 3.12 (not 3.13)
- 64-bit Python
- At least 2GB free disk space

### Issue: "Training is very slow"
**Solutions**:
1. Reduce epochs to 10 for testing
2. Reduce batch size in `model_training.py` (line 189: change `batch_size=64` to `32`)
3. Use fewer images (create a subset of the dataset)
4. Use Google Colab for free GPU access

### Issue: "Out of memory during training"
**Solutions**:
1. Reduce batch size to 32 or 16
2. Close other applications
3. Restart computer and try again

### Issue: "Model accuracy is low (<40%)"
**Solutions**:
1. Train for more epochs
2. Check if dataset is balanced
3. Verify images are loading correctly

---

## Alternative: Use Google Colab (Free GPU)

If your computer is slow or doesn't have enough resources:

### 1. Upload to Google Colab

1. Go to https://colab.research.google.com
2. Create new notebook
3. Upload your dataset and `model_training.py`

### 2. Enable GPU

- Runtime → Change runtime type → GPU → Save

### 3. Install Dependencies

```python
!pip install tensorflow keras numpy pandas scikit-learn pillow opencv-python
```

### 4. Upload Dataset

```python
from google.colab import files
# Upload your dataset zip file
uploaded = files.upload()
```

### 5. Run Training

```python
!python model_training.py
```

### 6. Download Model

```python
from google.colab import files
files.download('face_emotionModel.h5')
```

Then copy the downloaded model to your project folder.

---

## Quick Reference Commands

```powershell
# Install Python (if not installed)
# Download from python.org or Microsoft Store

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Train model
python model_training.py

# Test application
python app.py

# Commit and push
git add face_emotionModel.h5
git commit -m "Add trained model"
git push -u origin main
```

---

## Expected Results

After successful training:

✅ `face_emotionModel.h5` file created (10-50 MB)  
✅ Validation accuracy: 60-70%  
✅ Model can predict 7 emotions  
✅ Application works locally  
✅ Ready for deployment  

---

## Next Steps After Training

1. ✅ Test locally with `python app.py`
2. ✅ Push to GitHub
3. ✅ Deploy to Render (see DEPLOYMENT_GUIDE.md)
4. ✅ Save deployed URL to `link_web_app.txt`

---

## Need Help?

- Check error messages carefully
- Verify Python version: `python --version`
- Verify packages installed: `pip list`
- Check available disk space
- Ensure internet connection for package downloads

---

**Good luck with training!** 🚀

The dataset is already in place at `data/data/archive/` with:
- 28,709 training images
- 7,178 test images
- 7 emotion classes

You're ready to train once Python is installed!

