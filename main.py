from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

class Cat:
    def __init__(self, id, name: str, photo: str, age: int):
        self.id = id
        self.name = name
        self.photo = photo
        self.age = age
        
class CatDatabase:
    def __init__ (self, cats: list[Cat]):
        self._cats = cats
        
        
    def get_all(self) -> list[Cat]: 
        return self._cats
    
    def get_by_id(self, id: int) -> Cat | None: 
        for cat in self._cats:
            if cat.id == id:
                return cat
            
        return None
    

DATABASE = CatDatabase([
    Cat(1, "Valera", "https://cdn.britannica.com/70/234870-050-D4D024BB/Orange-colored-cat-yawns-displaying-teeth.jpg", 4),
    Cat(2, "Sergiy", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUu_vVr5ADkYaRaiOeH7GZLXJEz2Ix08ZB6w&s", 2),
    Cat(3, "Petro", "https://i.pinimg.com/474x/5d/a3/60/5da360c98b9af0ad709fe18606992229.jpg", 1)
])

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    cats = DATABASE.get_all()
    cats_count = len(cats)
    return templates.TemplateResponse(
        request=request, name="index.html", context={
            "cats_count": cats_count,
            "cats": cats
        }
    )
    
@app.get("/info", response_class=HTMLResponse)
def info(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="info.html")
    
@app.get("/{id}", response_class=HTMLResponse)
def cat(request: Request, id: int) -> HTMLResponse:
    cat = DATABASE.get_by_id(id)
    return templates.TemplateResponse(
        request=request, name="cat.html", context={
            "cat": cat,
            "cat_id":id
            }
    )
    