
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField,PasswordField,RadioField, TextAreaField
from wtforms.validators import InputRequired, EqualTo


class FilterForm(FlaskForm): #Tuples in choices, (1,2) 1st is value of option, 2nd is the text that appears.
    options = [("album_name", "Album Name"), ("artist", "Artist Name"), ("release_year", "Release Year"), ("genre", "Genre"), ("user_id", "User ID")]
    filter_by = RadioField("Filter By", choices=options, default="album_name")
    search = StringField("Search", validators=[InputRequired()])
    submit = SubmitField("Search")
 
class RegistrationForm(FlaskForm):
    user_id = StringField("User id:",
        validators=[InputRequired()])
    password = PasswordField("Password:",
        validators=[InputRequired()])
    password2 = PasswordField("Repeat Password:",
        validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")   

class LoginForm(FlaskForm):
    user_id = StringField("User id:",
        validators=[InputRequired()])
    password = PasswordField("Password:",
        validators=[InputRequired()])
    submit = SubmitField("Submit")       

class EditProfileForm(FlaskForm):
    bio = StringField("Bio")
    submit = SubmitField("Save")


class RatingForm(FlaskForm): 
    rating = RadioField("Rate", choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")], validators=[InputRequired()] )
    review = TextAreaField("Review") 
    submit = SubmitField("Save")


class LikeForm(FlaskForm):
    like_dislike = RadioField("Like/Dislike: ", choices=["Like", "Dislike"])  
    submit = SubmitField("Save")  

class ReviewSortForm(FlaskForm):
    sort = SelectField("Sort by:", choices=["Most Liked", "Most Disliked", "Newest", "Oldest"]) 
    submit = SubmitField("Sort")
 
   