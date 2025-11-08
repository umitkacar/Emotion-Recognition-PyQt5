import pickle
import json
import numpy

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

# data	    40 x 40 x 8064	video/trial x channel x data
# labels	40 x 4	video/trial x label (valence, arousal, dominance, liking)
# nChannel_label = ("AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4")
# nChannel_idx = [1,3,2,4,7,11,13,31,29,25,21,19,20,17]
# nLabel, nTrial, nUser, nChannel, nTime  = 4, 40, 32, 40, 8064

class DeapEegX(object):
    def __init__(self,model_name = 'KNN'):
        
        # Read config format json
        with open('config_deap_eeg.json') as cf_json:
            self.cf = json.load(cf_json)
        cf_json.close()
        
        self.model_name = model_name
        
        self.train_data = None
        self.train_label_valance = None
        self.train_label_arousal = None
        
        self.test_data = None
        self.test_label_valance = None
        self.test_label_arousal = None
        
        self.model_valance = None
        self.model_arousal = None
        
        self.predict_valance = None
        self.predict_arousal = None
        
        self.confusion_matrix_valance = None
        self.confusion_matrix_arousal = None
    
    def config_load(self):
        return self.cf
        
    def process_raw_data(self):
    #*********************************************************************************************
    # EEG RAW DATA (valance -arousal) IN TRAIN SET
    #*********************************************************************************************
        print("EEG raw data is processing in train set ")
        
        train_data_eeg = open(self.cf["train_data_eeg_path"],'w')
        train_label_valance = open(self.cf["train_label_valance_path"],'w')
        train_label_arousal = open(self.cf["train_label_arousal_path"],'w')
        
        for user in range(self.cf["nUser_train_head"],self.cf["nUser_train_end"]+1,self.cf["nUser_train_step"]):  #nUser
            
            filename = self.cf["raw_data_eeg_path"] + "s"+'{:02d}'.format(user)+".dat"
            
            f = open(filename, 'rb')
            x = pickle.load(f, encoding='latin1')
            print(filename)
            
            for tr in range(self.cf["nTrial_train_head"]-1,self.cf["nTrial_train_end"],self.cf["nTrial_train_step"]): #nTrial 
                
                for ch in self.cf["nChannel_ON"]:
                    
                    for dat in range(self.cf["nTime_head"],self.cf["nTime_end"]): #nTime interval : 384 - 8064, total =  60 seconds
                        train_data_eeg.write(str(x['data'][tr][self.cf["nChannel_ON"][ch]][dat]) + " ");

                train_label_valance.write(str(x['labels'][tr][0]) + "\n");
                train_label_arousal.write(str(x['labels'][tr][1]) + "\n");
                train_data_eeg.write("\n");

        train_label_valance.close()
        train_label_arousal.close()
        train_data_eeg.close()
        print("EEG data is ready in train set")
        #*********************************************************************************************
        # EEG RAW DATA (valance -arousal) IN TEST SET
        #*********************************************************************************************
        print("EEG raw data is processing in test set ")
        
        test_data_eeg = open(self.cf["test_data_eeg_path"],'w')
        test_label_valance = open(self.cf["test_label_valance_path"],'w')
        test_label_arousal = open(self.cf["test_label_arousal_path"],'w')
        
        for user in range(self.cf["nUser_test_head"],self.cf["nUser_test_end"]+1,self.cf["nUser_test_step"]):  #nUser
            
            filename = self.cf["raw_data_eeg_path"] + "s"+'{:02d}'.format(user)+".dat"
            
            f = open(filename, 'rb')
            x = pickle.load(f, encoding='latin1')
            print(filename)
            
            for tr in range(self.cf["nTrial_test_head"]-1,self.cf["nTrial_test_end"],self.cf["nTrial_test_step"]): #nTrial 
                
                for ch in self.cf["nChannel_ON"]:
                    
                    for dat in range(self.cf["nTime_head"],self.cf["nTime_end"]): #nTime interval : 384 - 8064, total =  60 seconds
                        test_data_eeg.write(str(x['data'][tr][self.cf["nChannel_ON"][ch]][dat]) + " ");

                test_label_valance.write(str(x['labels'][tr][0]) + "\n");
                test_label_arousal.write(str(x['labels'][tr][1]) + "\n");
                test_data_eeg.write("\n");

        test_label_valance.close()
        test_label_arousal.close()
        test_data_eeg.close()
        print("EEG data is ready in test set")
    
    def add_class_label(self):
    #*********************************************************************************************
    # EEG DATA - CLASS LABELS (valance -arousal) IN TRAIN SET
    #*********************************************************************************************
        print("Class labels are being added for EEG data in train set")
        
        train_label_valance_class = open(self.cf["train_label_valance_class_path"],'w')
        with open(self.cf["train_label_valance_path"],'r') as file:
            for value in file:
                if float(value) > self.cf["label_threshold"]:    # default 4.5
                    train_label_valance_class.write(str(1) + "\n");
                else:
                    train_label_valance_class.write(str(0) + "\n");
                    
        train_label_valance_class.close()
        
        train_label_arousal_class = open(self.cf["train_label_arousal_class_path"],'w')
        with open(self.cf["train_label_arousal_path"],'r') as file:
            for value in file:
                if float(value) > self.cf["label_threshold"]:    # default 4.5
                    train_label_arousal_class.write(str(1) + "\n");
                else:
                    train_label_arousal_class.write(str(0) + "\n");
                    
        train_label_arousal_class.close()
        print("Class labels is ready for EEG data in train set")
    #*********************************************************************************************
    # EEG DATA - CLASS LABELS (valance -arousal) IN TEST SET
    #*********************************************************************************************
        print("Class labels are being added for EEG data in test set")
        
        test_label_valance_class = open(self.cf["test_label_valance_class_path"],'w')
        with open(self.cf["test_label_valance_path"],'r') as file:
            for value in file:
                if float(value) > self.cf["label_threshold"]:    # default 4.5
                    test_label_valance_class.write(str(1) + "\n");
                else:
                    test_label_valance_class.write(str(0) + "\n");
                    
        test_label_valance_class.close()
        
        test_label_arousal_class = open(self.cf["test_label_arousal_class_path"],'w')
        with open(self.cf["test_label_arousal_path"],'r') as file:
            for value in file:
                if float(value) > self.cf["label_threshold"]:    # default 4.5
                    test_label_arousal_class.write(str(1) + "\n");
                else:
                    test_label_arousal_class.write(str(0) + "\n");
                    
        test_label_arousal_class.close()
        print("Class labels is ready for EEG data in test set.")
        
    def load_dataset(self):
        print("Train & Test set are being loading ...")
        #*********************************************************************************************
        # LOAD TRAIN SET
        #*********************************************************************************************
        self.train_data = numpy.genfromtxt(self.cf["train_data_eeg_path"], delimiter=' ')
        self.train_label_valance = numpy.genfromtxt(self.cf["train_label_valance_class_path"], delimiter=' ')
        self.train_label_arousal = numpy.genfromtxt(self.cf["train_label_arousal_class_path"], delimiter=' ')
        #*********************************************************************************************
        # LOAD TEST SET
        #*********************************************************************************************
        self.test_data = numpy.genfromtxt(self.cf["test_data_eeg_path"], delimiter=' ')
        self.test_label_valance = numpy.genfromtxt(self.cf["test_label_valance_class_path"], delimiter=' ')
        self.test_label_arousal = numpy.genfromtxt(self.cf["test_label_arousal_class_path"], delimiter=' ')
        print("Train & Test set are loaded.")

    def model_select(self,model_name):
        
        if model_name == 'KNN':
            # Logistic regression
            self.model_arousal = KNeighborsClassifier(n_neighbors=5,leaf_size=200)
            self.model_valance = KNeighborsClassifier(n_neighbors=5,leaf_size=200)
        
        if model_name == 'SVM':
            pass
        
        print("Model is selected: " + model_name)
        
    def model_train(self):
        print("Model training is starting...")
        self.model_arousal.fit(self.train_data,self.train_label_arousal)
        self.model_valance.fit(self.train_data,self.train_label_valance)
        print("Model is trained")
    
    def model_test(self):
        print("Test is starting...")
        self.predict_arousal = self.model_arousal.predict(self.test_data)
        self.predict_valance = self.model_valance.predict(self.test_data)
        print("Test finished")
    
    def model_result(self):
        self.confusion_matrix_arousal = confusion_matrix(self.test_label_arousal,self.predict_arousal)
        self.confusion_matrix_valance = confusion_matrix(self.test_label_valance,self.predict_valance)
        print(self.confusion_matrix_arousal)
        print(self.confusion_matrix_valance)
        print("Arousal accuracy score = " + str(accuracy_score(self.test_label_arousal,self.predict_arousal)))
        print("Valance accuracy score = " + str(accuracy_score(self.test_label_valance,self.predict_valance)))
        
    def model_save(self):
        pickle.dump(self.model_arousal, open(self.cf["model_arousal_save_path"], 'wb'))
        pickle.dump(self.model_valance, open(self.cf["model_valance_save_path"], 'wb'))
        print("Model is saved")
        
    def model_load(self):
        self.model_arousal = pickle.load(open(self.cf["model_arousal_save_path"], 'rb'))
        self.model_valance = pickle.load(open(self.cf["model_valance_save_path"], 'rb'))
        print("Model is loaded")

if __name__ == '__main__':
    
    deapEeg = DeapEegX()
    #deapEeg.process_raw_data()
    #deapEeg.add_class_label()
    deapEeg.load_dataset()
    #deapEeg.model_select('KNN')
    #deapEeg.model_train()
    deapEeg.model_load()
    deapEeg.model_test()
    deapEeg.model_result()
    #deapEeg.model_save()
    