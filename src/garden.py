from evolution import evolution
from selection import get_best_trees

class HybridGarden:
    
    def __init__(self, n_trees=60, models=None, task=None):

        self.n_trees = n_trees
        self.models = models
        self.task = task        
        self.trees = []
        self.fited_trees = []
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

    def _median_proba(y):    
        y = [np.median(classes) for classes in y]
        return y

    def fit(self, X, y):
        current_run_id, solution, solution_fitness, solution_idx = evolution(X, y, models=None, task=None)        
        self.current_run_id = current_run_id        
        self.best_solution = solution
        self.solution_fitness = solution_fitness
        self.solution_idx = solution_idx
        self.trees, self.metas = get_trees(n_trees=60)
        self.fited_trees = [(fit_func(tree, meta['solution'], meta['solution_idx'])) for tree, meta in zip(self.trees, self.metas)]
        self.best_tree = get_best_tree(self.best_solution, self.solution_idx)        
        self.trees.extend(trees)

    def predict(self, X):
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(tree_preds, 0, 1)
        y_pred = [_most_common_label(tree_pred) for tree_pred in tree_preds]
        return np.array(y_pred)

    def predict_proba(self, X):
        tree_proba_preds = np.array([tree.predict_proba(X[:,features]) for (tree, features) in self.fitted_trees]) 
        tree_proba_preds = np.moveaxis(tree_proba_preds, [0, 1, 2], [2, 0, 1])
        tree_proba_preds = np.array([_median_proba(y_proba) for y_proba in tree_proba_preds])
        return np.array(y_pred_proba)
        

