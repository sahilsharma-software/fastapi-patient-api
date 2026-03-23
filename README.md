# 🚀 Patient Management API (FastAPI)

A simple and functional REST API built using FastAPI to manage patient records.
It supports CRUD operations and automatically calculates BMI with a health verdict.

---

## 📌 Features

* Create Patient
* View All Patients
* View Single Patient
* Update Patient
* Delete Patient
* Sort Patients (height, weight, bmi)
* Automatic BMI Calculation
* Health Verdict (Underweight, Normal, Overweight, Obesity)

---

## 🛠 Tech Stack

* FastAPI
* Pydantic
* Python
* JSON (File Storage)

---

## ▶️ Run Locally

1. Install dependencies:

```
pip install fastapi uvicorn
```

2. Run server:

```
uvicorn main:apps --reload
```

3. Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## 📬 API Endpoints

* GET `/` → Welcome message
* GET `/about` → About API
* GET `/view` → Get all patients
* GET `/patients/{id}` → Get patient by ID
* POST `/create` → Create patient
* PUT `/edit/{id}` → Update patient
* DELETE `/delete/{id}` → Delete patient
* GET `/sort` → Sort patients

---

## 📊 Example JSON (Create Patient)

```
{
  "id": "P001",
  "name": "Rahul",
  "city": "Delhi",
  "age": 25,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}
```

---

## 📈 BMI Logic

BMI = weight / (height²)

* < 18.5 → Underweight
* 18.5 - 24.9 → Normal
* 25 - 29.9 → Overweight
* 30+ → Obesity

---

## 🧪 Testing

You can test APIs using:

* Swagger UI (`/docs`)
* Postman

---

## ⚠️ Note

Data is stored in a local JSON file (`patients.json`).

---

## 🚀 Future Improvements

* Add Database (PostgreSQL / MongoDB)
* Add Authentication (JWT)
* Deploy API online

---

## 👨‍💻 Author

Sahil Sharma

---

⭐ Star this repo if you like it!
