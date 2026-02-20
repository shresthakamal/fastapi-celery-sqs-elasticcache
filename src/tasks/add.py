from app.celery import app

@app.task(name="calculator.add")
def add(a: int, b: int) -> int:
    """
    Add two numbers.
    """
    return a + b