from flask import Flask, render_template, request

app = Flask(__name__)

def estimate_rank_percentile(marks):
    top_ranks = {
        686: 1,
        685: 5,
        684: 10,
        683: 15,
        682: 25,
        681: 35,
        680: 50,
        679: 70,
        678: 90,
        677: 120,
        676: 160
    }

    top_score = 686
    total_candidates = 2300000  # Update as per NEET 2025 stats

    if marks in top_ranks:
        rank = top_ranks[marks]
    elif marks >= 670:
        rank = int(200 + (686 - marks) * 80)
    elif marks >= 630:
        rank = int(1200 + (670 - marks) * 150)
    elif marks >= 580:
        rank = int(4000 + (630 - marks) * 300)
    elif marks >= 530:
        rank = int(9000 + (580 - marks) * 600)
    elif marks >= 480:
        rank = int(18000 + (530 - marks) * 1000)
    elif marks >= 400:
        rank = int(33000 + (480 - marks) * 1200)
    elif marks >= 300:
        rank = int(50000 + (400 - marks) * 1500)
    elif marks >= 200:
        rank = int(70000 + (300 - marks) * 1800)
    elif marks >= 100:
        rank = int(100000 + (200 - marks) * 2000)
    else:
        rank = int(140000 + (100 - marks) * 3000)

    rank = min(max(rank, 1), total_candidates)
    percentile = round(((total_candidates - rank) / total_candidates) * 100, 3)

    return rank, percentile


@app.route('/')
def index():
    return render_template('index.html')

def predict_college(rank, category):
    # Dummy example logic — you can refine it based on real cutoffs later
    if rank <= 1000:
        return ["AIIMS Delhi", "JIPMER Puducherry"]
    elif rank <= 5000:
        return ["Maulana Azad Medical College", "CMC Vellore"]
    elif rank <= 15000:
        return ["BHU Varanasi", "KGMU Lucknow"]
    elif rank <= 25000:
        return ["BJMC Pune", "GMC Nagpur"]
    elif rank <= 40000:
        return ["ESIC Medical College", "Government Medical Colleges (State)"]
    else:
        return ["Private Medical Colleges", "Deemed Universities"]


@app.route('/predict', methods=['POST'])
def predict():
    marks = int(request.form['marks'])
    category = request.form['category'].strip().upper()

    # Calculate rank and percentile
    rank, percentile = estimate_rank_percentile(marks)

    # Category-wise cutoff (you can fine-tune values as needed)
    cutoffs = {
    "General": 145,
    "OBC": 125,
    "SC": 125,
    "ST": 125,
    "EWS": 125
}

    cutoff = cutoffs.get(category, 145)
    not_qualified = marks < cutoff

    # Predicted colleges
    colleges = predict_college(rank, category) if not not_qualified else []

    return render_template("result.html", 
        marks=marks, 
        category=category,
        rank=rank, 
        percentile=percentile, 
        cutoff=cutoff, 
        not_qualified=not_qualified,
        colleges=colleges
    )


if __name__ == '__main__':
    app.run(debug=True)
