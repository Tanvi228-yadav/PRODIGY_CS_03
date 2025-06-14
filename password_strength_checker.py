import re
from flask import Flask, render_template_string, request

app = Flask(__name__)

class PasswordStrengthChecker:
    def __init__(self, password: str):
        self.password = password
        self.criteria_results = {}
        self.strength_score = 0

    def check_length(self):
        length = len(self.password)
        if length >= 16:
            self.criteria_results['length'] = (3, "Excellent length (16+ chars)")
        elif length >= 12:
            self.criteria_results['length'] = (2, "Good length (12-15 chars)")
        elif length >= 8:
            self.criteria_results['length'] = (1, "Acceptable length (8-11 chars)")
        else:
            self.criteria_results['length'] = (0, "Too short (<8 chars)")

    def check_upper(self):
        if re.search(r'[A-Z]', self.password):
            self.criteria_results['uppercase'] = (1, "Contains uppercase letters")
        else:
            self.criteria_results['uppercase'] = (0, "No uppercase letters")

    def check_lower(self):
        if re.search(r'[a-z]', self.password):
            self.criteria_results['lowercase'] = (1, "Contains lowercase letters")
        else:
            self.criteria_results['lowercase'] = (0, "No lowercase letters")

    def check_digit(self):
        if re.search(r'\d', self.password):
            self.criteria_results['number'] = (1, "Contains numbers")
        else:
            self.criteria_results['number'] = (0, "No numbers")

    def check_special(self):
        if re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=~`\\/\[\];\'\s]', self.password):
            self.criteria_results['special'] = (1, "Contains special characters")
        else:
            self.criteria_results['special'] = (0, "No special characters")

    def check_repeats(self):
        patterns = [
            r'(.)\1{2,}',            # 3 or more repeated characters
            r'(..)\1{2,}',           # 2-character pattern repeated 3+ times
            r'(.{3,})\1{1,}'         # 3+ character pattern repeated
        ]
        for pat in patterns:
            if re.search(pat, self.password):
                self.criteria_results['repeats'] = (0, "Contains repetitive patterns")
                return
        self.criteria_results['repeats'] = (1, "No repetitive patterns")

    def check_dictionary(self):
        common_words = {'password', 'admin', 'qwerty', 'letmein', 'welcome', 'monkey', 'dragon', 'football'}
        for word in common_words:
            if word.lower() in self.password.lower():
                self.criteria_results['dictionary'] = (0, f"Contains common word: {word}")
                return
        self.criteria_results['dictionary'] = (1, "No common dictionary words detected")

    def check_sequential(self):
        seq = "abcdefghijklmnopqrstuvwxyz0123456789"
        for i in range(len(seq) - 2):
            pattern = seq[i:i+3]
            if pattern in self.password.lower():
                self.criteria_results['sequential'] = (0, f"Contains sequential pattern: {pattern}")
                return
        self.criteria_results['sequential'] = (1, "No sequential patterns detected")

    def assess(self):
        self.check_length()
        self.check_upper()
        self.check_lower()
        self.check_digit()
        self.check_special()
        self.check_repeats()
        self.check_dictionary()
        self.check_sequential()
        self.strength_score = sum([score for score, _ in self.criteria_results.values()])
        return self.strength_score

    def feedback(self):
        messages = [message for _, message in self.criteria_results.values()]
        score = self.strength_score
        if score >= 8:
            verdict = "Excellent password! 🚀"
            color = "#4CAF50"
        elif score >= 6:
            verdict = "Good password, but could be stronger."
            color = "#2196F3"
        elif score >= 4:
            verdict = "Fair password, consider improving it."
            color = "#ff9800"
        else:
            verdict = "Weak password! You should strengthen it."
            color = "#f44336"

        bar = "█" * score + "-" * (8 - score)
        return {
            "bar": bar,
            "score": score,
            "messages": messages,
            "verdict": verdict,
            "color": color
        }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Password Strength Checker</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #eef2f3; color: #222; }
        .container { max-width: 470px; margin: 60px auto; background: #fff; border-radius: 14px; box-shadow: 0 2px 20px #bbb; padding: 32px 36px; }
        h2 { color: #4CAF50; }
        input[type="password"] { width: 90%; padding: 12px; font-size: 1.1rem; margin: 10px 0 16px 0; border: 1px solid #ccc; border-radius: 6px; }
        button { background: #4CAF50; color: #fff; font-size: 1rem; border: none; padding: 10px 24px; border-radius: 6px; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #388e3c; }
        .strength-bar { font-size: 2rem; letter-spacing: 2px; margin-bottom: 12px; }
        .feedback { margin: 18px 0 0 0; padding: 12px; border-radius: 8px; background: #f8f8f8; box-shadow: 0 1px 3px #eee; }
        .criteria { margin-top: 12px; }
        .criteria li { margin-bottom: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔒 Password Strength Checker</h2>
        <form method="post">
            <input type="password" name="password" placeholder="Enter your password..." required>
            <button type="submit">Check Strength</button>
        </form>
        {% if result %}
            <div class="feedback" style="border-left: 8px solid {{ result.color }}">
                <div class="strength-bar" style="color: {{ result.color }};">
                    {{ result.bar }} ({{ result.score }}/8)
                </div>
                <strong>{{ result.verdict }}</strong>
                <ul class="criteria">
                    {% for msg in result.messages %}
                    <li>{{ msg }}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        pw = request.form["password"]
        checker = PasswordStrengthChecker(pw)
        checker.assess()
        result = checker.feedback()
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True)