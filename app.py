from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# =======================
# DEFICIENCY DATABASE
# =======================
deficiency_db = {
    "Iron Deficiency": {
        "symptoms": ["fatigue", "hairfall", "pale skin", "weak immunity"],
        "foods": ["Spinach", "Jaggery", "Dates", "Beetroot", "Ragi", "Rajma",
                  "Chana", "Pomegranate", "Apple", "Anjeer", "Fenugreek",
                  "Amaranth", "Black Sesame", "Peas", "Soybean", "Tofu",
                  "Groundnut", "Red Rice", "Drumstick", "Broccoli"],
        "lifestyle": "Pair iron foods with vitamin C (lemon, amla) for better absorption. Avoid tea/coffee 1 hour after meals."
    },
    "Calcium Deficiency": {
        "symptoms": ["bone pain", "muscle cramps", "weak bones"],
        "foods": ["Milk", "Curd", "Paneer", "Ragi", "Sesame Seeds", "Almonds",
                  "Walnuts", "Soy Milk", "Tofu", "Broccoli", "Okra", "Figs",
                  "Chia Seeds", "Moringa", "Cheese", "Yogurt", "Cabbage"],
        "lifestyle": "15–20 min of morning sun exposure for vitamin D helps calcium absorption. Daily walking strengthens bones."
    },
    "Vitamin D Deficiency": {
        "symptoms": ["back pain", "low immunity", "fatigue"],
        "foods": ["Mushroom (sun-dried)", "Fortified Milk", "Egg Yolk", "Fortified Cereals"],
        "lifestyle": "Get 15–20 minutes of direct morning sunlight daily on arms and face. This is the primary natural source."
    },
    "Protein Deficiency": {
        "symptoms": ["muscle loss", "weakness", "slow recovery"],
        "foods": ["Dal", "Chana", "Eggs", "Milk", "Paneer", "Soybean", "Tofu", "Peanuts",
                  "Rajma", "Moong", "Masoor", "Chickpeas", "Greek Yogurt"],
        "lifestyle": "Include a protein source in every meal. Spread intake across the day rather than in one large meal."
    },
    "Vitamin B12 Deficiency": {
        "symptoms": ["memory loss", "fatigue", "tingling hands"],
        "foods": ["Milk", "Curd", "Eggs", "Cheese", "Fortified Cereals", "Nutritional Yeast"],
        "lifestyle": "Vegetarians are at higher risk. Get blood levels checked annually. Supplement if needed with doctor guidance."
    }
}

# =======================
# VITAMIN & MINERAL ENCYCLOPEDIA
# Comprehensive reference: RDA, deficiency signs, Indian food
# sources, absorption tips, and curated learning resources.
# =======================
nutrient_db = [
    {
        "key": "vitamin-a", "name": "Vitamin A", "category": "vitamin",
        "also_known": "Retinol / Beta-Carotene",
        "icon": "👁️", "icon_bg": "background:linear-gradient(135deg,#f59e0b,#b45309);",
        "rda": "700–900 mcg/day (adults)",
        "short": "Supports vision, immune function, and skin health.",
        "long": "Vitamin A is essential for low-light and colour vision, maintains the skin and mucous membrane barrier against infection, and supports immune cell function. It exists as retinol (animal foods) and beta-carotene (plant foods), which the body converts as needed.",
        "deficiency_signs": ["Night blindness", "Dry eyes", "Frequent infections", "Dry, rough skin", "Slow wound healing"],
        "foods": ["Carrot", "Sweet Potato", "Spinach", "Mango", "Papaya", "Pumpkin", "Egg Yolk", "Milk", "Red Bell Pepper", "Amaranth Leaves"],
        "tip": "Beta-carotene absorbs best with a little fat — cook carrots or spinach with a teaspoon of ghee or oil.",
        "video": "https://www.youtube.com/embed/X2tDtpkbWE4",
        "official_name": "NIH — Vitamin A Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/VitaminA-Consumer/",
        "official_desc": "Office of Dietary Supplements consumer fact sheet on Vitamin A."
    },
    {
        "key": "vitamin-b1", "name": "Vitamin B1 (Thiamine)", "category": "vitamin",
        "also_known": "Thiamine",
        "icon": "⚡", "icon_bg": "background:linear-gradient(135deg,#c8862a,#9c6418);",
        "rda": "1.1–1.2 mg/day",
        "short": "Helps convert food into cellular energy and supports nerve function.",
        "long": "Thiamine is a coenzyme in carbohydrate metabolism, helping turn the food you eat into usable energy. It's also needed for healthy nerve signalling, which is why severe deficiency (beriberi) causes nerve and heart problems.",
        "deficiency_signs": ["Fatigue", "Irritability", "Tingling in hands/feet", "Loss of appetite", "Confusion (severe cases)"],
        "foods": ["Whole Wheat", "Brown Rice", "Lentils (Dal)", "Peanuts", "Sunflower Seeds", "Green Peas", "Oats"],
        "tip": "Thiamine is lost in excess washing/boiling of rice and dal — use minimal water and don't over-rinse.",
        "video": "https://www.youtube.com/embed/8O7xVZK33-8",
        "official_name": "NIH — Thiamine Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/Thiamin-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin B1."
    },
    {
        "key": "vitamin-b3", "name": "Vitamin B3 (Niacin)", "category": "vitamin",
        "also_known": "Niacin",
        "icon": "🔥", "icon_bg": "background:linear-gradient(135deg,#c8862a,#9c6418);",
        "rda": "14–16 mg/day",
        "short": "Supports energy metabolism, skin health, and nervous system function.",
        "long": "Niacin helps enzymes convert carbohydrates, fats, and proteins into energy. It also supports DNA repair and healthy skin. Severe long-term deficiency causes pellagra (dermatitis, diarrhoea, dementia).",
        "deficiency_signs": ["Skin rashes/pigmentation", "Digestive upset", "Fatigue", "Mouth soreness", "Memory issues (severe)"],
        "foods": ["Peanuts", "Brown Rice", "Whole Wheat", "Mushrooms", "Green Peas", "Sesame Seeds", "Dates"],
        "tip": "Niacin from plant foods is well absorbed; pairing with B-complex-rich whole grains supports overall metabolism.",
        "video": "https://www.youtube.com/embed/8O7xVZK33-8",
        "official_name": "NIH — Niacin Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/Niacin-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin B3."
    },
    {
        "key": "vitamin-b6", "name": "Vitamin B6", "category": "vitamin",
        "also_known": "Pyridoxine",
        "icon": "🧠", "icon_bg": "background:linear-gradient(135deg,#c8862a,#9c6418);",
        "rda": "1.3–1.7 mg/day",
        "short": "Involved in brain development, mood regulation, and protein metabolism.",
        "long": "Vitamin B6 helps the body break down protein and is involved in producing neurotransmitters like serotonin and dopamine, which affect mood and sleep. It also supports red blood cell formation.",
        "deficiency_signs": ["Irritability/low mood", "Confusion", "Weakened immunity", "Cracked lips (cheilosis)", "Anemia"],
        "foods": ["Chickpeas (Chana)", "Banana", "Potato", "Brown Rice", "Spinach", "Watermelon", "Sunflower Seeds"],
        "tip": "B6 is water-soluble and heat-sensitive — lightly steam vegetables rather than over-boiling.",
        "video": "https://www.youtube.com/embed/AcvB-tUWXNs",
        "official_name": "NIH — Vitamin B6 Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/VitaminB6-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin B6."
    },
    {
        "key": "vitamin-b12", "name": "Vitamin B12", "category": "vitamin",
        "also_known": "Cobalamin",
        "icon": "🩸", "icon_bg": "background:linear-gradient(135deg,#c8862a,#9c6418);",
        "rda": "2.4 mcg/day",
        "short": "Essential for nerve function, red blood cell formation, and DNA synthesis.",
        "long": "Vitamin B12 is required to make healthy red blood cells and maintain the protective covering of nerves. It's found almost exclusively in animal products, which makes vegetarians and vegans a high-risk group for deficiency.",
        "deficiency_signs": ["Memory loss", "Fatigue", "Tingling in hands/feet", "Pale or jaundiced skin", "Mood changes"],
        "foods": ["Milk", "Curd", "Paneer", "Eggs", "Cheese", "Fortified Cereals", "Nutritional Yeast"],
        "tip": "Vegetarians should get B12 blood levels checked annually — diet alone often isn't enough without dairy/eggs or fortified foods.",
        "video": "https://www.youtube.com/embed/AcvB-tUWXNs",
        "official_name": "NIH — Vitamin B12 Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/VitaminB12-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin B12."
    },
    {
        "key": "vitamin-c", "name": "Vitamin C", "category": "vitamin",
        "also_known": "Ascorbic Acid",
        "icon": "🍊", "icon_bg": "background:linear-gradient(135deg,#f59e0b,#b45309);",
        "rda": "65–90 mg/day",
        "short": "Boosts immunity, aids iron absorption, and supports collagen production.",
        "long": "Vitamin C is a powerful antioxidant that supports immune defence, helps the body absorb non-heme (plant-based) iron more efficiently, and is required to build collagen for skin, blood vessels, and wound healing.",
        "deficiency_signs": ["Bleeding gums", "Slow wound healing", "Frequent colds", "Dry, rough skin", "Joint pain (severe)"],
        "foods": ["Amla (Indian Gooseberry)", "Orange", "Lemon", "Guava", "Bell Pepper", "Tomato", "Papaya", "Kiwi"],
        "tip": "Vitamin C is destroyed by heat — eat citrus fruits and amla raw or only lightly cooked.",
        "video": "https://www.youtube.com/embed/CqL2RxXJiqI",
        "official_name": "NIH — Vitamin C Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/VitaminC-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin C."
    },
    {
        "key": "vitamin-d", "name": "Vitamin D", "category": "vitamin",
        "also_known": "Calciferol / The Sunshine Vitamin",
        "icon": "☀️", "icon_bg": "background:linear-gradient(135deg,#f59e0b,#b45309);",
        "rda": "15–20 mcg (600–800 IU)/day",
        "short": "Vital for calcium absorption, bone strength, and immune regulation.",
        "long": "Vitamin D enables the gut to absorb calcium and phosphorus, making it essential for bone strength. It's mostly made in the skin via sunlight exposure rather than obtained from food, which is why deficiency is extremely common, even in sunny countries, due to indoor lifestyles.",
        "deficiency_signs": ["Bone/back pain", "Frequent illness", "Fatigue", "Muscle weakness", "Mood changes"],
        "foods": ["Mushroom (sun-dried)", "Fortified Milk", "Egg Yolk", "Fortified Cereals"],
        "tip": "15–20 minutes of midday sun on arms and face, a few times a week, is the primary natural source — food alone rarely covers it.",
        "video": "https://www.youtube.com/embed/9Wd1eVHkjpE",
        "official_name": "NIH — Vitamin D Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/VitaminD-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin D."
    },
    {
        "key": "vitamin-e", "name": "Vitamin E", "category": "vitamin",
        "also_known": "Tocopherol",
        "icon": "🌻", "icon_bg": "background:linear-gradient(135deg,#f59e0b,#b45309);",
        "rda": "15 mg/day",
        "short": "Antioxidant that protects cells and supports skin and eye health.",
        "long": "Vitamin E protects cell membranes from oxidative damage, supports immune function, and contributes to skin elasticity and eye health. It's fat-soluble, so it's best absorbed alongside dietary fat.",
        "deficiency_signs": ["Muscle weakness", "Vision problems", "Dry/rough skin", "Weakened immunity"],
        "foods": ["Almonds", "Sunflower Seeds", "Peanuts", "Spinach", "Avocado", "Wheat Germ", "Mustard Oil"],
        "tip": "Lightly roasted nuts and seeds preserve more vitamin E than deep-fried versions.",
        "video": "https://www.youtube.com/embed/X2tDtpkbWE4",
        "official_name": "NIH — Vitamin E Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/VitaminE-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin E."
    },
    {
        "key": "vitamin-k", "name": "Vitamin K", "category": "vitamin",
        "also_known": "Phylloquinone",
        "icon": "🩹", "icon_bg": "background:linear-gradient(135deg,#f59e0b,#b45309);",
        "rda": "90–120 mcg/day",
        "short": "Essential for normal blood clotting and bone metabolism.",
        "long": "Vitamin K activates proteins needed for blood clotting, preventing excess bleeding from cuts and injuries. It also plays a supporting role in bone mineralisation alongside calcium and vitamin D.",
        "deficiency_signs": ["Easy bruising", "Excess bleeding from cuts", "Bleeding gums", "Heavy menstrual bleeding"],
        "foods": ["Spinach", "Broccoli", "Cabbage", "Mustard Greens", "Fenugreek Leaves", "Cauliflower"],
        "tip": "Vitamin K is fat-soluble — a drizzle of oil or ghee with leafy greens improves absorption.",
        "video": "https://www.youtube.com/embed/X2tDtpkbWE4",
        "official_name": "NIH — Vitamin K Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/VitaminK-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Vitamin K."
    },
    {
        "key": "calcium", "name": "Calcium", "category": "mineral",
        "also_known": "Ca",
        "icon": "🦴", "icon_bg": "background:linear-gradient(135deg,#40916c,#1b4332);",
        "rda": "1000–1200 mg/day",
        "short": "Builds and maintains strong bones and teeth; supports muscle and nerve function.",
        "long": "Calcium is the most abundant mineral in the body, stored mainly in bones and teeth. Beyond skeletal strength, it's needed for muscle contraction (including the heartbeat) and nerve signal transmission. The body draws calcium from bones if dietary intake is too low, weakening them over time.",
        "deficiency_signs": ["Bone pain", "Muscle cramps", "Weak/brittle bones", "Brittle nails", "Numbness/tingling"],
        "foods": ["Milk", "Curd", "Paneer", "Ragi", "Sesame Seeds", "Almonds", "Tofu", "Broccoli", "Figs", "Moringa"],
        "tip": "Pair calcium-rich foods with 15–20 minutes of morning sunlight — vitamin D is required for the gut to actually absorb calcium.",
        "video": "https://www.youtube.com/embed/3o7valt2A1k",
        "official_name": "ICMR-NIN — Dietary Guidelines for Indians",
        "official_url": "https://www.nin.res.in/",
        "official_desc": "Official RDA tables and dietary guidance from India's National Institute of Nutrition."
    },
    {
        "key": "iron", "name": "Iron", "category": "mineral",
        "also_known": "Fe",
        "icon": "🩸", "icon_bg": "background:linear-gradient(135deg,#40916c,#1b4332);",
        "rda": "8–18 mg/day (higher for menstruating women)",
        "short": "Carries oxygen in the blood; deficiency is one of the most common globally.",
        "long": "Iron is a core component of haemoglobin, the protein in red blood cells that carries oxygen from your lungs to the rest of the body. Without enough iron, the body can't make enough healthy red blood cells, leading to iron-deficiency anaemia — the most common nutritional deficiency worldwide.",
        "deficiency_signs": ["Fatigue", "Hair fall", "Pale skin", "Weak immunity", "Shortness of breath", "Dizziness"],
        "foods": ["Spinach", "Jaggery", "Dates", "Beetroot", "Ragi", "Rajma", "Chana", "Pomegranate", "Fenugreek", "Sesame Seeds"],
        "tip": "Pair iron-rich foods with vitamin C (lemon, amla, tomato) to boost absorption, and avoid tea/coffee within an hour of meals — tannins block iron uptake.",
        "video": "https://www.youtube.com/embed/CDjPNTjJzv8",
        "official_name": "WHO — Iron Deficiency Anaemia",
        "official_url": "https://www.who.int/news-room/fact-sheets/detail/anaemia",
        "official_desc": "World Health Organization fact sheet on anaemia and iron deficiency."
    },
    {
        "key": "zinc", "name": "Zinc", "category": "mineral",
        "also_known": "Zn",
        "icon": "🛡️", "icon_bg": "background:linear-gradient(135deg,#40916c,#1b4332);",
        "rda": "8–11 mg/day",
        "short": "Supports immune function, wound healing, and taste/smell perception.",
        "long": "Zinc is involved in hundreds of enzyme reactions, supports immune cell production, helps wounds heal, and is needed for normal taste and smell. It also plays a role in growth and development, particularly important in children.",
        "deficiency_signs": ["Frequent infections", "Slow wound healing", "Loss of taste/smell", "Hair thinning", "Poor appetite"],
        "foods": ["Pumpkin Seeds", "Chickpeas", "Cashews", "Yogurt", "Whole Grains", "Sesame Seeds", "Peanuts"],
        "tip": "Soaking or sprouting legumes and grains before cooking reduces phytates, which otherwise block zinc absorption.",
        "video": "https://www.youtube.com/embed/CqL2RxXJiqI",
        "official_name": "NIH — Zinc Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/Zinc-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Zinc."
    },
    {
        "key": "magnesium", "name": "Magnesium", "category": "mineral",
        "also_known": "Mg",
        "icon": "💪", "icon_bg": "background:linear-gradient(135deg,#40916c,#1b4332);",
        "rda": "310–420 mg/day",
        "short": "Supports muscle/nerve function, energy production, and bone health.",
        "long": "Magnesium is involved in over 300 enzymatic reactions, including energy production, muscle relaxation, and nerve signalling. It also works alongside calcium and vitamin D for bone health, and low levels are linked to cramps, fatigue, and poor sleep.",
        "deficiency_signs": ["Muscle cramps/twitches", "Fatigue", "Poor sleep", "Irregular heartbeat (severe)", "Irritability"],
        "foods": ["Spinach", "Almonds", "Cashews", "Whole Grains", "Bananas", "Dark Chocolate", "Black Beans"],
        "tip": "Cooking leafy greens lightly (steaming, not boiling away the water) preserves more magnesium than deep boiling.",
        "video": "https://www.youtube.com/embed/8O7xVZK33-8",
        "official_name": "NIH — Magnesium Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/Magnesium-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Magnesium."
    },
    {
        "key": "potassium", "name": "Potassium", "category": "mineral",
        "also_known": "K",
        "icon": "❤️", "icon_bg": "background:linear-gradient(135deg,#40916c,#1b4332);",
        "rda": "2600–3400 mg/day",
        "short": "Regulates fluid balance, nerve signals, and healthy blood pressure.",
        "long": "Potassium helps balance fluids inside and outside cells, supports normal nerve and muscle function (including the heart), and helps counteract sodium's effect on blood pressure. It's lost through sweat, so needs rise with heat and activity.",
        "deficiency_signs": ["Muscle weakness", "Cramps", "Fatigue", "Irregular heartbeat (severe)", "Constipation"],
        "foods": ["Banana", "Coconut Water", "Potato", "Spinach", "Sweet Potato", "Curd", "Beans", "Orange"],
        "tip": "Coconut water and buttermilk (chaas) are quick, natural ways to replenish potassium lost through sweating in hot weather.",
        "video": "https://www.youtube.com/embed/Hu1plUSXcKY",
        "official_name": "NIH — Potassium Fact Sheet",
        "official_url": "https://ods.od.nih.gov/factsheets/Potassium-Consumer/",
        "official_desc": "Office of Dietary Supplements fact sheet on Potassium."
    },
    {
        "key": "iodine", "name": "Iodine", "category": "mineral",
        "also_known": "I",
        "icon": "🦋", "icon_bg": "background:linear-gradient(135deg,#40916c,#1b4332);",
        "rda": "150 mcg/day",
        "short": "Required to make thyroid hormones, which regulate metabolism.",
        "long": "Iodine is essential for the thyroid gland to produce hormones that regulate metabolism, growth, and brain development. It's especially critical during pregnancy for fetal brain development. Iodised salt programs have made severe deficiency rare, but mild deficiency still occurs.",
        "deficiency_signs": ["Goitre (neck swelling)", "Fatigue", "Weight gain", "Cold sensitivity", "Developmental issues in children"],
        "foods": ["Iodised Salt", "Milk", "Curd", "Eggs", "Seaweed (where available)", "Fish"],
        "tip": "Use iodised salt for cooking and add it after cooking rather than during prolonged boiling, since iodine can be lost to heat over time.",
        "video": "https://www.youtube.com/embed/9Wd1eVHkjpE",
        "official_name": "WHO — Iodine Deficiency",
        "official_url": "https://www.who.int/news-room/fact-sheets/detail/micronutrients",
        "official_desc": "World Health Organization fact sheet on micronutrient deficiencies including iodine."
    },
]

nutrient_db_by_key = {n["key"]: n for n in nutrient_db}



# =======================
# HOME PAGE
# =======================
@app.route("/")
def index():
    return render_template("index.html")

# =======================
# HEALTH ANALYSIS FORM
# =======================
@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    name   = request.form.get("name", "Guest")
    height = float(request.form.get("height", 170))
    weight = float(request.form.get("weight", 65))
    symptoms = request.form.getlist("symptoms")

    bmi = round(weight / ((height / 100) ** 2), 2)

    detected = []
    for d, info in deficiency_db.items():
        if any(s in info["symptoms"] for s in symptoms):
            detected.append(d)

    return render_template(
        "result.html",
        name=name,
        bmi=bmi,
        detected=detected,
        db=deficiency_db
    )

# =======================
# DASHBOARD
# =======================
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    name = request.form.get("name", "User") if request.method == "POST" else "User"
    return render_template("dashboard.html", name=name)

# =======================
# SYMPTOMS & DEFICIENCY
# =======================
@app.route("/symptoms")
def symptoms():
    all_symptoms = sorted({s for d in deficiency_db.values() for s in d["symptoms"]})
    return render_template("symptoms.html", symptoms=all_symptoms)

@app.route("/deficiency")
def deficiency():
    return render_template("deficiency.html", deficiencies=deficiency_db)

# =======================
# BMI PAGE
# =======================
@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    bmi_value = None
    category = None
    if request.method == "POST":
        h = float(request.form["height"])
        w = float(request.form["weight"])
        bmi_value = round(w / ((h / 100) ** 2), 2)
        if bmi_value < 18.5:
            category = "Underweight"
        elif bmi_value < 25:
            category = "Normal"
        elif bmi_value < 30:
            category = "Overweight"
        else:
            category = "Obese"
    return render_template("bmi.html", bmi=bmi_value, category=category)

# =======================
# HAIR CARE
# =======================
@app.route("/haircare")
def haircare():
    return render_template("haircare.html")

# =======================
# SKIN CARE
# =======================
@app.route("/skincare")
def skincare():
    return render_template("skincare.html")

# =======================
# WEIGHT LOSS
# =======================
@app.route("/weightloss", methods=["GET", "POST"])
def weightloss():
    plan = None
    if request.method == "POST":
        plan = {
            "tips": "Low calorie diet, walking 30 min daily, yoga",
            "foods": ["Green Salad", "Dal", "Brown Rice", "Curd", "Oats",
                      "Moong Dal", "Cucumber", "Lemon Water", "Sprouts"],
            "video": "https://www.youtube.com/embed/UBMk30rjy0o"
        }
    return render_template("weightloss.html", plan=plan)

# =======================
# WEIGHT GAIN
# =======================
@app.route("/weightgain", methods=["GET", "POST"])
def weightgain():
    plan = None
    if request.method == "POST":
        plan = {
            "tips": "Calorie-rich nutritious foods, strength training",
            "foods": ["Milk", "Paneer", "Rice", "Dal", "Dry Fruits",
                      "Banana", "Peanut Butter", "Ghee", "Chana", "Eggs"],
            "video": "https://www.youtube.com/embed/1skBf6h2ksI"
        }
    return render_template("weightgain.html", plan=plan)

# =======================
# FEEDBACK
# =======================
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    submitted = request.method == "POST"
    return render_template("feedback.html", submitted=submitted)

# =======================
# SEASONAL FOOD GUIDE
# =======================
@app.route("/seasonal")
def seasonal():
    return render_template("seasonal.html")

# =======================
# VEGETARIAN PROTEIN CALCULATOR
# =======================
@app.route("/protein")
def protein():
    return render_template("protein.html")

# =======================
# HOME WORKOUT PLANNER
# =======================
@app.route("/workout")
def workout():
    return render_template("workout.html")

# =======================
# YOGA FOR DEFICIENCIES
# =======================
@app.route("/yoga")
def yoga():
    return render_template("yoga.html")

# =======================
# STEP GOAL TRACKER
# =======================
@app.route("/steps")
def steps():
    return render_template("steps.html")

# =======================
# IMMUNITY BOOSTER RECIPES
# =======================
@app.route("/immunity")
def immunity():
    return render_template("immunity.html")

# =======================
# VITAMIN & MINERAL ENCYCLOPEDIA
# =======================
@app.route("/nutrients")
def nutrients():
    return render_template(
        "nutrients.html",
        nutrients=nutrient_db,
        nutrients_json=json.dumps(nutrient_db)
    )

@app.route("/resources")
def resources():
    return render_template("resources.html")

# =======================
if __name__ == "__main__":
    app.run(debug=True)
