import gc
gc.collect()

import numpy as np
import os
from django.conf import settings

# fpath="/content/CowBreedClassifier/MyDrive/CowBreedClassifier/CowsFinal"
#print(os.listdir(fpath))
fpath = settings.DATA_SET_PATH
cow_classes = os.listdir(fpath)


breeds=[breed for breed in cow_classes]


from itertools import chain
X=[]
y=[]
fullpaths=[str(fpath)+'/{}'.format(cow_class) for cow_class in cow_classes]
# print('running',fullpaths)
for counter,fullpath in enumerate(fullpaths):
    for imgname in os.listdir(fullpath):
        X.append([fullpath + '/' + imgname])
        y.append(breeds[counter])

#print(X[:10],"\n")
#print(y[:10],"\n")

X=list(chain.from_iterable(X))
#print(X[:10],"\n")
len(X)




import random
combined=list(zip(X,y))
#print(combined[:10],"\n")
random.shuffle(combined)
#print(combined[:10],"\n")
X[:],y[:]=zip(*combined)





from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

le=LabelEncoder()
le.fit(y)
y_ohe=to_categorical(le.transform(y),len(breeds))
# print(y_ohe.shape)
# print('run2---------------------------------------------------')
y_ohe=np.array(y_ohe)


import numpy as np
from tensorflow.keras.utils import img_to_array,load_img


def predict_image(img_path,testing_model):
  img_data=np.array([img_to_array(load_img(img_path, target_size = (299,299,3)))])
  x_test1 = img_data / 255
  test_predictions = testing_model.predict(x_test1)
  predictions = le.classes_[np.argmax(test_predictions,axis=1)]

  name=predictions[0].upper().replace("_"," ")
  return name
