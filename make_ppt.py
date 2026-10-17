"""
Placement Predictor — TAGDA PowerPoint Presentation
Website ka pura code, technology aur screenshots ke saath.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------- Rang (website ke dark theme se) ----------
BG = RGBColor(7, 7, 26)          # #07071a — website ka background
PANEL = RGBColor(20, 20, 48)     # card jaisa halka panel
CYAN = RGBColor(34, 211, 238)    # #22d3ee
PURPLE = RGBColor(167, 139, 250)  # #a78bfa
PINK = RGBColor(244, 114, 182)   # #f472b6
GREEN = RGBColor(52, 211, 153)   # #34d399
YELLOW = RGBColor(251, 191, 36)  # #fbbf24
WHITE = RGBColor(232, 232, 245)  # #e8e8f5
SOFT = RGBColor(185, 192, 232)   # #b9c0e8
DIM = RGBColor(120, 126, 160)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height


def add_slide():
    """Naya dark slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    bg.line.fill.background()
    bg.shadow.inherit = False
    return slide


def add_text(slide, left, top, width, height, text, size=18, color=WHITE,
             bold=False, align=PP_ALIGN.LEFT, font="Segoe UI", anchor=MSO_ANCHOR.TOP,
             line_spacing=1.15):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.runs[0] if p.runs else p.add_run()
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = font
    return tb


def add_panel(slide, left, top, width, height, fill=PANEL, radius=0.15):
    """Halka glass jaisa panel."""
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = RGBColor(60, 60, 110)
    sh.line.width = Pt(1)
    sh.shadow.inherit = False
    try:
        sh.adjustments[0] = radius
    except Exception:
        pass
    return sh


def add_accent_bar(slide, left, top, width=Inches(1.6), color=CYAN):
    """Title ke neeche chhota gradient-like bar."""
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Pt(5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar


def slide_header(slide, title, subtitle=None, accent=CYAN):
    add_text(slide, Inches(0.6), Inches(0.35), Inches(12), Inches(0.8),
             title, size=34, bold=True, color=WHITE)
    add_accent_bar(slide, Inches(0.65), Inches(1.05), color=accent)
    if subtitle:
        add_text(slide, Inches(0.6), Inches(1.15), Inches(12), Inches(0.5),
                 subtitle, size=15, color=SOFT)


def add_code_box(slide, left, top, width, height, code, size=12):
    """Code dikhane ke liye gehra panel + monospace text."""
    panel = add_panel(slide, left, top, width, height, fill=RGBColor(10, 10, 32), radius=0.06)
    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12),
                                  width - Inches(0.36), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(code.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line if line else " "
        r = p.runs[0] if p.runs else p.add_run()
        r.font.size = Pt(size)
        r.font.name = "Consolas"
        r.font.color.rgb = RGBColor(170, 220, 255)  # halka cyan jaisa
    return panel


def add_bullet_block(slide, left, top, width, items, size=15, gap=0.42, color=SOFT):
    """Points ki list — har point ke saath chhota colored dot."""
    y = top
    for text, dot_color in items:
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, y + Pt(6), Pt(9), Pt(9))
        dot.fill.solid()
        dot.fill.fore_color.rgb = dot_color
        dot.line.fill.background()
        dot.shadow.inherit = False
        add_text(slide, left + Inches(0.28), y, width - Inches(0.28), Inches(0.4),
                 text, size=size, color=color)
        y += Inches(gap)
    return y


# ============================================================
# SLIDE 1 — Title
# ============================================================
s = add_slide()
# Bade neon jaise title ke peeche halka glow panel
glow = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.6), Inches(1.7),
                          Inches(10.1), Inches(4.2))
glow.fill.solid()
glow.fill.fore_color.rgb = RGBColor(14, 14, 40)
glow.line.color.rgb = PURPLE
glow.line.width = Pt(1.5)
glow.shadow.inherit = False
try:
    glow.adjustments[0] = 0.08
except Exception:
    pass

add_text(s, Inches(1.6), Inches(2.1), Inches(10.1), Inches(1.2),
         "\U0001F52E  PLACEMENT PREDICTOR", size=48, bold=True,
         color=CYAN, align=PP_ALIGN.CENTER)
add_text(s, Inches(1.6), Inches(3.25), Inches(10.1), Inches(0.7),
         "Machine Learning se jaano ki aapki placement hogi ya nahi!",
         size=22, color=PURPLE, align=PP_ALIGN.CENTER)
add_text(s, Inches(1.6), Inches(4.1), Inches(10.1), Inches(0.5),
         "Flask (Python)  •  HTML/CSS/JavaScript  •  scikit-learn  •  Random Forest",
         size=16, color=SOFT, align=PP_ALIGN.CENTER)
add_text(s, Inches(1.6), Inches(4.7), Inches(10.1), Inches(0.5),
         "Created by Vikas Yadav",
         size=18, bold=True, color=PINK, align=PP_ALIGN.CENTER)
add_text(s, Inches(1.6), Inches(5.3), Inches(10.1), Inches(0.4),
         "October 2026", size=13, color=DIM, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 2 — Website kya karti hai
# ============================================================
s = add_slide()
slide_header(s, "\U0001F310 Ye Website Kya Karti Hai?", "Idea ek line me: student ka data daalo → ML model prediction dega")

add_panel(s, Inches(0.6), Inches(1.9), Inches(6.0), Inches(4.9))
add_text(s, Inches(0.9), Inches(2.1), Inches(5.5), Inches(0.5),
         "Kaise Kaam Karta Hai?", size=20, bold=True, color=CYAN)
add_bullet_block(s, Inches(0.9), Inches(2.75), Inches(5.5), [
    ("Student apni details bharta hai (10th, 12th, CGPA, etc.)", CYAN),
    ("Website ye data Machine Learning model ko bhejti hai", PURPLE),
    ("Model predict karta hai: placement hogi ya nahi", PINK),
    ("Saath me chance ka % bhi dikhata hai (gauge me)", GREEN),
    ("Placed dikha to confetti celebration bhi hoti hai!", YELLOW),
], size=14)

add_panel(s, Inches(6.9), Inches(1.9), Inches(5.8), Inches(4.9))
add_text(s, Inches(7.2), Inches(2.1), Inches(5.2), Inches(0.5),
         "Form me 8 Details Bharti Hain", size=20, bold=True, color=PURPLE)
fields = [
    ("10th Percentage (%)", "e.g. 85"),
    ("12th Percentage (%)", "e.g. 80"),
    ("CGPA (0 - 10)", "e.g. 8.2"),
    ("Internships ki sankhya", "e.g. 2"),
    ("Projects ki sankhya", "e.g. 4"),
    ("Aptitude Score (0-100)", "e.g. 78"),
    ("Communication Score (0-100)", "e.g. 82"),
    ("Work Experience (Yes/No)", "Yes / No"),
]
y = Inches(2.75)
for name, eg in fields:
    add_text(s, Inches(7.2), y, Inches(3.4), Inches(0.35), "•  " + name, size=13, color=SOFT)
    add_text(s, Inches(10.6), y, Inches(1.9), Inches(0.35), eg, size=12, color=DIM)
    y += Inches(0.45)

# ============================================================
# SLIDE 3 — Technology Stack
# ============================================================
s = add_slide()
slide_header(s, "\U0001F9E9 Technology aur Languages", "Website 3 hisso se bani hai: Backend + ML + Frontend", accent=PURPLE)

techs = [
    ("Python 3.13", "Backend language", "Flask app + ML model — pura dimaag isi me hai", CYAN, "\U0001F40D"),
    ("Flask", "Web Framework", "Python ki lightweight library — website chalati hai", PURPLE, "\U0001F310"),
    ("scikit-learn", "ML Library", "Random Forest model train karne ke liye", PINK, "\U0001F9E0"),
    ("HTML5", "Page Structure", "Website ka skeleton — forms, buttons, result box", GREEN, "\U0001F3E0"),
    ("CSS3", "Design + Animation", "Dark theme, glassmorphism, neon glow, animations", YELLOW, "\U0001F3A8"),
    ("JavaScript", "Interactivity", "Form data bhejna, animations, cursor, confetti", CYAN, "\u26A1"),
]
x, y = Inches(0.6), Inches(1.9)
for i, (name, role, desc, color, emoji) in enumerate(techs):
    col = i % 3
    row = i // 3
    left = Inches(0.6) + col * Inches(4.15)
    top = Inches(1.9) + row * Inches(2.45)
    add_panel(s, left, top, Inches(3.9), Inches(2.2))
    add_text(s, left + Inches(0.25), top + Inches(0.15), Inches(3.4), Inches(0.5),
             f"{emoji}  {name}", size=20, bold=True, color=color)
    add_text(s, left + Inches(0.25), top + Inches(0.75), Inches(3.4), Inches(0.4),
             role, size=13, bold=True, color=WHITE)
    add_text(s, left + Inches(0.25), top + Inches(1.2), Inches(3.4), Inches(0.85),
             desc, size=12, color=SOFT)

# ============================================================
# SLIDE 4 — Project Structure
# ============================================================
s = add_slide()
slide_header(s, "\U0001F4C1 Project Structure", "Har file ka kaam ek line me", accent=GREEN)

add_code_box(s, Inches(0.6), Inches(1.85), Inches(6.3), Inches(5.1), """placement-predictor/
|
|-- app.py              <- Flask website (backend)
|-- train_model.py      <- ML model train karta hai
|-- model.pkl           <- Trained model (auto save)
|-- placement_data.csv  <- Dataset (2000 students)
|-- requirements.txt    <- zaroori packages
|-- runtime.txt         <- Python version
|
|-- templates/
|   |-- index.html      <- Main website page
|   |-- login.html      <- Login page
|
|-- static/
|   |-- style.css       <- Design + animations
|   |-- script.js       <- Website ka JS logic
|   |-- bg.js           <- (backup background file)""", size=13)

add_panel(s, Inches(7.2), Inches(1.85), Inches(5.5), Inches(5.1))
add_text(s, Inches(7.5), Inches(2.05), Inches(5), Inches(0.5),
         "Files ka Kaam", size=20, bold=True, color=GREEN)
add_bullet_block(s, Inches(7.5), Inches(2.7), Inches(5), [
    ("app.py — website ka dil: routes, login, predict API", CYAN),
    ("train_model.py — dataset + model banata hai", PURPLE),
    ("model.pkl — trained Random Forest (auto load)", PINK),
    ("index.html — main page ka structure", GREEN),
    ("login.html — login page (inline design)", YELLOW),
    ("style.css — poora design + 10+ animations", CYAN),
    ("script.js — form logic + cursor + scan + confetti", PURPLE),
], size=13, gap=0.5)

# ============================================================
# SLIDE 5 — Login Page (screenshot)
# ============================================================
s = add_slide()
slide_header(s, "\U0001F512 Login Page", "Bina login kiye website nahi khulti — session security", accent=PINK)

s.shapes.add_picture("shot_login.png", Inches(0.6), Inches(1.85), height=Inches(5.1))

add_panel(s, Inches(7.0), Inches(1.85), Inches(5.7), Inches(5.1))
add_text(s, Inches(7.3), Inches(2.05), Inches(5.2), Inches(0.5),
         "Login Page Features", size=20, bold=True, color=PINK)
add_bullet_block(s, Inches(7.3), Inches(2.7), Inches(5.2), [
    ("Lamp + bulb animation (upar latka hua lamp)", YELLOW),
    ("Username + Password form (POST se bhejta hai)", CYAN),
    ("Password hide/show ka 👁 toggle button", PURPLE),
    ("Galat password par red error message", PINK),
    ("Session server par save hota hai (secret_key)", GREEN),
    ("Credentials app.py me defined hain", DIM),
], size=13, gap=0.5)
add_text(s, Inches(7.3), Inches(5.9), Inches(5.2), Inches(0.9),
         "Security: @login_required decorator har page ko protect karta hai — bina login ke / par redirect ho jata hai.",
         size=12, color=DIM)

# ============================================================
# SLIDE 6 — Login Code
# ============================================================
s = add_slide()
slide_header(s, "\U0001F527 Login ka Backend Code (app.py)", "Flask routes + session + decorator — sab simple hai", accent=CYAN)

add_code_box(s, Inches(0.6), Inches(1.8), Inches(6.5), Inches(5.2), """# Login credentials
VALID_USERNAME = "vikas yadav"
VALID_PASSWORD = "pit jaunpur"

# Har page ko protect karne wala decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# Login route — GET se form, POST se check
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == VALID_USERNAME \\
           and password == VALID_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        error = "Galat username ya password!"
    return render_template("login.html", error=error)""", size=12)

add_panel(s, Inches(7.4), Inches(1.8), Inches(5.3), Inches(5.2))
add_text(s, Inches(7.7), Inches(2.0), Inches(4.8), Inches(0.5),
         "Simple Bhasha Me", size=20, bold=True, color=CYAN)
add_bullet_block(s, Inches(7.7), Inches(2.65), Inches(4.8), [
    ('session — browser ke liye "identity card"', PURPLE),
    ("session['logged_in'] = True matlab login ho gaya", GREEN),
    ("Decorator har page par check karta hai", CYAN),
    ("Galat password par error variable me message", PINK),
    ("render_template() HTML file browser ko bhejta hai", YELLOW),
    ("url_for() sahi page ka path dhoondta hai", DIM),
], size=13, gap=0.55)

# ============================================================
# SLIDE 7 — Main Website (screenshot)
# ============================================================
s = add_slide()
slide_header(s, "\U0001F3C6 Main Website Page", "Dark theme + glassmorphism card + animated background", accent=PURPLE)

s.shapes.add_picture("shot_home.png", Inches(0.6), Inches(1.85), height=Inches(5.1))

add_panel(s, Inches(7.0), Inches(1.85), Inches(5.7), Inches(5.1))
add_text(s, Inches(7.3), Inches(2.05), Inches(5.2), Inches(0.5),
         "Screen par Kya Dikhta Hai", size=20, bold=True, color=PURPLE)
add_bullet_block(s, Inches(7.3), Inches(2.7), Inches(5.2), [
    ("Animated background — particles + shooting stars", CYAN),
    ("Floating glowing orbs (mouse ke saath chalti hain)", PURPLE),
    ("Glassmorphism card — mouse par 3D tilt hota hai", PINK),
    ("Gradient animated title + typewriter subtitle", GREEN),
    ("⚡ Power bar — fields bharo utna % badhta hai", YELLOW),
    ("Magnetic Predict button (cursor ko khichta hai)", CYAN),
    ("Neon 'Created by Vikas Yadav' credit", PINK),
], size=13, gap=0.5)

# ============================================================
# SLIDE 8 — Form + Result (2 screenshots)
# ============================================================
s = add_slide()
slide_header(s, "\U0001F4CB Form Bharo → Prediction Lo", "Form bharne par power bar full, submit par AI scan + result", accent=GREEN)

s.shapes.add_picture("shot_form.png", Inches(0.5), Inches(1.8), height=Inches(4.3))
s.shapes.add_picture("shot_result.png", Inches(4.9), Inches(1.8), height=Inches(4.3))

add_text(s, Inches(0.5), Inches(6.2), Inches(4.1), Inches(0.4),
         "① Form bharte waqt — Power bar badhta hai", size=13, color=SOFT, align=PP_ALIGN.CENTER)
add_text(s, Inches(4.9), Inches(6.2), Inches(4.1), Inches(0.4),
         "② Predict ke baad — Gauge + confetti", size=13, color=SOFT, align=PP_ALIGN.CENTER)

add_panel(s, Inches(9.3), Inches(1.8), Inches(3.5), Inches(4.9))
add_text(s, Inches(9.55), Inches(2.0), Inches(3), Inches(0.5),
         "Result Me Kya Milta Hai", size=17, bold=True, color=GREEN)
add_bullet_block(s, Inches(9.55), Inches(2.65), Inches(3), [
    ("Placed / Not Placed", GREEN),
    ("Chance ka exact %", CYAN),
    ("Neon circular gauge", PURPLE),
    ("Confetti celebration", PINK),
    ("Hologram glitch reveal", YELLOW),
    ("AI scan line animation", DIM),
], size=12, gap=0.52)

# ============================================================
# SLIDE 9 — Predict API Code
# ============================================================
s = add_slide()
slide_header(s, "\U0001F916 Prediction Ka Code (app.py)", "Form ka data → model → JSON response", accent=PINK)

add_code_box(s, Inches(0.6), Inches(1.8), Inches(6.6), Inches(5.2), """# Form se aane wale fields (same order me model ko bhejte hain)
FEATURES = [
    "tenth_percent", "twelfth_percent", "cgpa",
    "internships", "projects", "aptitude_score",
    "communication_score", "work_experience",
]

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    # JavaScript se student ka data aata hai (JSON)
    data = request.get_json()

    # Form ki values ko number me badlo
    values = [float(data[f]) for f in FEATURES]

    # Model ko do — lag 0.5 se placement ka chance
    prob = model.predict_proba([values])[0][1]

    placed = prob >= 0.5
    percent = round(prob * 100, 1)

    # Browser ko JSON wapas bhejo
    return jsonify({
        "prediction": "Placed" if placed else "Not Placed",
        "probability": percent,
        "message": "Strong profile!" if placed else "Skills improve karo!",
    })""", size=12)

add_panel(s, Inches(7.5), Inches(1.8), Inches(5.2), Inches(5.2))
add_text(s, Inches(7.8), Inches(2.0), Inches(4.7), Inches(0.5),
         "Flow Samjho", size=20, bold=True, color=PINK)
steps = [
    ("1. JavaScript fetch() se JSON bhejta hai", CYAN),
    ("2. Flask request.get_json() me padhta hai", PURPLE),
    ("3. model.predict_proba() chance nikalta hai", PINK),
    ("4. probability >= 50 → Placed, warna Not", GREEN),
    ("5. jsonify() se browser ko JSON wapas", YELLOW),
    ("6. JS result ko animation ke saath dikhata hai", DIM),
]
y = Inches(2.7)
for text, color in steps:
    add_text(s, Inches(7.8), y, Inches(4.7), Inches(0.5), text, size=14, color=color)
    y += Inches(0.6)

# ============================================================
# SLIDE 10 — ML Model
# ============================================================
s = add_slide()
slide_header(s, "\U0001F9E0 Machine Learning Model", "Random Forest Classifier — scikit-learn se train hua", accent=CYAN)

add_code_box(s, Inches(0.6), Inches(1.8), Inches(6.3), Inches(5.2), """# train_model.py ka core hissa

# 1. Dataset banaya — 2000 students
n = 2000
tenth = rng.normal(78, 9, n)     # 10th marks
cgpa  = rng.normal(7.5, 0.9, n)  # CGPA
# ... 8 features total

# 2. Placement chance ka formula
chance = (cgpa/10)*30 + (tenth/100)*15
       + internships*8 + projects*2
       + aptitude*0.15 + communication*0.15
       + work_exp*5
placed = (chance + noise > 75).astype(int)

# 3. Model train
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 4. Save for website
joblib.dump(model, "model.pkl")
# accuracy: ~87%""", size=12)

add_panel(s, Inches(7.2), Inches(1.8), Inches(5.5), Inches(5.2))
add_text(s, Inches(7.5), Inches(2.0), Inches(5), Inches(0.5),
         "Random Forest Kya Hai?", size=20, bold=True, color=CYAN)
add_bullet_block(s, Inches(7.5), Inches(2.65), Inches(5), [
    ("100 chhote decision trees ka group", PURPLE),
    ("Har tree apna guess karta hai", PINK),
    ("Sabka majority vote = final answer", GREEN),
    ("8 features input: marks, CGPA, skills...", CYAN),
    ("Output: 0 (Not Placed) ya 1 (Placed)", YELLOW),
    ("predict_proba() se % chance milta hai", DIM),
    ("Dataset: placement_data.csv (2000 rows)", SOFT),
], size=13, gap=0.5)

# ============================================================
# SLIDE 11 — HTML Code
# ============================================================
s = add_slide()
slide_header(s, "\U0001F3E0 HTML — Website ka Skeleton", "index.html — ye structure browser ko bhejta hai", accent=GREEN)

add_code_box(s, Inches(0.6), Inches(1.8), Inches(6.5), Inches(5.2), """<!-- templates/index.html (simplified) -->

<canvas id="bgParticles"></canvas>  <!-- background -->

<div class="container">             <!-- glass card -->
  <header>
    <h1 id="mainTitle">Placement Predictor</h1>
    <p id="tagline">Apni details bharo...</p>
    <div class="badge">AI Powered</div>
  </header>

  <div class="charge">...</div>     <!-- power bar -->

  <form id="predictForm">
    <label>10th Percentage</label>
    <input type="number" id="tenth_percent" />
    <!-- ... 8 fields total ... -->
    <button type="submit">Predict</button>
  </form>

  <div id="result" class="hidden">  <!-- result box -->
    <h2 id="predictionText"></h2>
    <div class="gauge">             <!-- neon ring -->
      <svg>...</svg>
    </div>
    <p id="messageText"></p>
  </div>
</div>""", size=11)

add_panel(s, Inches(7.4), Inches(1.8), Inches(5.3), Inches(5.2))
add_text(s, Inches(7.7), Inches(2.0), Inches(4.8), Inches(0.5),
         "HTML Kya Fix Karta Hai", size=20, bold=True, color=GREEN)
add_bullet_block(s, Inches(7.7), Inches(2.65), Inches(4.8), [
    ("canvas — animated background ka drawing area", CYAN),
    ("form + input — user ki 8 details", PURPLE),
    ("id='result' — JS isi me prediction likhta hai", PINK),
    ("SVG circle — neon gauge ring banati hai", GREEN),
    ("hidden class — result pehle chhupa rehta hai", YELLOW),
    ("url_for() — CSS/JS ka sahi path deta hai", DIM),
], size=13, gap=0.55)

# ============================================================
# SLIDE 12 — CSS
# ============================================================
s = add_slide()
slide_header(s, "\U0001F3A8 CSS — Design + 15+ Animations", "style.css — website ko sundar aur jaandar banata hai", accent=PURPLE)

add_panel(s, Inches(0.6), Inches(1.8), Inches(6.0), Inches(5.2))
add_text(s, Inches(0.9), Inches(2.0), Inches(5.5), Inches(0.5),
         "Design Techniques", size=20, bold=True, color=PURPLE)
add_bullet_block(s, Inches(0.9), Inches(2.65), Inches(5.5), [
    ("Glassmorphism — card par blur + transparency", CYAN),
    ("Neon glow — box-shadow se chamak", PINK),
    ("Gradient text — title me 3 rang badalte hain", GREEN),
    ("Dark theme — #07071a background", YELLOW),
    ("CSS variables — ek jagah rang define, jagah jagah use", PURPLE),
    ("Backdrop filter — background blur effect", SOFT),
], size=14, gap=0.55)

add_panel(s, Inches(6.9), Inches(1.8), Inches(5.8), Inches(5.2))
add_text(s, Inches(7.2), Inches(2.0), Inches(5.3), Inches(0.5),
         "Animations List", size=20, bold=True, color=PINK)
anims = [
    ("@keyframes float1/2/3 — orbs ka float", CYAN),
    ("@keyframes bgShift — background ka rang", PURPLE),
    ("@keyframes letterIn — title ke letters", PINK),
    ("@keyframes caretBlink — typewriter cursor", GREEN),
    ("@keyframes shine — button par light sweep", YELLOW),
    ("@keyframes scanSweep — AI scan line", CYAN),
    ("@keyframes glitchIn — hologram result", PURPLE),
    ("@keyframes eqBounce — thinking bars", PINK),
    ("@keyframes neonFlicker — credit sign", GREEN),
]
y = Inches(2.65)
for text, color in anims:
    add_text(s, Inches(7.2), y, Inches(5.3), Inches(0.35), "•  " + text, size=12, color=color)
    y += Inches(0.42)

# ============================================================
# SLIDE 13 — JavaScript
# ============================================================
s = add_slide()
slide_header(s, "\u26A1 JavaScript — Website ki Jaan", "script.js — sab kuch chalata hai (500+ lines)", accent=YELLOW)

boxes = [
    ("1. Background Animation", CYAN,
     "Canvas par 70 particles move + connect.\nMouse ke paas cyan lines.\nShooting stars aati rehti hain."),
    ("2. Title + Typewriter", PURPLE,
     "Har letter span me wrap.\nEk-ek karke uchhal ke aata hai.\nSubtitle akshar-akshar likhta hai."),
    ("3. 3D Tilt + Cursor", PINK,
     "Card mouse ke saath tilt.\nCustom neon dot + ring cursor.\nOrbs parallax move karti hain."),
    ("4. Form + Fetch", GREEN,
     "8 fields ka data collect.\nfetch('/predict') se JSON bhej.\nResponse me prediction padh."),
    ("5. Result Animations", YELLOW,
     "Gauge ring bharti hai (SVG).\n% count-up hota hai.\nPlaced ho to confetti barish."),
    ("6. AI Scan + Glitch", CYAN,
     "Scan line card par sweep.\nFields sequence me highlight.\nResult hologram glitch se aata hai."),
]
for i, (title, color, desc) in enumerate(boxes):
    col = i % 3
    row = i // 3
    left = Inches(0.6) + col * Inches(4.15)
    top = Inches(1.85) + row * Inches(2.5)
    add_panel(s, left, top, Inches(3.9), Inches(2.3))
    add_text(s, left + Inches(0.22), top + Inches(0.12), Inches(3.5), Inches(0.45),
             title, size=16, bold=True, color=color)
    add_text(s, left + Inches(0.22), top + Inches(0.65), Inches(3.5), Inches(1.55),
             desc, size=12, color=SOFT, line_spacing=1.3)

# ============================================================
# SLIDE 14 — JavaScript Code Example
# ============================================================
s = add_slide()
slide_header(s, "\U0001F4DD JavaScript Code — Form Submit", "User click karta hai → data jaata hai → result aata hai", accent=CYAN)

add_code_box(s, Inches(0.6), Inches(1.8), Inches(7.0), Inches(5.2), """// script.js — form submit hone par

document.getElementById("predictForm")
.addEventListener("submit", async function (e) {
  e.preventDefault();   // page reload mat ho

  // 1. Saari fields ka data lo
  const data = {
    tenth_percent:  document.getElementById("tenth_percent").value,
    twelfth_percent: document.getElementById("twelfth_percent").value,
    cgpa:           document.getElementById("cgpa").value,
    internships:    document.getElementById("internships").value,
    projects:       document.getElementById("projects").value,
    aptitude_score: document.getElementById("aptitude_score").value,
    communication_score: ...,
    work_experience: ...,
  };

  startScan();  // AI scan animation chalu

  // 2. Flask server ko bhejo
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  // 3. Result lo aur dikhao
  const result = await response.json();
  gaugeFill.style.strokeDashoffset = ...;  // ring bharo
  countUp(probText, result.probability);   // % count-up
  if (result.probability >= 50) fireConfetti();  // celebration
});""", size=11)

add_panel(s, Inches(7.9), Inches(1.8), Inches(4.8), Inches(5.2))
add_text(s, Inches(8.2), Inches(2.0), Inches(4.3), Inches(0.5),
         "3 Steps Me", size=20, bold=True, color=CYAN)
js_steps = [
    ("data object — sab fields collect", PURPLE),
    ("fetch() — server ko JSON bhejta hai", PINK),
    ("await — response ka wait karta hai", GREEN),
    ("result.prediction — Placed/Not", YELLOW),
    ("result.probability — % chance", CYAN),
    ("startScan() — AI scan animation", PINK),
    ("countUp() — % smooth badhta hai", PURPLE),
    ("fireConfetti() — celebration!", GREEN),
]
y = Inches(2.7)
for text, color in js_steps:
    add_text(s, Inches(8.2), y, Inches(4.3), Inches(0.45), "•  " + text, size=13, color=color)
    y += Inches(0.5)

# ============================================================
# SLIDE 15 — How to Run + Deploy
# ============================================================
s = add_slide()
slide_header(s, "\u25B6\uFE0F Kaise Chalayein aur Deploy Karein", "2 command me website apne computer par", accent=GREEN)

add_panel(s, Inches(0.6), Inches(1.85), Inches(6.0), Inches(5.0))
add_text(s, Inches(0.9), Inches(2.05), Inches(5.5), Inches(0.5),
         "Computer Par Chalane Ka", size=20, bold=True, color=GREEN)
add_code_box(s, Inches(0.9), Inches(2.7), Inches(5.4), Inches(1.6),
             "# Step 1 — model train (ek baar)\npython train_model.py\n\n# Step 2 — website chalao\npython app.py", size=13)
add_text(s, Inches(0.9), Inches(4.5), Inches(5.4), Inches(2.0),
         "Phir browser me kholo: http://127.0.0.1:5000\n\n"
         "Dusre device (same WiFi) ke liye:\n"
         "Terminal me jo IP print hota hai wahi use karo.\n\n"
         "Credentials: vikas yadav / pit jaunpur",
         size=13, color=SOFT, line_spacing=1.35)

add_panel(s, Inches(6.9), Inches(1.85), Inches(5.8), Inches(5.0))
add_text(s, Inches(7.2), Inches(2.05), Inches(5.3), Inches(0.5),
         "Free Deploy (Render.com)", size=20, bold=True, color=CYAN)
add_code_box(s, Inches(7.2), Inches(2.7), Inches(5.2), Inches(2.3),
             "# Build command\npip install -r requirements.txt\n\n# Start command\ngunicorn app:app --bind 0.0.0.0:$PORT\n\n# Instance: Free", size=12)
add_text(s, Inches(7.2), Inches(5.2), Inches(5.2), Inches(1.4),
         "GitHub → Render → Web Service → repo select → Deploy.\n"
         "Free plan: 15 min idle par website so jati hai (cold start).",
         size=13, color=SOFT, line_spacing=1.3)

# ============================================================
# SLIDE 16 — Features Summary
# ============================================================
s = add_slide()
slide_header(s, "\u2728 Website ki Khaas Baatein", "Ek line me: simple code + tagda ML + zabardast animations", accent=PINK)

feat_left = [
    ("\U0001F9E0 ML Powered — Random Forest (87% accuracy)", PURPLE),
    ("\U0001F512 Login Security — session + decorator", PINK),
    ("\U0001F3AF 8 Features se accurate prediction", CYAN),
    ("\U0001F4CA Neon gauge + count-up percentage", GREEN),
    ("\U0001F389 Confetti celebration (Placed ho to)", YELLOW),
    ("\U0001F50D AI scan animation (predict karte waqt)", CYAN),
]
feat_right = [
    ("\U0001F3A8 15+ custom CSS animations", PINK),
    ("\U0001F5B1 Custom neon cursor (dot + ring)", PURPLE),
    ("\U0001F4A8 Glassmorphism + 3D tilt card", GREEN),
    ("\U0001F680 Zero external libraries — pure CSS/JS", YELLOW),
    ("\U0001F4F1 Mobile friendly + reduced motion support", CYAN),
    ("\U0001F310 Deploy ready — Render free hosting", PINK),
]
add_bullet_block(s, Inches(0.7), Inches(2.0), Inches(6.0), feat_left, size=15, gap=0.62)
add_bullet_block(s, Inches(6.9), Inches(2.0), Inches(6.0), feat_right, size=15, gap=0.62)

add_panel(s, Inches(0.6), Inches(5.9), Inches(12.1), Inches(1.1))
add_text(s, Inches(0.9), Inches(6.05), Inches(11.5), Inches(0.8),
         "Total Code: app.py (119 lines) + train_model.py (89) + index.html (118) + login.html (271) + style.css (868) + script.js (593)  ≈  2000+ lines — sab handwritten, koi library nahi!",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ============================================================
# SLIDE 17 — Thank You
# ============================================================
s = add_slide()
glow = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(2.2),
                          Inches(8.9), Inches(3.1))
glow.fill.solid()
glow.fill.fore_color.rgb = RGBColor(14, 14, 40)
glow.line.color.rgb = CYAN
glow.line.width = Pt(1.5)
glow.shadow.inherit = False
try:
    glow.adjustments[0] = 0.1
except Exception:
    pass

add_text(s, Inches(2.2), Inches(2.6), Inches(8.9), Inches(1.0),
         "Thank You!", size=48, bold=True, color=CYAN, align=PP_ALIGN.CENTER)
add_text(s, Inches(2.2), Inches(3.7), Inches(8.9), Inches(0.6),
         "Koi sawaal ho to poochh lo  \U0001F642", size=20, color=PURPLE, align=PP_ALIGN.CENTER)
add_text(s, Inches(2.2), Inches(4.45), Inches(8.9), Inches(0.5),
         "Placement Predictor  •  Created by Vikas Yadav", size=16, bold=True,
         color=PINK, align=PP_ALIGN.CENTER)

# ---------- Save ----------
out = "Placement_Predictor_Presentation.pptx"
prs.save(out)
print(f"PPT ban gaya: {out}")
print(f"Slides: {len(prs.slides)}")
