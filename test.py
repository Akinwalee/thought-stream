
from backend import create_app  # Adjust the import based on your app's structure
from backend.models import db

app = create_app()  # Create your Flask app instance
with app.app_context():
    db.drop_all()  # This will work now within the context
