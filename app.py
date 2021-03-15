from flask import Flask, request, render_template, make_response
from io import BytesIO
from plotting import generate_plot, close_fig

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/ss.png')
def image():
    date = request.args.get('date', default='2021-01-01', type=str) # TODO: make it today
    n = request.args.get('n', default = 5, type=int)
    fig = generate_plot(n, date)
    fmt = "png"
    bio = BytesIO()
    fig.savefig(bio, format=fmt)
    close_fig(fig)
    response=make_response(bio.getvalue())
    response.headers['Content-Type'] = 'image/{}'.format(fmt)
    bio.close()
    return response
