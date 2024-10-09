from fastapi import FastAPI

# from .controllers import item_controller
from controllers import item_controller

app = FastAPI()

# Include the item routes
app.include_router(item_controller.router)
