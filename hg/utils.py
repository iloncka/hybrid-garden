import os
import pickle
from pathlib import Path
import config as cfg

WORK_DIR = cfg.WORK_DIR
MODELS_DIR = cfg.MODELS_DIR
METADATA_DIR = cfg.METADATA_DIR

def save_model(clf, solution, solution_idx, fitness, scores, selected_features, gen_idx):
    
    
    model_id = uuid.uuid4().hex
    model_path = '/{current_run_id}/{model_name}_{fitness:.2f}_{model_id}.pickle'.format(
                                                current_run_id=current_run_id,
                                                model_name=model_name,
                                                fitness=fitness,
                                                model_id=model_id)
    metadata_path = '/{current_run_id}/{model_name}_{fitness:.2f}_{model_id}.pickle'.format(
                                                current_run_id=current_run_id,
                                                model_name=model_name,
                                                fitness=fitness,
                                                model_id=model_id)
    file_path = os.path.join(MODELS_DIR, model_path)
    meta_path = os.path.join(METADATA_DIR, metadata_path)
    model_meta = {}
    model_meta = {'current_run_id': current_run_id,
                'file_path': file_path,
                'solution': solution,
                'solution_idx': solution_idx,
                'fitness': fitness,
                'model_id': model_id,
                'scores': scores,
                'selected_features': selected_features,
                'gen_idx': gen_idx}
    with open(file_path, 'wb') as handle:
        pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(meta_path, 'wb') as handle:
        pickle.dump(model_meta, handle, protocol=pickle.HIGHEST_PROTOCOL)
