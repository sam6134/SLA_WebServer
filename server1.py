from flask import Flask, render_template, Response, flash, request, send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = '21a00ee024ebe902cf1848208f5c1a29'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route('/')
def index():
    return "homepage"

@app.route('/prime/<int:num>',methods=["GET"])
def prime(num):
    for i in range(1,int(num**(0.5)+1)):
        if(num%i == 0):
            return "Not Prime"
        else:
            return "Prime"

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=False, debug=True,port=5050)