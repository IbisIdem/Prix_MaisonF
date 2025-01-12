from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pickle
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='templates')

# Charger le modèle
try:
    regmodel = pickle.load(open('./regmodel.pkl', 'rb'))
except FileNotFoundError:
    raise RuntimeError("Le fichier 'regmodel.pkl' est introuvable ! Placez-le au bon endroit.")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict")
def predict(request: Request,
            sqft_living: str = Form(...),
            grade: str = Form(...),
            sqft_above: str = Form(...),
            sqft_living15: str = Form(...),
            bathrooms: str = Form(...)):
    
    # Valider les entrées : elles doivent être des entiers
    inputs = [sqft_living, grade, sqft_above, sqft_living15, bathrooms]
    try:
        data = [int(value) for value in inputs]  # Convertir les entrées en entiers
    except ValueError:
        return templates.TemplateResponse("home.html", {
            "request": request,
            "error": "Veuillez fournir uniquement des nombres entiers dans tous les champs."
        })
    
    # Vérifier que le grade est compris entre 1 et 12
    grade_value = data[1]
    if not (1 <= grade_value <= 12):
        return templates.TemplateResponse("home.html", {
            "request": request,
            "error": "La valeur de 'grade' doit être comprise entre 1 et 12."
        })
    
    # Vérifier que le nombre de salles de bain est compris entre 1 et 5
    bathrooms_value = data[4]
    if not (1 <= bathrooms_value <= 5):
        return templates.TemplateResponse("home.html", {
            "request": request,
            "error": "Le nombre de salles de bain doit être compris entre 1 et 5."
        })
    
    try:
        prediction = regmodel.predict([data])[0]
    except Exception as e:
        return templates.TemplateResponse("home.html", {
            "request": request,
            "error": f"Erreur de prédiction : {str(e)}"
        })
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "prediction_text": f"Le Prix de la maison est {prediction:.2f}"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
