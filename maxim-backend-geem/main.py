from geem import app, run  # noqa: F401


@app.on_event('startup')
async def init_db():
    await run()
