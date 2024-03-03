from flask import Flask,redirect,request,render_template,flash

app = Flask(__name__)
app.secret_key = 'joao07'
app.config['DEBUG'] = True


@app.route('/')
def home():
    return render_template('index.html')







if __name__ == '__main__':
    app.run(debug=True)

