
# Diabetes Risk Prediction App

A professional web application for predicting diabetes risk using **Fuzzy Logic** and **Machine Learning**. The app provides a user-friendly interface, pictorial risk visualization, feature breakdown, doctor-like recommendations, and age-specific tips.

---

## **Features**

- Predict diabetes risk using **8 PIMA features**:
  - Pregnancies
  - Glucose
  - Blood Pressure
  - Skin Thickness
  - Insulin
  - BMI
  - Diabetes Pedigree Function (DPF)
  - Age
- Interactive **risk gauge** (pictorial representation with Chart.js)
- **Dark-themed professional UI** with Bootstrap
- Shows **feature-wise summary**
- Alerts and advice based on **risk level**
- High-risk patients get:
  - Full recommendations
  - Daily routines
  - Suggested doctor tests
- Age-specific health tips
- Download prediction reports as **PDF**
- History tracking of past predictions

---

## **Screenshots**

<img width="1919" height="871" alt="image" src="https://github.com/user-attachments/assets/d0c9b509-ad41-4d23-8e5d-d1f880a5c9b0" />
 
*Home page for entering patient details*

<img width="1919" height="866" alt="image" src="https://github.com/user-attachments/assets/f9180f72-9ebb-4668-a457-104eda0afd95" />
 
*Risk prediction with gauge, alerts, and recommendations*

<img width="1919" height="868" alt="image" src="https://github.com/user-attachments/assets/6b18b157-0641-4649-bf11-7e783d2147ad" />
  
*Past prediction history*

---

## **Tech Stack**

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn, joblib, numpy, pandas
- **Frontend**: HTML, CSS, Bootstrap 5, Chart.js
- **Optional**: Fuzzy Logic integration (for interpretable predictions)

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/ankitsunil530/diabetes-app.git
   cd diabetes-app


2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux / macOS
   venv\Scripts\activate       # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Make sure your model and scaler files are present:

   * `diabetes_model.pkl`
   * `scaler.pkl`

---

## **Running the App**

```bash
python app.py
```

Open a browser and visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## **Folder Structure**

```
diabetes-app/
├── app.py
├── templates/
│   ├── home.html
│   ├── result.html
│   ├── history.html
│   └── about.html
├── static/
│   ├── hospital.css
│   └── images/
├── diabetes_model.pkl
├── scaler.pkl
├── requirements.txt
└── README.md
```

---

## **Usage**

1. Enter patient details in the form.
2. Click **Predict Risk**.
3. Check **risk gauge**, **alerts**, and **recommendations**.
4. Download report if needed.
5. Track past predictions in **History**.

---

## **License**

MIT License © 2025 Sunil Kumar

---

## **Author**

* **Sunil Kumar**
  Student & Developer | CSE | IIITDM Jabalpur
  GitHub: [https://github.com/ankitsunil530](https://github.com/ankitsunil530)

```

---



