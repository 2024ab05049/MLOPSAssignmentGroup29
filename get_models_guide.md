# Getting Your Model Files for Local Testing

You need trained model files (`.joblib`) to test the API locally. Here are your options:

## Option 1: Download from Google Colab (Recommended)

If you ran the notebook in Google Colab, the models were saved to:
```
/content/gdrive/MyDrive/Mlops/Assignmentgrp29/models/
```

**Steps:**
1. Open Google Colab and navigate to your notebook
2. Open the file browser (folder icon on the left)
3. Navigate to: `Mlops/Assignmentgrp29/models/`
4. Download these files:
   - `best_logreg_pipeline.joblib`
   - `best_randomforest_pipeline.joblib`
   - (or `logreg_cv_best_pipeline.joblib` and `rf_cv_best_pipeline.joblib`)
5. Place the downloaded files in the `models/` directory in this project

## Option 2: Train Models Locally

If you don't have access to the Colab files, you can train the models locally by running the relevant cells from your notebook.

**Quick Training Script:**
1. Extract the model training code from your notebook (cells that do GridSearchCV)
2. Run them locally to generate the model files
3. The models will be saved to `models/` directory

## Option 3: Use a Sample Model (For Testing Only)

If you just want to test the API structure without the actual trained models, you can create a dummy model file. However, predictions won't be accurate.

## After Getting Model Files

Once you have the model files in the `models/` directory:

1. **Verify they're there:**
   ```bash
   dir models
   ```

2. **Run the setup check again:**
   ```bash
   python setup_local_test.py
   ```

3. **Start the API:**
   ```bash
   python app.py
   ```

4. **Test it:**
   - Open browser: http://localhost:8000/docs
   - Or run: `python test_api.py`

