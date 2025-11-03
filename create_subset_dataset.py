"""
Create a smaller subset of the emotion dataset for faster training.
This script copies a specified number of images from each emotion class.
"""

import os
import shutil
import random
from pathlib import Path

# Configuration
TRAIN_IMAGES_PER_CLASS = 800  # Number of training images per emotion class
TEST_IMAGES_PER_CLASS = 200   # Number of test images per emotion class

SOURCE_TRAIN_DIR = "data/data/archive/train"
SOURCE_TEST_DIR = "data/data/archive/test"

DEST_TRAIN_DIR = "data/data/subset/train"
DEST_TEST_DIR = "data/data/subset/test"

EMOTION_CLASSES = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

def create_subset(source_dir, dest_dir, images_per_class, dataset_type="train"):
    """
    Create a subset of the dataset by copying random images from each class.
    
    Args:
        source_dir: Source directory containing emotion class folders
        dest_dir: Destination directory for the subset
        images_per_class: Number of images to copy per class
        dataset_type: "train" or "test" for logging purposes
    """
    print(f"\n📂 Creating {dataset_type} subset...")
    print(f"   Source: {source_dir}")
    print(f"   Destination: {dest_dir}")
    print(f"   Images per class: {images_per_class}\n")
    
    total_copied = 0
    
    for emotion in EMOTION_CLASSES:
        source_emotion_dir = os.path.join(source_dir, emotion)
        dest_emotion_dir = os.path.join(dest_dir, emotion)
        
        # Create destination directory
        os.makedirs(dest_emotion_dir, exist_ok=True)
        
        # Get all image files from source
        image_files = [f for f in os.listdir(source_emotion_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Determine how many images to copy
        available_images = len(image_files)
        num_to_copy = min(images_per_class, available_images)
        
        # Randomly select images
        selected_images = random.sample(image_files, num_to_copy)
        
        # Copy selected images
        for img_file in selected_images:
            source_path = os.path.join(source_emotion_dir, img_file)
            dest_path = os.path.join(dest_emotion_dir, img_file)
            shutil.copy2(source_path, dest_path)
        
        total_copied += num_to_copy
        
        print(f"   ✓ {emotion:8s}: Copied {num_to_copy:4d} / {available_images:4d} images")
    
    print(f"\n   Total {dataset_type} images copied: {total_copied}")
    return total_copied

def main():
    """Main function to create dataset subset."""
    print("=" * 70)
    print("Creating Smaller Dataset Subset for Faster Training")
    print("=" * 70)
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create train subset
    train_total = create_subset(
        SOURCE_TRAIN_DIR, 
        DEST_TRAIN_DIR, 
        TRAIN_IMAGES_PER_CLASS,
        "train"
    )
    
    # Create test subset
    test_total = create_subset(
        SOURCE_TEST_DIR, 
        DEST_TEST_DIR, 
        TEST_IMAGES_PER_CLASS,
        "test"
    )
    
    print("\n" + "=" * 70)
    print("✅ Subset Creation Complete!")
    print("=" * 70)
    print(f"\nDataset Summary:")
    print(f"  Training images:   {train_total:5d} ({TRAIN_IMAGES_PER_CLASS} per class × 7 classes)")
    print(f"  Test images:       {test_total:5d} ({TEST_IMAGES_PER_CLASS} per class × 7 classes)")
    print(f"  Total images:      {train_total + test_total:5d}")
    print(f"\nNew dataset location:")
    print(f"  Train: {DEST_TRAIN_DIR}")
    print(f"  Test:  {DEST_TEST_DIR}")
    print(f"\nTo use this subset, update model_training.py:")
    print(f"  Change train_dir to: '{DEST_TRAIN_DIR}'")
    print(f"  Change val_dir to:   '{DEST_TEST_DIR}'")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()

