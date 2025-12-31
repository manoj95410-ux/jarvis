from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# File to store subscription data
SUBSCRIPTIONS_FILE = 'subscriptions.json'

def load_subscriptions():
    if os.path.exists(SUBSCRIPTIONS_FILE):
        with open(SUBSCRIPTIONS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_subscriptions(subscriptions):
    with open(SUBSCRIPTIONS_FILE, 'w') as f:
        json.dump(subscriptions, f, indent=4)

@app.route("/jarvis")
def jarvis():
    return render_template("Jarvis.html")

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/functions")
def functions():
    return render_template("functions.html")
@app.route("/subscription")
def subscription():
    return render_template("Subscription.html")
@app.route("/price")
def price():
    return render_template("price.html")

@app.route("/subscribe", methods=['POST'])
def subscribe():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    amount = data.get('amount')
    
    # Validate data
    if not name or not email or not amount:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    # Load existing subscriptions
    subscriptions = load_subscriptions()
    
    # Check if email already subscribed
    for sub in subscriptions:
        if sub['email'] == email:
            return jsonify({'success': False, 'message': 'This email is already subscribed'})
    
    # Add new subscription
    new_subscription = {
        'name': name,
        'email': email,
        'amount': amount,
        'status': 'active',
        'jarvis_access': True
    }
    subscriptions.append(new_subscription)
    
    # Save to file
    save_subscriptions(subscriptions)
    
    # Log transaction (you can add payment processing here later)
    print(f"Payment received: ${amount} from {name} ({email})")
    
    return jsonify({'success': True, 'message': 'Subscription successful'})

if __name__ == "__main__":
    app.run()

   