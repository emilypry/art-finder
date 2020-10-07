'''These functions can be used to train and evaluate PreferenceModels.
'''
from preference_model import PreferenceModel


# given x_train and y_train, builds model, quickly or more slowly

def train_quickly(X_train, y_train, solver, C):
    '''Trains a model relatively quickly, using a solver and regularization parameter that have
    already been used successfully (instead of looping through various solvers and Cs). 
    '''
    