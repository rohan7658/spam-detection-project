from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
import os
import joblib

#model1 = joblib.load(os.path.dirname(__file__) + "\\mySVCModel1.pkl")
#model2 = joblib.load(os.path.dirname(__file__) + "\\myModel.pkl")

model1_path = os.path.join(os.path.dirname(__file__), "mySVCModel1.pkl")
model2_path = os.path.join(os.path.dirname(__file__), "myModel.pkl")

# Load the models with error handling
try:
    model1 = joblib.load(model1_path)
    model2 = joblib.load(model2_path)
except Exception as e:
    print(f"Error loading models: {e}")
    model1, model2 = None, None

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if(request.method == "POST"):
        un = request.POST.get('username')
        up = request.POST.get('password')
        
        if(un == "manu" and up == "manu"):
            request.session['authdetails'] = "manu"
            if(request.session['authdetails'] == "manu"):
                return render(request, 'index.html')
            else:
                return redirect('/auth')
        else:
            return render(request, 'auth.html')
    else:
        if(request.session.has_key('authdetails') == True):
            print("Session Auth")
            return render(request, 'index.html')
        else:
            return render(request, 'auth.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkSpam(request):
    if request.method == "POST":
        if request.session.get('authdetails') == "manu":
            algo = request.POST.get("algo")
            rawData = request.POST.get("rawdata")
            rawData = [rawData]  # Ensure rawData is in the correct format for prediction

            # Model prediction
            if algo == "Algo-1":
                prediction = model1.predict(rawData)[0]  # Get the prediction (0 or 1)
            elif algo == "Algo-2":
                prediction = model2.predict(rawData)[0]  # Get the prediction (0 or 1)

            # Map prediction to "ham" or "spam"
            result = "ham" if prediction == 0 else "spam"

            # Return result to the output page
            return render(request, 'output.html', {"answer": result})

        else:
            return redirect('/')
    else:
        return render(request, 'index.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if(request.session.has_key('authdetails') == True):
        request.session.clear()
        print("-----------------")
        # request.session.flush()
        return redirect('/')
    else:
        return redirect('/')