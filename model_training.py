'''These functions can be used to train and evaluate PreferenceModels.
'''
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import datetime
import csv
import time 

from permanent_database import PermanentDatabase
from utilities import convert

def get_data(database):
    '''Retrieves all of the vectors and likes from the database and returns them as numpy arrays.
    '''
    # Get the lists of artworks vectors and of likes (0 or 1) from the database
    x, y = database.get_vectors_and_likes()
    
    # Return as numpy arrays (currently lists)
    return np.asarray(x), np.asarray(y)

def divide_dataset(x, y):
    '''Given numpy arrays of all x and all y, divides the dataset into a training set, a cross
    validation set, and a testing set randomly. Returns each as a numpy array. 
    '''
    # Add column of 1s to x to make design matrix
    X = np.column_stack((np.ones(x.shape[0]), x))
    
    # Divide X and y randomly into the training set and 'rest' set
    X_train, X_rest, y_train, y_rest = train_test_split(X, y, test_size=.4, shuffle=True)
    
    # Divide the 'rest' set into cross validation and testing sets
    X_cv, X_test, y_cv, y_test = train_test_split(X_rest, y_rest, test_size=.5)
    
    # Return the sets as numpy arrays (currently lists)
    return np.asarray(X_train), np.asarray(y_train), np.asarray(X_cv), np.asarray(y_cv), np.asarray(X_test), np.asarray(y_test)
    
def cost(theta, X, y):
    '''Finds the cost of a model.
    '''
    product = np.dot(X, theta)
    predictions = 1/(1+np.exp(-product))
    cost = -(1/X.shape[0]) * np.sum(np.dot(y, np.log(predictions)) + np.dot(1-y, np.log(1-predictions)))
    return cost

def train_slowly(X_train, y_train, X_cv, y_cv):
    '''Trains a model relatively slowly, by looping through various solvers and Cs and returning
    the model with the lowest cross-validation error. 
    '''
    print('Finding best model...')
    lowest_cv_error = 1e20
    best_model = None
    solvers = ['lbfgs', 'newton-cg', 'liblinear', 'sag', 'saga']
    #solvers = ['lbfgs', 'saga']
    #solvers = ['sag']
    Cs = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100]
    for solver in solvers:
        last_two = [1e20, 1e20]
        for C in Cs:
            #model = LogisticRegression(solver = solver, C=C, max_iter=50).fit(X_train, y_train)
            model = LogisticRegression(solver = solver, C=C, max_iter=200).fit(X_train, y_train)
            #model = LogisticRegression(solver = solver, C=C, max_iter=800).fit(X_train, y_train)
            theta = np.transpose(model.coef_)
            
            cv_error = cost(theta, X_cv, y_cv)
            
            if cv_error < lowest_cv_error:
                best_model = model
                lowest_cv_error = cv_error
            
            
            print('last two:', last_two)
            print('serror:', cost(theta, X_train, y_train), cv_error)
            print('C, SOLVER:', C, solver)
            print('BEST CV SO FAR:', lowest_cv_error)
            
            # Stop looping through C values using this solver if this cv_error has gotten larger
            # over the last three iterations; it'll probably just continue
            # to increase as C increases
            if cv_error > last_two[1] and cv_error > last_two[0]: 
                break
            
            # Stop looping through C values using this solver if this cv_error has been larger than
            # the lowest_cv_error over the past two iterations
            if cv_error > lowest_cv_error and last_two[1] > lowest_cv_error and last_two[1] != 1e20:
                break
            
            last_two[0] = last_two[1]
            last_two[1] = cv_error
                  
    print('Found best model')
    
    return best_model

def export_model(model, models_txt, X_train, y_train, X_cv, y_cv, X_test, y_test, quick, time_to_train):
    '''Gathers and exports a model's info to model.txt, delimited by ~.
    '''
    # The theta vector for the model
    theta = np.transpose(model.coef_)
    
    # The cost of the model on each dataset
    error_train = cost(theta, X_train, y_train)
    error_cv = cost(theta, X_cv, y_cv)
    error_test = cost(theta, X_test, y_test)
    
    # The accuracy of the model on each dataset
    acc_train = model.score(X_train, y_train) * 100
    acc_cv = model.score(X_cv, y_cv) * 100
    acc_test = model.score(X_test, y_test) * 100
    
    # The precision, recall, and f1 score of the model for 0 and 1 (disliked and liked artworks)
    # on the training set
    info = classification_report(y_train, model.predict(X_train), output_dict=True)
    prec_disliked = info.get('0').get('precision')
    rec_disliked = info.get('0').get('recall')
    f1_disliked = info.get('0').get('f1-score')
    prec_liked = info.get('1').get('precision')
    rec_liked = info.get('1').get('recall')
    f1_liked = info.get('1').get('f1-score')

    # The size of each dataset
    m_train = X_train.shape[0]
    m_cv = X_cv.shape[0]
    m_test = X_test.shape[0]
    
    # The solver and C used to train the model
    solver = model.get_params().get('solver')
    C = model.get_params().get('C')
    
    # The time at which the model was exported
    time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    
    # Turn theta from a numpy array to an unrolled list 
    theta = list(theta.ravel())
    
    # Make lists of the values that must be rounded off and those that don't
    must_round = [error_train, error_cv, error_test, acc_train, acc_cv, acc_test,
                  prec_disliked, rec_disliked, f1_disliked, prec_liked, rec_liked, f1_liked]
    rest = [m_train, m_cv, m_test, solver, C, time, quick, time_to_train, theta]
        
    # Add the model_info as a new row in models.csv
    file = open(models_txt, 'a')
    file.write('\n')
    for info in must_round:
        file.write('{num: .4f}'.format(num=info))
        file.write('~')
    for info in rest:
        file.write(str(info))
        file.write('~')
    file.close()

def train_model(database, models_txt, quick):
    '''Executes a training of a model, either quickly (if quick==True) by using the solver and C
    from the latest model stored in model.txt, or slowly (if quick==False) by looping through
    various solvers and Cs. Exports the model's info to models.csv and returns the model. 
    '''
    print('Training model...')
    
    # Track how long it takes to train the model
    beginning_time = time.perf_counter()
    
    # Extract the data from the database
    x, y = get_data(database)
    
    # Divide the dataset
    X_train, y_train, X_cv, y_cv, X_test, y_test = divide_dataset(x, y)
    
    model = None
    # If training the model quickly
    if quick == True:
        # Get the most recent solver and C from model.txt
        solver, C = get_solver_and_c(models_txt)
        # Train the model quickly using that solver and C
        model = LogisticRegression(solver=solver, C=C, max_iter=800).fit(X_train, y_train)
    # If training the model slowly
    else:
        model = train_slowly(X_train, y_train, X_cv, y_cv)
    
    # Get the time it took to train the model 
    ending_time = time.perf_counter()
    length = f'{(ending_time - beginning_time)/60:.2f}'
    
    # Add the model to models.csv
    export_model(model, models_txt, X_train, y_train, X_cv, y_cv, X_test, y_test, quick, length)
    
    # Print verification
    print('Trained and exported new model')
    
    return model

def get_solver_and_c(models_txt):
    '''Returns the solver and C value from the last-added model in models.txt.
    '''
    file = open(models_txt, 'r').readlines()
    i=1
    solver = ''
    C = ''
    while i < len(file):
        if file[-i]:
            num_delimiters = 0
            x = 0
            while x < len(file[-i]):
                
                if num_delimiters == 15:
                    while file[-i][x] != '~':
                        solver += file[-i][x]
                        x+=1
                    x+=1
                    while file[-i][x] != '~':
                        C += file[-i][x]
                        x += 1
                    break
                if file[-i][x]=='~':
                    num_delimiters+=1            
                x+=1
            break
        i+=1
    
    return solver, float(C)

def get_theta(models_txt):
    '''Gets the values of theta from the latest model in models.txt.
    '''
    file = open(models_txt, 'r').readlines()
    i=1
    theta = []
    while i < len(file):
        if file[-i]:
            num_delimiters = 0
            x = 1
            while x < len(file[-i]):
                if num_delimiters == 20:
                    while file[-i][x] != '[' and len(theta)<7501:
                        this_value = ''
                        
                        while file[-i][x] != ',' and file[-i][x] != ']':
                            this_value += file[-i][x]
                            x+=1
                        theta.append(float(this_value))
                        
                        x+=1

                if file[-i][x]=='~':
                    num_delimiters+=1            
                x+=1
            break
        i+=1
    
    return np.transpose(np.asarray(theta))

def predict_if_liked(artwork_location, theta):
    '''Given theta values from a model, predicts if an artwork will be liked. Returns 1 if so.
    '''
    # Convert the artwork to an unrolled vector
    artwork = np.asarray(convert(artwork_location))
        
    # Add a 1 to the beginning of the vector
    artwork = np.insert(artwork, 0, 1)

    # Get the probability that the user will like that artwork, given the latest model
    probability = 1/(1+np.exp(-np.dot(artwork, theta)))
      
    if probability >= .5:
        return 1
    else:
        return 0


def show_learning_curve(models_txt):
    '''Displays a graph of the learning curve of the model across multiple trainings. 
    '''
    pass
