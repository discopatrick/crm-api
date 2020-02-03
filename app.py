from flask import Flask

app = Flask(__name__)


@app.route('/contact', methods=('POST',))
def add_contact():
    return 'Will add contact'


if __name__ == '__main__':
    app.run()
