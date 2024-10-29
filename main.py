from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)

posts = [
    {
        "author": "Obatula Fuad",
        "title": "First Blog Post",
        "text": "This is the first post in this blog and I'm using it to test the flask Jinja templating thing",
        "date": datetime.now()
    },
    {
        "author": "Jognn Does",
        "title": "Second Blog Post",
        "text": "John Doe is John Doe because John Does loves John Does",
        "date": datetime.now()
    }
]



@app.route("/")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about/")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)