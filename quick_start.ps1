# Quick Start Script for BERT Emotion Detection Training
# Run this script to start training immediately

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan
Write-Host "BERT Emotion Detection - Quick Start" -ForegroundColor Green
Write-Host "Mental Health Coaching AI Project" -ForegroundColor Green
Write-Host ("="*70) -ForegroundColor Cyan

Write-Host "`nStep 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 2: Checking data files..." -ForegroundColor Yellow
$dataFiles = @("goemotions\data\train.tsv", "goemotions\data\dev.tsv", "goemotions\data\test.tsv")
$allFilesExist = $true
foreach ($file in $dataFiles) {
    if (Test-Path $file) {
        Write-Host "✓ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "✗ Missing: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "`n✗ Some data files are missing!" -ForegroundColor Red
    Write-Host "Please ensure all data files are in goemotions/data/ directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nStep 3: Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes..." -ForegroundColor Cyan
pip install -r requirements_tf2.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Error installing dependencies" -ForegroundColor Red
    Write-Host "Try running manually: pip install -r requirements_tf2.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nStep 4: Checking TensorFlow installation..." -ForegroundColor Yellow
$tfCheck = python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__}'); print(f'GPU: {len(tf.config.list_physical_devices(''GPU''))} devices')" 2>&1
Write-Host $tfCheck -ForegroundColor Green

Write-Host "`n" + ("="*70) -ForegroundColor Cyan
Write-Host "READY TO START TRAINING!" -ForegroundColor Green
Write-Host ("="*70) -ForegroundColor Cyan

$response = Read-Host "`nDo you want to start training now? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Host "`nStarting training..." -ForegroundColor Green
    Write-Host "This will take 30-180 minutes depending on your hardware.`n" -ForegroundColor Yellow
    
    python train_emotion_model.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n" + ("="*70) -ForegroundColor Cyan
        Write-Host "TRAINING COMPLETED SUCCESSFULLY!" -ForegroundColor Green
        Write-Host ("="*70) -ForegroundColor Cyan
        Write-Host "`nYour trained model is saved in: trained_models\" -ForegroundColor Cyan
        Write-Host "`nNext steps:" -ForegroundColor Yellow
        Write-Host "1. Check the training_history.png for training plots" -ForegroundColor White
        Write-Host "2. Run evaluation: python evaluate_model.py <model_path> <config_path>" -ForegroundColor White
        Write-Host "3. Test predictions: python predict_emotion.py <model_path> <config_path>" -ForegroundColor White
        Write-Host "4. Start API server: python api_server.py <model_path> <config_path>" -ForegroundColor White
        Write-Host "`nSee TRAINING_GUIDE.md for detailed instructions." -ForegroundColor Cyan
    } else {
        Write-Host "`n✗ Training encountered an error" -ForegroundColor Red
        Write-Host "Check the error messages above for details" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nSetup complete! Run 'python train_emotion_model.py' when ready." -ForegroundColor Cyan
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
