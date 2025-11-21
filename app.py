from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import numpy as np
import os, json, uuid, io, datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# load joblib or pickle
def load_obj(path):
    try:
        import joblib
        return joblib.load(path)
    except Exception:
        import pickle
        with open(path, "rb") as f:
            return pickle.load(f)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-your-secret'

MODEL_PATH = "diabetes_model.pkl"
SCALER_PATH = "scaler.pkl"
HISTORY_FILE = "history.json"

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise FileNotFoundError("Model or scaler not found. Place diabetes_model.pkl and scaler.pkl in project root.")

model = load_obj(MODEL_PATH)
scaler = load_obj(SCALER_PATH)

def get_probability(model, X):
    X = np.asarray(X)
    try:
        probs = model.predict_proba(X)
        return float(probs[0][-1])
    except Exception:
        pass
    try:
        df = model.decision_function(X)
        return 1.0/(1.0 + np.exp(-float(df[0])))
    except Exception:
        pass
    p = model.predict(X)[0]
    return 0.85 if int(p)==1 else 0.15

def save_history(record):
    data = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []
    data.insert(0, record)  # newest first
    # keep last 50
    data = data[:50]
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, default=str, indent=2)

def create_pdf_report(record):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 60, "Diabetes Risk Report")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 90, f"Generated: {record['timestamp']}")
    c.line(50, height-95, width-50, height-95)

    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Input Features:")
    c.setFont("Helvetica", 11)
    y -= 20
    for k,v in record['features'].items():
        c.drawString(60, y, f"{k}: {v}")
        y -= 16

    y -= 6
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Prediction Summary:")
    y -= 18
    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Risk Label: {record['risk_label']} ({record['risk_pct']}%)")
    y -= 18
    c.drawString(60, y, f"Advice: {record['advice_short']}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Doctor Recommendations:")
    y -= 18
    c.setFont("Helvetica", 11)
    for line in record['doctor_reco'].split('\n'):
        c.drawString(60, y, f"- {line}")
        y -= 14
        if y < 80:
            c.showPage()
            y = height - 60

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ROUTES
@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/", methods=["GET"])
def home():
    # read history preview
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except:
            history = []
    return render_template("home_hospital.html", recent=history[:5])

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # read 8 PIMA features from form
        preg = float(request.form.get("preg", 0))
        glucose = float(request.form.get("glucose", 0))
        bp = float(request.form.get("bp", 0))
        skin = float(request.form.get("skin", 0))
        insulin = float(request.form.get("insulin", 0))
        bmi = float(request.form.get("bmi", 0))
        dpf = float(request.form.get("dpf", 0))
        age = float(request.form.get("age", 0))

        features = {"Pregnancies": preg, "Glucose": glucose, "Blood Pressure": bp,
                    "Skin Thickness": skin, "Insulin": insulin, "BMI": bmi,
                    "DPF": dpf, "Age": age}

        raw = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
        scaled = scaler.transform(raw)
        pred = int(model.predict(scaled)[0])
        prob = get_probability(model, scaled)
        risk_pct = round(prob*100,1)

        if risk_pct >= 65:
            risk_label = "High Risk"
            alert_type = "danger"
            color = "#d9534f"
        elif risk_pct >= 35:
            risk_label = "Medium Risk"
            alert_type = "warning"
            color = "#f0ad4e"
        else:
            risk_label = "Low Risk"
            alert_type = "success"
            color = "#5cb85c"

        # concise advice and doctor reco
        if risk_label == "High Risk":
            advice_short = "Immediate lifestyle changes and medical checkup recommended."
            doctor_reco = "1) Fasting Blood Sugar\n2) HbA1c test\n3) Consult Endocrinologist\n4) Personalized diet plan\n5) Regular follow-ups"
        elif risk_label == "Medium Risk":
            advice_short = "Reduce sugar & carbs; increase physical activity."
            doctor_reco = "1) Monitor fasting glucose monthly\n2) Consult Dietitian if weight gain\n3) Increase daily activity"
        else:
            advice_short = "Maintain healthy lifestyle; routine checkups."
            doctor_reco = "1) Annual checkup\n2) Maintain healthy diet and exercise"

        rec = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "features": features,
            "risk_label": risk_label,
            "risk_pct": risk_pct,
            "advice_short": advice_short,
            "doctor_reco": doctor_reco
        }

        save_history(rec)

        # store current record in session-like temp file (for PDF download)
        # save single latest
        with open("latest.json", "w") as f:
            json.dump(rec, f, indent=2)

        return render_template("result_hospital.html",
                               feature_summary=features,
                               risk_pct=risk_pct,
                               risk_label=risk_label,
                               color=color,
                               alert_type=alert_type,
                               advice_short=advice_short,
                               doctor_reco=doctor_reco)
    except Exception as e:
        return render_template("error.html", error=str(e))

@app.route("/download_report", methods=["GET"])
def download_report():
    if not os.path.exists("latest.json"):
        return "No report available", 404
    with open("latest.json", "r") as f:
        rec = json.load(f)
    pdf_buffer = create_pdf_report(rec)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"diabetes_report_{rec['id']}.pdf", mimetype='application/pdf')

@app.route("/history", methods=["GET"])
def history():
    data = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    return render_template("history.html", history=data)

# simple error template
@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
