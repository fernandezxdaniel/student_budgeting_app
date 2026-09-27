from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Segment Tree implementation
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        self.build(data)

    def build(self, data):
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index, value):
        pos = index + self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]

    def query(self, left, right):
        result = 0
        left += self.n
        right += self.n
        while left < right:
            if left % 2:
                result += self.tree[left]
                left += 1
            if right % 2:
                right -= 1
                result += self.tree[right]
            left //= 2
            right //= 2
        return result

# Categories
categories = ["Food", "Transport", "Rent", "School", "Water", "Savings"]
expenses = [0] * len(categories)
seg_tree = SegmentTree(expenses)

@app.route('/')
def home():
    return render_template('index.html', categories=categories)

@app.route('/update', methods=['POST'])
def update_expense():
    data = request.json
    index = categories.index(data['category'])
    value = int(data['amount'])
    expenses[index] = value
    seg_tree.update(index, value)
    return jsonify({"message": f"{data['category']} updated to {value}"})

@app.route('/summary')
def summary():
    total = seg_tree.query(0, len(categories))
    most = categories[expenses.index(max(expenses))]
    least = categories[expenses.index(min(expenses))]
    combined = list(zip(categories, expenses))  # fix for Jinja2
    return render_template('summary.html',
                           total=total,
                           most=most,
                           least=least,
                           combined=combined,
                           categories=categories,
                           expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
