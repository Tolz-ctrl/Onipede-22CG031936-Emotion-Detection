# Deployment Guide - Emotion Detection Web App

This guide will walk you through deploying your emotion detection application to either Render or Vercel.

## Prerequisites

Before deploying, ensure you have:
- ✅ Git repository initialized and committed
- ✅ GitHub account created
- ✅ All files committed to git
- ✅ Trained model file (`face_emotionModel.h5`) - if not, see "Training the Model" section below

## Step 1: Push to GitHub

### 1.1 Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and log in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it: `emotion-detection-app` (or any name you prefer)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 1.2 Push Your Local Repository

GitHub will show you commands. Use these in your terminal:

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/emotion-detection-app.git

# Push your code
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 2: Training the Model (If Not Already Done)

**IMPORTANT**: The model file must be trained before deployment!

### Option A: Train Locally

If you have the FER2013 dataset:

```bash
# Make sure you have the dataset in data/data/emotions.csv
python model_training.py
```

This will create `face_emotionModel.h5` (approximately 10-50 MB).

### Option B: Use Pre-trained Model

If you don't have the dataset, you can:
1. Download a pre-trained emotion detection model
2. Place it in the root directory as `face_emotionModel.h5`
3. Ensure it outputs 7 emotion classes in this order: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral

After training, commit and push the model:

```bash
git add face_emotionModel.h5
git commit -m "Add trained emotion detection model"
git push
```

## Step 3: Deploy to Render (Recommended)

Render is recommended because it supports larger files and has better support for ML models.

### 3.1 Create Render Account

1. Go to [Render.com](https://render.com)
2. Sign up with your GitHub account

### 3.2 Create New Web Service

1. Click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository
4. Select the `emotion-detection-app` repository

### 3.3 Configure the Service

Fill in the following settings:

- **Name**: `emotion-detection-app` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### 3.4 Environment Variables (Optional)

You can add these if needed:
- `PYTHON_VERSION`: `3.11.6`

### 3.5 Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Once deployed, you'll get a URL like: `https://emotion-detection-app.onrender.com`

### 3.6 Save the URL

Copy the deployed URL and paste it into `link_web_app.txt`:

```bash
echo "https://emotion-detection-app.onrender.com" > link_web_app.txt
git add link_web_app.txt
git commit -m "Add deployed web app URL"
git push
```

## Step 4: Alternative - Deploy to Vercel

Vercel is faster but has file size limitations (100MB for free tier).

### 4.1 Install Vercel CLI

```bash
npm install -g vercel
```

### 4.2 Login to Vercel

```bash
vercel login
```

### 4.3 Deploy

```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- What's your project's name? `emotion-detection-app`
- In which directory is your code located? `./`

### 4.4 Production Deployment

```bash
vercel --prod
```

You'll get a URL like: `https://emotion-detection-app.vercel.app`

### 4.5 Save the URL

```bash
echo "https://emotion-detection-app.vercel.app" > link_web_app.txt
git add link_web_app.txt
git commit -m "Add deployed web app URL"
git push
```

## Step 5: Test Your Deployment

1. Open the deployed URL in your browser
2. Upload a test image with a face
3. Click "Analyze Emotion"
4. Verify the prediction works correctly

## Troubleshooting

### Issue: "Model file not found"

**Solution**: Make sure `face_emotionModel.h5` is committed and pushed to GitHub.

```bash
git add face_emotionModel.h5
git commit -m "Add model file"
git push
```

Then redeploy on Render/Vercel.

### Issue: "Application Error" or 500 Error

**Solution**: Check the logs on Render/Vercel dashboard. Common issues:
- Missing dependencies in `requirements.txt`
- Model file too large (use Render instead of Vercel)
- Python version mismatch

### Issue: Deployment takes too long

**Solution**: 
- TensorFlow is a large package (~500MB)
- First deployment can take 10-15 minutes
- Subsequent deployments are faster (cached)

### Issue: Out of memory

**Solution**: On Render, upgrade to a paid plan with more RAM. ML models need at least 512MB RAM.

## File Size Considerations

- **Render Free Tier**: Supports larger files, better for ML apps
- **Vercel Free Tier**: 100MB limit, may not work with large models

If your model is >50MB, use Render.

## Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] Can upload images
- [ ] Emotion prediction works
- [ ] Results display correctly
- [ ] URL saved in `link_web_app.txt`
- [ ] All changes committed and pushed to GitHub

## Updating Your Deployment

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push
```

- **Render**: Automatically redeploys on push
- **Vercel**: Run `vercel --prod` again

## Support

If you encounter issues:
1. Check Render/Vercel logs
2. Verify all files are committed
3. Ensure model file exists and is valid
4. Check Python version compatibility

## Next Steps

After successful deployment:
1. Share your app URL
2. Test with various facial images
3. Monitor usage in Render/Vercel dashboard
4. Consider adding more features (webcam support, batch processing, etc.)

---

**Congratulations!** Your emotion detection app is now live! 🎉

