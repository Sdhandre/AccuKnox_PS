import requests
import matplotlib.pyplot as plt

#Assumed URL
API_URL = "https://api.assumed.com/student-scores"


def get_fallback_data():
    return [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 92},
        {"name": "Charlie", "score": 78},
        {"name": "David", "score": 88}
    ]

def fetch_student_scores():
    try:
        response = requests.get(API_URL, timeout=10)

        if response.status_code != 200:
            print("API failed, using assumed data")
            return get_fallback_data()

        data = response.json()

        if not isinstance(data, list):
            print("Invalid data format, using assumed data")
            return get_fallback_data()

        return data

    except Exception as e:
        print("API request failed:", e)
        print("Using assumed data")
        return get_fallback_data()

    
def clean_scores(data):

    names = []
    scores = []

    for record in data:
        name = record.get("name")
        score = record.get("score")

        if not name:
            continue

        if not isinstance(score, (int, float)):
            continue

        names.append(name)
        scores.append(score)

    return names, scores

def calculate_average(scores):

    if not scores:
        return 0

    return sum(scores) / len(scores)


def plot_scores(names, scores, average):
    plt.figure()
    plt.bar(names, scores)
    plt.xlabel("Students")
    plt.ylabel("Scores")
    plt.title(f"Student Test Scores (Average: {average:.2f})")
    plt.tight_layout()
    plt.show()


def main():

    raw_data = fetch_student_scores()


    names, scores = clean_scores(raw_data)


    average = calculate_average(scores)
    print("Average Score:", average)
    if names and scores:
        plot_scores(names, scores, average)
    else:
        print("No valid data available for visualization")




if __name__ == "__main__":
    main()