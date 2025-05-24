from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html


from app.routers import auth, mechanici, zakaznici, zakazky



app = FastAPI(
    title="Autoservis IS",
    description="REST API pro autoservis – zakázky, mechanici, zákazníci, autentizace a jednoho dne i konverzace.",
    version="1.0.0"
)


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# pridavani routeru
app.include_router(auth.router)
app.include_router(mechanici.router)
app.include_router(zakaznici.router)
app.include_router(zakazky.router)



# zprava z backendu do konzole
@app.get("/")
def root():
    return {"zprava": "Autoservis API běží!"}


# proboha ta silena bila....
@app.get("/docs", include_in_schema=False)
async def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Autoservis API",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_ui_parameters={"theme": "dark"},
    )
