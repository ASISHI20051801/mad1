from flask import Flask, request, render_template, redirect, url_for
from database import *
from database import db  # Ensure db is imported
from werkzeug.security import generate_password_hash
from datetime import datetime





app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'

db.init_app(app)

active_user=None
active=None
home=None
profile=None

with app.app_context():
    db.create_all()

###################################################################################################################################################################################################################################

@app.route("/", methods=["GET", "POST"])
def root():
    return render_template("root.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


###################################################################################################################################################################################################################################
@app.route("/admin",methods=["GET"])
def admin():
    return render_template("admin.html")
###################################################################################################################################################################################################################################


@app.route("/register", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dateofbirth = request.form.get("dateofbirth")
        gender = request.form.get("gender")
        bio = request.form.get("bio")
        email = request.form.get('email')
        phone = request.form.get('phone')
        alternate_phone = request.form.get('alternate_phone')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if password and confirm_password match
        if password != confirm_password:
            error_message = "Passwords do not match. Please re-enter."
            return render_template("user.html", error_message=error_message)

        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            error_message = "Email already exists. Please try again."
            return render_template("user.html", error_message=error_message)


        # Create a new user object
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            dateofbirth=dateofbirth,
            gender=gender,
            bio=bio,
            email=email,
            phone=phone,
            alternate_phone=alternate_phone,
            address=address,
            pincode=pincode,
            city=city,
            country=country,
            state=state,
            password=password,
            confirm_password=confirm_password  # Save the hashed password
        )

        # Add new user to the database session
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful registration
        return redirect(url_for("login"))  # Assuming the login route is named "login"

    return render_template("user.html")


# ###################################################################################################################################################################################################################################



# @app.route("/sponsor", methods=["GET", "POST"])
# def sponsor():
#     if request.method == "POST":
#         firstname = request.form.get("firstname")
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         address = request.form.get('address')
#         pin = request.form.get('pin')
#         state = request.form.get('state')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm_password')

#         # Check if password and confirm_password match
#         if password != confirm_password:
#             error_message = "Passwords do not match. Please re-enter."
#             return render_template("sponsor.html", error_message=error_message)

#         # Check if email already exists
#         existing_email = Sponsor_create_account.query.filter_by(email=email).first()
#         if existing_email:
#             error_message = "Email already exists. Please try again."
#             return render_template("sponsor.html", error_message=error_message)

#         # Hash the password before saving it


#         # Create a new Sponsor_create_account object
#         new_sponsor = Sponsor_create_account(
#             firstname=firstname,
#             email=email,
#             phone=phone,
#             address=address,
#             pincode=pin,
#             state=state,
#             password=password,
#             confirm_password=confirm_password
#         )

#         # Add new sponsor to the database session
#         db.session.add(new_sponsor)
#         db.session.commit()

#         return redirect(url_for('login'))  # Redirect to login page after successful registration

#     return render_template("sponsor.html")


# ####################################################################################################################################################################################################################################
# @app.route("/about", methods=["GET", "POST"])
# def ab():
#     if request.method == "POST":
#         # You can process the form data or handle POST-specific logic here
#         # For now, it just renders the about page
#         return render_template("about.html")
#     else:
#         # Render the about page for GET request
#         return render_template("about.html")


# @app.route("/steps", methods=["GET", "POST"])
# def ste():
#     if request.method == "POST":
#         # You can process the form data or handle POST-specific logic here
#         # For now, it just renders the about page
#         return render_template("steps.html")
#     else:
#         # Render the about page for GET request
#         return render_template("steps.html")
# ####################################################################################################################################################################################################################################


@app.route("/user_login", methods=["POST"])
def dash():
    global active_user
    global active
    global home

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            active_user = user.id
            home = user.id
            return render_template("user_dashboard.html", name=user.first_name, email=user.email)

        # If no account matches, render the login page again
        return render_template("in_login.html")

    # Default case if it's not a POST request
    return render_template("login.html")


############################################################################################################################################################################################################################################

@app.route("/admin_login", methods=["POST"])
def admin_login():
    global active_user
    global active
    global home

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.password == password:
            active_user = admin.id
            home = admin.id
            return render_template("admin_dashboard.html")

        # If no account matches, render the login page again
        return render_template("in_login.html")

    # Default case if it's not a POST request
    return render_template("admin.html")

# ###################################################################################################################################################################################################################################
# @app.route("/home_influencer")
# def home_influencer():
#     global home
#     inf=Influencers_create_account.query.get(home)
#     return render_template("influencerdashboard.html",name=inf.companyname, email=inf.email)


# # @app.route("/home_influencer_to_logout")
# # def home_influencer():
# #     global home
# #     inf=Influencers_create_account.query.get(home)
# #     return render_template("logout.html",name=inf.companyname, email=inf.email)



# @app.route("/home_sponsor")
# def home_sponsor():
#     global home
#     sp=Sponsor_create_account.query.get(home)
#     return render_template("sponsordashboard.html",name=sp.firstname, email=sp.email)


@app.route("/profile" , methods=["GET", "POST"])
def profile_one():
    global profile
    return render_template("user_profile.html",user=profile)


# @app.route("/home_influencer_search_to_dashboard")
# def home_influencer_search_to_dashboard():
#     global profile
#     return render_template("influencerdashboard.html",name=profile.name,email=profile.email)





# @app.route("/home_sponsor_search_to_profile")
# def home_sponsor_search_to_profile():
#     global profile
#     return render_template("profilesponsor.html",company_name=profile.company_name, bio=profile.bio, email=profile.email, industry=profile.industry, password=profile.password, username=profile.username, name=profile.username)


# @app.route("/home_sponsor_search_to_dashboard")
# def home_sponsor_search_to_dashboard():
#     global profile
#     return render_template("sponsordashboard.html",name=profile.company_name,email=profile.email)



# ###################################################################################################################################################################################################################################




@app.route("/profile",methods=["GET","POST"])
def profile():
    global active_user, profile
    x= User.query.get(active_user)
    profile= User.query.get(active_user)
    if request.method=="POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dateofbirth = request.form.get("dateofbirth")
        gender = request.form.get("gender")
        bio = request.form.get("bio")
        email = request.form.get('email')
        phone = request.form.get('phone')
        alternate_phone = request.form.get('alternate_phone')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        

       
        x.name=name
        x.username=username
        x.email=email
        x.niche=niche
        x.reach=reach
        x.bio=bio
        x.password=password
        x.category=category

        db.session.commit()

        return render_template("profileinfluencer.html",name=name,bio=bio,email=email,category=category,password=password,username=username,reach=reach,niche=niche)

    name=x.name
    email=x.email
    category=x.category
    bio=x.bio
    reach=x.reach
    niche=x.niche
    username=x.username
    password=x.password
    return render_template("profileinfluencer.html",name=name,reach=reach,niche=niche,bio=bio,email=email,category=category,password=password,username=username)



# ###################################################################################################################################################################################################################################








# ####################################################################################################################################################################################################################################

# @app.route("/profile_of_sponsor", methods=["GET", "POST"])
# def profile_sponsor():
#     global active_user, profile
#     y = Sponsor_create_account.query.get(active_user)
#     profile = Sponsor_create_account.query.get(active_user)
#     if request.method == "POST":
#         company_name = request.form.get("company_name")
#         username = request.form.get("username")
#         email = request.form.get("email")
#         password = request.form.get("password")
#         bio = request.form.get("bio")
#         industry = request.form.get("industry")

#         y.company_name = company_name
#         y.username = username
#         y.email = email
#         y.password = password
#         y.bio = bio
#         y.industry = industry

#         db.session.commit()

#         return render_template("profilesponsor.html", company_name=company_name, bio=bio, email=email, industry=industry, password=password, username=username, name=username)

#     usernam = y.username
#     company_name = y.company_name
#     industry = y.industry
#     email = y.email
#     bio = y.bio
#     password = y.password

#     return render_template("profilesponsor.html", company_name=company_name, industry=industry, email=email, bio=bio, name=company_name, password=password, username=usernam)



# ###################################################################################################################################################################################################################################
# @app.route("/logout")
# def logout():
#     # Clear all global variables
#     global active_user, active, home, profile
#     active_user = None
#     active = None
#     home = None
#     profile = None
    
#     # Redirect to login page
#     return redirect(url_for('login'))

# # If you want to show a logout confirmation page instead:
# @app.route("/logout_confirmation")
# def logout_confirmation():
#     # Clear all global variables
#     global active_user, active, home, profile
#     active_user = None
#     active = None
#     home = None
#     profile = None
    
#     return render_template("logout.html")


###################################################################################################################################################################################################################################



if __name__ == "__main__":
    app.run(debug=True,port=8000)






