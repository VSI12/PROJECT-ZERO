import io
import base64
import pandas as pd
import os
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import preprocessing
from flask import Flask, flash, render_template,request,redirect, url_for, jsonify
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder,OneHotEncoder,StandardScaler
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from intrusion_detection import confusion_matrixDecisionTreeClassifier,confusion_matrixKNN,X_Df_Preprocessed
from intrusion_detection import load_dataset, col_names,confusion_matrix,categorical_columns


app = Flask(__name__)
app.config['SECRET_KEY']='supersecret'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.debug = True


route_accessed = {"upload_KNN": False, "upload_DecisionTree": False, "upload_SVM": False}


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload FIle")


@app.route("/")
def home():
    return render_template("index.html", model_url = url_for)

@app.route("/model")
def model():
    return render_template("model.html")

@app.route("/upload_KNN")
def upload_KNN():
    route_accessed["upload_KNN"] = True
    form = UploadFileForm()
    return render_template('upload.html', form=form)

@app.route("/upload_DecisionTree")
def upload_DecisionTree():
    route_accessed["upload_DecisionTree"]=True
    form = UploadFileForm()
    return render_template('upload.html', form=form)

@app.route("/upload_SVM")
def upload_SVM():
    route_accessed["upload_SVM"] = True
    form = UploadFileForm()
    return render_template('upload.html', form=form)


@app.route('/submit', methods=['POST'])
def submit():
    file = request.files['file']
    file_path = "/" + file.filename
    file.save("dataset.csv")


   
    if request.method == 'POST':
        #check for if file is empty
        if file.filename == '':
            return "Error: No file selected for upload"
        
        #read the uploaded dataset
        try:
            df = pd.read_csv('dataset.csv', header=None, names=col_names)
        except pd.errors.EmptyDataError:
            return "Error: Uploaded file is empty or contains no data"
        
        #check is dataframe is empty
        if df.empty:
            return "Error: Uploaded file is empty"
      


        if route_accessed["upload_DecisionTree"] == True:
            #load the trained model
            with open('IDS_model_DECISION TREE CLASSIFIER.pkl', "rb") as file:
                clf = pickle.load(file)

            # Save confusion matrix plot
            plt.figure(figsize=(8, 6))
            sns.heatmap(confusion_matrixDecisionTreeClassifier, annot=True, fmt='d', cmap='Blues')
            plt.title('Confusion Matrix')
            plt.xlabel('Predicted Label')
            plt.ylabel('True Label')
            #plt.tight_layout()
            plt.savefig('confusion_matrix.png')

            # Convert plot to base64 for display in HTML
            with open('confusion_matrix.png', 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')


            return render_template('result.html', confusion_matrix=img_base64)


        elif route_accessed["upload_KNN"] == True:
            #load the trained model
             with open('IDS_model_KNN.pkl', "rb") as file:
                clf = pickle.load(file)

                 # Save confusion matrix plot
                plt.figure(figsize=(8, 6))
                sns.heatmap(confusion_matrixKNN, annot=True, fmt='d', cmap='Blues')
                plt.title('Confusion Matrix')
                plt.xlabel('Predicted Label')
                plt.ylabel('True Label')
                #plt.tight_layout()
                plt.savefig('confusion_matrix.png')

                # Convert plot to base64 for display in HTML
                with open('confusion_matrix.png', 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

                

                return render_template('result.html', confusion_matrix=img_base64)



        else:
            #load the trained model
            with open('IDS_model_SVM.pkl', "rb") as file:
                clf = pickle.load(file)


                predictions = clf.predict(X_Df_Preprocessed)
                # Save confusion matrix plot
                plt.figure(figsize=(8, 6))
                #sns.heatmap(confusion_matrixSVM, annot=True, fmt='d', cmap='Blues')
                plt.title('Confusion Matrix')
                plt.xlabel('Predicted Label')
                plt.ylabel('True Label')
                #plt.tight_layout()
                plt.savefig('confusion_matrixSVM.png')

                # Convert plot to base64 for display in HTML
                with open('confusion_matrixSVM.png', 'rb') as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')


        #Check if 'label' column is present in the DataFrame
     #   if 'label' not in df.columns:
      #    return "Error: 'label' column not found in the uploaded file"

        
         #Perform prediction only on features (exclude 'label' column)
       # features = df.drop(columns=['label'])

        # Perform intrusion detection
       # predictions = clf.predict(features)
    
   
    

    return 'Well done! File uploaded sucessfully'




if __name__ == '__main__':
    app.run(port=6500)