from flask import Flask, render_template, request

app = Flask(__name__)

def estimate_rank_percentile(marks):
    top_ranks = {
        720: 1,
        719: 3,
        718: 6,
        717: 10,
        716: 14,
        715: 20,
        714: 28,
        713: 37,
        712: 47,
        711: 58,
        710: 70
    }

    total_candidates = 2090000  # Based on NEET 2023 stats

    if marks in top_ranks:
        rank = top_ranks[marks]
    elif marks >= 700:
        rank = int(100 + (710 - marks) * 80)
    elif marks >= 650:
        rank = int(1000 + (700 - marks) * 150)
    elif marks >= 600:
        rank = int(2500 + (650 - marks) * 300)
    elif marks >= 550:
        rank = int(7500 + (600 - marks) * 600)
    elif marks >= 500:
        rank = int(15000 + (550 - marks) * 1000)
    elif marks >= 400:
        rank = int(30000 + (500 - marks) * 1200)
    elif marks >= 300:
        rank = int(45000 + (400 - marks) * 1500)
    elif marks >= 200:
        rank = int(60000 + (300 - marks) * 1800)
    elif marks >= 100:
        rank = int(90000 + (200 - marks) * 2000)
    else:
        rank = int(130000 + (100 - marks) * 3000)

    # Ensure rank is not more than total candidates
    rank = min(max(rank, 1), total_candidates)

    # Percentile estimation
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
        "General": 137,
        "OBC": 107,
        "SC": 107,
        "ST": 107,
        "EWS": 120
    }

    cutoff = cutoffs.get(category, 137)
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
