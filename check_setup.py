"""
System Check Script - Verify setup before training
"""

import sys
import os

def print_header(text):
    print("\n" + "="*70)
    print(text)
    print("="*70)

def print_check(item, status, details=""):
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {item}")
    if details:
        print(f"  {details}")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    required = (3, 8)
    status = version >= required
    details = f"Current: {version.major}.{version.minor}.{version.micro} | Required: {required[0]}.{required[1]}+"
    return status, details

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        return True, "Installed"
    except ImportError:
        return False, "Not installed"

def check_tensorflow():
    """Check TensorFlow installation and GPU"""
    try:
        import tensorflow as tf
        version = tf.__version__
        gpus = tf.config.list_physical_devices('GPU')
        gpu_count = len(gpus)
        
        if gpu_count > 0:
            details = f"Version {version} | GPUs: {gpu_count} device(s)"
        else:
            details = f"Version {version} | No GPU detected (will use CPU)"
        
        return True, details
    except ImportError:
        return False, "TensorFlow not installed"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_data_files():
    """Check if required data files exist"""
    data_dir = "goemotions/data"
    required_files = {
        "train.tsv": "Training data",
        "dev.tsv": "Validation data",
        "test.tsv": "Test data",
        "emotions.txt": "Emotion labels"
    }
    
    results = {}
    for filename, description in required_files.items():
        filepath = os.path.join(data_dir, filename)
        exists = os.path.exists(filepath)
        
        if exists:
            size = os.path.getsize(filepath)
            size_mb = size / (1024 * 1024)
            results[filename] = (True, f"{description} - {size_mb:.2f} MB")
        else:
            results[filename] = (False, f"{description} - File not found")
    
    return results

def check_disk_space():
    """Check available disk space"""
    try:
        import shutil
        stats = shutil.disk_usage('.')
        free_gb = stats.free / (1024**3)
        total_gb = stats.total / (1024**3)
        
        if free_gb < 5:
            return False, f"Only {free_gb:.1f} GB free (need 5+ GB)"
        else:
            return True, f"{free_gb:.1f} GB free of {total_gb:.1f} GB total"
    except Exception as e:
        return False, f"Could not check disk space: {str(e)}"

def estimate_training_time():
    """Estimate training time based on hardware"""
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        
        if len(gpus) > 0:
            return "Estimated: 30-45 minutes with GPU"
        else:
            return "Estimated: 2-3 hours with CPU"
    except:
        return "Could not estimate (install TensorFlow first)"

def main():
    print_header("BERT Emotion Detection - System Check")
    print("Verifying your system is ready for training...\n")
    
    all_checks_passed = True
    
    # Python version
    print_header("1. Python Environment")
    status, details = check_python_version()
    print_check("Python Version", status, details)
    all_checks_passed = all_checks_passed and status
    
    # Core packages
    print_header("2. Required Packages")
    
    packages = {
        'tensorflow': 'TensorFlow',
        'tensorflow_hub': 'TensorFlow Hub',
        'tensorflow_text': 'TensorFlow Text',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn'
    }
    
    package_status = True
    for pkg, name in packages.items():
        status, details = check_package(pkg)
        print_check(name, status, details)
        package_status = package_status and status
    
    all_checks_passed = all_checks_passed and package_status
    
    # TensorFlow details
    print_header("3. TensorFlow Configuration")
    status, details = check_tensorflow()
    print_check("TensorFlow", status, details)
    if status:
        print(f"  {estimate_training_time()}")
    all_checks_passed = all_checks_passed and status
    
    # Data files
    print_header("4. Dataset Files")
    data_results = check_data_files()
    data_status = True
    for filename, (status, details) in data_results.items():
        print_check(filename, status, details)
        data_status = data_status and status
    all_checks_passed = all_checks_passed and data_status
    
    # Disk space
    print_header("5. System Resources")
    status, details = check_disk_space()
    print_check("Disk Space", status, details)
    all_checks_passed = all_checks_passed and status
    
    # Training scripts
    print_header("6. Training Scripts")
    scripts = {
        'train_emotion_model.py': 'Main training script',
        'predict_emotion.py': 'Prediction script',
        'evaluate_model.py': 'Evaluation script',
        'api_server.py': 'API server script',
        'requirements_tf2.txt': 'Requirements file'
    }
    
    scripts_status = True
    for script, description in scripts.items():
        exists = os.path.exists(script)
        print_check(script, exists, description)
        scripts_status = scripts_status and exists
    all_checks_passed = all_checks_passed and scripts_status
    
    # Final summary
    print_header("Summary")
    
    if all_checks_passed:
        print("\n✓ ALL CHECKS PASSED!")
        print("\nYour system is ready for training.")
        print("\nNext steps:")
        print("  1. Run: python train_emotion_model.py")
        print("  2. Or run: .\\quick_start.ps1 (automated)")
        print("\nTraining will take " + estimate_training_time().lower() + "\n")
    else:
        print("\n✗ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before training.")
        print("\nCommon fixes:")
        print("  - Install packages: pip install -r requirements_tf2.txt")
        print("  - Download data files to goemotions/data/")
        print("  - Free up disk space (need 5+ GB)")
        print("  - Upgrade Python to 3.8+")
        print("\nSee TRAINING_GUIDE.md for detailed help.\n")
    
    print("="*70 + "\n")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
