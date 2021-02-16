class KFold:
  def __init__(self, edges, cv=5, RANDOM_SEED=None):
    self.edges = edges
    self.cv = cv
    self.RANDOM_SEED = RANDOM_SEED
  
  def get_split(self):
      rd.seed(seed=self.RANDOM_SEED)
      
      edges = self.edges
      n_f = len(edges)//cv

      # -- Randomizing data
      rd.shuffle(edges)

      return np.array([edges[k*n_f:(k+1)*n_f] if k<(cv-1) else edges[k*n_f:] for k in range(cv)])    

class StratifiedKFold(KFold):
  def __init__(self, edges, y, cv=5, RANDOM_SEED=None):
    super().__init__(edges, cv, RANDOM_SEED)
    self.y = y
  
  def get_split(self):
    edges = self.edges
    y = self.y
    rd.seed(seed=self.RANDOM_SEED)
    
    rd.shuffle(edges)
    pos = np.array_split(edges[y==1], self.cv)
    neg = np.array_split(edges[y==0], self.cv)

    return np.array([np.concatenate((pos[k], neg[k])) for k in range(self.cv)])