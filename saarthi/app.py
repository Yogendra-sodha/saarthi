from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'dasnadasbanavsoji'  # Change this to a secure secret key

# Sample data storage (for prototype)
users_data = []
drivers_data = []
assigned_rides = {}
completed_rides = []

# Define admin password (for prototype)
admin_password = "password123"

# Function to add a user to users_data
def add_user(user_name):
    users_data.append(user_name)

# Function to add a driver to drivers_data
def add_driver(driver_name):
    drivers_data.append(driver_name)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        user_name = request.form["user_name"]
        add_user(user_name)
        session['user_name'] = user_name
        return redirect(url_for('wait_for_ride'))

    return render_template("user.html")

@app.route("/driver", methods=["GET", "POST"])
def driver():
    if request.method == "POST":
        driver_name = request.form["driver_name"]
        add_driver(driver_name)
        session['driver_name'] = driver_name
        return redirect(url_for('wait_for_assignment'))

    return render_template("driver.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form["password"]
        if password == admin_password:
            session['admin_password'] = password
            return redirect(url_for('assign'))

    return render_template("admin.html")

@app.route("/wait_for_ride")
def wait_for_ride():
    user_name = session.get('user_name')
    return render_template("wait_for_ride.html", user_name=user_name)

@app.route("/wait_for_assignment")
def wait_for_assignment():
    driver_name = session.get('driver_name')
    return render_template("wait_for_assignment.html", driver_name=driver_name)

@app.route("/assign", methods=["POST"])
def assign():
    if request.method == "POST":
        driver_name = session.get('driver_name')
        selected_users = request.form.getlist("user")

        # Store assigned ride
        assigned_rides[driver_name] = selected_users

        flash('Ride assigned successfully!')
        return redirect(url_for('admin'))

@app.route("/ride_status")
def ride_status():
    admin_password = session.get('admin_password')
    if admin_password != admin_password:
        return redirect(url_for('admin'))

    return render_template("ride_status.html", assigned_rides=assigned_rides)

@app.route("/finish_ride/<driver_name>")
def finish_ride(driver_name):
    if driver_name in assigned_rides:
        completed_rides.append(assigned_rides.pop(driver_name))
        return redirect(url_for('ride_status'))

if __name__ == "__main__":
    app.run(debug=True)
