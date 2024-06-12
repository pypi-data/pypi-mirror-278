from pathlib import Path

import joblib


def save_pipeline(pipeline, model_name):
    save_path = Path(f'{model_name}')
    joblib.dump(pipeline, save_path)


def load_pipeline(model_name):
    save_path = Path(f'{model_name}')
    return joblib.load(save_path)
