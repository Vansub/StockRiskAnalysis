import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle
import os

data = pd.read_csv("investment_risk_assessment.csv")
X = data.drop(['risk_level'], axis = 1)
y= data['risk_level']

# Encode 
le = LabelEncoder()
y=le.fit_transform(y)

#train_test_split
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

#Train the model
model= DecisionTreeClassifier(random_state=42)
model.fit(X_train,y_train)

#Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test,y_pred)
print(f"Model Accuracy:{accuracy:.2f}")

os.makedirs('models',exist_ok=True)


#save the model
with open('risk_assessment_model.pk1','wb')as f:
    pickle.dump(model,f)

with open('label_encoder.pk1','wb') as f:
    pickle.dump(le,f)
print("Model and label encoder saved successfully")
    