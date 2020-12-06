from django.shortcuts import render
import pickle 
import pandas as pd
from sklearn.pipeline import make_pipeline


# Create your views here.
#def home(request):
#   return render(request, 'home.html')

from django.shortcuts import render
from .forms import ModelForm


def predict_model(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']            
            num_emply = form.cleaned_data['num_emply']
            mh_famhist = form.cleaned_data['mh_famhist']
            mh_resourc = form.cleaned_data['mh_resourc']
            mh_coverage = form.cleaned_data['mh_coverag']
            mh_discuss = form.cleaned_data['mh_discuss']
            mh_negativ = form.cleaned_data['mh_negativ']

            # Run new features through ML model
            model_features = pd.Series()
            model_features['mh_coverage_flag'] = mh_coverage                                         
            model_features['mh_employer_discussion'] = mh_discuss                                         
            model_features['mh_resources_provided'] = mh_resourc                             
            model_features['mh_neg_view_cowork'] = mh_negativ                           
            model_features['mh_family_hist'] = mh_famhist      
            model_features['age'] = age                  
            model_features['sex'] = sex              
            model_features['comp_no_empl'] = num_emply

            loaded_model = pickle.load(open("ml_model/music_books.pkl", 'rb'))
  #          print(pd.DataFrame([model_features]))

            prediction = loaded_model.predict(pd.DataFrame([model_features]))[0]

  #          prediction = "Mypred"
            return render(request, 'home.html', {'form': form, 'prediction': prediction})



    # if a GET (or any other method) we'll create a blank form
    else:
        form = ModelForm()

    return render(request, 'home.html', {'form': form})
