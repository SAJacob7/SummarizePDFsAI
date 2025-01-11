from flask import Flask, jsonify, redirect, url_for, render_template, request
import pdf_summarizer

app = Flask(__name__)

@app.route('/')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit_link', methods=['POST'])
def submit_link():
    link = request.form['link']
    result, second_result = pdf_summarizer.main(link)
    if second_result == False:
        return render_template('error.html', result=result)
    else:
        return render_template('result.html', result=result, second_result=second_result)


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()