# Disease model setup (VS Code on Windows)

The disease prediction page uses the local PyTorch CNN trained by `plant-disease-cnn-1 (1).ipynb`. The notebook now uses the dataset already in this project:

`Disease prediction/tomato disease detection/Dataset/<class name>/<image>`

It contains 10 tomato classes. The notebook makes a reproducible 80/20 train/validation split; you do not need Kaggle or separate `train`, `valid`, and `test` folders.

## Train and install the model

1. Open the AgriTech project root in VS Code.
2. Select the project Python environment (`.venv`) as the notebook kernel. Ensure the environment has PyTorch, torchvision, Pillow, numpy, matplotlib, seaborn, pandas, scikit-learn, and colorama installed.
3. Open `Disease prediction/plant-disease-cnn-1 (1).ipynb` and run all cells. Training may take a while on CPU; a CUDA-enabled PyTorch install can use an NVIDIA GPU if available.
4. The final cells write `plant_disease_model.pth` and `plant_disease_classes.json` directly into this `Disease prediction` folder.
5. Restart Flask (`python app.py` from the project root) and analyze a tomato leaf. The backend loads this model on the first request. There is no separate activation command.

The checkpoint is trained only on tomato classes, so select Tomato (or “I’m not sure” if that is the available option) when analyzing. Predictions are model outputs and should be confirmed by an agricultural expert.
