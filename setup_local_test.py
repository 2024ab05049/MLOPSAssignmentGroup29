"""
Setup script for local testing
This script helps set up the environment and checks for required files
"""
import os
import sys
from pathlib import Path

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = ['fastapi', 'uvicorn', 'numpy', 'sklearn', 'joblib', 'pydantic']
    missing = []
    
    for package in required:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    return True

def check_model_files():
    """Check if model files exist"""
    models_dir = Path("models")
    model_files = [
        "best_logreg_pipeline.joblib",
        "logreg_cv_best_pipeline.joblib",
        "best_randomforest_pipeline.joblib",
        "rf_cv_best_pipeline.joblib"
    ]
    
    if not models_dir.exists():
        print("❌ models/ directory does not exist")
        print("Creating models/ directory...")
        models_dir.mkdir(exist_ok=True)
        return False
    
    found_models = []
    for model_file in model_files:
        model_path = models_dir / model_file
        if model_path.exists():
            size = model_path.stat().st_size / (1024 * 1024)  # Size in MB
            print(f"✅ Found: {model_file} ({size:.2f} MB)")
            found_models.append(model_file)
        else:
            print(f"❌ Not found: {model_file}")
    
    if not found_models:
        print("\n⚠️  No model files found in models/ directory")
        print("\nTo get your model files:")
        print("1. Open your notebook in Google Colab")
        print("2. Download the model files from:")
        print("   - /content/gdrive/MyDrive/Mlops/Assignmentgrp29/models/")
        print("3. Place them in the models/ directory in this project")
        print("\nOr run the model training cells in your notebook locally to generate them.")
        return False
    
    return True

def check_app_file():
    """Check if app.py exists"""
    if Path("app.py").exists():
        print("✅ app.py found")
        return True
    else:
        print("❌ app.py not found")
        return False

def main():
    print("=" * 60)
    print("Local Testing Setup Check")
    print("=" * 60)
    print()
    
    checks = {
        "Python Version": check_python_version(),
        "App File": check_app_file(),
        "Dependencies": check_dependencies(),
        "Model Files": check_model_files()
    }
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = all(checks.values())
    
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print()
    if all_passed:
        print("🎉 All checks passed! You can now run the API:")
        print("   python app.py")
        print("\nThen test it with:")
        print("   python test_api.py")
        print("\nOr visit: http://localhost:8000/docs")
    else:
        print("⚠️  Some checks failed. Please fix the issues above before running the API.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

