from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        pass
    template = render_template('base.html')
    return template


if __name__ == '__main__':
    app.run(port=8000, debug=True)