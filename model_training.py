# model_training.py
"""
Emotion Detection Model Training Script
Trains a CNN model to classify facial expressions into 7 emotion categories
"""

# Set Keras backend to JAX (compatible with Python 3.14)
import os
os.environ['KERAS_BACKEND'] = 'jax'

import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.utils import to_categorical, image_dataset_from_directory
from sklearn.model_selection import train_test_split
from PIL import Image

print("🚀 Starting Emotion Detection Model Training...")
print(f"Keras Version: {keras.__version__}")
print(f"Backend: {keras.backend.backend()}")

# Emotion labels
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
IMG_SIZE = 48

def load_data_from_csv(csv_path='data/data/emotions.csv'):
    """Load and preprocess data from CSV file"""
    print(f"\n📂 Loading data from {csv_path}...")

    if not os.path.exists(csv_path):
        print(f"❌ Error: CSV file not found at {csv_path}")
        print("Please ensure the emotions.csv file is in the data/data/ folder")
        return None, None, None, None

    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} samples")

    # Extract pixels and labels
    pixels = df['pixels'].tolist()
    emotions = df['emotion'].values

    # Convert pixel strings to numpy arrays
    X = []
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.array(face).reshape(IMG_SIZE, IMG_SIZE, 1)
        X.append(face)

    X = np.array(X, dtype='float32')
    X = X / 255.0  # Normalize to [0, 1]

    # Convert labels to categorical
    y = to_categorical(emotions, num_classes=7)

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=emotions
    )

    print(f"📊 Training samples: {len(X_train)}")
    print(f"📊 Validation samples: {len(X_val)}")

    return X_train, X_val, y_train, y_val

def load_data_from_directory(train_dir='data/data/subset/train', val_dir='data/data/subset/test'):
    """Load data from directory structure using Keras 3 API"""
    print(f"\n📂 Loading data from directories...")
    print(f"   Train: {train_dir}")
    print(f"   Val: {val_dir}")

    # Load training data
    train_data = image_dataset_from_directory(
        train_dir,
        labels='inferred',
        label_mode='categorical',
        color_mode='grayscale',
        batch_size=64,
        image_size=(IMG_SIZE, IMG_SIZE),
        shuffle=True,
        seed=42
    )

    # Load validation data
    val_data = image_dataset_from_directory(
        val_dir,
        labels='inferred',
        label_mode='categorical',
        color_mode='grayscale',
        batch_size=64,
        image_size=(IMG_SIZE, IMG_SIZE),
        shuffle=False,
        seed=42
    )

    # Normalize pixel values to [0, 1]
    normalization_layer = keras.layers.Rescaling(1./255)
    train_data = train_data.map(lambda x, y: (normalization_layer(x), y))
    val_data = val_data.map(lambda x, y: (normalization_layer(x), y))

    print(f"✅ Training data loaded successfully")
    print(f"✅ Validation data loaded successfully")
    print(f"📊 Classes: {train_data.class_names}")

    return train_data, val_data

def build_model():
    """Build improved CNN model for emotion detection"""
    print("\n🏗️  Building CNN model...")

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
    # Try loading from CSV first
    X_train, X_val, y_train, y_val = load_data_from_csv()

    if X_train is None:
        print("\n⚠️  CSV loading failed. Trying directory structure...")
        # Fallback to directory loading
        train_data, val_data = load_data_from_directory()
        use_csv = False
    else:
        use_csv = True
        # Create data augmentation for CSV data
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest'
        )

    # Build model
    model = build_model()

    # Callbacks
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

    print("\n🎯 Starting training...")

    # Train model
    if use_csv:
        history = model.fit(
            datagen.flow(X_train, y_train, batch_size=64),
            validation_data=(X_val, y_val),
            epochs=20,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
    else:
        history = model.fit(
            train_data,
            validation_data=val_data,
            epochs=20,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )

    # Save model
    model.save('face_emotionModel.h5')
    print("\n✅ Model trained and saved as face_emotionModel.h5")

    # Print final metrics
    if use_csv:
        final_loss, final_acc = model.evaluate(X_val, y_val, verbose=0)
    else:
        final_loss, final_acc = model.evaluate(val_data, verbose=0)

    print(f"\n📊 Final Validation Accuracy: {final_acc*100:.2f}%")
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
