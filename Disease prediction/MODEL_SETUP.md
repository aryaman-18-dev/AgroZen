# Disease model setup (VS Code on Windows)

The disease prediction page uses the local PyTorch CNN trained by `plant-disease-cnn-1 (1).ipynb`. The notebook now uses the dataset already in this project:

`Disease prediction/tomato disease detection/Dataset/<class name>/<image>`

It contains 10 tomato classes. The notebook makes a reproducible 80/20 train/validation split; you do not need Kaggle or separate `train`, `valid`, and `test` folders.

## Retrain the model

1. Open the AgroZen project root in VS Code.
2. Select the project Python environment (`.venv`) as the notebook kernel. Ensure the environment has PyTorch, torchvision, Pillow, numpy, matplotlib, seaborn, pandas, scikit-learn, and colorama installed.
3. From the project root, run `python "Disease prediction/train_model.py"`. The script uses mild rotation, flips, and lighting/color augmentation; a stratified validation split; inverse-frequency class weights; early stopping; and saves the best validation checkpoint. Training can take a long time on CPU. A CUDA-enabled PyTorch install can use an NVIDIA GPU.
4. On successful completion, the script replaces `plant_disease_model.pth` and writes its matching `plant_disease_classes.json` in this folder. The old checkpoint is left in place if training fails before saving.
5. Restart Flask (`python app.py` from the project root) so the service reloads the new checkpoint, then analyze a tomato leaf.

The notebook `plant-disease-cnn-1 (1).ipynb` documents the original training experiment. Use `train_model.py` for retraining the app checkpoint so the improved augmentation, balanced loss, stratified validation, and best-checkpoint selection are applied.

The checkpoint is trained only on tomato classes, so select Tomato (or “I’m not sure” if that is the available option) when analyzing. The validation set comes from the same curated dataset and cannot prove accuracy on field photos. For better real-world performance, add correctly labeled field photos (different lighting, backgrounds, camera angles, and disease stages) to the matching dataset class folders before retraining. Predictions are model outputs and should be confirmed by an agricultural expert.
