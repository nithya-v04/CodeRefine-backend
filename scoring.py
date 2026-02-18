def calculate_score(review):
    penalty = (
        len(review["bugs"]) * 5 +
        len(review["security"]) * 7 +
        len(review["performance"]) * 3
    )
    return max(100 - penalty, 0)
