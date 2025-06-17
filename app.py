from flask import Flask, render_template, request

app = Flask(__name__)

def estimate_rank_percentile(marks):
    total_candidates = 2035851  # From NTA 2025 data

    # Handle marks above top range
    if marks >= 686:
        return 1, 100.0

    marks_rank_map = [
        (686, 1), (682, 2), (681, 3), (678, 8), (650, 77),
        (635, 170), (630, 250), (622, 412), (609, 845),
        (607, 981), (601, 1302), (589, 2341), (577, 4000),
        (571, 5123), (563, 7296), (549, 12860),
        (540, 17370), (528, 25541), (525, 27698), (515, 36843),
        (481, 76510), (478, 80336), (459, 107944),
        (435, 146846), (402, 206050), (398, 213371),
        (302, 436777), (257, 577330), (228, 684232),
        (172, 937041), (135, 1152192), (104, 1391647),
        (69, 1717603), (35, 2035851)
    ]

    for i in range(len(marks_rank_map) - 1):
        high_marks, high_rank = marks_rank_map[i]
        low_marks, low_rank = marks_rank_map[i + 1]

        if high_marks >= marks >= low_marks:
            rank = int(high_rank + ((high_marks - marks) / (high_marks - low_marks)) * (low_rank - high_rank))
            break
    else:
        rank = total_candidates

    percentile = round(((total_candidates - rank) / total_candidates) * 100, 3)
    return rank, percentile

def predict_college(rank):
    colleges = [
        (47, "All India Institute of Medical Sciences (AIIMS)"),
        (87, "Maulana Azad Medical College (MAMC)"),
        (129, "VMMC & Safdarjung Hospital"),
        (277, "JIPMER"),
        (567, "Lady Hardinge Medical College"),
        (781, "Seth GS Medical College"),
        (1007, "IMS-BHU"),
        (1529, "KGMU"),
        (2372, "BMCRI"),
        (5000, "JSS Medical College"),
        (10000, "Christian Medical College (CMC)"),
        (15000, "Kasturba Medical College (KMC)"),
        (20000, "Sri Ramachandra Medical College"),
        (25000, "St. John's National Academy of Health Sciences"),
        (30000, "HIMSR"),
        (35000, "Amrita School of Medicine"),
        (40000, "Dr. D.Y. Patil Vidyapeeth"),
        (45000, "K.S. Hegde Medical Academy")
    ]

    predicted = [name for r, name in colleges if rank <= r]
    
    # Show default colleges if no match found
    if not predicted:
        predicted = ["Any Private Medical College", "Any Deemed University"]

    return predicted

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    marks = int(request.form['marks'])
    category = request.form['category'].strip().upper()

    rank, percentile = estimate_rank_percentile(marks)

    topper_note = "🏆 Topper! You scored Rank 1 in NEET 2025!" if rank == 1 else ""

    cutoffs = {
        "GENERAL": 144,
        "GENERAL-PH": 127,
        "OBC": 113,
        "SC": 113,
        "ST": 113,
        "EWS": 144,
        "SC/OBC-PH": 113,
        "ST-PH": 113
    }

    cutoff = cutoffs.get(category, 144)
    not_qualified = marks < cutoff
    colleges = predict_college(rank) if not not_qualified else []

    return render_template("result.html",
        marks=marks,
        category=category,
        rank=rank,
        percentile=percentile,
        cutoff=cutoff,
        not_qualified=not_qualified,
        colleges=colleges,
        topper_note=topper_note
    )

if __name__ == '__main__':
    app.run(debug=True)
