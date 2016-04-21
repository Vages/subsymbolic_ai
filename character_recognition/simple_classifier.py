import os
import numpy as np
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import scale
import PIL.Image as Image
import pickle

X = []
y = []

for path, subdirs, files in os.walk('chars74k-lite'):
    if path == "chars74k-lite":
        continue
    for filename in files:
        f = os.path.join(path, filename)
        img = Image.open(f).convert('L')
        img_resized = np.asarray(img.getdata(), dtype=np.float64).reshape((img.size[1]*img.size[0], 1))
        img_resized = scale(img_resized)
        target = filename[0]
        X.append(img_resized)
        y.append(target)

X = np.array(X)
X = X.reshape(X.shape[:2])

classifier = SVC(verbose=1, kernel='poly', degree=2, C=4, probability=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)
print(classification_report(y_test, predictions))

pickle.dump(classifier, "classifier.pickle")
