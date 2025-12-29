"""
Modern BERT-based Emotion Detection Training Script
Uses TensorFlow 2.x, Keras, and TensorFlow Hub for mental health coaching AI
"""

import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set random seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

class EmotionConfig:
    """Configuration for emotion detection model"""
    def __init__(self):
        # Data paths
        self.data_dir = "goemotions/data"
        self.train_file = "train.tsv"
        self.dev_file = "dev.tsv"
        self.test_file = "test.tsv"
        self.emotions_file = "emotions.txt"
        
        # Model parameters
        self.bert_model_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4"
        self.bert_preprocess_url = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
        
        # Training parameters
        self.max_seq_length = 128
        self.batch_size = 32
        self.epochs = 4
        self.learning_rate = 2e-5
        self.dropout_rate = 0.1
        
        # Output
        self.output_dir = "trained_models"
        self.model_name = f"emotion_bert_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Evaluation
        self.classification_threshold = 0.3
        
    def load_emotions(self):
        """Load emotion labels from file"""
        emotions_path = os.path.join(self.data_dir, self.emotions_file)
        with open(emotions_path, 'r') as f:
            emotions = [line.strip() for line in f.readlines()]
        return emotions


class DataLoader:
    """Load and preprocess emotion detection data"""
    
    def __init__(self, config):
        self.config = config
        self.emotions = config.load_emotions()
        self.num_emotions = len(self.emotions)
        self.emotion_to_idx = {emotion: idx for idx, emotion in enumerate(self.emotions)}
        
    def load_tsv_data(self, file_path):
        """Load data from TSV file"""
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    text = parts[0]
                    # Parse emotion labels (can be comma-separated for multi-label)
                    emotion_indices = [int(x) for x in parts[1].split(',')]
                    data.append({
                        'text': text,
                        'emotions': emotion_indices
                    })
        return data
    
    def create_labels_vector(self, emotion_indices):
        """Convert emotion indices to one-hot encoded vector"""
        labels = np.zeros(self.num_emotions, dtype=np.float32)
        for idx in emotion_indices:
            if idx < self.num_emotions:
                labels[idx] = 1.0
        return labels
    
    def load_dataset(self, split='train'):
        """Load and process dataset split"""
        if split == 'train':
            file_name = self.config.train_file
        elif split == 'dev':
            file_name = self.config.dev_file
        elif split == 'test':
            file_name = self.config.test_file
        else:
            raise ValueError(f"Unknown split: {split}")
        
        file_path = os.path.join(self.config.data_dir, file_name)
        data = self.load_tsv_data(file_path)
        
        texts = [item['text'] for item in data]
        labels = np.array([self.create_labels_vector(item['emotions']) for item in data])
        
        print(f"Loaded {split} set: {len(texts)} samples")
        return texts, labels
    
    def create_tf_dataset(self, texts, labels, shuffle=True):
        """Create TensorFlow dataset"""
        dataset = tf.data.Dataset.from_tensor_slices((texts, labels))
        
        if shuffle:
            dataset = dataset.shuffle(buffer_size=10000, seed=42)
        
        dataset = dataset.batch(self.config.batch_size)
        dataset = dataset.prefetch(tf.data.AUTOTUNE)
        
        return dataset


class EmotionBERTModel:
    """BERT-based emotion detection model using TensorFlow Hub"""
    
    def __init__(self, config, num_emotions):
        self.config = config
        self.num_emotions = num_emotions
        self.model = None
        self.history = None
        
    def build_model(self):
        """Build BERT model using TensorFlow Hub"""
        # Input layer
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        
        # BERT preprocessing
        preprocessing_layer = hub.KerasLayer(
            self.config.bert_preprocess_url,
            name='preprocessing'
        )
        encoder_inputs = preprocessing_layer(text_input)
        
        # BERT encoder
        encoder = hub.KerasLayer(
            self.config.bert_model_url,
            trainable=True,
            name='BERT_encoder'
        )
        outputs = encoder(encoder_inputs)
        
        # Use pooled output (CLS token representation)
        pooled_output = outputs['pooled_output']
        
        # Classification head
        x = tf.keras.layers.Dropout(self.config.dropout_rate)(pooled_output)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dropout(self.config.dropout_rate)(x)
        output = tf.keras.layers.Dense(
            self.num_emotions,
            activation='sigmoid',  # Sigmoid for multi-label classification
            name='emotions'
        )(x)
        
        # Create model
        self.model = tf.keras.Model(inputs=text_input, outputs=output)
        
        # Compile model
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate)
        
        self.model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',  # For multi-label classification
            metrics=[
                'binary_accuracy',
                tf.keras.metrics.AUC(name='auc'),
                tf.keras.metrics.Precision(name='precision'),
                tf.keras.metrics.Recall(name='recall')
            ]
        )
        
        return self.model
    
    def get_model_summary(self):
        """Print model architecture"""
        if self.model:
            self.model.summary()
        else:
            print("Model not built yet. Call build_model() first.")
    
    def train(self, train_dataset, val_dataset, epochs=None):
        """Train the model"""
        if epochs is None:
            epochs = self.config.epochs
        
        # Create output directory
        model_dir = os.path.join(self.config.output_dir, self.config.model_name)
        os.makedirs(model_dir, exist_ok=True)
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(
                filepath=os.path.join(model_dir, 'best_model.h5'),
                monitor='val_loss',
                save_best_only=True,
                mode='min',
                verbose=1
            ),
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=2,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=1,
                min_lr=1e-7,
                verbose=1
            ),
            tf.keras.callbacks.TensorBoard(
                log_dir=os.path.join(model_dir, 'logs'),
                histogram_freq=1
            )
        ]
        
        # Train
        print(f"\n{'='*50}")
        print(f"Starting training for {epochs} epochs...")
        print(f"{'='*50}\n")
        
        self.history = self.model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history
    
    def save_model(self, path=None):
        """Save the trained model"""
        if path is None:
            path = os.path.join(self.config.output_dir, self.config.model_name, 'final_model')
        
        os.makedirs(path, exist_ok=True)
        self.model.save(path, save_format='tf')
        print(f"Model saved to: {path}")
        
    def load_model(self, path):
        """Load a trained model"""
        self.model = tf.keras.models.load_model(path)
        print(f"Model loaded from: {path}")


class ModelEvaluator:
    """Evaluate model performance"""
    
    def __init__(self, model, config, emotions):
        self.model = model
        self.config = config
        self.emotions = emotions
        
    def evaluate(self, test_dataset, test_labels):
        """Evaluate model on test set"""
        print(f"\n{'='*50}")
        print("Evaluating model on test set...")
        print(f"{'='*50}\n")
        
        # Get predictions
        predictions = self.model.predict(test_dataset)
        
        # Calculate metrics
        results = self.model.evaluate(test_dataset, verbose=1)
        
        # Print overall metrics
        print("\nOverall Metrics:")
        for name, value in zip(self.model.metrics_names, results):
            print(f"{name}: {value:.4f}")
        
        # Calculate accuracy at threshold
        pred_labels = (predictions > self.config.classification_threshold).astype(int)
        
        # Per-emotion metrics
        print("\nPer-Emotion Metrics:")
        print("-" * 70)
        
        for idx, emotion in enumerate(self.emotions):
            true_labels = test_labels[:, idx]
            pred_labels_emotion = pred_labels[:, idx]
            
            if true_labels.sum() > 0:  # Only if emotion exists in test set
                accuracy = accuracy_score(true_labels, pred_labels_emotion)
                print(f"{emotion:15s} - Accuracy: {accuracy:.4f}")
        
        return predictions, pred_labels
    
    def plot_training_history(self, history, save_path=None):
        """Plot training history"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss
        axes[0, 0].plot(history.history['loss'], label='Training Loss')
        axes[0, 0].plot(history.history['val_loss'], label='Validation Loss')
        axes[0, 0].set_title('Model Loss')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Accuracy
        axes[0, 1].plot(history.history['binary_accuracy'], label='Training Accuracy')
        axes[0, 1].plot(history.history['val_binary_accuracy'], label='Validation Accuracy')
        axes[0, 1].set_title('Model Accuracy')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Accuracy')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # AUC
        axes[1, 0].plot(history.history['auc'], label='Training AUC')
        axes[1, 0].plot(history.history['val_auc'], label='Validation AUC')
        axes[1, 0].set_title('Model AUC')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('AUC')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Precision and Recall
        axes[1, 1].plot(history.history['precision'], label='Training Precision')
        axes[1, 1].plot(history.history['val_precision'], label='Validation Precision')
        axes[1, 1].plot(history.history['recall'], label='Training Recall')
        axes[1, 1].plot(history.history['val_recall'], label='Validation Recall')
        axes[1, 1].set_title('Model Precision & Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Score')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Training plots saved to: {save_path}")
        
        plt.show()


def main():
    """Main training pipeline"""
    print("="*70)
    print("BERT-Based Emotion Detection Training for Mental Health AI")
    print("="*70)
    
    # Check GPU availability
    print(f"\nTensorFlow version: {tf.__version__}")
    print(f"GPU available: {tf.config.list_physical_devices('GPU')}")
    print(f"Number of GPUs: {len(tf.config.list_physical_devices('GPU'))}")
    
    # Initialize configuration
    config = EmotionConfig()
    
    # Load data
    print("\n" + "="*70)
    print("STEP 1: Loading and Preprocessing Data")
    print("="*70)
    
    data_loader = DataLoader(config)
    
    # Load datasets
    train_texts, train_labels = data_loader.load_dataset('train')
    val_texts, val_labels = data_loader.load_dataset('dev')
    test_texts, test_labels = data_loader.load_dataset('test')
    
    print(f"\nEmotion categories ({len(data_loader.emotions)}): {', '.join(data_loader.emotions)}")
    print(f"Training samples: {len(train_texts)}")
    print(f"Validation samples: {len(val_texts)}")
    print(f"Test samples: {len(test_texts)}")
    
    # Create TensorFlow datasets
    train_dataset = data_loader.create_tf_dataset(train_texts, train_labels, shuffle=True)
    val_dataset = data_loader.create_tf_dataset(val_texts, val_labels, shuffle=False)
    test_dataset = data_loader.create_tf_dataset(test_texts, test_labels, shuffle=False)
    
    # Build model
    print("\n" + "="*70)
    print("STEP 2: Building BERT Model")
    print("="*70)
    
    emotion_model = EmotionBERTModel(config, data_loader.num_emotions)
    model = emotion_model.build_model()
    
    print("\nModel Architecture:")
    emotion_model.get_model_summary()
    
    # Train model
    print("\n" + "="*70)
    print("STEP 3: Training Model")
    print("="*70)
    
    history = emotion_model.train(train_dataset, val_dataset)
    
    # Save model
    print("\n" + "="*70)
    print("STEP 4: Saving Model")
    print("="*70)
    
    emotion_model.save_model()
    
    # Save configuration
    model_dir = os.path.join(config.output_dir, config.model_name)
    config_path = os.path.join(model_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump({
            'emotions': data_loader.emotions,
            'num_emotions': data_loader.num_emotions,
            'max_seq_length': config.max_seq_length,
            'classification_threshold': config.classification_threshold,
            'training_date': datetime.now().isoformat()
        }, f, indent=2)
    print(f"Configuration saved to: {config_path}")
    
    # Evaluate model
    print("\n" + "="*70)
    print("STEP 5: Evaluating Model")
    print("="*70)
    
    evaluator = ModelEvaluator(model, config, data_loader.emotions)
    predictions, pred_labels = evaluator.evaluate(test_dataset, test_labels)
    
    # Plot training history
    plot_path = os.path.join(model_dir, 'training_history.png')
    evaluator.plot_training_history(history, save_path=plot_path)
    
    # Calculate overall accuracy
    overall_accuracy = accuracy_score(
        (test_labels > 0.5).astype(int).flatten(),
        pred_labels.flatten()
    )
    
    print("\n" + "="*70)
    print("TRAINING COMPLETE!")
    print("="*70)
    print(f"\nModel saved to: {model_dir}")
    print(f"Overall Test Accuracy: {overall_accuracy*100:.2f}%")
    
    if overall_accuracy >= 0.90:
        print("✓ Model achieved target accuracy of 90%+")
    else:
        print(f"✗ Model accuracy {overall_accuracy*100:.2f}% is below 90% target")
        print("  Consider: increasing epochs, adjusting learning rate, or data augmentation")
    
    return emotion_model, evaluator, overall_accuracy


if __name__ == "__main__":
    model, evaluator, accuracy = main()
