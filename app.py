from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL 
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["MYSQL_HOST"] = "localhost" 
app.config["MYSQL_PORT"] = 3308
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "blood_bridge"

db = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about_us.html")

@app.route("/mission")
def mission():
    return render_template("our_mission.html")

@app.route("/request")
def request_blood():
    return render_template("request.html")

@app.route("/donor")
def donor():
    return render_template("donor.html") 

@app.route("/contact")
def contact():
    return render_template("contact_us.html") 

@app.route("/register")
def register():
    return render_template("register.html")  

@app.route("/login")
def login():
    return render_template("login.html")  

@app.route("/find_login")
def find_login():
    return render_template("find_login.html")  

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")  

@app.route("/submit", methods=["GET", "POST"])
def submit():

    if request.method == "POST":
        fullname = request.form['fullname'] 
        username = request.form['username']
        email = request.form['email']
        contact = request.form['contact']
        dob = request.form['dob']
        gender = request.form['gender']
        bloodgroup = request.form['bloodgroup']
        password = request.form['password'] 
        hashed_password = generate_password_hash(password) 
        state = request.form['state']
        city = request.form['city']
        pin = request.form['pin']
        role = request.form['role']

        cur = db.connection.cursor()

        cur.execute("""INSERT INTO users (fullname, username, email, contact, dob, gender, bloodgroup, password, state, city, pin, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (fullname, username, email, contact, dob, gender, bloodgroup, hashed_password, state, city, pin, role))

        db.connection.commit()
        cur.close()

        return """<script>alert("Registration Successful!"); window.location.href="/register";</script>"""

@app.route("/submit_login", methods=["GET", "POST"])
def submit_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cur = db.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            stored_password = user[8]
            role = user[11]

            if check_password_hash(stored_password, password):

                session["email"] = email
                session["role"] = role

                if role == "Patient":

                    return """
                    <script>
                        alert("Login Successful!");
                        window.location.href="/find_donor";
                    </script>
                    """

                elif role == "Donor":

                    return """
                    <script>
                        alert("Login Successful!");
                        window.location.href="/donor";
                    </script>
                    """

            else:

                return """
                <script>
                    alert("Incorrect Password!");
                    window.location.href="/login";
                </script>
                """

        else:

            return """
            <script>
                alert("Email not found!");
                window.location.href="/login";
            </script>
            """

    return render_template("login.html")

@app.route("/submit_loginfind", methods=["GET", "POST"])
def submit_loginfind():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cur = db.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            stored_password = user[8]
            role = user[11]

            if check_password_hash(stored_password, password):

                session["email"] = email
                session["role"] = role

                if role == "Patient":

                    session["user_id"] = user[0]
                    session["email"] = user[3]
                    session["role"] = role

                    if "donor_id" in session:
                        donor_id = session.pop("donor_id")
                        return redirect(url_for("donor_profile", id=donor_id))

                return redirect(url_for("find_donor"))

            else:

                return """
                <script>
                    alert("Incorrect Password!");
                    window.location.href="/find_login";
                </script>
                """

        else:

            return """
            <script>
                alert("Email not found!");
                window.location.href="/find_login";
            </script>
            """

    return render_template("find_login.html")

# @app.route("/view_donor/<int:id>")
# def view_donor(id):

#     # Store the donor ID in the session
#     session["donor_id"] = id

#     # If not logged in, go to the Find Donor login page
#     if "user_id" not in session:
#         return redirect(url_for("submit_loginfind"))

#     # Already logged in
#     return redirect(url_for("donor_profile", id=id))

@app.route("/request_submit", methods=["GET","POST"])
def request_submit():

    if request.method == "POST":
        patientname = request.form['patientname'] 
        bloodgroup = request.form['bloodgroup']
        unit = request.form['unit']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        email = request.form['email']
        hospitalname = request.form['hospitalname']
        hospitaladdress = request.form['hospitaladdress']
        city = request.form['city']
        requireddate = request.form['requireddate']
        emergency = request.form['emergency']

        cur = db.connection.cursor()

        cur.execute("""INSERT INTO blood_request(patientname, bloodgroup, unit, age, gender, contact, email, hospitalname, hospitaladdress, city, requireddate, emergency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (patientname, bloodgroup, unit, age, gender,contact, email, hospitalname, hospitaladdress,city, requireddate, emergency))

        db.connection.commit()
        cur.close()

        return """<script>alert("Request Submitted Successfully!");window.location.href="/request";</script>"""

@app.route("/blood_donor", methods=["GET","POST"])
def blood_donor():

    if request.method == "POST":
        fullName = request.form['fullName'] 
        bloodgroup = request.form['bloodgroup']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        email = request.form['email']
        state = request.form['state']
        city = request.form['city']
        pin = request.form['pin']
        lastdonationdate = request.form['lastdonationdate']
        availability = request.form['availability']

        cur = db.connection.cursor()

        cur.execute("""INSERT INTO blood_donor(fullName, bloodgroup, age, gender, contact, email, state, city, pin, lastdonationdate, availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (fullName, bloodgroup, age, gender, contact, email, state, city, pin, lastdonationdate, availability))

        db.connection.commit()
        cur.close()

        return """<script>alert("Donation Form Submitted Successfully!");window.location.href="/donor";</script>"""

@app.route("/message", methods=["GET","POST"])
def message():

    if request.method == "POST":
        fullName = request.form['fullName'] 
        email = request.form['email']
        contact = request.form['contact']
        subject = request.form['subject']
        message = request.form['message']

        cur = db.connection.cursor()

        cur.execute("""INSERT INTO message(fullName, email, contact, subject, message)
        VALUES (%s, %s, %s, %s, %s)""", (fullName, email, contact, subject, message))

        db.connection.commit()
        cur.close()

        return """<script>alert("Message Sent Successfully!");window.location.href="/contact";</script>"""

@app.route("/forgot", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirmpassword"]

        if password != confirm:
            return """
            <script>
                alert("Passwords do not match!");
                window.location.href="/forgot";
            </script>
            """

        cur = db.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        if user is None:

            cur.close()

            return """
            <script>
                alert("Email not found!");
                window.location.href="/forgot";
            </script>
            """

        hashed_password = generate_password_hash(password)

        cur.execute(
            "UPDATE users SET password=%s WHERE email=%s",
            (hashed_password, email)
        )

        db.connection.commit()
        cur.close()

        return """
        <script>
            alert("Password Updated Successfully!");
            window.location.href="/login";
        </script>
        """

    return render_template("forgot.html")

@app.route("/update_donor", methods=["POST"])
def update_donor():

    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]
    contact = request.form["contact"]
    city = request.form["city"]
    pin = request.form["pin"]

    cur = db.connection.cursor()

    cur.execute("""UPDATE users SET contact=%s, city=%s, pin=%s WHERE email=%s""",
    (contact, city, pin, email))

    cur.execute(""" UPDATE blood_donor SET contact=%s, city=%s, pin=%s WHERE email=%s """, (contact, city, pin, email))

    db.connection.commit()
    cur.close()

    return """<script>alert("Profile Updated Successfully!");window.location.href="/update";</script>"""   

@app.route("/update")
def update():

    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]

    cur = db.connection.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))

    user = cur.fetchone()

    cur.close()

    return render_template("update.html", user=user)

@app.route("/find_donor", methods=["GET", "POST"])
def find_donor():

    donors = []

    if request.method == "POST":

        bloodgroup = request.form["bloodgroup"]
        state = request.form["state"]
        city = request.form["city"]
        pin = request.form["pin"]

        cur = db.connection.cursor()

        cur.execute("""SELECT id, fullname, bloodgroup, contact, email, state, city, pin,lastdonationdate, availability FROM blood_donor
            WHERE bloodgroup=%s AND state=%s AND city=%s AND pin=%s AND availability='Available' """, (bloodgroup, state, city, pin))

        donors = cur.fetchall()
        cur.close()

    return render_template("user.html", donors=donors)

@app.route("/logout")
def logout():
    session.clear()      # Remove all session data
    return redirect(url_for("login"))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cur = db.connection.cursor()

        cur.execute(
            "SELECT * FROM admin WHERE email=%s AND password=%s",
            (email, password)
        )

        admin = cur.fetchone()

        cur.close()

        if admin:
            session["admin_id"] = admin[0]
            session["admin_email"] = admin[2]

            return redirect(url_for("admin_dashboard"))

        else:
            return """
            <script>
                alert("Invalid Email or Password");
                window.location.href="/admin/login";
            </script>
            """

    return render_template("admin/login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cur = db.connection.cursor()

    # Total Users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # Total Donors
    cur.execute("SELECT COUNT(*) FROM users WHERE role='Donor'")
    total_donors = cur.fetchone()[0]

    # Total Blood Requests
    cur.execute("SELECT COUNT(*) FROM blood_request")
    total_requests = cur.fetchone()[0]

    # Total Donations
    cur.execute("SELECT COUNT(*) FROM blood_donor")
    total_donations = cur.fetchone()[0]

    # Total Messages
    cur.execute("SELECT COUNT(*) FROM message")
    total_messages = cur.fetchone()[0]

    cur.close()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_donors=total_donors,
        total_requests=total_requests,
        total_donations=total_donations,
        total_messages=total_messages

    )

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(url_for("admin_login"))

@app.route("/admin/users")
def admin_users():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()
    role = request.args.get("role", "").strip()

    query = """
        SELECT id,
               fullname,
               username,
               email,
               contact,
               bloodgroup,
               city,
               role
        FROM users
        WHERE 1=1
    """

    values = []

    # Search
    if search:
        query += """
        AND (
            fullname LIKE %s
            OR username LIKE %s
            OR email LIKE %s
            OR contact LIKE %s
        )
        """

        keyword = "%" + search + "%"

        values.extend([keyword, keyword, keyword, keyword])

    # Role Filter
    if role:
        query += " AND role=%s"
        values.append(role)

    query += " ORDER BY id ASC"

    cur = db.connection.cursor()
    cur.execute(query, values)

    users = cur.fetchall()

    cur.close()

    return render_template("admin/users.html", users=users)

@app.route("/admin/delete_user/<int:id>")
def delete_user(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cur = db.connection.cursor()

    cur.execute("DELETE FROM users WHERE id=%s", (id,))

    db.connection.commit()

    cur.close()

    return redirect(url_for("admin_users"))

@app.route("/admin/donors")
def admin_donors():

    # Check admin login
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()
    availability = request.args.get("availability", "").strip()

    query = """
        SELECT
            id,
            fullName,
            bloodgroup,
            age,
            gender,
            contact,
            email,
            state,
            city
        FROM blood_donor
        WHERE 1=1
    """

    values = []

    # Search by Name, Email, Contact, Blood Group
    if search:
        query += """
            AND (
                fullName LIKE %s
                OR email LIKE %s
                OR age LIKE %s
                OR gender LIKE %s
                OR state LIKE %s
                OR city LIKE %s
                OR contact LIKE %s
                OR bloodgroup LIKE %s
            )
        """

        keyword = "%" + search + "%"
        values.extend([keyword, keyword, keyword, keyword, keyword, keyword, keyword, keyword])

    # Filter by Availability
    if availability:
        query += " AND availability=%s"
        values.append(availability)

    query += " ORDER BY id ASC"

    cur = db.connection.cursor()
    cur.execute(query, tuple(values))

    donors = cur.fetchall()

    cur.close()

    return render_template("admin/donors.html", donors=donors)

@app.route("/admin/donations")
def admin_donations():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    query = """
        SELECT
            id,
            fullName,
            bloodgroup,
            age,
            gender,
            contact,
            email,
            state,
            city,
            lastdonationdate,
            availability
        FROM blood_donor
        WHERE 1=1
    """

    values = []

    # Search
    if search:
        query += """
            AND (
                fullName LIKE %s
                OR email LIKE %s
                OR age LIKE %s
                OR gender LIKE %s
                OR state LIKE %s
                OR city LIKE %s
                OR contact LIKE %s
                OR bloodgroup LIKE %s
            )
        """

        values.extend([
            keyword,
            keyword,
            keyword,
            keyword,
            keyword,
            keyword,
            keyword,
            keyword
        ])

    # Status Filter
    if status:
        query += " AND status=%s"
        values.append(status)

    query += " ORDER BY id ASC"

    cur = db.connection.cursor()
    cur.execute(query, tuple(values))

    donations = cur.fetchall()

    cur.close()

    return render_template(
        "admin/donations.html",
        donations=donations
    )

@app.route("/admin/requests")
def admin_requests():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()
    emergency = request.args.get("emergency", "").strip()

    query = """
        SELECT
            id,
            patientname,
            bloodgroup,
            unit,
            age,
            gender,
            contact,
            email,
            hospitalname,
            hospitaladdress,
            city,
            requireddate,
            emergency
        FROM blood_request
        WHERE 1=1
    """

    values = []

    # Search
    if search:

        query += """
            AND (
                patientname LIKE %s
                OR bloodgroup LIKE %s
                OR contact LIKE %s
                OR email LIKE %s
                OR hospitalname LIKE %s
                OR city LIKE %s
            )
        """

        keyword = "%" + search + "%"

        values.extend([
            keyword,
            keyword,
            keyword,
            keyword,
            keyword,
            keyword
        ])

    # Emergency Filter
    if emergency:

        query += " AND emergency=%s"
        values.append(emergency)

    query += " ORDER BY id ASC"

    cur = db.connection.cursor()
    cur.execute(query, tuple(values))

    requests = cur.fetchall()

    cur.close()

    return render_template(
        "admin/requests.html",
        requests=requests
    )

@app.route("/admin/delete_request/<int:id>")
def delete_request(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cur = db.connection.cursor()

    cur.execute(
        "DELETE FROM blood_request WHERE id=%s",
        (id,)
    )

    db.connection.commit()

    cur.close()

    return redirect(url_for("admin_requests"))

@app.route("/admin/messages")
def admin_messages():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "").strip()

    query = """
        SELECT
            id,
            fullName,
            email,
            contact,
            subject,
            message
        FROM message
        WHERE 1=1
    """

    values = []

    if search:

        query += """
            AND (
                fullName LIKE %s
                OR email LIKE %s
                OR contact LIKE %s
                OR subject LIKE %s
            )
        """

        keyword = "%" + search + "%"

        values.extend([
            keyword,
            keyword,
            keyword,
            keyword
        ])

    query += " ORDER BY id ASC"

    cur = db.connection.cursor()

    cur.execute(query, tuple(values))

    messages = cur.fetchall()

    cur.close()

    return render_template(
        "admin/messages.html",
        messages=messages
    )

@app.route("/admin/delete_message/<int:id>")
def delete_message(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cur = db.connection.cursor()

    cur.execute(
        "DELETE FROM message WHERE id=%s",
        (id,)
    )

    db.connection.commit()

    cur.close()

    return redirect(url_for("admin_messages"))

@app.route("/donor_profile/<int:id>")
def donor_profile(id):

    cur = db.connection.cursor()

    cur.execute("""
SELECT
    id,
    fullName,
    bloodgroup,
    age,
    gender,
    contact,
    email,
    state,
    city,
    pin,
    lastdonationdate,
    availability
FROM blood_donor
WHERE id=%s
""",(id,))

    donor = cur.fetchone()
    cur.close()

    if donor is None:
        return "Donor not found"

    return render_template("donor_profile.html", donor=donor)

@app.route("/view_contact/<int:id>")
def view_contact(id):

    # Save selected donor ID
    session["donor_id"] = id

    # If not logged in
    if "user_id" not in session:
        return redirect(url_for("submit_loginfind"))

    # Already logged in
    redirect(url_for("donor_profile", id=donor_id))

@app.route("/my_requests")
def my_requests():


    # Check user login
    if "email" not in session:
        return redirect(url_for("login"))

    email = session["email"]

    print("Logged in Email:", email)

    cur = db.connection.cursor()

    cur.execute("""
        SELECT
            id,
            patientname,
            bloodgroup,
            unit,
            age,
            gender,
            contact,
            email,
            hospitalname,
            hospitaladdress,
            city,
            requireddate,
            emergency
        FROM blood_request
        WHERE email=%s
        ORDER BY id ASC
    """, (email,))

    requests = cur.fetchall()

    cur.close()

    return render_template("my_requests.html", requests=requests)

@app.route("/request_delete/<int:id>")
def request_delete(id):

    if "email" not in session:
        return redirect(url_for("login"))

    cur = db.connection.cursor()

    cur.execute(
        "DELETE FROM blood_request WHERE id=%s AND email=%s",
        (id, session["email"])
    )

    db.connection.commit()
    cur.close()

    return redirect(url_for("my_requests"))

@app.route("/donor_dashboard")
def donor_dashboard():

    # Check donor login
    if "email" not in session or session.get("role") != "Donor":
        return redirect(url_for("login"))

    email = session["email"]

    cur = db.connection.cursor()

    # --------------------------
    # Logged-in Donor Details
    # --------------------------
    cur.execute("""
        SELECT
            id,
            fullName,
            bloodgroup,
            age,
            gender,
            contact,
            email,
            state,
            city,
            pin,
            lastdonationdate,
            availability
        FROM blood_donor
        WHERE email=%s
    """, (email,))

    donor = cur.fetchone()

    if donor is None:
        cur.close()
        return "Donor record not found."

    # --------------------------
    # Blood Requests
    # (Only same blood group)
    # --------------------------
    cur.execute("""
SELECT
    id,
    patientname,
    bloodgroup,
    unit,
    age,
    gender,
    contact,
    email,
    hospitalname,
    hospitaladdress,
    city,
    requireddate,
    emergency
FROM blood_request
ORDER BY requireddate ASC
""")

    requests = cur.fetchall()

    cur.close()

    return render_template(
        "donor_dashboard.html",
        donor=donor,
        requests=requests
    )

if __name__ == "__main__":
    app.run(debug=True)