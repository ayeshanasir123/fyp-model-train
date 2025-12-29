"""
Advanced Model Evaluation and Testing Script
"""

import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_recall_fscore_support,
    multilabel_confusion_matrix, hamming_loss
)
from datetime import datetime


class DetailedEvaluator:
    """Comprehensive model evaluation"""
    
    def __init__(self, model_path, config_path, data_dir="goemotions/data"):
        """Initialize evaluator"""
        # Load model and config
        print(f"Loading model from: {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.emotions = self.config['emotions']
        self.num_emotions = len(self.emotions)
        self.threshold = self.config.get('classification_threshold', 0.3)
        self.data_dir = data_dir
        
        print(f"Model loaded with {self.num_emotions} emotion categories")
    
    def load_test_data(self):
        """Load test dataset"""
        test_path = os.path.join(self.data_dir, "test.tsv")
        
        texts = []
        labels = []
        
        with open(test_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    text = parts[0]
                    emotion_indices = [int(x) for x in parts[1].split(',')]
                    
                    label_vector = np.zeros(self.num_emotions, dtype=np.float32)
                    for idx in emotion_indices:
                        if idx < self.num_emotions:
                            label_vector[idx] = 1.0
                    
                    texts.append(text)
                    labels.append(label_vector)
        
        return texts, np.array(labels)
    
    def evaluate_model(self, save_dir=None):
        """Comprehensive model evaluation"""
        
        if save_dir is None:
            save_dir = f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(save_dir, exist_ok=True)
        
        print("\n" + "="*70)
        print("Loading Test Data")
        print("="*70)
        
        texts, true_labels = self.load_test_data()
        print(f"Test samples: {len(texts)}")
        
        print("\n" + "="*70)
        print("Making Predictions")
        print("="*70)
        
        predictions = self.model.predict(texts, batch_size=32, verbose=1)
        pred_labels = (predictions > self.threshold).astype(int)
        
        # Overall metrics
        print("\n" + "="*70)
        print("Overall Metrics")
        print("="*70)
        
        overall_accuracy = accuracy_score(true_labels.flatten(), pred_labels.flatten())
        hamming = hamming_loss(true_labels, pred_labels)
        
        print(f"Overall Accuracy: {overall_accuracy*100:.2f}%")
        print(f"Hamming Loss: {hamming:.4f}")
        
        # Per-emotion metrics
        print("\n" + "="*70)
        print("Per-Emotion Metrics")
        print("="*70)
        
        emotion_metrics = []
        
        for idx, emotion in enumerate(self.emotions):
            true_emotion = true_labels[:, idx]
            pred_emotion = pred_labels[:, idx]
            
            if true_emotion.sum() > 0:
                precision, recall, f1, support = precision_recall_fscore_support(
                    true_emotion, pred_emotion, average='binary', zero_division=0
                )
                accuracy = accuracy_score(true_emotion, pred_emotion)
                
                emotion_metrics.append({
                    'emotion': emotion,
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1,
                    'support': int(support)
                })
                
                print(f"{emotion:15s} - Acc: {accuracy:.3f} | Prec: {precision:.3f} | "
                      f"Rec: {recall:.3f} | F1: {f1:.3f} | Support: {int(true_emotion.sum())}")
        
        # Save detailed metrics
        metrics_df = pd.DataFrame(emotion_metrics)
        metrics_path = os.path.join(save_dir, 'emotion_metrics.csv')
        metrics_df.to_csv(metrics_path, index=False)
        print(f"\nDetailed metrics saved to: {metrics_path}")
        
        # Plot metrics
        self.plot_emotion_metrics(metrics_df, save_dir)
        
        # Confusion matrices for top emotions
        self.plot_confusion_matrices(true_labels, pred_labels, save_dir)
        
        # Distribution analysis
        self.plot_distribution_analysis(true_labels, predictions, save_dir)
        
        # Sample predictions
        self.save_sample_predictions(texts, true_labels, predictions, save_dir, n_samples=50)
        
        # Summary report
        self.generate_summary_report(overall_accuracy, hamming, emotion_metrics, save_dir)
        
        print("\n" + "="*70)
        print("Evaluation Complete!")
        print("="*70)
        print(f"Results saved to: {save_dir}")
        
        return {
            'overall_accuracy': overall_accuracy,
            'hamming_loss': hamming,
            'emotion_metrics': emotion_metrics,
            'save_dir': save_dir
        }
    
    def plot_emotion_metrics(self, metrics_df, save_dir):
        """Plot per-emotion metrics"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Sort by F1 score
        metrics_sorted = metrics_df.sort_values('f1_score', ascending=True)
        
        # Accuracy
        axes[0, 0].barh(metrics_sorted['emotion'], metrics_sorted['accuracy'])
        axes[0, 0].set_xlabel('Accuracy')
        axes[0, 0].set_title('Accuracy per Emotion')
        axes[0, 0].grid(axis='x', alpha=0.3)
        
        # Precision
        axes[0, 1].barh(metrics_sorted['emotion'], metrics_sorted['precision'])
        axes[0, 1].set_xlabel('Precision')
        axes[0, 1].set_title('Precision per Emotion')
        axes[0, 1].grid(axis='x', alpha=0.3)
        
        # Recall
        axes[1, 0].barh(metrics_sorted['emotion'], metrics_sorted['recall'])
        axes[1, 0].set_xlabel('Recall')
        axes[1, 0].set_title('Recall per Emotion')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # F1 Score
        axes[1, 1].barh(metrics_sorted['emotion'], metrics_sorted['f1_score'])
        axes[1, 1].set_xlabel('F1 Score')
        axes[1, 1].set_title('F1 Score per Emotion')
        axes[1, 1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        save_path = os.path.join(save_dir, 'emotion_metrics.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Metrics plot saved to: {save_path}")
        plt.close()
    
    def plot_confusion_matrices(self, true_labels, pred_labels, save_dir, top_n=6):
        """Plot confusion matrices for top emotions"""
        # Get emotions with most samples
        emotion_counts = true_labels.sum(axis=0)
        top_indices = np.argsort(emotion_counts)[-top_n:][::-1]
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, idx in enumerate(top_indices):
            cm = confusion_matrix(true_labels[:, idx], pred_labels[:, idx])
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i],
                       xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'])
            axes[i].set_title(f'{self.emotions[idx]}\n(Support: {int(emotion_counts[idx])})')
            axes[i].set_ylabel('True Label')
            axes[i].set_xlabel('Predicted Label')
        
        plt.tight_layout()
        save_path = os.path.join(save_dir, 'confusion_matrices.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Confusion matrices saved to: {save_path}")
        plt.close()
    
    def plot_distribution_analysis(self, true_labels, predictions, save_dir):
        """Analyze prediction distributions"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Prediction confidence distribution
        axes[0, 0].hist(predictions.flatten(), bins=50, edgecolor='black', alpha=0.7)
        axes[0, 0].axvline(self.threshold, color='red', linestyle='--', label=f'Threshold: {self.threshold}')
        axes[0, 0].set_xlabel('Prediction Confidence')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Distribution of Prediction Confidences')
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # Number of emotions per sample (true)
        true_counts = true_labels.sum(axis=1)
        axes[0, 1].hist(true_counts, bins=range(int(true_counts.max())+2), 
                       edgecolor='black', alpha=0.7, color='green')
        axes[0, 1].set_xlabel('Number of Emotions')
        axes[0, 1].set_ylabel('Number of Samples')
        axes[0, 1].set_title('True Emotion Distribution per Sample')
        axes[0, 1].grid(alpha=0.3)
        
        # Number of emotions per sample (predicted)
        pred_labels = (predictions > self.threshold).astype(int)
        pred_counts = pred_labels.sum(axis=1)
        axes[1, 0].hist(pred_counts, bins=range(int(pred_counts.max())+2), 
                       edgecolor='black', alpha=0.7, color='orange')
        axes[1, 0].set_xlabel('Number of Emotions')
        axes[1, 0].set_ylabel('Number of Samples')
        axes[1, 0].set_title('Predicted Emotion Distribution per Sample')
        axes[1, 0].grid(alpha=0.3)
        
        # Emotion frequency comparison
        true_freq = true_labels.sum(axis=0)
        pred_freq = pred_labels.sum(axis=0)
        
        x = np.arange(len(self.emotions))
        width = 0.35
        
        axes[1, 1].bar(x - width/2, true_freq, width, label='True', alpha=0.7)
        axes[1, 1].bar(x + width/2, pred_freq, width, label='Predicted', alpha=0.7)
        axes[1, 1].set_xlabel('Emotion')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Emotion Frequency: True vs Predicted')
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(self.emotions, rotation=90)
        axes[1, 1].legend()
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        save_path = os.path.join(save_dir, 'distribution_analysis.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Distribution analysis saved to: {save_path}")
        plt.close()
    
    def save_sample_predictions(self, texts, true_labels, predictions, save_dir, n_samples=50):
        """Save sample predictions for manual inspection"""
        samples = []
        
        indices = np.random.choice(len(texts), min(n_samples, len(texts)), replace=False)
        
        for idx in indices:
            text = texts[idx]
            true_emotions = [self.emotions[i] for i in range(self.num_emotions) if true_labels[idx, i] == 1]
            
            pred_probs = predictions[idx]
            top_pred_indices = np.argsort(pred_probs)[-3:][::-1]
            predicted_emotions = [
                f"{self.emotions[i]} ({pred_probs[i]:.3f})" 
                for i in top_pred_indices
            ]
            
            samples.append({
                'text': text,
                'true_emotions': ', '.join(true_emotions),
                'predicted_emotions': ', '.join(predicted_emotions)
            })
        
        samples_df = pd.DataFrame(samples)
        save_path = os.path.join(save_dir, 'sample_predictions.csv')
        samples_df.to_csv(save_path, index=False)
        print(f"Sample predictions saved to: {save_path}")
    
    def generate_summary_report(self, overall_accuracy, hamming_loss, emotion_metrics, save_dir):
        """Generate text summary report"""
        report_path = os.path.join(save_dir, 'evaluation_summary.txt')
        
        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("EMOTION DETECTION MODEL - EVALUATION REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Number of Emotions: {self.num_emotions}\n")
            f.write(f"Classification Threshold: {self.threshold}\n\n")
            
            f.write("="*70 + "\n")
            f.write("OVERALL PERFORMANCE\n")
            f.write("="*70 + "\n")
            f.write(f"Overall Accuracy: {overall_accuracy*100:.2f}%\n")
            f.write(f"Hamming Loss: {hamming_loss:.4f}\n\n")
            
            if overall_accuracy >= 0.90:
                f.write("✓ MODEL ACHIEVED TARGET ACCURACY OF 90%+\n\n")
            else:
                f.write(f"✗ Model accuracy ({overall_accuracy*100:.2f}%) is below 90% target\n")
                f.write("  Recommendations:\n")
                f.write("  - Increase training epochs\n")
                f.write("  - Adjust learning rate\n")
                f.write("  - Try data augmentation\n")
                f.write("  - Consider using RoBERTa instead of BERT\n\n")
            
            f.write("="*70 + "\n")
            f.write("TOP PERFORMING EMOTIONS\n")
            f.write("="*70 + "\n")
            
            sorted_metrics = sorted(emotion_metrics, key=lambda x: x['f1_score'], reverse=True)
            for metric in sorted_metrics[:10]:
                f.write(f"{metric['emotion']:15s} - F1: {metric['f1_score']:.3f} | "
                       f"Acc: {metric['accuracy']:.3f}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("RECOMMENDATIONS FOR DEPLOYMENT\n")
            f.write("="*70 + "\n")
            f.write("1. Model is ready for integration with React frontend\n")
            f.write("2. Use api_server.py to create REST API endpoint\n")
            f.write("3. Monitor predictions for emotions with lower F1 scores\n")
            f.write("4. Consider retraining with more data for underperforming emotions\n")
            f.write("5. Implement confidence thresholding in production\n")
        
        print(f"Summary report saved to: {report_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python evaluate_model.py <model_path> <config_path>")
        print("\nExample:")
        print("python evaluate_model.py trained_models/emotion_bert_20231229_120000/final_model trained_models/emotion_bert_20231229_120000/config.json")
        sys.exit(1)
    
    model_path = sys.argv[1]
    config_path = sys.argv[2]
    
    evaluator = DetailedEvaluator(model_path, config_path)
    results = evaluator.evaluate_model()
    
    print(f"\n{'='*70}")
    print(f"Overall Accuracy: {results['overall_accuracy']*100:.2f}%")
    print(f"{'='*70}\n")
