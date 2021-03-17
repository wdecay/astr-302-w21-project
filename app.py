"""
Flask application main module.

Run in development mode:
set FLASK_ENV=development
flask run
"""

from flask import Flask, request, render_template, make_response
from io import BytesIO
from plotting import initialize_matplotlib, generate_plot, close_fig
from solar import compute_orbit

initialize_matplotlib()
app = Flask(__name__) # starts the flask application

@app.route('/')
def main():
    """
    Returns:
        Rendered index page template
    """
    return render_template('index.html')

@app.route('/ss.png')
def image():
    """
    Serves ss.png?date=<date>&n=<n>

    Get parameters:
        date: in the `yyyy-mm-dd` format
        n: limit on the number of planets to render (e.g.,., 4 to go up to Mars)

    Returns:
        Rendered image of the locations and orbits of the 
        <n> planets on the given date

    Raises:
        Will raise exceptions if GET parameters are missing or incorrect.
        Warning: no error checks are implemented.
    """
    date = request.args.get('date', type=str)
    n = request.args.get('n', default = 4, type=int)
    
    fig = generate_plot(date, n)
    fmt = "png"
    
    # here the generated matplotlib plot is saved into a binary stream 
    bio = BytesIO()
    fig.savefig(bio, format=fmt)
    close_fig(fig)
    
    #... which is then returned along with the HTTP response
    r = make_response(bio.getvalue())
    r.headers['Content-Type'] = 'image/{}'.format(fmt)
    # Note: browser caching was disabled to facilitate testing
    r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '-1'
    bio.close()
    return r
