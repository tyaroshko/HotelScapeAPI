from fastapi import FastAPI

from routers import (auth_routers, booking_routers, client_routers,
                     invoice_routers, room_routers)

app = FastAPI(
    title="Hotel Administration API",
    description="API for hotel management",
    version="0.0.1",
)

app.include_router(auth_routers.router)
app.include_router(room_routers.router)
app.include_router(client_routers.router)
app.include_router(booking_routers.router)
app.include_router(invoice_routers.router)
