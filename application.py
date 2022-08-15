from time import sleep
from flask import Flask, render_template
from test import get_sheet, list_of_lists

app = Flask(__name__)


@app.route('/')
def index():
    # Home page
    get_sheet()
    return render_template('index.html', list_of_lists=list_of_lists)


if __name__ == "__main__":
    app.run()
