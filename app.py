import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

posts = []

# New: comments store karne ke liye har post ke sath ek list add kar rahe hain
# comments ek list of lists hogi, har post ki comments ke liye
comments = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts, comments=comments)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        image = request.files.get('image')
        image_filename = None
        
        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        posts.append({
            'title': title,
            'content': content,
            'image': image_filename,
            'likes': 0   # Add likes count here
        })
        # Jab naya post create ho, uske liye empty comment list bhi create kar do
        comments.append([])
        return redirect(url_for('index'))

    return render_template('create.html')

# Route to handle liking a post
@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if 0 <= post_id < len(posts):
        posts[post_id]['likes'] += 1
    return redirect(url_for('index'))

# New route to handle adding comments
@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 0 <= post_id < len(posts):
        comment_text = request.form.get('comment')
        if comment_text:
            comments[post_id].append(comment_text)
    return redirect(url_for('index'))

# Contact Route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

# Categories Route
@app.route('/categories')
def categories():
    return render_template('categories.html')

if __name__ == '__main__':
    app.run(debug=True)
