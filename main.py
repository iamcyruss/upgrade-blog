from flask import Flask, render_template
import requests


app = Flask(__name__)
api_endpoint = "https://api.npoint.io/6e789129e8b4d33e00c4"
api_response = requests.get(api_endpoint)
api_data_json = api_response.json()


@app.route('/')
def index():
    return render_template('index.html', blog_data=api_data_json)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


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


if __name__ == '__main__':
    app.run(debug=True)
