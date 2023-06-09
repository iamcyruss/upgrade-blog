from flask import Flask, render_template, request
import requests
import os
import smtplib


app = Flask(__name__)
api_endpoint = "https://api.npoint.io/6e789129e8b4d33e00c4"
api_response = requests.get(api_endpoint)
api_data_json = api_response.json()
GMAIL_PW = os.environ['GMAIL_PW']
MY_EMAIL = "russnicosia.auto@gmail.com"


@app.route('/')
def index():
    return render_template('index.html', blog_data=api_data_json)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<post_id>')
def post(post_id):
    for post_data in api_data_json:
        if int(post_id) == int(post_data['id']):
            post_dict = {
                "id": post_data['id'],
                "title": post_data['title'],
                "subtitle": post_data['subtitle'],
                "body": post_data['body'],
                "author": post_data['author'],
                "publish": post_data['publish']
            }
    return render_template("post.html", post_dict=post_dict, blog_id=id)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        message_data = {
            'name': data['name'],
            'email': data['email'],
            'phone': data['phone'],
            'message': data['message']
        }
        with smtplib.SMTP("smtp.gmail.com", 587) as gmail_connection:
            gmail_connection.starttls()
            gmail_connection.login(user=MY_EMAIL, password=GMAIL_PW)
            gmail_connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs='russnicosia@gmail.com',
                msg=f"Subject: Message From Website\n\n"
                      f"From: {data['name']}\n"
                      f"Email: {data['email']}\n"
                      f"Phone: {data['phone']}\n"
                      f"Message: {data['message']}\n\n"
                      f"- Automated Russ"
            )
        return render_template('contact.html', message_data=message_data)
    else:
        return render_template('contact.html')


"""
@app.route('/form-entry', methods=['POST'])
def receive_data():
    data = request.form
    return f"<h1>Successfully sent message.</h1><p>{data['name']}</p><p>{data['email']}</p><p>{data['phone']}</p><p>{data['message']}</p>"
"""

if __name__ == '__main__':
    app.run(debug=True)
