'''The PreferenceModel class stores information about a model trained through SciKit Learn. Will be
used for making predictions about whether the viewer will like a given artwork. 
'''

class PreferenceModel:
    def __init__(self, theta=[], solver='', C=0, set_train=[], set_cv=[], set_test=[],
                 error_train=0, error_cv=0, error_test=0, precision_train=[],
                 recall_train=[], f1_train=0, precision_cv=[], recall_cv=[], f1_cv=0, precision_test=[],
                 recall_test=[], f1_test=0, accuracy_train=0, accuracy_cv=0, accuracy_test=0):
        self.theta = theta 
        self.solver = solver 
        self.C = C  
        self.set_train = set_train  # A list of the IDs of the Artworks in the training set
        self.set_cv = set_cv  # A list of the IDs of the Artworks in the cross validation set
        self.set_test = set_test  # A list of the IDs of the Artworks in the testing set
        self.error_train = error_train  # The model's training error
        self.error_cv = error_cv  # The model's cross validation error
        self.error_test = error_test  # The model's testing error
        self.precision_train = precision_train  # A list of the precision of the model on the training
                                                # set for y=0 and y=1, respectively
        self.recall_train = recall_train  # A list of the recall of the model on the training set for
                                            # y=0 and y=1, respectively
        self.f1_train = f1_train  # A list of the f1-score of the model on the training set for y=0
                                    # and y=1, respectively
        self.precision_cv = precision_cv
        self.recall_cv = recall_cv
        self.f1_cv = f1_cv
        self.precision_test = precision_test
        self.recall_test = recall_test
        self.f1_test = f1_test
        self.accuracy_train = accuracy_train # The proportion of accurately classified examples in the
                                                # training set
        self.accuracy_cv = accuracy_cv
        self.accuracy_test = accuracy_test
        
    def print_info(self):
        print('ID:', self.id_num, '\n   Training Error:', self.error_train, 'Cross Validation Error:',
              self.error_cv, 'Testing Error:', self.error_test, '\n   Training F1:', self.f1_train,
              'Cross Validation F1:', self.f1_cv, 'Testing F1:', self.f1_test,
              '\n   Training Accuracy:', self.accuracy_train, 'Cross Validation Accuracy:',
              self.accuracy_cv, 'Testing Accuracy:', self.accuracy_test)
        
    def get_string(self):
        '''Returns the string of all info for model, delimited by ~.
        '''
        info = str(self.id_num)+'~'+str(self.theta)+'~'+self.solver+'~'+str(self.C)+'~' \
               +str(self.set_train)+'~'+str(self.set_cv)+'~'+str(self.set_test)+'~' \
               +str(self.error_train)+'~'+str(self.error_cv)+'~'+str(self.error_test)+'~' \
               +str(self.precision_train)+'~'+str(self.recall_train)+'~'+str(self.f1_train)+'~' \
               +str(self.precision_cv)+'~'+str(self.recall_cv)+'~'+str(self.f1_cv)+'~' \
               +str(self.precision_test)+'~'+str(self.recall_test)+'~'+str(self.f1_test)+'~' \
               +str(self.accuracy_train)+'~'+str(self.accuracy_cv)+'~'+str(self.accuracy_test)

        return info
