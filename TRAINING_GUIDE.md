# BERT Emotion Detection Training Guide
## Mental Health Coaching AI Project

Complete step-by-step guide for training BERT-based emotion detection model using TensorFlow 2.x, Keras, and TensorFlow Hub.

---

## 📋 Project Overview

**Objective**: Train an emotion detection model to identify emotions from text communication between AI coach and clients.

**Target Accuracy**: 90%+ correct predictions

**Technologies**: 
- TensorFlow 2.x
- TensorFlow Keras
- TensorFlow Hub
- BERT (Bidirectional Encoder Representations from Transformers)

**Dataset**: GoEmotions - 58k Reddit comments with 28 emotion labels

---

## 🗂️ Files Overview

### Training Files
- `train_emotion_model.py` - Main training script
- `evaluate_model.py` - Detailed model evaluation
- `predict_emotion.py` - Inference/prediction script
- `api_server.py` - Flask API for React integration
- `requirements_tf2.txt` - Python dependencies

### Data Files (in goemotions/data/)
- `train.tsv` - Training data (43,410 samples)
- `dev.tsv` - Validation data (5,426 samples)
- `test.tsv` - Test data (5,427 samples)
- `emotions.txt` - List of 28 emotions

---

## 🚀 Step-by-Step Training Process

### Step 1: Install Dependencies

Open PowerShell terminal and run:

```powershell
# Navigate to project directory
cd "C:\Users\99TECH\Desktop\model training"

# Install required packages
pip install -r requirements_tf2.txt
```

**Note**: This may take 5-10 minutes depending on your internet speed.

### Step 2: Verify Data Files

Check that your data files exist:

```powershell
# Check data files
Get-ChildItem "goemotions\data\*.tsv"

# Should show:
# train.tsv
# dev.tsv  
# test.tsv
```

### Step 3: Train the Model

Run the training script:

```powershell
python train_emotion_model.py
```

**What happens during training:**
1. ✓ Loads and preprocesses data (train/dev/test splits)
2. ✓ Downloads BERT model from TensorFlow Hub
3. ✓ Builds emotion detection model
4. ✓ Trains for 4 epochs (adjustable)
5. ✓ Validates after each epoch
6. ✓ Saves best model based on validation loss
7. ✓ Evaluates on test set
8. ✓ Generates training plots

**Training Time**: 
- CPU: 2-3 hours
- GPU: 30-45 minutes

**Expected Output:**
```
Training samples: 43410
Validation samples: 5426
Test samples: 5427

Epoch 1/4
1357/1357 ━━━━━━━━━━━━━━━━━━━━ 789s - loss: 0.1234 - accuracy: 0.8567
...
Overall Test Accuracy: 91.23%
✓ Model achieved target accuracy of 90%+
```

### Step 4: Model Output Location

After training completes, find your model in:

```
trained_models/
└── emotion_bert_YYYYMMDD_HHMMSS/
    ├── final_model/           # Saved TensorFlow model
    ├── best_model.h5          # Best checkpoint
    ├── config.json            # Model configuration
    ├── training_history.png   # Training plots
    └── logs/                  # TensorBoard logs
```

### Step 5: Evaluate Model Performance

Run detailed evaluation:

```powershell
python evaluate_model.py "trained_models\emotion_bert_YYYYMMDD_HHMMSS\final_model" "trained_models\emotion_bert_YYYYMMDD_HHMMSS\config.json"
```

**Evaluation Output:**
- Overall accuracy, precision, recall, F1
- Per-emotion metrics
- Confusion matrices
- Distribution analysis
- Sample predictions
- Summary report

Results saved in: `evaluation_results_YYYYMMDD_HHMMSS/`

### Step 6: Test Predictions

Test the model with sample texts:

```powershell
python predict_emotion.py "trained_models\emotion_bert_YYYYMMDD_HHMMSS\final_model" "trained_models\emotion_bert_YYYYMMDD_HHMMSS\config.json"
```

**Sample Output:**
```
Text: I've been feeling really down lately
Top Emotion: sadness (confidence: 0.923)
Approach: empathetic_support
Suggested Tone: gentle and understanding
```

---

## 🔗 Integration with React Frontend

### Option 1: Flask API (Recommended)

1. **Start the API server:**

```powershell
python api_server.py "trained_models\emotion_bert_YYYYMMDD_HHMMSS\final_model" "trained_models\emotion_bert_YYYYMMDD_HHMMSS\config.json"
```

2. **API will run on:** `http://localhost:5000`

3. **Available Endpoints:**

```javascript
// POST /api/predict
fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'I am feeling happy today' })
})
.then(res => res.json())
.then(data => {
  console.log('Emotion:', data.top_emotion);
  console.log('Confidence:', data.top_confidence);
  console.log('Approach:', data.response_approach);
});

// GET /api/emotions
fetch('http://localhost:5000/api/emotions')
.then(res => res.json())
.then(data => console.log('Available emotions:', data.emotions));

// GET /api/health
fetch('http://localhost:5000/api/health')
.then(res => res.json())
.then(data => console.log('Status:', data.status));
```

### Option 2: Direct Python Integration

If your backend is Python, use directly:

```python
from predict_emotion import EmotionPredictor

# Initialize once
predictor = EmotionPredictor(
    model_path="trained_models/emotion_bert_XXXXXX/final_model",
    config_path="trained_models/emotion_bert_XXXXXX/config.json"
)

# Use for predictions
result = predictor.get_emotion_response("I'm feeling anxious")
print(result['top_emotion'])        # 'nervousness'
print(result['response_approach'])  # 'grounding_support'
```

---

## 📊 Understanding Results

### Emotion Categories (28 total)

**Positive Emotions:**
- admiration, amusement, approval, caring, desire, excitement, gratitude, joy, love, optimism, pride, relief

**Negative Emotions:**
- anger, annoyance, disappointment, disapproval, disgust, embarrassment, fear, grief, nervousness, remorse, sadness

**Ambiguous Emotions:**
- confusion, curiosity, realization, surprise

**Neutral:**
- neutral

### Response Approaches

The model provides coaching guidance for each emotion:

| Emotion | Approach | Suggested Tone |
|---------|----------|---------------|
| sadness | empathetic_support | gentle and understanding |
| anger | calm_validation | calm and validating |
| fear | reassuring_support | calm and reassuring |
| joy | positive_reinforcement | warm and encouraging |
| confusion | clarifying_support | patient and clarifying |

---

## 🎯 Achieving 90%+ Accuracy

### If accuracy is below 90%:

1. **Increase Training Epochs**
   - Edit `train_emotion_model.py`, line 34:
   ```python
   self.epochs = 6  # Change from 4 to 6
   ```

2. **Adjust Learning Rate**
   - Edit line 35:
   ```python
   self.learning_rate = 3e-5  # Try different values: 1e-5, 2e-5, 3e-5
   ```

3. **Try Different BERT Model**
   - Replace with RoBERTa (better performance):
   ```python
   self.bert_model_url = "https://tfhub.dev/tensorflow/roberta_en_uncased_L-12_H-768_A-12/2"
   ```

4. **Increase Batch Size** (if you have more RAM/GPU memory):
   ```python
   self.batch_size = 64  # Change from 32
   ```

5. **Data Augmentation**
   - Add more training data from similar sources
   - Use back-translation for augmentation

---

## 🐛 Troubleshooting

### Issue: Out of Memory Error

**Solution:**
```python
# Reduce batch size in train_emotion_model.py
self.batch_size = 16  # or even 8
```

### Issue: TensorFlow Hub Download Fails

**Solution:**
```powershell
# Set proxy if behind firewall
$env:HTTPS_PROXY = "http://your-proxy:port"
python train_emotion_model.py
```

### Issue: CUDA/GPU Not Detected

**Solution:**
```powershell
# Check GPU availability
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Install GPU version if needed
pip install tensorflow[and-cuda]
```

### Issue: Import Errors

**Solution:**
```powershell
# Reinstall dependencies
pip uninstall tensorflow tensorflow-hub tensorflow-text
pip install -r requirements_tf2.txt
```

---

## 📈 Model Optimization Tips

### 1. Monitor Training with TensorBoard

```powershell
# Start TensorBoard
tensorboard --logdir="trained_models\emotion_bert_YYYYMMDD_HHMMSS\logs"

# Open browser to: http://localhost:6006
```

### 2. Early Stopping

The model automatically stops if validation loss doesn't improve for 2 epochs.

### 3. Learning Rate Scheduling

The model reduces learning rate by 50% if validation loss plateaus.

### 4. Best Model Selection

Training saves the model with lowest validation loss (not the last epoch).

---

## 🔄 Retraining or Fine-tuning

To retrain with new data:

1. Add new data to `goemotions/data/train.tsv`
2. Run training again (will create new model directory)
3. Compare performance with previous model

To continue training existing model:

```python
# Load existing model
model = tf.keras.models.load_model("path/to/previous/model")

# Continue training
history = model.fit(train_dataset, epochs=2, ...)
```

---

## 📝 Best Practices for Production

1. **Version Control**: Keep track of model versions and training dates
2. **Monitoring**: Log predictions and confidence scores
3. **Thresholding**: Adjust classification threshold based on use case
4. **Fallback**: Have backup response for low-confidence predictions
5. **Updates**: Retrain periodically with new conversation data
6. **Privacy**: Ensure client data privacy and consent

---

## 🎓 Next Steps

1. ✅ Train model using this guide
2. ✅ Achieve 90%+ accuracy
3. ✅ Test with sample mental health conversations
4. ✅ Integrate with React frontend via API
5. ✅ Deploy API server (Flask/FastAPI)
6. ✅ Monitor real-world performance
7. ✅ Collect feedback and retrain

---

## 📞 Quick Reference Commands

```powershell
# Install dependencies
pip install -r requirements_tf2.txt

# Train model
python train_emotion_model.py

# Evaluate model
python evaluate_model.py "model_path" "config_path"

# Test predictions
python predict_emotion.py "model_path" "config_path"

# Start API server
python api_server.py "model_path" "config_path"

# View TensorBoard
tensorboard --logdir="model_path\logs"
```

---

## 📚 Additional Resources

- TensorFlow Hub BERT: https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4
- GoEmotions Paper: https://arxiv.org/abs/2005.00547
- BERT Paper: https://arxiv.org/abs/1810.04805
- TensorFlow Documentation: https://www.tensorflow.org/

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Data files present and accessible
- [ ] Model trains without errors
- [ ] Training completes (4 epochs)
- [ ] Model accuracy ≥ 90%
- [ ] Model saved successfully
- [ ] Predictions work correctly
- [ ] API server runs
- [ ] React frontend can connect
- [ ] Real-time emotion detection works

---

**Good luck with your mental health coaching AI project! 🚀🧠💚**
