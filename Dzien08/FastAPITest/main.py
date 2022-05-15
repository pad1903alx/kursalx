from fastapi import FastAPI, Response, status, Path, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from typing import List, Optional
from employee import Employee
import uvicorn
from pydantic import ValidationError

app = FastAPI()

employees : List[Employee] = []
emp = Employee(id=1, fname="Jan", lname="Kowalski", pesel="12345678901")
employees.append(emp)
emp = Employee(id=2, fname="Marek", lname="Nowak", pesel="12345678901", acl=[987,123])
employees.append(emp)

try:
    emp = Employee(id=2, fname="Marek", lname="Nowak", pesel="jjjj", acl=[987,123])
    employees.append(emp)
except ValidationError as exc:
    print(exc.raw_errors[0].exc)

@app.get("/employees", response_model=List[Employee])
async def get_all():
    return employees

@app.get("/employee/{emp_id}")
async def get_employee(emp_id: int, response: Response):
    result = list( filter(lambda x: x.id==emp_id , employees) )
    if len(result):
        return result[0]
    #response.status_code = status.HTTP_404_NOT_FOUND
    #return {"message":"Nie znaleziono pracownika"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono pracownika")

@app.get("/")
async def main():
    return {"message":"Hello world!"}

@app.get("/img")
async def show_image():
    fd = open("kot.jpg", "rb")
    return StreamingResponse(fd, media_type="image/jpg")

@app.get("/html")
async def html_example():
    html = """
    <html>
     <body>
       <h1>Hello FastAPI!</h1>
     </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=status.HTTP_200_OK)

@app.get("/request")
async def get_request(r : Request):
    return {
        "headers" : r.headers,
        "cookies" : r.cookies,
        "client"  : r.client
    }

@app.post("/add_employee")
async def add_employee(emp : Employee, response : Response):
    employees.append(emp)
    response.status_code = status.HTTP_201_CREATED
    return {"message":"Dodałem pracownika"}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app", port=1234, reload=True)


