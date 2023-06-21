#Dylan Creedon
#122117537

# --------------------------------------------------------features----------------------------------------------------------------------------- #
# Create account
# Login
# Logout
# Search album/user using filters
# Search will give overview of album, but must be logged in to rate album and view user reviews. Also need to be logged in to view user profiles.
# Albums - user can rate and reviews albums (* You must rate if you're posting a review, but it is not necessary to post a review if you just want to rate). 
# Users can delete ratings/reviews too.
# Users can view other user reviews and sort by different parameters on the album page, such as most liked reviews, most disliked etc..(the album "Thriller" has been set up with liked and disliked reviews at different times if you want to test the sort function)
# User reviews can be liked or disliked, but not user ratings. Also users can't like/dislike their own reviews.
# Other user's profiles can be viewed to see all their opinions. You can also follow users, and view their followers and who they follow.
# Once following a user, recent ratings from those users will pop up on the index/Search page. (* A recent rating is a rating made within the last week)
# Users can create bios on their own profile pages. They can delete ratings and reviews too on their profile or on album pages.
#                                                       further notes #
# List of albums that can be searched on this demo site:
#   ('Thriller', 'Michael Jackson', 1982, 'Pop', 0,'Thriller_image.jpg' ),
#   ('Abbey Road', 'The Beatles', 1969, 'Rock', 0, 'Abbey_Road_image.jpg'),
#   ('Nevermind', 'Nirvana', 1991, 'Grunge',0,'Nevermind_image.jpg'),
#   ('Kind of Blue', 'Miles Davis', 1959, 'Jazz',0,'Kind_of_Blue_image.jpeg'),
#   ('Rumours', 'Fleetwood Mac', 1977, 'Rock', 0, 'Rumours_image.jpg'),
#   ('Franz Ferdinand', 'Franz Ferdinand', 2004, 'Indie Rock',0,'Franz_Ferdinand_image.jpg'),
#   ('Hot Fuss', 'The Killers', 2004, 'Indie Rock', 0,'Hot_Fuss_image.jpeg'),
#   ('American Idiot', 'Green Day', 2004, 'Pop Punk',0,'American_Idiot_image.jpeg'),
#   ('Demon Days', 'Gorillaz', 2005, 'Alternative',0,'Demon_Days_image.jpg'),
#   ('Currents', 'Tame Impala', 2015, 'Alternative',0,'Currents_image.jpg'),
#   ('More Life', 'Drake', 2017, 'Hip Hop', 0,'More_Life_image.jpg'),
#   ('Dawn FM', 'The Weeknd', 2022, 'Pop',0,'Dawn_FM_image.jpg'),
#   ('Gloria', 'Sam Smith', 2023, 'Pop',0,'Gloria_image.jpg');


# Test account - 
# UserID: Test
# Password: 1234

from flask import Flask, render_template, session, redirect, url_for, g, request, flash,get_flashed_messages
from flask_session import Session
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from forms import FilterForm, RegistrationForm, LoginForm, EditProfileForm, RatingForm, ReviewSortForm
from functools import wraps
import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.teardown_appcontext(close_db)


@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash('Please log in to access this feature') 
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view 


@app.route('/', methods=['GET', 'POST'])
def index():
     # check if the 'viewed_user_id' key is present in the session
    if 'viewed_user_id' in session:
        # remove the 'viewed_user_id' key from the session
        session.pop('viewed_user_id')
    db = get_db()
    form = FilterForm()
    filter_by = form.filter_by.data
    follow_news = None 

    if g.user: #This will check if user is logged in then show Followed news
        follow_news = db.execute("""SELECT reviews.rating, albums.album_name, followers.user_id, albums.album_id
                                    FROM reviews 
                                    JOIN followers ON reviews.user_id = followers.user_id
                                    JOIN albums ON reviews.album_id = albums.album_id
                                    WHERE followers.follower_id = ? AND DATETIME(reviews.date_added) >= DATETIME('now', '-7 days')
                                    ORDER BY reviews.date_added DESC
                                    LIMIT 20;""",(g.user,))
 
        
    
    if filter_by == "user_id": #if filtering by user_id it will search users table
        if form.validate_on_submit():

            # Retrieve form data and convert to lowercase
            search = form.search.data.lower()
            # LOWER() will ignore case sensitivity
            users = db.execute(f"""SELECT * FROM users 
                                WHERE LOWER({filter_by}) 
                                LIKE ? """, ('%' + search + '%',)).fetchall()
            
            

            return render_template('results.html', users=users, search=search)            
    
    else:    #search albums table
        if form.validate_on_submit():
            
            search = form.search.data.lower()
            albums = db.execute(f"""SELECT * FROM albums 
                                    WHERE LOWER({filter_by}) 
                                    LIKE ? ORDER BY album_name;""", ('%' + search + '%',)).fetchall()
            
            return render_template('results.html', albums=albums, search=search)
            

    return render_template('index.html', form=form, follow_news = follow_news)


@app.route("/register", methods=["GET", "POST"])   
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data  
        password2 = form.password2.data 
        db = get_db() 
        possible_clashing_user = db.execute("""SELECT * FROM users 
                        WHERE user_id = ?;""", (user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("User id already taken!")
        else:
            db.execute("""INSERT INTO users (user_id, password)
            VALUES (?, ?);""",
            (user_id, generate_password_hash(password)))   
            db.commit()
            return redirect( url_for("login")) 
    return render_template("register.html", form=form)        


@app.route("/login", methods=["GET", "POST"])   
def login():
    messages = get_flashed_messages()
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data  
        db = get_db() 
        possible_clashing_user = db.execute("""SELECT * FROM users 
                        WHERE user_id = ?;""", (user_id,)).fetchone()

        if possible_clashing_user is  None:
            form.user_id.errors.append("No such user")
        elif not check_password_hash(possible_clashing_user["password"], password):
            form.password.errors.append("Incorrect password!")    
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
                
            return redirect(next_page) 
    return render_template("login.html", form=form, messages = messages)     


@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index"))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    db = get_db()
    user_profile = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (g.user,)).fetchall()
    album_ratings = db.execute("""SELECT albums.album_name, reviews.rating, reviews.review, albums.album_id, albums.image_url,reviews.likes
                                FROM reviews, albums
                                WHERE reviews.user_id = ? and albums.album_id = reviews.album_id ;""", (g.user,)).fetchall()
    #Update bio
    if form.validate_on_submit():
        bio = form.bio.data
        db.execute("""UPDATE users 
                      SET bio = ? 
                      WHERE user_id = ?;""", (bio, g.user))
        db.commit()
        
        return redirect(url_for("profile"))
       
    return render_template("profile.html", form=form, user_profile = user_profile, album_ratings = album_ratings)
    
  
@app.route("/view_profile/<user_id>")
@login_required
def view_profile(user_id):
    if g.user == user_id:
        return redirect(url_for("profile")) #If someone is trying to view their own profile, send them to profile and not view_profile.
    session['viewed_user_id'] = user_id #adding the user_id that was inserted from the previous search into the function, into session.


        
    db = get_db()
    existing_follower = db.execute("""SELECT * 
                                    FROM followers 
                                    WHERE user_id = ? AND follower_id = ?;""",(user_id, g.user,)).fetchone()
    profile = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (user_id,)).fetchall()
    album_ratings = db.execute("""SELECT albums.album_name, reviews.rating, reviews.review, albums.album_id,reviews.review_id,reviews.likes,reviews.dislikes,albums.image_url
                                FROM reviews, albums
                                WHERE reviews.user_id = ? and albums.album_id = reviews.album_id ;""", (user_id,)).fetchall()

    return render_template("view_profile.html", profile = profile, album_ratings = album_ratings, existing_follower = existing_follower)

    
@app.route("/rating/<int:album_id>", methods = ['GET', 'POST'])
@login_required
def rating(album_id):
    form = RatingForm()
    db = get_db()
    viewed_user_id = session.get("viewed_user_id")
    

    album = db.execute("""SELECT * FROM albums
                         WHERE album_id = ?;""", (album_id,)).fetchall()
    user_check = db.execute("""SELECT * FROM reviews WHERE album_id = ? and user_id = ?;""", (album_id,g.user,)).fetchall()
    avg_rating = None 
    #Check if user has already made rating.
    if user_check:
        # Since SQL sets the "DEFAULT CURRENT_TIMESTAMP" when added, we need to get current date and set it when updating a review.
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if form.validate():
            rating = form.rating.data
            review = form.review.data
            # Update review and rating on user's profile
            db.execute("""UPDATE reviews 
                          SET rating = ?, review = ?, date_added = ?
                          WHERE user_id = ? AND album_id = ?;""",
                        (rating,review,current_date, g.user, album_id ))
            db.commit()
            # After updating the user's rating, get the average of all ratings with the same album_id and insert it back into the database
            avg_rating = db.execute("""SELECT AVG(rating) FROM reviews WHERE album_id = ?;""", (album_id,)).fetchone()[0]
            
           
            db.execute(f"""UPDATE albums 
                           SET avg_rating = {avg_rating} 
                           WHERE album_id = ? ;""",
                        ( album_id, ))
            db.commit()
            
            return redirect(url_for("rating",album_id=album_id))


    else:    # If user has not already made an opinion on the album, insert into database.
        if form.validate():
            rating = form.rating.data
            review = form.review.data

            db.execute("""INSERT INTO reviews (user_id, album_id, rating, review) 
                          VALUES (?, ?, ?, ?);""",
                        (g.user, album_id, rating, review))
            db.commit()
            
            avg_rating = db.execute("""SELECT AVG(rating) 
                                       FROM reviews 
                                       WHERE album_id = ?;""", (album_id,)).fetchone()[0]
            db.execute(f"""UPDATE albums 
                           SET avg_rating = {avg_rating} 
                           WHERE album_id = ?;""",
                         ( album_id, ))
            db.commit()

            return redirect(url_for("rating",album_id=album_id))
            
    return render_template("rating.html", form=form, album = album, user_check = user_check, viewed_user_id = viewed_user_id)
            

@app.route("/delete_rating/<int:album_id>", methods = ['GET', 'POST'])
@login_required
def delete_rating(album_id):
    db = get_db()
    # Delete 
    db.execute("""DELETE FROM reviews 
                  WHERE user_id = ? AND album_id = ?;""", (g.user, album_id,))
    db.commit()

    # Recalculate the average rating for the album.
    avg_rating = db.execute("""SELECT AVG(rating) 
                               FROM reviews 
                               WHERE album_id = ?;""", (album_id,)).fetchone()[0]
    # Update the avg_rating column in the albums table.
    db.execute("""UPDATE albums SET avg_rating = ? 
                  WHERE album_id = ?;""", (avg_rating, album_id))
    db.commit()

    return redirect(request.referrer or url_for('profile'))
    #request.referrer will return back to page being viewed, otherwise go to user's profile.
     
    

@app.route("/view_reviews/<album_id>", methods = ['GET', 'POST'])
def view_reviews(album_id):
    db = get_db()
    form = ReviewSortForm()
    sort = form.sort.data 
    reviews = db.execute("""SELECT * 
                            FROM reviews
                            WHERE album_id = ? AND review != '';""", (album_id, )).fetchall()
    
    #Sort by most liked
    if sort == "Most Liked":
        reviews = db.execute("""SELECT * 
                                FROM reviews 
                                WHERE album_id = ? AND review != ''
                                ORDER BY likes DESC;""", (album_id,)).fetchall()
        return render_template("reviews.html", reviews = reviews, form = form, album_id = album_id)
    #Sort by most disliked
    if sort == "Most Disliked":
        reviews = db.execute("""SELECT * 
                                FROM reviews 
                                WHERE album_id = ? AND review != ''
                                ORDER BY dislikes DESC;""", (album_id,)).fetchall() 
        return render_template("reviews.html", reviews = reviews, form = form, album_id = album_id)
    #Sort by most recently uploaded
    if sort == "Newest":
        reviews = db.execute("""SELECT * 
                                FROM reviews 
                                WHERE album_id = ? AND review != ''
                                ORDER BY date_added DESC;""", (album_id,)).fetchall() 
        return render_template("reviews.html", reviews = reviews, form = form, album_id = album_id)  
    #Sort by oldest date uploaded
    if sort == "Oldest":
        reviews = db.execute("""SELECT * 
                                FROM reviews 
                                WHERE album_id = ? AND review != ''
                                ORDER BY date_added;""", (album_id,)).fetchall() 
        return render_template("reviews.html", reviews = reviews, form = form, album_id = album_id)      

    return render_template("reviews.html", reviews = reviews, form = form, album_id = album_id )
    

@app.route("/like_review/<review_id>")
@login_required
def like_review(review_id):
    db = get_db()
    viewed_user_id = session.get("viewed_user_id")
    # Check if the user has already liked or disliked this review
    existing_like = db.execute("""SELECT * 
                                FROM likes_dislikes 
                                WHERE user_id = ? AND review_id = ?;""",
                                (g.user, review_id)).fetchone()

    if existing_like is None:
        # Add new like
        db.execute(
            """INSERT INTO likes_dislikes (user_id, review_id, like_or_dislike) 
               VALUES (?, ?, 'like')""",(g.user, review_id))
        db.execute("""UPDATE reviews 
                      SET likes = likes + 1 
                      WHERE review_id = ?;""", (review_id,))

    elif existing_like["like_or_dislike"] == "dislike":
        # Replace existing dislike with like
        db.execute("""UPDATE likes_dislikes 
                      SET like_or_dislike = 'like' 
                      WHERE like_dislike_id = ?;""",(existing_like["like_dislike_id"],)
        )
        db.execute("""UPDATE reviews 
                      SET likes = likes + 1, dislikes = dislikes - 1 
                      WHERE review_id = ?;""", (review_id,))

    else:
        # Remove the existing like
        db.execute("""DELETE FROM likes_dislikes 
                      WHERE like_dislike_id = ?;""", (existing_like["like_dislike_id"],))
        db.execute("""UPDATE reviews SET likes = likes - 1 WHERE review_id = ?;""", (review_id,))

    db.commit()

    return redirect(request.referrer or url_for("view_profile", user_id=viewed_user_id))
    # url_for("view_profile", user_id=viewed_user_id) the session "viewed_user_id" needs to passed to the "view_profile" function by adding user_id=viewed_user_id


@app.route("/dislike_review/<review_id>")
@login_required
def dislike_review(review_id):
    db = get_db()
    viewed_user_id = session.get("viewed_user_id")

    # Check if the user has already liked or disliked the review
    existing_like = db.execute("""SELECT * 
                                  FROM likes_dislikes 
                                  WHERE user_id = ? AND review_id = ?;""",(g.user, review_id) ).fetchone()

    if existing_like is None:
        # Add new dislike
        db.execute("""INSERT INTO likes_dislikes (user_id, review_id, like_or_dislike) 
                      VALUES (?, ?, 'dislike');""",
                    (g.user, review_id))
        db.execute("""UPDATE reviews 
                      SET dislikes = dislikes + 1 
                      WHERE review_id = ?;""", (review_id,))

    elif existing_like["like_or_dislike"] == "like":
        # Replace existing like with dislike
        db.execute("""UPDATE likes_dislikes 
                      SET like_or_dislike = 'dislike' 
                      WHERE like_dislike_id = ?;""",(existing_like["like_dislike_id"],) )
        db.execute("""UPDATE reviews 
                      SET dislikes = dislikes + 1, likes = likes - 1 
                      WHERE review_id = ?;""", (review_id,))

    else:
        # Remove the existing dislike
        db.execute("""DELETE FROM likes_dislikes 
                      WHERE like_dislike_id = ?;""", (existing_like["like_dislike_id"],))
        db.execute("""UPDATE reviews 
                      SET dislikes = dislikes - 1 
                      WHERE review_id = ?;""", (review_id,))

    db.commit()

    return redirect(request.referrer or url_for("view_profile", user_id=viewed_user_id))


@app.route("/follow/<user_id>")
@login_required
def follow(user_id):
    db = get_db()
    # Check if already following
    existing_follower = db.execute("""SELECT * 
                                    FROM followers 
                                    WHERE user_id = ? AND follower_id = ?;""",(user_id, g.user,)).fetchone()

    if existing_follower is None:
        # Follow
        db.execute("""INSERT INTO followers (user_id, follower_id) 
                      VALUES (?, ?)""",(user_id, g.user))
        db.execute("""UPDATE users 
                      SET followers_amount = followers_amount + 1 
                      WHERE user_id = ?;""", (user_id,))
        db.execute("""UPDATE users 
                      SET following_amount = following_amount + 1 
                      WHERE user_id = ?""", (g.user,))

    else:
        # Unfollow
        db.execute("""DELETE FROM followers 
                      WHERE user_id = ?;""", (user_id,))
        db.execute("""UPDATE users 
                      SET followers_amount = followers_amount - 1 
                      WHERE user_id = ?;""", (user_id,))
        db.execute("""UPDATE users 
                      SET following_amount = following_amount - 1 
                      WHERE user_id = ?;""", (g.user,))

    db.commit()

    return redirect(url_for("view_profile", user_id=user_id, existing_follower = existing_follower))
    
    
@app.route("/view_followers/<user_id>")
def view_followers(user_id):
    db = get_db()

    follower_data = db.execute("""SELECT follower_id 
                                  FROM followers 
                                  WHERE user_id = ?;""",(user_id,)).fetchall()
    following_data = db.execute("""SELECT user_id 
                                   FROM followers 
                                   WHERE follower_id = ?;""",(user_id,)).fetchall()
    
    return render_template("followers.html", follower_data = follower_data, following_data = following_data, user_id = user_id)

