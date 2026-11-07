# Run Crop Yield Prediction in AgriTech (Windows / VS Code)

The main AgriTech Flask app serves the integrated yield page at `http://127.0.0.1:5000/yield/`. The notebook `cropYieldPrediction1.ipynb` trains the model used by that page. Training writes one inference bundle to `crop_yield_app/models/crop_yield_model_bundle.joblib`.

## 1. Open the project and activate its virtual environment

In VS Code, open the AgriTech repository root. In the integrated PowerShell terminal:

```powershell
cd C:\Users\KIIT0001\OneDrive\Desktop\AgriTech
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, run the notebook and server with the explicit interpreter path shown below instead.

## 2. Install notebook training packages

```powershell
python -m pip install pandas numpy matplotlib seaborn scikit-learn scipy joblib tqdm ipykernel xgboost catboost
```

LightGBM, Optuna, and SHAP are optional. LightGBM is automatically skipped if absent; Optuna and SHAP are optional notebook enhancements. To install LightGBM too, run `python -m pip install lightgbm`.

## 3. Select the notebook kernel

Install the VS Code Python and Jupyter extensions if they are not already installed. Open `Crop Yield Prediction/cropYieldPrediction1.ipynb`. In VS Code, choose the AgriTech `.venv` as the notebook kernel. The notebook is configured to find `Crop Yield Prediction/Datasets/crop_yield.csv` whether VS Code opened the repository root or the notebook folder.

## 4. Train and export the model

Choose **Run All** and wait for the notebook to finish. It trains and compares the configured models; on a CPU this can take several minutes or longer. The final save cell exports `crop_yield_model_bundle.joblib` and supporting evaluation artifacts under `Crop Yield Prediction/crop_yield_app/models`.

The training/inference features intentionally exclude `Production`, because production directly reveals the yield target. Provide crop, year, season, state, area, annual rainfall, fertilizer use, and pesticide use. Predictions are expressed in the source dataset's yield units, which may vary across crops.

## 5. Start or restart Flask

Stop an already-running Flask process with **Ctrl+C**, then from the repository root run:

```powershell
python app.py
```

Or, without activating the environment:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000/yield/`, choose the supported inputs, and submit the form. The model is loaded when Flask starts; after retraining, restart Flask to load the new bundle.

## Troubleshooting

- If `/yield/` returns 503, the bundle is missing or invalid. Confirm the final notebook cell completed and the joblib file exists in `Crop Yield Prediction/crop_yield_app/models`, then restart Flask.
- If a crop, season, or state is rejected, choose an item from the page's dropdowns; those lists come from the notebook's fitted encoders.
- The page restricts year to the training dataset's year range. This model was not trained to extrapolate to future years.

