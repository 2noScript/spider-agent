import uvicorn
from browser.settings import FastAPISettings

print("FastAPISettings.reload_on_file_change",FastAPISettings.reload_on_file_change)

if __name__ == "__main__":
    uvicorn.run(
        "browser.main:app",
        host=FastAPISettings.ip,
        port=FastAPISettings.port,
        reload=FastAPISettings.reload_on_file_change,
    )
