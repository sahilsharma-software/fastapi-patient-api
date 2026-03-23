from fastapi import FastAPI , Path ,HTTPException ,Query
import json
apps =FastAPI()

def load_data():
    with open("patients.json","r") as f:
        data =json.load(f)
    return data



@apps.get("/")
def fake():
    return {"MESSAGE":"A fully functional Patient Management API ::"}

@apps.get("/about")
def latest():
    return {"MESSAGE":"A fully functional API to manage Your Patient -Records"}

@apps.get("/view")
def view():
    data = load_data()
    return data


@apps.get("/patients/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="Id of the patient in the database", example="P001")
):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="patient record not found")
@apps.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="sort on the basis of height, weight or bmi"),
    order: str = Query('asc', description="sort in ascending or descending order")
):
    valid_field = ["height", "weight", "bmi"]
    
    if sort_by not in valid_field:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_field}"
        )
    
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Select from 'asc' or 'desc'"
        )
    
    data = load_data()
    
    sort_order = True if order == "desc" else False
    
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )
    
    return sorted_data