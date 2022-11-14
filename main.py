import uvicorn
import os

from dotenv import load_dotenv

from app import create_app


load_dotenv(verbose=True, dotenv_path=".env.local")
load_dotenv(verbose=True, dotenv_path=".env")


if __name__ == '__main__':
    uvicorn.run("main:app", host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 5000)),
                log_level="info", reload=True, reload_dirs=["app"])
else:
    app = create_app()
