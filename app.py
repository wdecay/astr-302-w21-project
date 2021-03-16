from flask import Flask, request, render_template, make_response
from io import BytesIO
from plotting import initialize_matplotlib, generate_plot, close_fig

initialize_matplotlib()
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
    r = make_response(bio.getvalue())
    r.headers['Content-Type'] = 'image/{}'.format(fmt)
    r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '-1'
    bio.close()
    return r
