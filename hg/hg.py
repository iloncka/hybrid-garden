from evolution import evolution
from selection import get_trees, get_best_tree
from utils import save_model
from scipy import stats

class HybridGarden:
    
    def __init__(self, n_trees=60, fitness_thresh=0.5, models=None, task=None):

        self.n_trees = n_trees
        self.fitness_thresh = fitness_thresh
        self.models = models
        self.task = task        
        self.trees = []        
        self.metas = []
        self.features = []        
        self.best_solution = None
        self.current_run_id = None
        self.solution_fitness = None
        self.solution_idx = None
        self.best_tree = None

    def _most_common_label(y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common

    def _mode_proba(y):    
        y = [stats.mode(classes) for classes in y]
        return y

    def _fit_func(X, y, tree, meta):

        solution = meta['solution'] 
        solution_idx = meta['solution_idx'] 
        selected_features = meta['selected_features']
        gen_idx = meta['gen_idx']
        fitness = meta['fitness']
        scores = meta['scores']

        tree.fit(X[:,selected_features], y)
        
        save_model(tree, solution, solution_idx, fitness, scores, selected_features, gen_idx)
    
        return tree, meta
        


    def fit(self, X, y):
        current_run_id, solution, solution_fitness, solution_idx = evolution(X, y, models=None, task=None)        
        self.current_run_id = current_run_id        
        self.best_solution = solution
        self.solution_fitness = solution_fitness
        self.solution_idx = solution_idx
        self.trees, self.metas = get_trees(self.current_run_id, self.n_trees, self.fitness_thresh)
        self.trees = [(_fit_func(X, y, tree, meta)
                    ) for tree, meta in zip(self.trees, self.metas)]
        self.best_tree = get_best_tree(self.trees, self.best_solution, self.solution_idx)        
        

    def predict(self, X):
        tree_preds = np.array([tree.predict(X[:,features]) for (tree, features) in self.trees])
        tree_preds = np.swapaxes(tree_preds, 0, 1)
        y_pred = np.array([_most_common_label(tree_pred) for tree_pred in tree_preds])
        return y_pred

    def predict_proba(self, X):
        tree_proba_preds = np.array([tree.predict_proba(X[:,features]) for (tree, features) in self.trees]) 
        tree_proba_preds = np.moveaxis(tree_proba_preds, [0, 1, 2], [2, 0, 1])
        y_pred_proba = np.array([_mode_proba(y_proba) for y_proba in tree_proba_preds])
        return y_pred_proba
        

