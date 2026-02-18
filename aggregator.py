from scoring import calculate_score

def aggregate(review):
    review["code_health_score"] = calculate_score(review)
    return review
