# BERT Emotion Detection for Mental Health Coaching AI

🧠 **AI Cognitive System for Mental Health Coaches**

This project trains a BERT-based deep learning model to detect emotions from text conversations between AI coaches and clients, enabling empathetic and context-aware responses.

---

## 🎯 Project Goals

- **Accuracy Target**: 90%+ emotion detection accuracy
- **Real-time**: Fast inference for live chat applications
- **Multi-label**: Detect multiple emotions simultaneously
- **Integration**: Easy integration with React frontend and Python backend

---

## 📊 Dataset

**GoEmotions Dataset**
- 58,009 Reddit comments
- 28 emotion categories + neutral
- Pre-split into train/dev/test sets
- High-quality human annotations

**Emotion Categories:**
- Positive: joy, gratitude, love, admiration, excitement, optimism, etc.
- Negative: sadness, anger, fear, disappointment, grief, etc.
- Ambiguous: confusion, surprise, curiosity, realization, etc.

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```powershell
# Run the quick start script
.\quick_start.ps1
```

This will:
1. Check Python installation
2. Verify data files
3. Install dependencies
4. Start training

### Option 2: Manual Setup

```powershell
# 1. Install dependencies
pip install -r requirements_tf2.txt

# 2. Train the model
python train_emotion_model.py

# 3. Evaluate the model
python evaluate_model.py "trained_models\emotion_bert_XXXXXX\final_model" "trained_models\emotion_bert_XXXXXX\config.json"

# 4. Start API server
python api_server.py "trained_models\emotion_bert_XXXXXX\final_model" "trained_models\emotion_bert_XXXXXX\config.json"
```

---

## 📁 Project Structure

```
model training/
│
├── train_emotion_model.py          # Main training script
├── predict_emotion.py               # Inference script
├── evaluate_model.py                # Detailed evaluation
├── api_server.py                    # Flask API for React
├── requirements_tf2.txt             # Python dependencies
├── quick_start.ps1                  # Automated setup script
├── react_integration_example.jsx    # React integration code
├── TRAINING_GUIDE.md                # Detailed guide
├── README.md                        # This file
│
├── goemotions/                      # Original dataset code
│   ├── data/
│   │   ├── train.tsv               # Training data (43,410 samples)
│   │   ├── dev.tsv                 # Validation data (5,426 samples)
│   │   ├── test.tsv                # Test data (5,427 samples)
│   │   └── emotions.txt            # List of 28 emotions
│   └── ...
│
└── trained_models/                  # Saved models (created after training)
    └── emotion_bert_YYYYMMDD_HHMMSS/
        ├── final_model/             # TensorFlow SavedModel
        ├── config.json              # Model configuration
        ├── best_model.h5            # Best checkpoint
        └── training_history.png     # Training plots
```

---

## 🛠️ Technology Stack

### Machine Learning
- **TensorFlow 2.15** - Deep learning framework
- **TensorFlow Hub** - Pre-trained BERT model
- **TensorFlow Text** - Text preprocessing
- **BERT** - Transformer-based language model

### Data Processing
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation
- **scikit-learn** - Metrics and evaluation

### Visualization
- **Matplotlib** - Plotting
- **Seaborn** - Statistical visualization

### API
- **Flask** - REST API framework
- **Flask-CORS** - Cross-origin support

---

## 📖 Detailed Documentation

See **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)** for:
- Step-by-step training instructions
- Troubleshooting guide
- Performance optimization tips
- React integration details
- API documentation

---

## 🔌 API Integration

### Start the API Server

```powershell
python api_server.py "trained_models\emotion_bert_XXXXXX\final_model" "trained_models\emotion_bert_XXXXXX\config.json"
```

Server runs on: `http://localhost:5000`

### API Endpoints

**Predict Emotion**
```bash
POST /api/predict
Content-Type: application/json

{
  "text": "I'm feeling really anxious about my exam tomorrow"
}

Response:
{
  "text": "I'm feeling really anxious about my exam tomorrow",
  "top_emotion": "nervousness",
  "top_confidence": 0.89,
  "response_approach": "grounding_support",
  "suggested_tone": "calm and grounding",
  "coaching_suggestion": "Offer grounding techniques, validate concerns",
  "detected_emotions": [
    {"emotion": "nervousness", "confidence": 0.89},
    {"emotion": "fear", "confidence": 0.72}
  ]
}
```

**Get Available Emotions**
```bash
GET /api/emotions

Response:
{
  "emotions": ["admiration", "amusement", "anger", ...],
  "count": 28
}
```

**Health Check**
```bash
GET /api/health

Response:
{
  "status": "healthy",
  "model_loaded": true,
  "tensorflow_version": "2.15.0"
}
```

---

## 💻 React Integration

See **[react_integration_example.jsx](react_integration_example.jsx)** for complete React examples.

### Quick Example

```javascript
import { useEmotionDetection } from './react_integration_example';

function ChatComponent() {
  const { detectEmotion, loading } = useEmotionDetection();
  
  const handleMessage = async (text) => {
    const emotion = await detectEmotion(text);
    console.log('Detected:', emotion.top_emotion);
    // Adjust AI response based on emotion
  };
  
  return (
    // Your chat UI
  );
}
```

---

## 📈 Model Performance

### Expected Results

After training for 4 epochs:
- **Overall Accuracy**: 90-93%
- **Training Time**: 30-180 minutes (depending on hardware)
- **Inference Speed**: ~100-200ms per prediction

### Performance by Emotion Type

| Emotion Category | Typical F1 Score |
|-----------------|------------------|
| Joy, Gratitude  | 0.85 - 0.95     |
| Sadness, Anger  | 0.80 - 0.90     |
| Fear, Anxiety   | 0.75 - 0.85     |
| Neutral         | 0.90 - 0.95     |

---

## 🔧 Configuration

### Model Parameters (in `train_emotion_model.py`)

```python
class EmotionConfig:
    # Training
    batch_size = 32              # Increase for more RAM/GPU
    epochs = 4                   # Increase for better accuracy
    learning_rate = 2e-5         # Adjust if needed
    max_seq_length = 128         # Maximum text length
    
    # Classification
    classification_threshold = 0.3  # Confidence threshold
    dropout_rate = 0.1           # Regularization
```

---

## 🎓 Training Tips

### For Better Accuracy

1. **Increase Epochs**: Try 6-8 epochs
2. **Adjust Learning Rate**: Try 1e-5 or 3e-5
3. **Use RoBERTa**: Replace BERT with RoBERTa model
4. **Data Augmentation**: Add more training samples
5. **Fine-tune Threshold**: Adjust classification threshold

### For Faster Training

1. **Reduce Batch Size**: Lower to 16 or 8
2. **Use GPU**: Enable CUDA acceleration
3. **Reduce Max Length**: Lower max_seq_length to 64
4. **Early Stopping**: Already enabled by default

---

## 🐛 Troubleshooting

### Common Issues

**Out of Memory**
```python
# Reduce batch size
self.batch_size = 16  # or 8
```

**Model Not Downloading**
```powershell
# Check internet connection
# Try using different network
```

**Low Accuracy**
```python
# Increase training epochs
self.epochs = 6

# Adjust learning rate
self.learning_rate = 3e-5
```

**API Connection Error**
```javascript
// Check if API server is running
// Verify CORS is enabled
// Check API_BASE_URL
```

See **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)** for more troubleshooting help.

---

## 📊 Evaluation Metrics

The model provides comprehensive metrics:

- **Accuracy**: Overall correct predictions
- **Precision**: Positive prediction accuracy
- **Recall**: Coverage of actual positives
- **F1 Score**: Harmonic mean of precision/recall
- **Hamming Loss**: Multi-label classification error
- **AUC**: Area under ROC curve
- **Confusion Matrices**: Per-emotion confusion
- **Distribution Analysis**: Emotion distribution patterns

---

## 🔄 Workflow

```
1. Data Preparation
   ↓
2. Model Training (train_emotion_model.py)
   ↓
3. Model Evaluation (evaluate_model.py)
   ↓
4. Model Testing (predict_emotion.py)
   ↓
5. API Deployment (api_server.py)
   ↓
6. React Integration (your frontend)
   ↓
7. Production Monitoring
```

---

## 🌟 Features

✅ **Modern TensorFlow 2.x** - Latest deep learning framework  
✅ **TensorFlow Hub** - Pre-trained BERT models  
✅ **Multi-label Classification** - Detect multiple emotions  
✅ **Real-time Inference** - Fast predictions for live chat  
✅ **REST API** - Easy integration with any frontend  
✅ **Comprehensive Evaluation** - Detailed performance metrics  
✅ **Response Guidance** - Coaching approach suggestions  
✅ **Production Ready** - Error handling, logging, monitoring  

---

## 📝 Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB for models and data
- **GPU**: Optional but recommended for faster training
- **OS**: Windows, Linux, or macOS

---

## 🚀 Deployment

### Development
```powershell
python api_server.py <model_path> <config_path>
```

### Production

Consider using:
- **Gunicorn** (Linux) or **Waitress** (Windows) for production server
- **Docker** for containerization
- **Cloud services** (AWS, Azure, GCP) for scaling
- **Load balancer** for high traffic
- **Redis** for caching predictions

---

## 📚 References

- **BERT Paper**: [Devlin et al., 2018](https://arxiv.org/abs/1810.04805)
- **GoEmotions Paper**: [Demszky et al., 2020](https://arxiv.org/abs/2005.00547)
- **TensorFlow Hub**: https://tfhub.dev
- **Mental Health AI**: Best practices for ethical AI in mental health

---

## 🤝 Contributing

This is a student project for mental health coaching AI. Feel free to:
- Report issues
- Suggest improvements
- Share feedback
- Add more emotions
- Improve accuracy

---

## ⚖️ Ethical Considerations

**Important Notes:**
- This AI is for **coaching support**, not clinical diagnosis
- Always maintain **client privacy** and confidentiality
- Ensure **informed consent** for data collection
- Have **human oversight** for critical decisions
- Follow **mental health regulations** in your region
- Provide **crisis resources** for emergencies

---

## 📞 Support

For questions or issues:
1. Check **[TRAINING_GUIDE.md](TRAINING_GUIDE.md)**
2. Review error messages carefully
3. Check TensorFlow and Python versions
4. Verify data file integrity
5. Test with smaller batch sizes

---

## ✅ Success Checklist

Before deployment:
- [ ] Model accuracy ≥ 90%
- [ ] All 28 emotions working
- [ ] API server running
- [ ] React frontend connected
- [ ] Error handling tested
- [ ] Response times acceptable
- [ ] Privacy measures in place
- [ ] Crisis protocols established

---

## 📄 License

This project uses the GoEmotions dataset and BERT model, which have their own licenses. Please review:
- Google Research License
- Apache License 2.0 (TensorFlow)
- Check institutional requirements for mental health AI

---

## 🎓 Academic Use

If using for academic purposes, please cite:
- GoEmotions dataset paper
- BERT original paper
- TensorFlow framework

---

**Built with ❤️ for better mental health support through AI**

*Last Updated: December 29, 2025*
