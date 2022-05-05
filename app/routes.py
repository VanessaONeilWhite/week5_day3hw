from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm, LoginForm, RegisterForm
from app import app 
from .models import User 
from flask_login import current_user, logout_user, login_user, login_required

#routes 
@app.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        #do poke stuff
        poke = form.pokename.data
        url = f"https://pokeapi.co/api/v2/pokemon/{poke}"
        
        response = requests.get(url)
        if response.ok:
            poke = response.json()
            poke_dict={
                "poke_name":poke['name'],
                "attack_base_stat":poke ["stats"][1]["base_stat"],
                "hp_base_stat": poke["stats"][0]["base_stat"],
                "defense_base_stat": poke["stats"][2]["base_stat"],
                "front_shiny": poke["sprites"]["front_shiny"],
                "ability_name": poke["abilities"][0]["ability"]["name"],
                "base_experience": poke["base_experience"],
            }
        else:
            return "Please enter a valid Pokemon"
        
        return render_template('pokemon.html.j2', poke=poke_dict, form=form)
        
    return render_template('pokemon.html.j2', form=form)   

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email=form.email.data.lower() 
        password=form.password.data

        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash("Welcome to Pokebook, let's battle!", 'success')
            return redirect(url_for('index'))
        flash('Incorrect Email Password Combo', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template('login.html.j2', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm() 
    if request.method == 'POST' and form.validate_on_submit():
        try: 
            new_user_data={
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            new_user_object =User() 
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        
        except:
            flash("There was an unexpected Error creating your account, Please try again later", "danger")
            return render_template('register.html.j2', form=form)
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('login'))
