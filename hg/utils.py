import os
import pickle
import Path

WORK_DIR = Path(__file__).parent 

def save_model(clf, solution, solution_idx, fitness, scores, selected_features, gen_idx):
    
    
    model_id = uuid.uuid4().hex
    model_path = 'models/{current_run_id}/{model_name}_{fitness:.2f}_{model_id}.pickle'.format(
                                                current_run_id=current_run_id,
                                                model_name=model_name,
                                                fitness=fitness,
                                                model_id=model_id)
    metadata_path = 'metadata/{current_run_id}/{model_name}_{fitness:.2f}_{model_id}.pickle'.format(
                                                current_run_id=current_run_id,
                                                model_name=model_name,
                                                fitness=fitness,
                                                model_id=model_id)
    file_path = os.path.join(WORK_DIR, model_path)
    meta_path = os.path.join(WORK_DIR, metadata_path)
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
