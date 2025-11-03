# model_training_simple.py
"""
Simplified Emotion Detection Model Training Script for Keras 3
Trains a CNN model to classify facial expressions into 7 emotion categories
"""

print("Script started!", flush=True)

# Set Keras backend to JAX (compatible with Python 3.14)
import os
print("Imported os", flush=True)
os.environ['KERAS_BACKEND'] = 'jax'
print("Set backend to JAX", flush=True)

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.utils import to_categorical
from PIL import Image
import glob
import json
import time
from datetime import datetime

print("🚀 Starting Emotion Detection Model Training...", flush=True)
print(f"Keras Version: {keras.__version__}", flush=True)
print(f"Backend: {keras.backend.backend()}", flush=True)

# Configuration
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
IMG_SIZE = 48
BATCH_SIZE = 64
EPOCHS = 20

class TrainingMonitorCallback(keras.callbacks.Callback):
    """Custom callback to save training progress to JSON file for web monitoring"""

    def __init__(self, filepath='training_progress.json'):
        super().__init__()
        self.filepath = filepath
        self.start_time = None

    def on_train_begin(self, logs=None):
        """Initialize progress file at training start"""
        self.start_time = time.time()
        progress = {
            'status': 'training',
            'start_time': datetime.now().isoformat(),
            'total_epochs': EPOCHS,
            'current_epoch': 0,
            'epochs_completed': 0,
            'history': {
                'epoch': [],
                'accuracy': [],
                'loss': [],
                'val_accuracy': [],
                'val_loss': [],
                'learning_rate': []
            },
            'model_info': {
                'total_params': 6003143,
                'trainable_params': 5999815,
                'model_size_mb': 22.9,
                'train_samples': 5236,
                'val_samples': 1311,
                'batch_size': BATCH_SIZE,
                'img_size': IMG_SIZE,
                'num_classes': 7,
                'emotions': EMOTIONS
            },
            'estimated_time_remaining': None,
            'elapsed_time': 0
        }
        self._save_progress(progress)

    def on_epoch_begin(self, epoch, logs=None):
        """Update current epoch at epoch start"""
        progress = self._load_progress()
        progress['current_epoch'] = epoch + 1
        progress['status'] = 'training'
        self._save_progress(progress)

    def on_epoch_end(self, epoch, logs=None):
        """Save metrics after each epoch"""
        progress = self._load_progress()

        # Update history
        progress['history']['epoch'].append(epoch + 1)
        progress['history']['accuracy'].append(float(logs.get('accuracy', 0)))
        progress['history']['loss'].append(float(logs.get('loss', 0)))
        progress['history']['val_accuracy'].append(float(logs.get('val_accuracy', 0)))
        progress['history']['val_loss'].append(float(logs.get('val_loss', 0)))
        progress['history']['learning_rate'].append(float(logs.get('learning_rate', 0.001)))

        # Update progress
        progress['epochs_completed'] = epoch + 1
        progress['current_epoch'] = epoch + 1

        # Calculate time estimates
        elapsed = time.time() - self.start_time
        progress['elapsed_time'] = int(elapsed)

        if epoch > 0:
            avg_time_per_epoch = elapsed / (epoch + 1)
            remaining_epochs = EPOCHS - (epoch + 1)
            progress['estimated_time_remaining'] = int(avg_time_per_epoch * remaining_epochs)

        # Latest metrics
        progress['latest_metrics'] = {
            'epoch': epoch + 1,
            'accuracy': float(logs.get('accuracy', 0)),
            'loss': float(logs.get('loss', 0)),
            'val_accuracy': float(logs.get('val_accuracy', 0)),
            'val_loss': float(logs.get('val_loss', 0))
        }

        self._save_progress(progress)

    def on_train_end(self, logs=None):
        """Mark training as complete"""
        progress = self._load_progress()
        progress['status'] = 'completed'
        progress['end_time'] = datetime.now().isoformat()
        progress['total_training_time'] = int(time.time() - self.start_time)
        self._save_progress(progress)

    def _load_progress(self):
        """Load progress from JSON file"""
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_progress(self, progress):
        """Save progress to JSON file"""
        with open(self.filepath, 'w') as f:
            json.dump(progress, f, indent=2)

def load_images_from_directory(directory):
    """Load images from directory structure manually"""
    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    X = []
    y = []

    for emotion_idx, emotion in enumerate(emotions):
        emotion_dir = os.path.join(directory, emotion)
        if not os.path.exists(emotion_dir):
            print(f"⚠️  Warning: {emotion_dir} not found", flush=True)
            continue

        image_files = glob.glob(os.path.join(emotion_dir, '*.jpg')) + \
                     glob.glob(os.path.join(emotion_dir, '*.png')) + \
                     glob.glob(os.path.join(emotion_dir, '*.jpeg'))

        print(f"Loading {len(image_files)} images from {emotion}...", flush=True)

        for idx, img_path in enumerate(image_files):
            try:
                # Load and preprocess image
                img = Image.open(img_path).convert('L')  # Convert to grayscale
                img = img.resize((IMG_SIZE, IMG_SIZE))
                img_array = np.array(img, dtype='float32') / 255.0  # Normalize
                img_array = img_array.reshape(IMG_SIZE, IMG_SIZE, 1)

                X.append(img_array)
                y.append(emotion_idx)

                # Progress indicator
                if (idx + 1) % 100 == 0:
                    print(f"  Loaded {idx + 1}/{len(image_files)} images", flush=True)
            except Exception as e:
                print(f"Error loading {img_path}: {e}", flush=True)
                continue

    print(f"Converting to numpy arrays...", flush=True)
    X = np.array(X)
    y = to_categorical(y, num_classes=7)

    return X, y

def load_data():
    """Load data from directory structure"""
    print("\n" + "="*70)
    print("LOADING DATA")
    print("="*70)

    train_dir = 'data/data/subset/train'
    val_dir = 'data/data/subset/test'

    print(f"Train directory: {train_dir}")
    print(f"Val directory: {val_dir}")
    print()

    # Load training data
    print("Loading training images...")
    X_train, y_train = load_images_from_directory(train_dir)
    print(f"✅ Loaded {len(X_train)} training images")

    # Load validation data
    print("Loading validation images...")
    X_val, y_val = load_images_from_directory(val_dir)
    print(f"✅ Loaded {len(X_val)} validation images")

    print(f"📊 Image shape: {X_train[0].shape}")
    print(f"📊 Number of classes: 7")
    print(f"📊 Classes: {EMOTIONS}")

    return X_train, y_train, X_val, y_val

def build_model():
    """Build CNN model for emotion detection"""
    print("\n" + "="*70)
    print("BUILDING MODEL")
    print("="*70)

    model = Sequential([
        # First Convolutional Block
        Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),

        # Second Convolutional Block
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),

        # Third Convolutional Block
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(256, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),

        # Fully Connected Layers
        Flatten(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(7, activation='softmax')  # 7 emotion classes
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("✅ Model built successfully!")
    print(f"\n📋 Model Summary:")
    model.summary()

    return model

def train_model():
    """Main training function"""
    # Load data
    X_train, y_train, X_val, y_val = load_data()

    # Build model
    model = build_model()

    # Callbacks
    monitor_callback = TrainingMonitorCallback('training_progress.json')

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )

    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )

    # Train model
    print("\n" + "="*70)
    print("TRAINING MODEL")
    print("="*70)
    print(f"Epochs: {EPOCHS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Early stopping patience: 10")
    print(f"Learning rate reduction patience: 5")
    print()

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        callbacks=[monitor_callback, early_stopping, reduce_lr],
        verbose=1
    )

    # Save model
    print("\n" + "="*70)
    print("SAVING MODEL")
    print("="*70)

    model.save('face_emotionModel.h5')
    print("✅ Model saved as face_emotionModel.h5")

    # Print final metrics
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)

    final_loss, final_acc = model.evaluate(X_val, y_val, verbose=0)

    print(f"📊 Final Validation Accuracy: {final_acc*100:.2f}%")
    print(f"📊 Final Validation Loss: {final_loss:.4f}")

    return model, history

if __name__ == "__main__":
    try:
        model, history = train_model()
        print("\n🎉 Training completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()

