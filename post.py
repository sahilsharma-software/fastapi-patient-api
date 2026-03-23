from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
import json
import os

apps = FastAPI()

# ----------------- Patient Model -----------------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="name of the patient")]
    city: Annotated[str, Field(..., description="city where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="age of the patient")]
    gender: Annotated[Literal["male","female","other"], Field(..., description="gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="height should be in meters")]
    weight: Annotated[float, Field(..., gt=0, description="weight should be in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"
# -------------new pydantic model(update - [patient])------------
class Patient_Update(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal["male","female","other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]



# ----------------- JSON Handling -----------------
DATA_FILE = "patients.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE,"r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

# ----------------- Routes -----------------
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

@apps.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="patient already exist")
    # Save patient including computed fields
    patient_dict = patient.model_dump() | {"bmi": patient.bmi, "verdict": patient.verdict}
    data[patient.id] = patient_dict
    save_data(data)
    return JSONResponse(status_code=201, content={"message":"patient created successfully"})

#---------------update route----
#---------------update route----
@apps.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update:Patient_Update):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # ensure id present
    existing_patient_info["id"] = patient_id

    # recreate patient to recalc bmi & verdict
    try:
        patient_pydantic_obj = Patient(**existing_patient_info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ❌ bug tha: id remove ho raha tha
    # existing_patient_info = patient_pydantic_obj.model_dump(exclude="id")

    # ✅ fix:
    existing_patient_info = patient_pydantic_obj.model_dump()

    data[patient_id] = existing_patient_info

    save_data(data)

    # ❌ bug: empty response
    return JSONResponse(
        status_code=202,
        content={"message": "patient updated successfully"}
    )
#-------------delete-------------
@apps.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200,content={"message":"deleted successfully"})
