import pandas as pd
import os

def _create_plane_meta(nested_meta):
    plane_meta = {}
    for k, v in nested_meta.items():
        if k != 'scores':
            plane_meta[k] = v
        else:
            for item in nested_meta['scores']:
                plane_meta[item] = np.mean(nested_meta['scores'][item])
    return plane_meta

def get_trees(current_run_id, n_trees, fitness_thresh):

    REPORTS_DIR = '../artifacts/reports/{current_run_id}'.format(current_run_id=current_run_id)
    META_DIR = '../artifacts/metadata/{current_run_id}'.format(current_run_id=current_run_id)
    MODELS_DIR = '../artifacts/models/{current_run_id}'.format(current_run_id=current_run_id)
    
    meta_files = [name for name in os.listdir(META_DIR) if os.path.isfile(os.path.join(meta_dir, name))]
    
    all_metas = []
    for filename in meta_files:
        with open(os.path.join(META_DIR, filename), 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            meta = pickle.load(f)
            all_metas.append(meta)

    solutions = [(tuple(meta['solution']), meta['fitness'], meta['model_id'])  for meta in all_metas if meta['fitness'] > fitness_thresh]
    solutions_df = pd.DataFrame(solutions, columns=['solution', 'fitness','model_id'])
    solutions_df = solutions_df.sort_values('fitness', ascending=False).drop_duplicates('solution').sort_index()
    selected_models = solutions_df.model_id.to_list()
    del solutions_df

    unique_meta = [_create_plane_meta(meta) for meta in all_metas if meta['model_id'] in selected_models]
    unique_meta_df = pd.DataFrame(unique_meta)

    best_fitness_list = unique_meta_df.sort_values(['fitness', 'test_precision'], ascending=False)[:n_trees].model_id.to_list()
    best_precisions_list = unique_meta_df.sort_values(['test_precision', 'fitness'], ascending=False)[:n_trees].model_id.to_list()
    best_recalls_list = unique_meta_df.sort_values(['test_recall', 'fitness'], ascending=False)[:n_trees].model_id.to_list()
    
    best_unique = set(best_fitness_list + best_precisions_list + best_recalls_list)
    unique_meta_df = unique_meta_df.loc[unique_meta_df.model_id.isin(best_unique)]
    unique_meta_df.to_csv(os.path.join(REPORTS_DIR, 'best_models_{current_run_id}.csv'.format(current_run_id=current_run_id)))

    selected_metas = [meta for meta in all_metas if meta['model_id'] in best_unique]
    del all_metas
    
    best_models = []
    for item in selected_metas:    
        with open(item['file_path'], 'rb') as f:
            # The protocol version used is detected automatically, so we do not
            # have to specify it.
            model = pickle.load(f)
            best_models.append(model)

    return best_models, selected_metas

def get_best_tree(trees, best_solution, solution_idx):
    selected_tree = [tree, meta for (tree, meta) in trees if (meta['solution'] == best_solution) 
            and (meta['solution_idx'] == solution_idx)] 
    return selected_tree[0], selected_tree[1]
