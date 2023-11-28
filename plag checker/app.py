from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from difflib import SequenceMatcher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class PlagiarismForm(FlaskForm):
    text1 = TextAreaField('Text 1', validators=[DataRequired()])
    text2 = TextAreaField('Text 2', validators=[DataRequired()])

def similarity_ratio(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PlagiarismForm()

    if form.validate_on_submit():
        similarity = similarity_ratio(form.text1.data, form.text2.data)
        return redirect(url_for('result', similarity=similarity))

    return render_template('index.html', form=form)

@app.route('/result', methods=['POST'])
def result():
    text1 = request.form.get('text1')
    text2 = request.form.get('text2')
    similarity = (similarity_ratio(text1, text2)*100)
    return render_template('result.html', similarity=similarity)

if __name__ == '__main__':
    app.run(debug=True)
