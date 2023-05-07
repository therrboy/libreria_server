from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)


class AddBoks(FlaskForm):
    bookName = StringField(label='Book Name', validators=[DataRequired()])
    bookAuthor = StringField(label='Book Author', validators=[DataRequired()])
    rating = FloatField(label='Book Rating', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class EditBooks(FlaskForm):
    rating = FloatField(label='Book Rating', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


@app.route('/')
def home():
    with app.app_context():
        all_books = db.session.query(Books).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = AddBoks()
    if form.validate_on_submit():
        with app.app_context():
            new_book = Books(title=form.bookName.data, author=form.bookAuthor.data,
                             rating=form.rating.data)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("add.html", form=form)


@app.route('/edits/<int:id>', methods=["POST", "GET"])
def edit_prg(id):
    book = db.session.get(Books, id)
    form = EditBooks()
    if form.validate_on_submit():
        with app.app_context():
            book_to_update = db.session.get(Books, id)
            book_to_update.rating = form.rating.data
            db.session.commit()
            return redirect(url_for('home'))
    else:
        print("none")

    return render_template("edits.html", book=book, form=form)

@app.route('/delete/<int:id>', methods=["POST", "GET"])
def delete(id):
    with app.app_context():
        book_to_delete = db.session.query(Books).get(id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
