# Project Notes — Placement Predictor

> Ye file humari poori baat-cheet ka summary hai. Jab bhi kuch yaad karna ho, ye khol lo!

## 🌐 Ye website kya hai
Student ki details (10th %, 12th %, CGPA, internships, projects, aptitude, communication, work experience) se
**Machine Learning model** predict karta hai ki placement hoga ya nahi — aur kitne % chance hain.

## 📁 Important files
| File | Kaam |
|------|------|
| `app.py` | Flask website ka main code |
| `train_model.py` | Model train karta hai (placement_data.csv se) |
| `model.pkl` | Trained ML model (RandomForest) |
| `templates/index.html` | Website ka design (isme corner me "Created by Vikas Yadav" hai) |
| `static/style.css` | Website ka styling |
| `static/script.js` | Form ka JavaScript |
| `requirements.txt` | Zaroori packages (exact versions ke saath) |
| `runtime.txt` | Python 3.13.7 (server ke liye) |
| `sorts/` | Alag project — C sorting programs (bubble, insertion, quick, heap, merge) |

## ▶️ Website apne computer par chalane ka tareeka
```bash
python app.py
```
Phir browser me: **http://127.0.0.1:5000**

## 📱 Dusre computer/phone par (same WiFi)
- `app.py` ab `host="0.0.0.0"` par chalta hai — dusre devices connect kar sakte hain
- Chalane par terminal me **network IP** print hota hai (jaise `http://192.168.x.x:5000`) — wahi dusre device me kholo
- Pehli baar **Windows Firewall popup** aaye to "Allow access" dabana
- Nahi khule to **mobile hotspot** try karo (college WiFi par devices block hote hain)

## 🎨 Design — TAGDA version (October 2026)
- Dark animated background: floating glowing orbs (mouse parallax ke saath) + particle network + **shooting stars**
- Glassmorphism card jo mouse ke saath **3D tilt** hota hai (glare light effect ke saath)
- Title ke letters ek-ek karke uchhal ke aate hain + subtitle **typewriter** effect
- Magnetic button (cursor ki taraf khichta hai) + click par ripple
- Result me **circular neon gauge** (ring bharti hai) + % count-up + confetti barish + center blast
- "Created by Vikas Yadav" — **neon sign** jaisa flicker + gradient + sparkle ✦
- Sab kuch pure CSS + vanilla JS — koi external library nahi
- Files: `templates/index.html`, `static/style.css`, `static/script.js`

## ✨ UNIQUE animations (October 2026 — "kuch alag banao")
1. **Custom neon cursor** — glowing dot jo cursor turant follow karta hai + peeche ek ring lerp
   (dhire-dhire) saath chalti hai; button/input par hover karne par ring 56px tak badh jati hai.
   Sirf desktop (hover-capable) par; mobile/touch aur reduced-motion users ko native cursor milta hai.
2. **⚡ Profile Power Bar** — header ke neeche progress bar. Jitni fields bharo, utna % badhta hai;
   har field bharne par label ke saath green **✓** tick uchhal ke aata hai. 100% par bar flash karta
   hai aur Predict button ki glow tez ho jati hai (`button.charged`).
3. **AI Scan line** — "Predict Karo" click karte hi card par ek cyan **scan line** upar se neeche
   sweep karti hai, aur har field uske guzarne par 520ms ke liye cyan glow karke highlight hota hai
   (jaise AI data scan kar raha ho). Card ki border bhi cyan glow karti hai.
4. **Thinking equalizer** — sochne ke waqt button ka text **5-bar audio equalizer** ban jata hai
   (bouncing bars) + "Soch rahe hain...". Kam se kam 1.6s animation chalti hai taaki effect dikhe.
5. **Hologram glitch reveal** — result box aate waqt 0.75s ka **glitch** (RGB split, clip-path
   bands, hue-rotate) chalta hai, phir settle hota hai. Confetti + gauge uske baad.
- Sab me `prefers-reduced-motion` ka respect — kam motion wale users ko sab kuch seedha milta hai.

## ✅ Jo kaam ho chuka hai (September 2026)
1. ✔️ `host="0.0.0.0"` add kiya — dusre devices ke liye
2. ✔️ Deployment files banayi: `requirements.txt` me exact versions + gunicorn, `runtime.txt`, `.gitignore`
3. ✔️ Website corner me credit: **"Created by Vikas Yadav"** (bottom-right, `templates/index.html` line 65)
4. ✔️ Git setup: commit `eb90e49` (author: Vikas Yadav <vikasyadavdharmapur70@gmail.com>)
5. ✔️ GitHub par push: **github.com/vikasyadavdharmapur70-boop/placement-predictor-**

## 🚀 Ab bacha hai: Render par deploy (free hosting)
> Deploy files ready hain (requirements.txt, runtime.txt, .gitignore, model.pkl repo me hai).
1. **render.com** → **Sign up with GitHub**
2. **New +** → **Web Service** → repo select karo (`placement-predictor-`)
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Instance type: **Free** → **Deploy**
6. 4-6 min me link milega: `https://placement-predictor-xxxx.onrender.com`

### Deploy se judi baatein
- ⚠️ `model.pkl` GitHub repo me hai — server par wahi load hota hai, isliye scikit-learn version bilkul same chahiye (isliye requirements.txt me pin kiya hai)
- 😴 Free plan: website 15 min idle hone par so jati hai — pehli request me 30-60 sec lagte hain
- 🔄 Aage code badlo to: `git add .` → `git commit -m "message"` → `git push` — Render khud dobara deploy kar dega

## 🔧 Aage ke ideas (jab time mile)
- Result ke saath bar chart / gauge
- GPT se career tips ka section
- Custom domain (jaise `placement.site`)
- Database me predictions save karna
