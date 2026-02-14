import os
from flask import Flask, render_template, request, session, redirect, url_for
import datetime
import pymysql
import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'language_learning_key_2026'


def get_server_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        cursorclass=pymysql.cursors.DictCursor
    )

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="flask",
        cursorclass=pymysql.cursors.DictCursor
    )

def setup_database():
    conn = get_server_connection()
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS flask")
    cursor.execute("USE flask")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()



#Provimet
EXAMS_DATA = {
    # JAVA 1: Alfabeti, Numrat, Ngjyrat, Kafshët
    "1": [
        {"q": {"sq": "Një", "en": "One", "de": "Eins"}, "options": [{"sq": "Një", "en": "One", "de": "Eins"}, {"sq": "Dy", "en": "Two", "de": "Zwei"}, {"sq": "Tri", "en": "Three", "de": "Drei"}], "a": "Një"},
        {"q": {"sq": "Qen", "en": "Dog", "de": "Hund"}, "options": [{"sq": "Qen", "en": "Dog", "de": "Hund"}, {"sq": "Mace", "en": "Cat", "de": "Katze"}, {"sq": "Luan", "en": "Lion", "de": "Löwe"}], "a": "Qen"},
        {"q": {"sq": "E kuqe", "en": "Red", "de": "Rot"}, "options": [{"sq": "E kuqe", "en": "Red", "de": "Rot"}, {"sq": "E kaltër", "en": "Blue", "de": "Blau"}, {"sq": "E verdhë", "en": "Yellow", "de": "Gelb"}], "a": "E kuqe"},
        {"q": {"sq": "Mace", "en": "Cat", "de": "Katze"}, "options": [{"sq": "Mace", "en": "Cat", "de": "Katze"}, {"sq": "Qen", "en": "Dog", "de": "Hund"}, {"sq": "Lepur", "en": "Rabbit", "de": "Hase"}], "a": "Mace"},
        {"q": {"sq": "Dhjetë", "en": "Ten", "de": "Zehn"}, "options": [{"sq": "Dhjetë", "en": "Ten", "de": "Zehn"}, {"sq": "Nëntë", "en": "Nine", "de": "Neun"}, {"sq": "Tetë", "en": "Eight", "de": "Acht"}], "a": "Dhjetë"},
        {"q": {"sq": "E kaltër", "en": "Blue", "de": "Blau"}, "options": [{"sq": "E kaltër", "en": "Blue", "de": "Blau"}, {"sq": "E gjelbër", "en": "Green", "de": "Grün"}, {"sq": "E zezë", "en": "Black", "de": "Schwarz"}], "a": "E kaltër"},
        {"q": {"sq": "Pesë", "en": "Five", "de": "Fünf"}, "options": [{"sq": "Pesë", "en": "Five", "de": "Fünf"}, {"sq": "Gjashtë", "en": "Six", "de": "Sechs"}, {"sq": "Katër", "en": "Four", "de": "Vier"}], "a": "Pesë"},
        {"q": {"sq": "Luan", "en": "Lion", "de": "Löwe"}, "options": [{"sq": "Luan", "en": "Lion", "de": "Löwe"}, {"sq": "Ujk", "en": "Wolf", "de": "Wolf"}, {"sq": "Ari", "en": "Bear", "de": "Bär"}], "a": "Luan"},
        {"q": {"sq": "E verdhë", "en": "Yellow", "de": "Gelb"}, "options": [{"sq": "E verdhë", "en": "Yellow", "de": "Gelb"}, {"sq": "E kuqe", "en": "Red", "de": "Rot"}, {"sq": "E bardhë", "en": "White", "de": "Weiß"}], "a": "E verdhë"},
        {"q": {"sq": "A", "en": "A", "de": "A"}, "options": [{"sq": "A", "en": "A", "de": "A"}, {"sq": "B", "en": "B", "de": "B"}, {"sq": "C", "en": "C", "de": "C"}], "a": "A"}
    ],

    # JAVA 2: Ushqimet, Pijet, Sweets, Frutat, Perimet
    "2": [
        {"q": {"sq": "Bukë", "en": "Bread", "de": "Brot"}, "options": [{"sq": "Bukë", "en": "Bread", "de": "Brot"}, {"sq": "Mish", "en": "Meat", "de": "Fleisch"}, {"sq": "Vezë", "en": "Egg", "de": "Ei"}], "a": "Bukë"},
        {"q": {"sq": "Ujë", "en": "Water", "de": "Wasser"}, "options": [{"sq": "Ujë", "en": "Water", "de": "Wasser"}, {"sq": "Kafe", "en": "Coffee", "de": "Kaffee"}, {"sq": "Çaj", "en": "Tea", "de": "Tee"}], "a": "Ujë"},
        {"q": {"sq": "Mollë", "en": "Apple", "de": "Apfel"}, "options": [{"sq": "Mollë", "en": "Apple", "de": "Apfel"}, {"sq": "Dardhë", "en": "Pear", "de": "Birne"}, {"sq": "Pjeshkë", "en": "Peach", "de": "Pfirsich"}], "a": "Mollë"},
        {"q": {"sq": "Patate", "en": "Potato", "de": "Kartoffel"}, "options": [{"sq": "Patate", "en": "Potato", "de": "Kartoffel"}, {"sq": "Karotë", "en": "Carrot", "de": "Karotte"}, {"sq": "Qepë", "en": "Onion", "de": "Zwiebel"}], "a": "Patate"},
        {"q": {"sq": "Kafe", "en": "Coffee", "de": "Kaffee"}, "options": [{"sq": "Kafe", "en": "Coffee", "de": "Kaffee"}, {"sq": "Ujë", "en": "Water", "de": "Wasser"}, {"sq": "Lëng", "en": "Juice", "de": "Saft"}], "a": "Kafe"},
        {"q": {"sq": "Mish", "en": "Meat", "de": "Fleisch"}, "options": [{"sq": "Mish", "en": "Meat", "de": "Fleisch"}, {"sq": "Peshk", "en": "Fish", "de": "Fisch"}, {"sq": "Pula", "en": "Chicken", "de": "Hähnchen"}], "a": "Mish"},
        {"q": {"sq": "Çokollatë", "en": "Chocolate", "de": "Schokolade"}, "options": [{"sq": "Çokollatë", "en": "Chocolate", "de": "Schokolade"}, {"sq": "Akullore", "en": "Ice cream", "de": "Eis"}, {"sq": "Tortë", "en": "Cake", "de": "Kuchen"}], "a": "Çokollatë"},
        {"q": {"sq": "E hënë", "en": "Monday", "de": "Montag"}, "options": [{"sq": "E hënë", "en": "Monday", "de": "Montag"}, {"sq": "E martë", "en": "Tuesday", "de": "Dienstag"}, {"sq": "E diel", "en": "Sunday", "de": "Sonntag"}], "a": "E hënë"},
        {"q": {"sq": "Verë", "en": "Summer", "de": "Sommer"}, "options": [{"sq": "Verë", "en": "Summer", "de": "Sommer"}, {"sq": "Dimër", "en": "Winter", "de": "Winter"}, {"sq": "Pranverë", "en": "Spring", "de": "Frühling"}], "a": "Verë"},
        {"q": {"sq": "Domate", "en": "Tomato", "de": "Tomate"}, "options": [{"sq": "Domate", "en": "Tomato", "de": "Tomate"}, {"sq": "Spec", "en": "Pepper", "de": "Paprika"}, {"sq": "Sallatë", "en": "Lettuce", "de": "Salat"}], "a": "Domate"}
    ],

    # JAVA 3: People, Body parts, Clothing, Emotions, Professions, Sports
    "3": [
        {"q": {"sq": "Njeri", "en": "Person", "de": "Mensch"}, "options": [{"sq": "Njeri", "en": "Person", "de": "Mensch"}, {"sq": "Burrë", "en": "Man", "de": "Mann"}, {"sq": "Grua", "en": "Woman", "de": "Frau"}], "a": "Njeri"},
        {"q": {"sq": "Koka", "en": "Head", "de": "Kopf"}, "options": [{"sq": "Koka", "en": "Head", "de": "Kopf"}, {"sq": "Syri", "en": "Eye", "de": "Auge"}, {"sq": "Dora", "en": "Hand", "de": "Hand"}], "a": "Koka"},
        {"q": {"sq": "I lumtur", "en": "Happy", "de": "Glücklich"}, "options": [{"sq": "I lumtur", "en": "Happy", "de": "Glücklich"}, {"sq": "I mërzitur", "en": "Sad", "de": "Traurig"}, {"sq": "I lodhur", "en": "Tired", "de": "Müde"}], "a": "I lumtur"},
        {"q": {"sq": "Mjek", "en": "Doctor", "de": "Arzt"}, "options": [{"sq": "Mjek", "en": "Doctor", "de": "Arzt"}, {"sq": "Mësues", "en": "Teacher", "de": "Lehrer"}, {"sq": "Polic", "en": "Policeman", "de": "Polizist"}], "a": "Mjek"},
        {"q": {"sq": "Futboll", "en": "Football", "de": "Fußball"}, "options": [{"sq": "Futboll", "en": "Football", "de": "Fußball"}, {"sq": "Tenis", "en": "Tennis", "de": "Tennis"}, {"sq": "Not", "en": "Swimming", "de": "Schwimmen"}], "a": "Futboll"},
        {"q": {"sq": "Këmisha", "en": "Shirt", "de": "Hemd"}, "options": [{"sq": "Këmisha", "en": "Shirt", "de": "Hemd"}, {"sq": "Pantallona", "en": "Pants", "de": "Hose"}, {"sq": "Kapele", "en": "Hat", "de": "Hut"}], "a": "Këmisha"},
        {"q": {"sq": "Nëna", "en": "Mother", "de": "Mutter"}, "options": [{"sq": "Nëna", "en": "Mother", "de": "Mutter"}, {"sq": "Babai", "en": "Father", "de": "Vater"}, {"sq": "Motra", "en": "Sister", "de": "Schwester"}], "a": "Nëna"},
        {"q": {"sq": "Dora", "en": "Hand", "de": "Hand"}, "options": [{"sq": "Dora", "en": "Hand", "de": "Hand"}, {"sq": "Këmba", "en": "Leg", "de": "Bein"}, {"sq": "Veshi", "en": "Ear", "de": "Ohr"}], "a": "Dora"},
        {"q": {"sq": "I mërzitur", "en": "Sad", "de": "Traurig"}, "options": [{"sq": "I mërzitur", "en": "Sad", "de": "Traurig"}, {"sq": "I lumtur", "en": "Happy", "de": "Glücklich"}, {"sq": "I zemëruar", "en": "Angry", "de": "Wütend"}], "a": "I mërzitur"},
        {"q": {"sq": "Goja", "en": "Mouth", "de": "Mund"}, "options": [{"sq": "Goja", "en": "Mouth", "de": "Mund"}, {"sq": "Hunda", "en": "Nose", "de": "Nase"}, {"sq": "Syri", "en": "Eye", "de": "Auge"}], "a": "Goja"}
    ]
}

@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except:
            message = "Ky username ekziston ❌"

    return render_template('register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Këtu po e ruajmë me emrin 'username'
            session['username'] = user['username'] 
            return redirect(url_for('index'))
        else:
            message = "Username ose password gabim ❌"
    return render_template('login.html', message=message)

@app.route('/index')
def index():
    # DUHET TË JETË 'username', jo 'user_id'
    if 'username' not in session: 
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear() # Fshin të gjitha të dhënat (user_id, lang, etj.)
    return redirect(url_for('login'))


@app.route('/set_language', methods=['POST'])
def set_language():
    # Merr të dhënat nga forma e Settings (dropdown)
    my_lang = request.form.get('my_lang')
    learn_lang = request.form.get('learn_lang')
    
    if my_lang:
        session['my_lang'] = my_lang
    if learn_lang:
        session['learn_lang'] = learn_lang
        
    return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))

    # 1. Marrim rezultatet nga session (nëse nuk ka, është dict bosh)
    scores = session.get('scores', {})
    exams_finished = len(scores) # Sa provime janë kryer (0, 1, 2 ose 3)

    passed_count = 0
    failed_count = 0
    
    # 2. Shikojmë sa provime janë kaluar (pikët 3 e lart)
    for exam_id, score in scores.items():
        if score >= 3: 
            passed_count += 1
        else:
            failed_count += 1

    # 3. LLOGARITJA E PËRQINDJEVE
    # Progress Bar: 1 test = 33%, 2 = 66%, 3 = 100%
    total_percent = int((exams_finished / 3) * 100) if exams_finished > 0 else 0
    
    # Statistikat e vogla poshtë vijës
    p_passed = int((passed_count / exams_finished) * 100) if exams_finished > 0 else 0
    p_failed = int((failed_count / exams_finished) * 100) if exams_finished > 0 else 0

    # 4. Hapja e provimeve (Lock/Unlock)
    unlocked = {
        "1": True,
        "2": scores.get("1", 0) >= 3,
        "3": scores.get("2", 0) >= 3
    }

    # I dërgojmë vlerat reale te HTML
    return render_template('homepage.html', 
                           total_percent=total_percent, 
                           exams_finished=exams_finished,
                           passed_count=passed_count, 
                           failed_count=failed_count,
                           p_passed=p_passed, 
                           p_failed=p_failed, 
                           unlocked=unlocked)

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    exam_id = str(data.get('exam_id'))
    score = int(data.get('score')) 
    if 'scores' not in session: session['scores'] = {}
    s = session['scores']
    s[exam_id] = score
    session['scores'] = s
    session.modified = True
    return {"status": "success"}

@app.route('/certificate_form')
def certificate_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Marrim rezultatet për të 3 javët
    cursor.execute("SELECT exam_id, score FROM scores WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    
    # Llogarisim totalin e pikëve dhe totalin e mundshëm
    total_score = 0
    exams_count = 0
    
    # Këtu duhet të dish sa pyetje ka pasur çdo provim (supozojmë 4 për çdo javë)
    questions_per_exam = 4 
    
    for row in results:
        total_score += row['score']
        exams_count += 1
    
    # Llogaritja e përqindjes totale (Average)
    if exams_count > 0:
        total_possible = exams_count * questions_per_exam
        overall_percent = Math.round((total_score / total_possible) * 100)
    else:
        overall_percent = 0

    cursor.close()
    conn.close()

    return render_template('certificate_form.html', percent=overall_percent)

@app.route('/certificate', methods=['GET', 'POST'])
def certificate():
    # Merri pikët nga sesioni
    scores = session.get('scores', {})
    score_3 = scores.get('3', 0)
    
    # Supozojmë se testi 3 ka 5 pyetje
    percent = int((score_3 / 10) * 100) 

    if request.method == 'POST':
        user_data = {
            "emri": request.form.get('emri'),
            "mbiemri": request.form.get('mbiemri'),
            "datelindja": request.form.get('datelindja'),
            "data_sot": request.form.get('data_sot'),
            "percent": f"{percent}%"
        }
        return render_template('certificate_view.html', user=user_data)
    
    return render_template('certificate_form.html', percent=percent)

@app.route('/first_week')
def first_week():

    # Struktura me tri gjuhët
    data = {
        "Alfabeti": [
            {"sq": "A", "en": "A", "de": "A"},
            {"sq": "B", "en": "B", "de": "B"},
            {"sq": "C", "en": "C", "de": "C"},
            {"sq": "Ç", "en": "-", "de": "-"},
            {"sq": "D", "en": "D", "de": "D"},
            {"sq": "DH", "en": "-", "de": "-"},
            {"sq": "E", "en": "E", "de": "E"},
            {"sq": "Ë", "en": "-", "de": "-"},
            {"sq": "F", "en": "F", "de": "F"},
            {"sq": "G", "en": "G", "de": "G"},
            {"sq": "GJ", "en": "-", "de": "-"},
            {"sq": "H", "en": "H", "de": "H"},
            {"sq": "I", "en": "I", "de": "I"},
            {"sq": "J", "en": "J", "de": "J"},
            {"sq": "K", "en": "K", "de": "K"},
            {"sq": "L", "en": "L", "de": "L"},
            {"sq": "LL", "en": "-", "de": "-"},
            {"sq": "M", "en": "M", "de": "M"},
            {"sq": "N", "en": "N", "de": "N"},
            {"sq": "NJ", "en": "-", "de": "-"},
            {"sq": "O", "en": "O", "de": "O"},
            {"sq": "P", "en": "P", "de": "P"},
            {"sq": "Q", "en": "Q", "de": "Q"},
            {"sq": "R", "en": "R", "de": "R"},
            {"sq": "RR", "en": "-", "de": "-"},
            {"sq": "S", "en": "S", "de": "S"},
            {"sq": "SH", "en": "-", "de": "-"},
            {"sq": "T", "en": "T", "de": "T"},
            {"sq": "TH", "en": "-", "de": "-"},
            {"sq": "U", "en": "U", "de": "U"},
            {"sq": "V", "en": "V", "de": "V"},
            
            # W nga gjuha angleze dhe gjermaane
            {"sq": "-", "en": "W", "de": "W"},
            
            {"sq": "X", "en": "X", "de": "X"},
            {"sq": "XH", "en": "-", "de": "-"},
            {"sq": "Y", "en": "Y", "de": "Y"},
            {"sq": "Z", "en": "Z", "de": "Z"},
            {"sq": "ZH", "en": "-", "de": "-"},

            # Shkronjat gjermane me UMLAUTS
            {"sq": "-", "en": "-", "de": "Ä"},
            {"sq": "-", "en": "-", "de": "Ö"},
            {"sq": "-", "en": "-", "de": "Ü"},
            {"sq": "-", "en": "-", "de": "ß"}
        ],

        "Numrat": [
            {"sq": "Një", "en": "One", "de": "Eins", "digit": "1"},
            {"sq": "Dy", "en": "Two", "de": "Zwei", "digit": "2"},
            {"sq": "Tri", "en": "Three", "de": "Drei", "digit": "3"},
            {"sq": "Katër", "en": "Four", "de": "Vier", "digit": "4"},
            {"sq": "Pesë", "en": "Five", "de": "Fünf", "digit": "5"},
            {"sq": "Gjashtë", "en": "Six", "de": "Sechs", "digit": "6"},
            {"sq": "Shtatë", "en": "Seven", "de": "Sieben", "digit": "7"},
            {"sq": "Tetë", "en": "Eight", "de": "Acht", "digit": "8"},
            {"sq": "Nëntë", "en": "Nine", "de": "Neun", "digit": "9"},
            {"sq": "Dhjetë", "en": "Ten", "de": "Zehn", "digit": "10"},
            {"sq": "Njëmbëdhjetë", "en": "Eleven", "de": "Elf", "digit": "11"},
            {"sq": "Dymbëdhjetë", "en": "Twelve", "de": "Zwölf", "digit": "12"},
            {"sq": "Trembëdhjetë", "en": "Thirteen", "de": "Dreizehn", "digit": "13"},
            {"sq": "Katërmbëdhjetë", "en": "Fourteen", "de": "Vierzehn", "digit": "14"},
            {"sq": "Pesëmbëdhjetë", "en": "Fifteen", "de": "Fünfzehn", "digit": "15"},
            {"sq": "Gjashtëmbëdhjetë", "en": "Sixteen", "de": "Sechzehn", "digit": "16"},
            {"sq": "Shtatëmbëdhjetë", "en": "Seventeen", "de": "Siebzehn", "digit": "17"},
            {"sq": "Tetëmbëdhjetë", "en": "Eighteen", "de": "Achtzehn", "digit": "18"},
            {"sq": "Nëntëmbëdhjetë", "en": "Nineteen", "de": "Neunzehn", "digit": "19"},
            {"sq": "Njëzet", "en": "Twenty", "de": "Zwanzig", "digit": "20"},
            {"sq": "Njëzet e një", "en": "Twenty-one", "de": "Einundzwanzig", "digit": "21"},
            {"sq": "Njëzet e dy", "en": "Twenty-two", "de": "Zweiundzwanzig", "digit": "22"},
            {"sq": "Njëzet e tri", "en": "Twenty-three", "de": "Dreiundzwanzig", "digit": "23"},
            {"sq": "Njëzet e katër", "en": "Twenty-four", "de": "Vierundzwanzig", "digit": "24"},
            {"sq": "Njëzet e pesë", "en": "Twenty-five", "de": "Fünfundzwanzig", "digit": "25"},
            {"sq": "Njëzet e gjashtë", "en": "Twenty-six", "de": "Sechsundzwanzig", "digit": "26"},
            {"sq": "Njëzet e shtatë", "en": "Twenty-seven", "de": "Siebenundzwanzig", "digit": "27"},
            {"sq": "Njëzet e tetë", "en": "Twenty-eight", "de": "Achtundzwanzig", "digit": "28"},
            {"sq": "Njëzet e nëntë", "en": "Twenty-nine", "de": "Neunundzwanzig", "digit": "29"},
            {"sq": "Tridhjetë", "en": "Thirty", "de": "Dreißig", "digit": "30"},
            {"sq": "Tridhjetë e një", "en": "Thirty-one", "de": "Einunddreißig", "digit": "31"},
            {"sq": "Tridhjetë e dy", "en": "Thirty-two", "de": "Zweiunddreißig", "digit": "32"},
            {"sq": "Tridhjetë e tri", "en": "Thirty-three", "de": "Dreiunddreißig", "digit": "33"},
            {"sq": "Tridhjetë e katër", "en": "Thirty-four", "de": "Vierunddreißig", "digit": "34"},
            {"sq": "Tridhjetë e pesë", "en": "Thirty-five", "de": "Fünfunddreißig", "digit": "35"},
            {"sq": "Tridhjetë e gjashtë", "en": "Thirty-six", "de": "Sechsounddreißig", "digit": "36"},
            {"sq": "Tridhjetë e shtatë", "en": "Thirty-seven", "de": "Siebenunddreißig", "digit": "37"},
            {"sq": "Tridhjetë e tetë", "en": "Thirty-eight", "de": "Achtunddreißig", "digit": "38"},
            {"sq": "Tridhjetë e nëntë", "en": "Thirty-nine", "de": "Neununddreißig", "digit": "39"},
            {"sq": "Dyzet", "en": "Forty", "de": "Vierzig", "digit": "40"},
            {"sq": "Dyzet e një", "en": "Forty-one", "de": "Einundvierzig", "digit": "41"},
            {"sq": "Dyzet e dy", "en": "Forty-two", "de": "Zweiundvierzig", "digit": "42"},
            {"sq": "Dyzet e tri", "en": "Forty-three", "de": "Dreiundvierzig", "digit": "43"},
            {"sq": "Dyzet e katër", "en": "Forty-four", "de": "Vierundvierzig", "digit": "44"},
            {"sq": "Dyzet e pesë", "en": "Forty-five", "de": "Fünfundvierzig", "digit": "45"},
            {"sq": "Dyzet e gjashtë", "en": "Forty-six", "de": "Sechsundvierzig", "digit": "46"},
            {"sq": "Dyzet e shtatë", "en": "Forty-seven", "de": "Siebenundvierzig", "digit": "47"},
            {"sq": "Dyzet e tetë", "en": "Forty-eight", "de": "Achtundvierzig", "digit": "48"},
            {"sq": "Dyzet e nëntë", "en": "Forty-nine", "de": "Neunundvierzig", "digit": "49"},
            {"sq": "Pesëdhjetë", "en": "Fifty", "de": "Fünfzig", "digit": "50"},
            {"sq": "Pesëdhjetë e një", "en": "Fifty-one", "de": "Einundfünfzig", "digit": "51"},
            {"sq": "Pesëdhjetë e dy", "en": "Fifty-two", "de": "Zweiundfünfzig", "digit": "52"},
            {"sq": "Pesëdhjetë e tri", "en": "Fifty-three", "de": "Dreiundfünfzig", "digit": "53"},
            {"sq": "Pesëdhjetë e katër", "en": "Fifty-four", "de": "Vierundfünfzig", "digit": "54"},
            {"sq": "Pesëdhjetë e pesë", "en": "Fifty-five", "de": "Fünfundfünfzig", "digit": "55"},
            {"sq": "Pesëdhjetë e gjashtë", "en": "Fifty-six", "de": "Sechsundfünfzig", "digit": "56"},
            {"sq": "Pesëdhjetë e shtatë", "en": "Fifty-seven", "de": "Siebenundfünfzig", "digit": "57"},
            {"sq": "Pesëdhjetë e tetë", "en": "Fifty-eight", "de": "Achtundfünfzig", "digit": "58"},
            {"sq": "Pesëdhjetë e nëntë", "en": "Fifty-nine", "de": "Neunundfünfzig", "digit": "59"},
            {"sq": "Gjashtëdhjetë", "en": "Sixty", "de": "Sechzig", "digit": "60"},
            {"sq": "Gjashtëdhjetë e një", "en": "Sixty-one", "de": "Einundsechzig", "digit": "61"},
            {"sq": "Gjashtëdhjetë e dy", "en": "Sixty-two", "de": "Zweiundsechzig", "digit": "62"},
            {"sq": "Gjashtëdhjetë e tri", "en": "Sixty-three", "de": "Dreiundsechzig", "digit": "63"},
            {"sq": "Gjashtëdhjetë e katër", "en": "Sixty-four", "de": "Vierundsechzig", "digit": "64"},
            {"sq": "Gjashtëdhjetë e pesë", "en": "Sixty-five", "de": "Fünfundsechzig", "digit": "65"},
            {"sq": "Gjashtëdhjetë e gjashtë", "en": "Sixty-six", "de": "Sechsundsechzig", "digit": "66"},
            {"sq": "Gjashtëdhjetë e shtatë", "en": "Sixty-seven", "de": "Siebenundsechzig", "digit": "67"},
            {"sq": "Gjashtëdhjetë e tetë", "en": "Sixty-eight", "de": "Achtundsechzig", "digit": "68"},
            {"sq": "Gjashtëdhjetë e nëntë", "en": "Sixty-nine", "de": "Neunundsechzig", "digit": "69"},
            {"sq": "Shtatëdhjetë", "en": "Seventy", "de": "Siebzig", "digit": "70"},
            {"sq": "Shtatëdhjetë e një", "en": "Seventy-one", "de": "Einundsiebzig", "digit": "71"},
            {"sq": "Shtatëdhjetë e dy", "en": "Seventy-two", "de": "Zweiundsiebzig", "digit": "72"},
            {"sq": "Shtatëdhjetë e tri", "en": "Seventy-three", "de": "Dreiundsiebzig", "digit": "73"},
            {"sq": "Shtatëdhjetë e katër", "en": "Seventy-four", "de": "Vierundsiebzig", "digit": "74"},
            {"sq": "Shtatëdhjetë e pesë", "en": "Seventy-five", "de": "Fünfundsiebzig", "digit": "75"},
            {"sq": "Shtatëdhjetë e gjashtë", "en": "Seventy-six", "de": "Sechsundsiebzig", "digit": "76"},
            {"sq": "Shtatëdhjetë e shtatë", "en": "Seventy-seven", "de": "Siebenundsiebzig", "digit": "77"},
            {"sq": "Shtatëdhjetë e tetë", "en": "Seventy-eight", "de": "Achtundsiebzig", "digit": "78"},
            {"sq": "Shtatëdhjetë e nëntë", "en": "Seventy-nine", "de": "Neunundsiebzig", "digit": "79"},
            {"sq": "Tetëdhjetë", "en": "Eighty", "de": "Achtzig", "digit": "80"},
            {"sq": "Tetëdhjetë e një", "en": "Eighty-one", "de": "Einundachtzig", "digit": "81"},
            {"sq": "Tetëdhjetë e dy", "en": "Eighty-two", "de": "Zweiundachtzig", "digit": "82"},
            {"sq": "Tetëdhjetë e tri", "en": "Eighty-three", "de": "Dreiundachtzig", "digit": "83"},
            {"sq": "Tetëdhjetë e katër", "en": "Eighty-four", "de": "Vierundachtzig", "digit": "84"},
            {"sq": "Tetëdhjetë e pesë", "en": "Eighty-five", "de": "Fünfundachtzig", "digit": "85"},
            {"sq": "Tetëdhjetë e gjashtë", "en": "Eighty-six", "de": "Sechsundachtzig", "digit": "86"},
            {"sq": "Tetëdhjetë e shtatë", "en": "Eighty-seven", "de": "Siebenundachtzig", "digit": "87"},
            {"sq": "Tetëdhjetë e tetë", "en": "Eighty-eight", "de": "Achtundachtzig", "digit": "88"},
            {"sq": "Tetëdhjetë e nëntë", "en": "Eighty-nine", "de": "Neunundachtzig", "digit": "89"},
            {"sq": "Nëntëdhjetë", "en": "Ninety", "de": "Neunzig", "digit": "90"},
            {"sq": "Nëntëdhjetë e një", "en": "Ninety-one", "de": "Einundneunzig", "digit": "91"},
            {"sq": "Nëntëdhjetë e dy", "en": "Ninety-two", "de": "Zweiundneunzig", "digit": "92"},
            {"sq": "Nëntëdhjetë e tri", "en": "Ninety-three", "de": "Dreiundneunzig", "digit": "93"},
            {"sq": "Nëntëdhjetë e katër", "en": "Ninety-four", "de": "Vierundneunzig", "digit": "94"},
            {"sq": "Nëntëdhjetë e pesë", "en": "Ninety-five", "de": "Fünfundneunzig", "digit": "95"},
            {"sq": "Nëntëdhjetë e gjashtë", "en": "Ninety-six", "de": "Sechsundneunzig", "digit": "96"},
            {"sq": "Nëntëdhjetë e shtatë", "en": "Ninety-seven", "de": "Siebenundneunzig", "digit": "97"},
            {"sq": "Nëntëdhjetë e tetë", "en": "Ninety-eight", "de": "Achtundneunzig", "digit": "98"},
            {"sq": "Nëntëdhjetë e nëntë", "en": "Ninety-nine", "de": "Neunundneunzig", "digit": "99"},
            {"sq": "Njëqind", "en": "One hundred", "de": "Hundert", "digit": "100"}
        ],

        "Ngjyrat": [
            {"sq": "E kuqe", "en": "Red", "de": "Rot", "color": "#FF0000"},
            {"sq": "E kaltër", "en": "Blue", "de": "Blau", "color": "#0000FF"},
            {"sq": "E gjelbër", "en": "Green", "de": "Grün", "color": "#008000"},
            {"sq": "E verdhë", "en": "Yellow", "de": "Gelb", "color": "#FFFF00"},
            {"sq": "E portokalltë", "en": "Orange", "de": "Orange", "color": "#FFA500"},
            {"sq": "E rozë", "en": "Pink", "de": "Rosa", "color": "#FFC0CB"},
            {"sq": "Vjollcë", "en": "Purple", "de": "Lila", "color": "#800080"},
            {"sq": "E zezë", "en": "Black", "de": "Schwarz", "color": "#000000"},
            {"sq": "E bardhë", "en": "White", "de": "Weiß", "color": "#FFFFFF"},
            {"sq": "E hirtë", "en": "Gray", "de": "Grau", "color": "#808080"},
            {"sq": "E kaftë", "en": "Brown", "de": "Braun", "color": "#A52A2A"},
            {"sq": "E artë", "en": "Gold", "de": "Gold", "color": "#FFD700"},
            {"sq": "E argjendtë", "en": "Silver", "de": "Silber", "color": "#C0C0C0"}
        ],

        "Kafshët": [
            {"sq": "Mace", "en": "Cat", "de": "Katze", "emoji": "🐱"},
            {"sq": "Qen", "en": "Dog", "de": "Hund", "emoji": "🐶"},
            {"sq": "Kalë", "en": "Horse", "de": "Pferd", "emoji": "🐴"},
            {"sq": "Lopë", "en": "Cow", "de": "Kuh", "emoji": "🐮"},
            {"sq": "Dhelpër", "en": "Fox", "de": "Fuchs", "emoji": "🦊"},
            {"sq": "Luan", "en": "Lion", "de": "Löwe", "emoji": "🦁"},
            {"sq": "Ari", "en": "Bear", "de": "Bär", "emoji": "🐻"},
            {"sq": "Ujk", "en": "Wolf", "de": "Wolf", "emoji": "🐺"},
            {"sq": "Lepur", "en": "Rabbit", "de": "Hase", "emoji": "🐰"},
            {"sq": "Gjirafë", "en": "Giraffe", "de": "Giraffe", "emoji": "🦒"},
            {"sq": "Elefant", "en": "Elephant", "de": "Elefant", "emoji": "🐘"},
            {"sq": "Mogëll", "en": "Monkey", "de": "Affe", "emoji": "🐒"},
            {"sq": "Zog", "en": "Bird", "de": "Vogel", "emoji": "🐦"},
            {"sq": "Peshk", "en": "Fish", "de": "Fisch", "emoji": "🐟"},
            {"sq": "Gjarpër", "en": "Snake", "de": "Schlange", "emoji": "🐍"},
            {"sq": "Tigër", "en": "Tiger", "de": "Tiger", "emoji": "🐯"},
            {"sq": "Dele", "en": "Sheep", "de": "Schaf", "emoji": "🐑"},
            {"sq": "Derr", "en": "Pig", "de": "Schwein", "emoji": "🐷"}
        ],
        
        "Frutat": [
            {"sq": "Mollë", "en": "Apple", "de": "Apfel", "emoji": "🍎"},
            {"sq": "Dardhë", "en": "Pear", "de": "Birne", "emoji": "🍐"},
            {"sq": "Banane", "en": "Banana", "de": "Banane", "emoji": "🍌"},
            {"sq": "Portokall", "en": "Orange", "de": "Orange", "emoji": "🍊"},
            {"sq": "Rrush", "en": "Grapes", "de": "Trauben", "emoji": "🍇"},
            {"sq": "Luleshtrydhe", "en": "Strawberry", "de": "Erdbeere", "emoji": "🍓"},
            {"sq": "Shalqi", "en": "Watermelon", "de": "Wassermelone", "emoji": "🍉"},
            {"sq": "Qershi", "en": "Cherry", "de": "Kirsche", "emoji": "🍒"},
            {"sq": "Pjeshkë", "en": "Peach", "de": "Pfirsich", "emoji": "🍑"},
            {"sq": "Limoni", "en": "Lemon", "de": "Zitrone", "emoji": "🍋"},
            {"sq": "Ananas", "en": "Pineapple", "de": "Ananas", "emoji": "🍍"}
        ],

        "Perimet": [
            {"sq": "Patate", "en": "Potato", "de": "Kartoffel", "emoji": "🥔"},
            {"sq": "Karotë", "en": "Carrot", "de": "Karotte", "emoji": "🥕"},
            {"sq": "Domate", "en": "Tomato", "de": "Tomate", "emoji": "🍅"},
            {"sq": "Kastravec", "en": "Cucumber", "de": "Gurke", "emoji": "🥒"},
            {"sq": "Qepë", "en": "Onion", "de": "Zwiebel", "emoji": "🧅"},
            {"sq": "Hudhur", "en": "Garlic", "de": "Knoblauch", "emoji": "🧄"},
            {"sq": "Spec", "en": "Pepper", "de": "Paprika", "emoji": "🫑"},
            {"sq": "Misër", "en": "Corn", "de": "Mais", "emoji": "🌽"},
            {"sq": "Sallatë", "en": "Lettuce", "de": "Salat", "emoji": "🥬"},
            {"sq": "Brokoli", "en": "Broccoli", "de": "Brokkoli", "emoji": "🥦"}
        ]
    }
    return render_template('first_week.html', categories=data)

@app.route('/second_week')
def second_week():
    data = {
        "Ushqimet": [
            {"sq": "Bukë", "en": "Bread", "de": "Brot", "emoji": "🍞"},
            {"sq": "Mish", "en": "Meat", "de": "Fleisch", "emoji": "🥩"},
            {"sq": "Djathë", "en": "Cheese", "de": "Käse", "emoji": "🧀"},
            {"sq": "Vezë", "en": "Egg", "de": "Ei", "emoji": "🥚"},
            {"sq": "Pula", "en": "Chicken", "de": "Hähnchen", "emoji": "🍗"},
            {"sq": "Oriz", "en": "Rice", "de": "Reis", "emoji": "🍚"},
            {"sq": "Pasta", "en": "Pasta", "de": "Nudeln", "emoji": "🍝"}
        ],

        "Pijet": [
            {"sq": "Ujë", "en": "Water", "de": "Wasser", "emoji": "💧"},
            {"sq": "Kafe", "en": "Coffee", "de": "Kaffee", "emoji": "☕"},
            {"sq": "Çaj", "en": "Tea", "de": "Tee", "emoji": "🍵"},
            {"sq": "Qumësht", "en": "Milk", "de": "Milch", "emoji": "🥛"},
            {"sq": "Lëng", "en": "Juice", "de": "Saft", "emoji": "🧃"},
            {"sq": "Birrë", "en": "Beer", "de": "Bier", "emoji": "🍺"},
            {"sq": "Verë", "en": "Wine", "de": "Wein", "emoji": "🍷"}
        ],

        "Sweets": [
            {"sq": "Ëmbëlsirë", "en": "Dessert", "de": "Nachtisch", "emoji": "🍰"},
            {"sq": "Çokollatë", "en": "Chocolate", "de": "Schokolade", "emoji": "🍫"},
            {"sq": "Akullore", "en": "Ice cream", "de": "Eis", "emoji": "🍦"},
            {"sq": "Tortë", "en": "Cake", "de": "Kuchen", "emoji": "🎂"},
            {"sq": "Biskota", "en": "Cookies", "de": "Kekse", "emoji": "🍪"}
        ],

        "Ditet": [
            {"sq": "E hënë", "en": "Monday", "de": "Montag"},
            {"sq": "E martë", "en": "Tuesday", "de": "Dienstag"},
            {"sq": "E mërkurë", "en": "Wednesday", "de": "Mittwoch"},
            {"sq": "E enjte", "en": "Thursday", "de": "Donnerstag"},
            {"sq": "E premte", "en": "Friday", "de": "Freitag"},
            {"sq": "E shtunë", "en": "Saturday", "de": "Samstag"},
            {"sq": "E diel", "en": "Sunday", "de": "Sonntag"}
        ],

        "Muajt": [
            {"sq": "Janar", "en": "January", "de": "Januar"},
            {"sq": "Shkurt", "en": "February", "de": "Februar"},
            {"sq": "Mars", "en": "March", "de": "März"},
            {"sq": "Prill", "en": "April", "de": "April"},
            {"sq": "Maj", "en": "May", "de": "Mai"},
            {"sq": "Qershor", "en": "June", "de": "Juni"},
            {"sq": "Korrik", "en": "July", "de": "Juli"},
            {"sq": "Gusht", "en": "August", "de": "August"},
            {"sq": "Shtator", "en": "September", "de": "September"},
            {"sq": "Tetor", "en": "October", "de": "Oktober"},
            {"sq": "Nëntor", "en": "November", "de": "November"},
            {"sq": "Dhjetor", "en": "December", "de": "Dezember"}
        ],

        "Stinet": [
            {"sq": "Pranverë", "en": "Spring", "de": "Frühling", "emoji": "🌸"},
            {"sq": "Verë", "en": "Summer", "de": "Sommer", "emoji": "☀️"},
            {"sq": "Vjeshtë", "en": "Autumn", "de": "Herbst", "emoji": "🍂"},
            {"sq": "Dimër", "en": "Winter", "de": "Winter", "emoji": "❄️"}
        ]
    }
    return render_template('second_week.html', categories=data)

@app.route('/third_week')
def third_week():
    # Për javën e tretë me 3 gjuhë
    data = {
        "People": [
            {"sq": "Njeri", "en": "Person", "de": "Mensch", "emoji": "👤"},
            {"sq": "Burrë", "en": "Man", "de": "Mann", "emoji": "👨"},
            {"sq": "Grua", "en": "Woman", "de": "Frau", "emoji": "👩"},
            {"sq": "Fëmijë", "en": "Child", "de": "Kind", "emoji": "👶"},
            {"sq": "Babai", "en": "Father", "de": "Vater", "emoji": "👨‍🍼"},
            {"sq": "Nëna", "en": "Mother", "de": "Mutter", "emoji": "👩‍🍼"},
            {"sq": "Djali (i prindit)", "en": "Son", "de": "Sohn", "emoji": "👦"},
            {"sq": "Vajza (e prindit)", "en": "Daughter", "de": "Tochter", "emoji": "👧"},
            {"sq": "Vëllai", "en": "Brother", "de": "Bruder", "emoji": "👦"},
            {"sq": "Motra", "en": "Sister", "de": "Schwester", "emoji": "👧"},
            {"sq": "Gjyshi", "en": "Grandfather", "de": "Großvater", "emoji": "👴"},
            {"sq": "Gjyshja", "en": "Grandmother", "de": "Großmutter", "emoji": "👵"},
            {"sq": "Daja / Axha", "en": "Uncle", "de": "Onkel", "emoji": "👨‍💼"},
            {"sq": "Tezja / Halla", "en": "Aunt", "de": "Tante", "emoji": "👩‍💼"},
            {"sq": "Kushëri", "en": "Cousin", "de": "Cousin", "emoji": "👱‍♂️"},
            {"sq": "Fqinj", "en": "Neighbor", "de": "Nachbar", "emoji": "🏠"},
        ],
        "Body parts": [
            {"sq": "Koka", "en": "Head", "de": "Kopf", "emoji": "👤"},
            {"sq": "Syri", "en": "Eye", "de": "Auge", "emoji": "👁️"},
            {"sq": "Veshi", "en": "Ear", "de": "Ohr", "emoji": "👂"},
            {"sq": "Hunda", "en": "Nose", "de": "Nase", "emoji": "👃"},
            {"sq": "Goja", "en": "Mouth", "de": "Mund", "emoji": "👄"},
            {"sq": "Dora", "en": "Hand", "de": "Hand", "emoji": "✋"},
            {"sq": "Këmba", "en": "Leg", "de": "Bein", "emoji": "🦵"},
            {"sq": "Zemra", "en": "Heart", "de": "Herz", "emoji": "❤️"}
        ],
        "Clothing": [
            {"sq": "Këmisha", "en": "Shirt", "de": "Hemd", "emoji": "👕"},
            {"sq": "Pantallona", "en": "Pants", "de": "Hose", "emoji": "👖"},
            {"sq": "Fustan", "en": "Dress", "de": "Kleid", "emoji": "👗"},
            {"sq": "Këpucë", "en": "Shoes", "de": "Schuhe", "emoji": "👟"},
            {"sq": "Pallto", "en": "Coat", "de": "Mantel", "emoji": "🧥"},
            {"sq": "Kapele", "en": "Hat", "de": "Hut", "emoji": "🧢"}
        ],
        "Emotions": [
            {"sq": "I lumtur", "en": "Happy", "de": "Glücklich", "emoji": "😊"},
            {"sq": "I mërzitur", "en": "Sad", "de": "Traurig", "emoji": "😢"},
            {"sq": "I zemëruar", "en": "Angry", "de": "Wütend", "emoji": "😠"},
            {"sq": "I lodhur", "en": "Tired", "de": "Müde", "emoji": "😴"},
            {"sq": "I frikësuar", "en": "Scared", "de": "Angstvoll", "emoji": "😨"},
            {"sq": "I befasuar", "en": "Surprised", "de": "Überrascht", "emoji": "😲"}
        ],
        "Profesions": [
            {"sq": "Mjek", "en": "Doctor", "de": "Arzt", "emoji": "👨‍⚕️"},
            {"sq": "Mësues", "en": "Teacher", "de": "Lehrer", "emoji": "👨‍🏫"},
            {"sq": "Inxhinier", "en": "Engineer", "de": "Ingenieur", "emoji": "👷"},
            {"sq": "Polic", "en": "Policeman", "de": "Polizist", "emoji": "👮"},
            {"sq": "Kuzhinier", "en": "Cook", "de": "Koch", "emoji": "👨‍🍳"},
            {"sq": "Programer", "en": "Programmer", "de": "Programmierer", "emoji": "💻"},
            {"sq": "Koleg", "en": "Colleague", "de": "Kollege", "emoji": "💼"},
            {"sq": "Student", "en": "Student", "de": "Student", "emoji": "🎓"},],
        "Sports": [
            {"sq": "Futboll", "en": "Football", "de": "Fußball", "emoji": "⚽"},
            {"sq": "Basketboll", "en": "Basketball", "de": "Basketball", "emoji": "🏀"},
            {"sq": "Tenis", "en": "Tennis", "de": "Tennis", "emoji": "🎾"},
            {"sq": "Volejboll", "en": "Volleyball", "de": "Volleyball", "emoji": "🏐"},
            {"sq": "Not", "en": "Swimming", "de": "Schwimmen", "emoji": "🏊"},
            {"sq": "Vrapim", "en": "Running", "de": "Laufen", "emoji": "🏃"}
        ]
    }
    return render_template('third_week.html', categories=data)

@app.route('/exam/<exam_id>')
def exam(exam_id):
    my_lang = session.get('my_lang', 'sq')      # Zakonisht 'sq'
    learn_lang = session.get('learn_lang', 'en') # 'en' ose 'de'
    
    raw_questions = EXAMS_DATA.get(exam_id, [])
    final_questions = []

    for item in raw_questions:
        final_questions.append({
            "q": item["q"][learn_lang],   # Pyetja: En ose De
            "options": [opt[my_lang] for opt in item["options"]], # Opsionet: Shqip
            "a": item["q"][my_lang]       # Përgjigja e saktë: Shqip
        })

    return render_template('exam.html', questions=final_questions, exam_id=exam_id)

if __name__ == '__main__':
    setup_database()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
