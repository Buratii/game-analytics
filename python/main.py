import logging
import uvicorn

def main():
    logging.basicConfig(level=logging.DEBUG)

    # Run the FastAPI app
    uvicorn.run(
        "app:app",          # path.to.module:app_instance
        host="0.0.0.0",
        port=8000,
        reload=True  # Optional: disable in production
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
