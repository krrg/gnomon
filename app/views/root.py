from app import app


@app.route('/')
@app.route('/index.html')
def root_index():
    return "Index Page"
