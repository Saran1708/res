from flask import Flask, render_template, request, redirect,session, url_for, flash, abort, make_response
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
import json
import os
import re
from flask import jsonify,send_file
import time
from mysql.connector import IntegrityError
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import pdfkit
from dotenv import load_dotenv




app = Flask(__name__)
application=app
app.secret_key = 'abdkfnsldladhlaihdkbck13445644t'  # Replace with a secure key

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')



load_dotenv()  # Load variables from .env

def get_db_connection():
    """Establish a new database connection."""
    return mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )

DEFAULT_PASSWORD = 'Mcc@123'
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@mcc\.edu\.in$'

def validate_email(email):
    return re.match(EMAIL_PATTERN, email) is not None


# Define a rate limit (e.g., 1 visit count increase per 5 minutes per IP)
RATE_LIMIT_PERIOD = timedelta(minutes=1)


@app.route('/view_details/<int:id>')
def view_details(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch color settings
        cursor.execute("SELECT header_color, sidebar_color FROM color_settings WHERE id = 1")
        color_settings = cursor.fetchone()

        # Fetch details of the profile
        query = "SELECT * FROM details WHERE id = %s"
        cursor.execute(query, (id,))
        details = cursor.fetchone()

        if details:
            # Safely load JSON fields
            details['research_ids'] = json.loads(details.get('research_ids', '[]'))
            details['education'] = json.loads(details.get('education', '[]'))
            details['funding'] = json.loads(details.get('funding', '[]'))
            details['publications'] = json.loads(details.get('publications', '[]'))
            details['administrative_position'] = json.loads(details.get('administrative_position', '[]'))
            details['honorary_positions'] = json.loads(details.get('honorary_positions', '[]'))
            details['conferences'] = json.loads(details.get('conferences', '[]'))
            details['resource_person'] = json.loads(details.get('resource_person', '[]'))

            # Process other fields
            details['career_highlights'] = [item.strip() for item in (details.get('career_highlights') or '').split('\n') if item.strip()]
            details['research_career'] = [item.strip() for item in (details.get('research_career') or '').split('\n') if item.strip()]
            details['research_areas'] = [item.strip() for item in (details.get('research_areas') or '').split('\n') if item.strip()]
            details['collab'] = [item.strip() for item in (details.get('collab') or '').split('\n') if item.strip()]
            details['consultancy'] = [item.strip() for item in (details.get('consultancy') or '').split('\n') if item.strip()]

    
            # Replace None values with empty strings
            for key in details:
                if details[key] is None:
                    details[key] = ''

            details['website'] = details.get('website', '')

            # Get visitor's IP address
            visitor_ip = request.remote_addr
            now = datetime.now()

            # Check the visit log for the user and IP
            cursor.execute("""
                SELECT timestamp FROM visit_logs
                WHERE user_id = %s AND ip_address = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """, (id, visitor_ip))
            last_visit = cursor.fetchone()

            # If last visit is within the rate limit period, do not increment the count
            if last_visit and now - last_visit['timestamp'] < RATE_LIMIT_PERIOD:
                cursor.close()
                connection.close()
                return render_template('view_details.html', details=details, colors=color_settings)

            # Increment the visit count and update visit log
            cursor.execute("UPDATE details SET visit_count = visit_count + 1 WHERE id = %s", (id,))
            cursor.execute("""
                INSERT INTO visit_logs (user_id, ip_address, timestamp)
                VALUES (%s, %s, %s)
            """, (id, visitor_ip, now))
            connection.commit()

        cursor.close()
        connection.close()

        if details:
            return render_template('view_details.html', details=details, colors=color_settings)
        else:
            flash('No details found for this ID.', 'warning')
            return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Error fetching data: {e}")
        flash('An error occurred while fetching data from the database.', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/pdf/<int:id>')
def pdf(id):
    try:
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch color settings
        cursor.execute("SELECT header_color, sidebar_color FROM color_settings WHERE id = 1")
        color_settings = cursor.fetchone()

        # Fetch details of the profile
        query = "SELECT * FROM details WHERE id = %s"
        cursor.execute(query, (id,))
        details = cursor.fetchone()

        if details:
            # Safely load JSON fields
            details['research_ids'] = json.loads(details.get('research_ids', '[]'))
            details['education'] = json.loads(details.get('education', '[]'))
            details['funding'] = json.loads(details.get('funding', '[]'))
            details['publications'] = json.loads(details.get('publications', '[]'))
            details['administrative_position'] = json.loads(details.get('administrative_position', '[]'))
            details['honorary_positions'] = json.loads(details.get('honorary_positions', '[]'))
            details['conferences'] = json.loads(details.get('conferences', '[]'))
            details['resource_person'] = json.loads(details.get('resource_person', '[]'))

            # Process other fields
            details['career_highlights'] = [item.strip() for item in (details.get('career_highlights') or '').split('\n') if item.strip()]
            details['research_career'] = [item.strip() for item in (details.get('research_career') or '').split('\n') if item.strip()]
            details['research_areas'] = [item.strip() for item in (details.get('research_areas') or '').split('\n') if item.strip()]
            details['collab'] = [item.strip() for item in (details.get('collab') or '').split('\n') if item.strip()]
            details['consultancy'] = [item.strip() for item in (details.get('consultancy') or '').split('\n') if item.strip()]

    
            # Replace None values with empty strings
            for key in details:
                if details[key] is None:
                    details[key] = ''

            details['website'] = details.get('website', '')

            

        cursor.close()
        connection.close()

        if details:
            return render_template('pdf.html', details=details, colors=color_settings)
        else:
            flash('No details found for this ID.', 'warning')
            return redirect(url_for('tables'))
    except Exception as e:
        print(f"Error fetching data: {e}")
        flash('An error occurred while fetching data from the database.', 'danger')
        return redirect(url_for('tables'))




@app.route('/index')
def index():
    try:
        # Establish a database connection
        connection = get_db_connection()
        cur = connection.cursor()

        # Fetch color settings
        cur.execute("SELECT header_color, sidebar_color FROM color_settings WHERE id = 1")
        color_settings = cur.fetchone()

        # Fetch funding, research_areas, and publications columns from all staff
        cur.execute("SELECT id, name, department, funding, research_areas, publications, visit_count FROM details")
        result = cur.fetchall()

        # Initialize counts and data lists
        total_funding_count = 0
        total_publications_count = 0
        all_funding = []
        all_research_areas = []
        all_publications = []  # New list to hold publication details

        # Process each row to count and collect funding and publication entries
        for row in result:
            staff_id, name, department, funding, research_areas, publications, visit_count = row

            # Handle funding: Parse JSON data
            if funding:
                try:
                    funding_list = json.loads(funding)  # Parse the JSON data
                    if isinstance(funding_list, list):
                        for fund in funding_list:
                            if isinstance(fund, dict):
                                all_funding.append({
                                    "name": name,
                                    "department": department,
                                    "project_title": fund.get("project_title", "N/A"),
                                    "funding_agency": fund.get("funding_agency", "N/A"),
                                    "year": fund.get("year", "N/A"),
                                    "amount": fund.get("amount", "N/A"),
                                    "status": fund.get("status","N/A")
                                })
                                total_funding_count += 1  # Increment funding count for each entry
                except json.JSONDecodeError:
                    print(f"Error decoding JSON for staff {name}: {funding}")

            # Handle research areas: Split by newlines and strip
            if research_areas:
                research_areas_list = [item.strip() for item in research_areas.split('\n') if item.strip()]
                for area in research_areas_list:
                    all_research_areas.append({
                        "name": name,
                        "department": department,
                        "research_area": area
                    })

            # Handle publications: Parse JSON-like string and add publication objects
            if publications:
                try:
                    publications_list = json.loads(publications)  # Parse the JSON data
                    for publication in publications_list:
                        all_publications.append({
                            "name": name,
                            "department": department,
                            "title": publication.get("title", "N/A"),
                            "link": publication.get("link", "#"),
                            "date": publication.get("date", "N/A"),
                            "type": publication.get("type", "N/A")
                        })
                        total_publications_count += 1
                except json.JSONDecodeError:
                    print(f"Error decoding JSON for publications for staff {name}: {publications}")

        # Sort funding and research areas alphabetically
        all_funding = sorted(all_funding, key=lambda x: (x["project_title"] or '').lower())
        all_research_areas = sorted(all_research_areas, key=lambda x: x["research_area"].lower())

        # Fetch top 5 profiles by visit count
        cur.execute("""
            SELECT id, name, visit_count
            FROM details
            ORDER BY visit_count DESC
            LIMIT 5
        """)
        top_visits = cur.fetchall()

        cur.close()
        connection.close()

        # Render the index template with counts, data lists, color settings, and visit counts
        return render_template(
            'index.html',
            funding_count=total_funding_count,
            publications_count=total_publications_count,
            all_funding=all_funding,
            all_research_areas=all_research_areas,
            all_publications=all_publications,  # Pass publication data
            header_color=color_settings[0],
            sidebar_color=color_settings[1],
            top_visits=top_visits
        )

    except Exception as e:
        # Handle exceptions (logging, error messages, etc.)
        print(f"An error occurred: {e}")
        return render_template('error.html', error_message="An error occurred while processing your request.")


@app.route('/save_colors', methods=['POST'])
def save_colors():
    header_color = request.form.get('header_color')
    sidebar_color = request.form.get('sidebar_color')
    
    connection = get_db_connection()
    cur = connection.cursor()
    
    # Assuming you have a single row in the `color_settings` table with `id=1`
    cur.execute("""
        UPDATE color_settings 
        SET header_color = %s, sidebar_color = %s 
        WHERE id = 1
    """, (header_color, sidebar_color))
    
    connection.commit()
    cur.close()
    connection.close()
    
    flash('Colour changed succesfull', 'success')
    return redirect(url_for('index'))
   

@app.route('/tables')
def tables():
    # Fetch all staff details from the database
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("SELECT * FROM details")
    staff_details = cur.fetchall()
    cur.close()
    connection.close()
    
    return render_template('tables.html', staff_details=staff_details)


@app.route('/staff', methods=['GET'])
def staff():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff")
    staff_details = cursor.fetchall()

    # Filter out admins
    non_admin_staff = [staff for staff in staff_details if staff['role'] != 'admin']

    # Calculate counts
    email_count = len(non_admin_staff)
    password_changed_count = sum(1 for staff in non_admin_staff if staff['password_changed'] == 1)
    profile_completed_count = sum(1 for staff in non_admin_staff if staff['profile_completed'] == 1)
    
    cursor.close()
    conn.close()
    
    return render_template('staff.html', 
                           staff_details=staff_details, 
                           email_count=email_count,
                           password_changed_count=password_changed_count,
                           profile_completed_count=profile_completed_count)


@app.route('/delete_details/<int:id>', methods=['POST'])
def delete_details(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Get the email of the details to delete
        cursor.execute("SELECT email FROM details WHERE id = %s", (id,))
        detail = cursor.fetchone()
        
        if detail:
            email = detail[0]  # Access tuple element by index

            cursor.execute("DELETE FROM visit_logs WHERE user_id = (SELECT id FROM details WHERE email = %s)", (email,))
            
            # Delete the details record
            cursor.execute("DELETE FROM details WHERE id = %s", (id,))

            # Delete corresponding staff record
            cursor.execute("DELETE FROM staff WHERE email = %s", (email,))

            connection.commit()
            flash('Staff details and credentials deleted successfully.', 'success')
        else:
            flash('Details not found.', 'danger')

    except Error as e:
        print(f"Database error: {e}")
        flash('An error occurred while deleting data from the database.', 'danger')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for('tables'))

@app.route('/delete_staff/<int:id>', methods=['POST'])
def delete_staff(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the email of the staff to delete
    cursor.execute("SELECT email FROM staff WHERE id = %s", (id,))
    staff = cursor.fetchone()
    
    if staff:
        email = staff[0]  # Access tuple element by index
        cursor.execute("DELETE FROM visit_logs WHERE user_id = (SELECT id FROM details WHERE email = %s)", (email,))
        
        # Delete the staff record
        cursor.execute("DELETE FROM staff WHERE id = %s", (id,))

        # Delete corresponding details record
        cursor.execute("DELETE FROM details WHERE email = %s", (email,))

        conn.commit()
        flash('Staff credentials and details deleted successfully.', 'success')
    else:
        flash('Staff not found.', 'danger')

    cursor.close()
    conn.close()
    return redirect(url_for('staff'))


@app.route('/add_staff', methods=['POST'])
def add_staff():
    emails = request.form.get('staffEmails')
    if emails:
        email_list = [email.strip() for email in emails.split('\n') if email.strip()]
        conn = get_db_connection()
        cursor = conn.cursor()
        success_count = 0
        error_count = 0
        error_emails = []

        for email in email_list:
            try:
                cursor.execute(
                    "INSERT INTO staff (email, password, password_changed, profile_completed, role) VALUES (%s, %s, %s, %s, %s)",
                    (email, 'Mcc@123', 0, 0, 'staff')
                )
                success_count += 1
            except mysql.connector.Error as e:
                if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                    error_emails.append(email)  # Collect duplicate emails
                    error_count += 1
                else:
                    # Handle other database errors
                    print(f"Database error: {e}")
                    flash('An error occurred while adding staff members. Please try again.', 'danger')
                    conn.rollback()
                    cursor.close()
                    conn.close()
                    return redirect(url_for('staff'))

        conn.commit()
        cursor.close()
        conn.close()

        if success_count > 0:
            flash(f'{success_count} staff member(s) added successfully!', 'success')
        if error_count > 0:
            flash(f'{error_count} email address(es) already exist: {", ".join(error_emails)}', 'warning')

    else:
        flash('No email addresses provided!', 'danger')

    return redirect(url_for('staff'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            
            return redirect(url_for('login'))

        if not validate_email(email):
            flash('Invalid email format. Please use an @mcc.edu.in address.', 'error')
            return redirect(url_for('login'))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Fetch user details from the users table including the role
            cursor.execute("SELECT password, password_changed, profile_completed, role FROM staff WHERE email=%s", (email,))
            user = cursor.fetchone()

            if user:
                stored_password, password_changed, profile_completed, role = user

                # Verify the password
                if stored_password == password:  # You should use hashed passwords in a real scenario
                    if role == 'admin':
                        # If user is admin, skip the additional checks
                        session['user_type'] = 'admin'
                        return redirect(url_for('index'))  # Redirect to the admin index page
                    else:
                        # If user is staff, perform additional checks
                        if stored_password == DEFAULT_PASSWORD:
                            if password == DEFAULT_PASSWORD:
                                # Redirect to reset_password with the email parameter
                                return redirect(url_for('reset_password', email=email))
                            else:
                                flash('Invalid credentials', 'error')
                                return redirect(url_for('login'))
                        else:
                            if password_changed == 0:
                                flash('Password has not been set up yet', 'error')
                                return redirect(url_for('login'))
                            elif profile_completed == 0:
                                # Redirect to the form page if profile is not completed
                                return redirect(url_for('submit_form',email=email))
                            else:
                                session['user_type'] = 'user'
                                # Redirect to the profile page if profile is completed
                                return redirect(url_for('profile', email=email))
                else:
                    flash('Invalid credentials', 'error')
                    return redirect(url_for('login'))
            else:
                flash('User does not exist', 'error')
                return redirect(url_for('login'))

        except Error as e:
            print(f"Database error: {e}")
            flash('An error occurred while processing your request.', 'error')
            return redirect(url_for('login'))

        finally:
            if connection:
                cursor.close()
                connection.close()

    # Render the login page with flash messages if there are any
    return render_template('login.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')

    if not email:
        flash('Invalid request. Email is required.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not new_password or not confirm_password:
            flash('Password cannot be empty.', 'error')
        elif new_password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif len(new_password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
        else:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE staff SET password=%s, password_changed=TRUE WHERE email=%s",
                (new_password, email)  # Store plain text password
            )
            connection.commit()
            flash('Password has been successfully reset.', 'success')
            return redirect(url_for('login'))

    # Render the template with an empty message if no errors
    return render_template('reset_password.html', email=email, message='')

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    email = request.args.get('email')
    if request.method == 'POST':
        # Retrieve personal information (existing code)
        title2 = request.form.get('title2', '').strip()  # Note: Changed 'Title' to 'title' to match the form field name
        name = request.form.get('name', '').strip()
        Title = request.form.get('Title', '').strip()  # Get the dropdown value
        OtherTitle = request.form.get('OtherTitle', '').strip()  # Get the 'Others' textbox value

        # If "Others" is selected, use the value from 'OtherTitle'
        if Title == 'Others':
            Title = OtherTitle  # Overwrite Title with the custom value from the textbox

        institution = request.form.get('institution', '').strip()
        department_order = request.form.get('department_order', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        website = request.form.get('website', '').strip()
        department = request.form.get('department', '').strip()
        research_areas = [line.strip() for line in request.form.get('research_areas', '').split('\n') if line.strip()]

        alternative_email = request.form.get('alternative_email', '').strip()

# Retrieve consultancy information
        consultancy = [line.strip() for line in request.form.get('consultancy', '').split('\n') if line.strip()]

        # Combine title and name into a single variable
        full_name = f"{title2} {name}".strip()

        # Convert the name to sentence case (capitalize first letter of each word)
        full_name = ' '.join(word.capitalize() for word in full_name.split())

        # Handle profile picture upload (existing code)
        default_picture_filename = 'default.webp'
        profile_picture = request.files.get('profile_picture')
        profile_picture_filename = default_picture_filename

        if profile_picture and profile_picture.filename != '':
            file_extension = os.path.splitext(profile_picture.filename)[1]
            timestamp = int(time.time())
            profile_picture_filename = f"{secure_filename(name)}_{timestamp}{file_extension}"
            profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)
            profile_picture.save(profile_picture_path)

        print(f"Profile picture filename: {profile_picture_filename}")

        # Retrieve dynamic research IDs (existing code)
        research_ids = []
        for i in range(50):
            research_id_title = request.form.get(f'research_ids_title_{i+1}', '').strip()
            link = request.form.get(f'research_ids_id_{i+1}', '').strip()
            if research_id_title or link:
                research_ids.append({"title": research_id_title, "id": link})

        administrative_position = []
        for i in range(50):  # Adjust range based on expected max entries or make it dynamic
            admin_position = request.form.get(f'admin_position_{i+1}', '').strip()
            admin_year1 = request.form.get(f'admin_year1_{i+1}', '').strip()
            admin_year2 = request.form.get(f'admin_year2_{i+1}', '').strip()
    
            if admin_position or (admin_year1 and admin_year2):
                administrative_position.append({
            "position": admin_position,
            "year_from": admin_year1,
            "year_to": admin_year2
        })

        honorary_positions = []
        for i in range(50):
            position = request.form.get(f'honorary_position_title_{i+1}', '').strip()
            year = request.form.get(f'honorary_position_year_{i+1}', '').strip()
            if position or year:
                honorary_positions.append({"position": position, "year": year})
    
             # Retrieve dynamic Conference Attended data
        conferences_attended = []
        for i in range(50):  # Adjust range as needed for maximum expected entries
            date_raw = request.form.get(f'conference_year_{i+1}', '').strip()
            
            conference_type = request.form.get(f'conference_type_{i+1}', '').strip()
            title_of_paper = request.form.get(f'title_of_paper_{i+1}', '').strip()
            conference_details = request.form.get(f'conference_details_{i+1}', '').strip()
            isbn = request.form.get(f'conference_isbn_{i+1}', '').strip()

            date_formatted = convert_to_month_year(date_raw)
            # Only add entry if at least one field has been filled out
            if date_formatted or conference_type or title_of_paper or conference_details or isbn:
                conferences_attended.append({
            "year": date_formatted,
            "type": conference_type,
            "title_of_paper": title_of_paper,
            "details": conference_details,
            "isbn": isbn
        })

    
            # Retrieve dynamic Resource Person data
        # Retrieve dynamic Resource Person data
        resource_persons = []
        for i in range(50):
        # Retrieve the raw date in YYYY-MM format
            date_raw = request.form.get(f'resource_person_date_{i+1}', '').strip()
            topic = request.form.get(f'resource_person_topic_{i+1}', '').strip()
            department_ = request.form.get(f'resource_person_department_{i+1}', '').strip()

        # Convert the date to "Month Year" format using the helper function
            date_formatted = convert_to_month_year(date_raw)

            if date_formatted or topic or department_:
                resource_persons.append({
                "date": date_formatted,  # Store the formatted date
                "topic": topic,
                "department_": department_
            })

        # Retrieve dynamic education fields (existing code)
        education = []
        for i in range(50):
            degree = request.form.get(f'education_degree_{i+1}', '').strip()
            college = request.form.get(f'education_college_{i+1}', '').strip()
            duration = request.form.get(f'education_duration_{i+1}', '').strip()
            if degree or college or duration:
                education.append({"degree": degree, "college": college, "duration": duration})

        # Retrieve dynamic funding fields
        funding_items = []
        for i in range(50):  # Adjust the range based on how many funding entries you allow
            project_title = request.form.get(f'project_title_{i+1}', '').strip()
            funding_agency = request.form.get(f'funding_agency_{i+1}', '').strip()
            date_raw = request.form.get(f'funding_year_{i+1}', '').strip()
            
            funding_amount = request.form.get(f'funding_amount_{i+1}', '').strip()
            funding_status = request.form.get(f'funding_status_{i+1}', '').strip()  # Retrieve funding status

            date_formatted = convert_to_month_year(date_raw)
             # Check if any of the fields are filled out, including funding status
            if project_title or funding_agency or date_formatted or funding_amount or funding_status:
                funding_items.append({
                    "project_title": project_title,
                    "funding_agency": funding_agency,
                    "year": date_formatted,
                    "amount": funding_amount,
                    "status": funding_status  # Add status to the dictionary
                })

        publications = []
        for i in range(150):  # Check for up to 50 publication entries
            pub_title = request.form.get(f'publications_title_{i}', '').strip()
            pub_link = request.form.get(f'publications_link_{i}', '').strip()
            pub_date = request.form.get(f'publications_date_{i}', '').strip()
            pub_type1 = request.form.get(f'publications_type_{i}', '').strip()
            pub_type2 = request.form.get(f'other_publications_type_{i}', '').strip()

    # Convert publication date from YYYY-MM to "Month Year"
            formatted_pub_date = convert_to_month_year(pub_date)
            pub_type = pub_type2 if pub_type1 == "Others" else pub_type1
            

    # Only append if at least one field is filled
            if pub_title or pub_link or formatted_pub_date or pub_type:
                publications.append({
            "title": pub_title,
            "link": pub_link,
            "date": formatted_pub_date,  # Use the converted date
            "type": pub_type
        })

        # Retrieve other sections (existing code)
        career_highlights = [line.strip() for line in request.form.get('career_highlights', '').split('\n') if line.strip()]
        research_career = [line.strip() for line in request.form.get('research_career', '').split('\n') if line.strip()]
        collab = [line.strip() for line in request.form.get('collab', '').split('\n') if line.strip()]

        # Updated PhD Scholars Section
        phd_scholars_produced = request.form.get('phd_scholars_produced', '0').strip()  # Default to '0' if empty
        phd_scholars_registered = request.form.get('phd_scholars_registered', '0').strip()  # Default to '0' if empty

        # Ensure the values are valid integers or default to 0
        phd_scholars_produced = int(phd_scholars_produced) if phd_scholars_produced.isdigit() else 0
        phd_scholars_registered = int(phd_scholars_registered) if phd_scholars_registered.isdigit() else 0

        # PhD Scholars Details
        phd_scholars = []
        for i in range(50):  # Assuming max 50 PhD scholars
            scholar_name = request.form.get(f'phd_name_{i}', '').strip()
            scholar_topic = request.form.get(f'phd_topic_{i}', '').strip()
            scholar_status = request.form.get(f'phd_status_{i}', '').strip()
            scholar_years = request.form.get(f'phd_years_{i}', '').strip()
            if scholar_name or scholar_topic or scholar_status or scholar_years:
                phd_scholars.append({
                    "name": scholar_name,
                    "topic": scholar_topic,
                    "status": scholar_status,
                    "years_of_completion": scholar_years
                })

        # Convert lists to JSON strings (existing code with added PhD scholars fields)
        research_ids_json = json.dumps(research_ids)
        administrative_position_json = json.dumps(administrative_position)
        education_json = json.dumps(education)
        funding_json = json.dumps(funding_items)
        publications_json = json.dumps(publications)
        phd_scholars_json = json.dumps(phd_scholars)
        honorary_positions_json = json.dumps(honorary_positions)
        conferences_attended_json = json.dumps(conferences_attended)
        resource_persons_json = json.dumps(resource_persons)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Insert Query (updated to include new PhD scholars fields)
            insert_query = """
            INSERT INTO details (name, Title, institution, department_order, email, phone, address, website, profile_picture, department, 
                                 research_areas, research_ids, education, funding, publications, career_highlights, 
                                 research_career, collab, phd_scholars_produced, phd_scholars_registered, phd_scholars,
                                 alternative_email, consultancy, administrative_position, honorary_positions,
                                 conferences, resource_person)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            

            # Execute Insert Query
            cursor.execute(insert_query, (
                full_name, Title, institution, department_order, email, phone, address, website, profile_picture_filename, department,
                '\n'.join(research_areas), research_ids_json, education_json, funding_json, publications_json,
                '\n'.join(career_highlights), '\n'.join(research_career), '\n'.join(collab),
                phd_scholars_produced, phd_scholars_registered, phd_scholars_json, alternative_email,'\n'.join(consultancy) ,
                administrative_position_json, honorary_positions_json , conferences_attended_json, resource_persons_json
            ))
            connection.commit()

            # Update profile_completed column in staff table (existing code)
            update_query = """
            UPDATE staff SET profile_completed = 1 WHERE email = %s
            """
            cursor.execute(update_query, (email,))
            connection.commit()

            cursor.close()
            connection.close()

            flash('Form submitted successfully!', 'success')
            return redirect(url_for('profile'))  # Redirect after successful POST
        except Exception as e:
            print(f"Error: {e}")
            flash('An error occurred while submitting the form. Please try again.', 'error')
            return redirect(url_for('profile'))

    return render_template('form.html', email=email)

# Function to convert YYYY-MM to "Month Year" format
def convert_to_month_year(yyyy_mm):
    try:
        # Convert the date string into a datetime object
        date_obj = datetime.strptime(yyyy_mm, "%Y-%m")
        # Return the date in "Month Year" format
        return date_obj.strftime("%B %Y")
    except ValueError:
        # Return an empty string or handle invalid format
        return ""
    
@app.route('/profile')
def profile():
    email = request.args.get('email')  # Get the email parameter

    if not email:
        return redirect(url_for('login', message='Email is required to view the profile.'))

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Query to get user details
        query = """
        SELECT
            id, name, Title, institution, email, phone, address, website,
            profile_picture, department, research_areas, research_ids, education,
            funding, publications, career_highlights, research_career
        FROM details
        WHERE email = %s
        """
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()

        if not user_data:
            abort(404, description="User not found")


        # Convert JSON strings back to lists
        user_data['research_areas'] = user_data['research_areas'].split('\n') if user_data['research_areas'] else []
        user_data['research_ids'] = json.loads(user_data['research_ids']) if user_data['research_ids'] else []
        user_data['education'] = json.loads(user_data['education']) if user_data['education'] else []
        user_data['funding'] = json.loads(user_data['funding']) if user_data['funding'] else []
        user_data['publications'] = json.loads(user_data['publications']) if user_data['publications'] else []
        user_data['career_highlights'] = user_data['career_highlights'].split('\n') if user_data['career_highlights'] else []
        user_data['research_career'] = user_data['research_career'].split('\n') if user_data['research_career'] else []

        cursor.close()
        connection.close()
        

        return render_template('profile.html', user=user_data)

    except Error as e:
        print(f"Error: {e}")
        abort(500, description="An error occurred while retrieving user data.")




@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET']) 
def dashboard():
    search_query = request.args.get('search', '').strip()
    selected_department = request.args.get('department', '').strip()

    staff_details = []
    departments_with_staff = {}

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all departments and their staff details
        query_departments = "SELECT DISTINCT department FROM details"
        cursor.execute(query_departments)
        departments = cursor.fetchall()

        for department in departments:
            dept_name = department['department']
            query_staff = """
                SELECT id, name, department_order 
                FROM details 
                WHERE department = %s 
                ORDER BY department_order ASC
                """
            cursor.execute(query_staff, (dept_name,))
            staff_in_dept = cursor.fetchall()
            departments_with_staff[dept_name] = staff_in_dept

        if selected_department:
            query = """
            SELECT id, profile_picture, name, Title, institution, department, email, phone, address, website, 
                   research_areas, research_ids, education, funding, publications, career_highlights, research_career, collab ,
                   alternative_email, consultancy, administrative_position , honorary_positions, conferences, resource_person
            FROM details
            WHERE department = %s
            ORDER BY id DESC
            """
            cursor.execute(query, (selected_department,))
        else:
            # Split the search query by commas and filter out empty terms
            search_terms = [term.strip().lower() for term in search_query.split(',') if term.strip()]
            
            if search_terms:
                search_conditions = []
                search_params = []

                # Build the dynamic query with multiple LIKE conditions
                for term in search_terms:
                    search_conditions.append("""
                    LOWER(name) LIKE %s OR LOWER(Title) LIKE %s OR LOWER(department) LIKE %s OR LOWER(institution) LIKE %s
                    OR LOWER(email) LIKE %s OR LOWER(phone) LIKE %s OR LOWER(address) LIKE %s OR LOWER(website) LIKE %s
                    OR LOWER(research_areas) LIKE %s OR LOWER(research_ids) LIKE %s OR LOWER(education) LIKE %s OR LOWER(funding) LIKE %s
                    OR LOWER(publications) LIKE %s OR LOWER(career_highlights) LIKE %s OR LOWER(research_career) LIKE %s OR LOWER(collab) LIKE %s
                    OR LOWER(alternative_email) LIKE %s OR LOWER(consultancy) LIKE %s OR LOWER(administrative_position) LIKE %s 
                    OR LOWER(honorary_positions) LIKE %s OR LOWER(conferences) LIKE %s OR LOWER(resource_person) LIKE %s
                    """)
                    # Add each search term to the parameters (for all fields)
                    search_params.extend([f"%{term}%"] * 22)

                # Combine all conditions
                query = f"""
                SELECT id, profile_picture, name, Title, institution, department, email, phone, address, website, 
                       research_areas, research_ids, education, funding, publications, career_highlights, research_career, collab,
                       alternative_email, consultancy, administrative_position , honorary_positions, conferences, resource_person
                FROM details
                WHERE {' OR '.join(search_conditions)}
                ORDER BY id DESC
                """
                cursor.execute(query, search_params)

                staff_details = cursor.fetchall()

                for detail in staff_details:
                    # For each detail, check if any of the search terms match
                    matched_texts = []
                    for term in search_terms:
                        matched_text = extract_matched_text(detail, term)
                        if matched_text:
                            matched_texts.append(matched_text)
                    detail['matched_text'] = ', '.join(matched_texts) if matched_texts else ''

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Database error: {e}")
        flash('An error occurred while processing your request.', 'danger')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If the request is AJAX, return JSON
        return jsonify(staff_details)
    else:
        # Otherwise, render the dashboard template
        return render_template('dashboard.html', 
                               staff_details=staff_details,
                               departments_with_staff=departments_with_staff,
                               search_query=search_query)


    

def clean_json_text(text):
    """Remove JSON-like symbols and special characters from the text."""
    # Remove JSON brackets, quotes, and extra whitespace
    cleaned_text = re.sub(r'[\[\]\"\'\s]+', ' ', text).strip()
    # Remove any URLs from the text
    cleaned_text = re.sub(r'http[s]?://\S+', '', cleaned_text).strip()
    return cleaned_text


def extract_matched_text(detail, search_query):
    """
    Extract the first matching word from the given detail dictionary based on search_query.
    If a match is found, return the matching text; otherwise, return an empty string.
    """
    search_query = search_query.lower()

    # Function to find and return the closest match in a list of words
    def find_closest_match(text, query):
        words = re.findall(r'\b\w+\b', text)  # Tokenize the text into words
        for word in words:
            if query in word.lower():
                return word  # Return the word containing the search query
        return None

    # Check if the search query matches the name field
    if 'name' in detail and search_query in detail['name'].lower():
        return find_closest_match(detail['name'], search_query)

    # Check other fields for a match
    for key, value in detail.items():
        if key == 'profile_picture':  # Skip the profile picture field
            continue
        if isinstance(value, str):
            # Clean the text to remove special characters
            value = clean_json_text(value)
            
            # Check if the value is JSON-encoded
            try:
                json_value = json.loads(value)
                if isinstance(json_value, list):
                    # Handle JSON list
                    for item in json_value:
                        if isinstance(item, dict):
                            item_text = ' '.join(item.values())
                            closest_match = find_closest_match(item_text, search_query)
                            if closest_match:
                                return closest_match
                        elif isinstance(item, str):
                            closest_match = find_closest_match(item, search_query)
                            if closest_match:
                                return closest_match
                elif isinstance(json_value, dict):
                    # Handle JSON dict
                    item_text = ' '.join(json_value.values())
                    closest_match = find_closest_match(item_text, search_query)
                    if closest_match:
                        return closest_match
                else:
                    # Handle plain text in JSON
                    closest_match = find_closest_match(value, search_query)
                    if closest_match:
                        return closest_match
            except (json.JSONDecodeError, TypeError):
                # Not a JSON-encoded string, handle as plain text
                if key in ['research_areas', 'career_highlights', 'research_career', 'collab', 'consultancy' ]:
                    # Special handling for specific fields
                    items = value.split('\n')
                    for item in items:
                        closest_match = find_closest_match(item, search_query)
                        if closest_match:
                            return closest_match
                else:
                    closest_match = find_closest_match(value, search_query)
                    if closest_match:
                        return closest_match

    # If no match is found, return an empty string (not "No match found")
    return ''



@app.route('/update_profile/<email>', methods=['GET'])
def render_update_page(email):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM details WHERE email = %s"
        
        cursor.execute(query, (email,))
        staff = cursor.fetchone()
        cursor.close()
        connection.close()


        if staff:

             # Split the name into title and actual name
            name_parts = staff['name'].split(' ', 1)  # Split only on the first space
            if len(name_parts) == 2:
                staff['title'] = name_parts[0]  # The title (Dr, Mr, Ms, etc.)
                staff['name'] = name_parts[1]    # The actual name
            else:
                staff['title'] = ''  # No title found
                staff['name'] = staff['name']  # Use the entire name as-is

            # Handle JSON fields
            try:
                staff['research_ids'] = json.loads(staff['research_ids']) if staff['research_ids'] else []
                staff['administrative_position'] = json.loads(staff['administrative_position']) if staff['administrative_position'] else []
                staff['education'] = json.loads(staff['education']) if staff['education'] else []
                staff['funding'] = json.loads(staff['funding']) if staff['funding'] else []
                staff['publications'] = json.loads(staff['publications']) if staff['publications'] else []
                staff['phd_scholars'] = json.loads(staff.get('phd_scholars', '[]')) if staff['phd_scholars'] else []
                staff['honorary_positions'] = json.loads(staff.get('honorary_positions', '[]')) if staff['honorary_positions'] else []
                staff['conferences'] = json.loads(staff.get('conferences', '[]')) if staff['conferences'] else []
                staff['resource_person'] = json.loads(staff.get('resource_person', '[]')) if staff['resource_person'] else []


                # Convert publication dates from "Month Year" to "YYYY-MM" format
                for item in staff['funding']:
                    if 'year' in item:
                        if item['year']:
                            try:
                                # Convert "Month Year" to "YYYY-MM"
                                date_obj = datetime.strptime(item['year'], '%B %Y')
                                item['year'] = date_obj.strftime('%Y-%m')  # Store in YYYY-MM format for input
                            except ValueError:
                                print(f"Date format error for conferences: {item['year']}")
                                continue  # Keep original if it fails

                # Convert publication dates from "Month Year" to "YYYY-MM" format
                for item in staff['conferences']:
                    if 'year' in item:
                        if item['year']:
                            try:
                                # Convert "Month Year" to "YYYY-MM"
                                date_obj = datetime.strptime(item['year'], '%B %Y')
                                item['year'] = date_obj.strftime('%Y-%m')  # Store in YYYY-MM format for input
                            except ValueError:
                                print(f"Date format error for conferences: {item['year']}")
                                continue  # Keep original if it fails

                # Convert publication dates from "Month Year" to "YYYY-MM" format
                for item in staff['publications']:
                    if 'date' in item:
                        if item['date']:
                            try:
                                # Convert "Month Year" to "YYYY-MM"
                                date_obj = datetime.strptime(item['date'], '%B %Y')
                                item['date'] = date_obj.strftime('%Y-%m')  # Store in YYYY-MM format for input
                            except ValueError:
                                print(f"Date format error for publication: {item['date']}")
                                continue  # Keep original if it fails


                for item in staff['resource_person']:
                    if 'date' in item:
                        if item['date']:
                            try:
                                # Convert "Month Year" to "YYYY-MM"
                                date_obj = datetime.strptime(item['date'], '%B %Y')
                                item['date'] = date_obj.strftime('%Y-%m')  # Store in YYYY-MM format for the input
                            except ValueError:
                                print(f"Date format error for resource person: {item['date']}")
                                continue  # Keep original if it fails

               

           

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")

           # Ensure safe handling of potential None values for each field
            staff['career_highlights'] = [item.strip() for item in (staff.get('career_highlights') or '').split('\n') if item.strip()]
            staff['research_career'] = [item.strip() for item in (staff.get('research_career') or '').split('\n') if item.strip()]
            staff['research_areas'] = [area.strip() for area in (staff.get('research_areas') or '').split(',') if area.strip()]
            staff['collab'] = [area.strip() for area in (staff.get('collab') or '').split(',') if area.strip()]
            staff['consultancy'] = [area.strip() for area in (staff.get('consultancy') or '').split(',') if area.strip()]

            


        return render_template('update.html', staff=staff)

    except Error as e:
        print(f"Database error: {e}")
        return redirect(url_for('profile'))


@app.route('/update_profile/<email>', methods=['POST'])
def update_profile(email):
    if request.method == 'POST':
        try:
            # Retrieve personal information from the form
            title2 = request.form.get('title2', '').strip()  # Note: Changed 'Title' to 'title' to match the form field name
            
            name = request.form.get('name') or None
            Title = request.form.get('Title', '').strip() or None  # Dropdown value
            OtherTitle = request.form.get('OtherTitle', '').strip() or None  # Textbox value for 'Others'
            # Handle designation logic
            if Title == 'Others':
                Title = OtherTitle  # Use the value from the 'OtherTitle' textbox if 'Others' is selected
            institution = request.form.get('institution') or None
            department_order = request.form.get('department_order') or None
            phone = request.form.get('phone') or None
            address = request.form.get('address') or None
            website = request.form.get('website') or None
            department = request.form.get('department') or None
            research_areas = [line.strip() for line in request.form.get('research_areas', '').split('\n') if line.strip()]

            # Retrieve career highlights and research career
            career_highlights = [line.strip() for line in request.form.get('career_highlights', '').split('\n') if line.strip()]
            research_career = [line.strip() for line in request.form.get('research_career', '').split('\n') if line.strip()]
            collab = [line.strip() for line in request.form.get('collab', '').split('\n') if line.strip()]

            alternative_email = request.form.get('alternative_email', '').strip()

            # Retrieve consultancy information
            consultancy = [line.strip() for line in request.form.get('consultancy', '').split('\n') if line.strip()]
            # Combine title and name into a single variable

            full_name = f"{title2} {name}".strip()
            full_name = ' '.join(word.capitalize() for word in full_name.split())

           

            # Handle profile picture file upload
            connection = get_db_connection()
            cursor = connection.cursor()

            # Retrieve the current profile picture filename from the database
            cursor.execute("SELECT profile_picture FROM details WHERE email=%s", (email,))
            result = cursor.fetchone()
            old_profile_picture_filename = result[0] if result else None
            cursor.close()

            # Handle new profile picture upload
            profile_picture = request.files.get('profile_picture')
            print(profile_picture)  # Debugging: Make sure this prints a valid file, not 'None'
            if profile_picture and profile_picture.filename:
                file_extension = os.path.splitext(profile_picture.filename)[1]
                timestamp = int(time.time())
                profile_picture_filename = f"{secure_filename(name)}_{timestamp}{file_extension}"
                profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)
    
                # Save the new profile picture to the uploads folder
                profile_picture.save(profile_picture_path)
    
                # Optionally: Remove the old profile picture if a new one is uploaded
                if old_profile_picture_filename:
                    old_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], old_profile_picture_filename)
                    if os.path.exists(old_picture_path):
                        os.remove(old_picture_path)
            else:
                # If no new picture was uploaded, keep the old one
                profile_picture_filename = old_profile_picture_filename


            administrative_position = []
            for i in range(50):  # Adjust range based on expected max entries or make it dynamic
                admin_position = request.form.get(f'admin_position_{i+1}', '').strip()
                admin_year1 = request.form.get(f'admin_year1_{i+1}', '').strip()
                admin_year2 = request.form.get(f'admin_year2_{i+1}', '').strip()

                if admin_position or (admin_year1 and admin_year2):
                    administrative_position.append({
            "position": admin_position,
            "year_from": admin_year1,
            "year_to": admin_year2
        })

            # Retrieve dynamic Honorary Positions
            honorary_positions = []
            for i in range(50):
                position = request.form.get(f'honorary_position_title_{i+1}', '').strip()
                year = request.form.get(f'honorary_position_year_{i+1}', '').strip()
                if position or year:
                    honorary_positions.append({"position": position, "year": year})
    
            conferences_attended = []
            for i in range(50):  # Adjust range as needed for maximum expected entries
                date_raw = request.form.get(f'conference_year_{i+1}', '').strip()
            
                conference_type = request.form.get(f'conference_type_{i+1}', '').strip()
                title_of_paper = request.form.get(f'title_of_paper_{i+1}', '').strip()
                conference_details = request.form.get(f'conference_details_{i+1}', '').strip()
                isbn = request.form.get(f'conference_isbn_{i+1}', '').strip()

                date_formatted = convert_to_month_year(date_raw)
            # Only add entry if at least one field has been filled out
                if date_formatted or conference_type or title_of_paper or conference_details or isbn:
                    conferences_attended.append({
            "year": date_formatted,
            "type": conference_type,
            "title_of_paper": title_of_paper,
            "details": conference_details,
            "isbn": isbn
        })

            # Retrieve dynamic Resource Persons
            resource_persons = []
            for i in range(50):
                date_raw = request.form.get(f'resource_person_date_{i+1}', '').strip()
                topic = request.form.get(f'resource_person_topic_{i+1}', '').strip()
                department_ = request.form.get(f'resource_person_department_{i+1}', '').strip()

                date_formatted = convert_to_month_year(date_raw)

                if date_formatted or topic or department_:
                    resource_persons.append({
                "date": date_formatted,
                "topic": topic,
                "department_": department_
            })

            

            # Retrieve dynamic research IDs
            research_ids = []   
            for i in range(50):
                title = request.form.get(f'research_ids_title_{i+1}', '').strip()
                link = request.form.get(f'research_ids_id_{i+1}', '').strip()
                if title or link:
                    research_ids.append({"title": title, "id": link})

            # Retrieve dynamic education fields
            education = []
            for i in range(50):
                degree = request.form.get(f'education_degree_{i+1}', '').strip()
                college = request.form.get(f'education_college_{i+1}', '').strip()
                duration = request.form.get(f'education_duration_{i+1}', '').strip()
                if degree or college or duration:
                    education.append({"degree": degree, "college": college, "duration": duration})

            # Retrieve dynamic funding fields
            funding_items = []
            for i in range(50):  # Adjust the range based on how many funding entries you allow
                project_title = request.form.get(f'funding_title_{i+1}', '').strip()
                funding_agency = request.form.get(f'funding_agency_{i+1}', '').strip()
                date_raw = request.form.get(f'funding_year_{i+1}', '').strip()
            
                funding_amount = request.form.get(f'funding_amount_{i+1}', '').strip()
                funding_status = request.form.get(f'funding_status_{i+1}', '').strip()  # Retrieve funding status

                date_formatted = convert_to_month_year(date_raw)
             # Check if any of the fields are filled out, including funding status
                if project_title or funding_agency or date_formatted or funding_amount or funding_status:
                    funding_items.append({
                    "project_title": project_title,
                    "funding_agency": funding_agency,
                    "year": date_formatted,
                    "amount": funding_amount,
                    "status": funding_status  # Add status to the dictionary
                })


            # Retrieve dynamic publications fields
            publications = []
            for i in range(150):
                date_raw = request.form.get(f'publications_date_{i}', '').strip()  # Month-Year format
                
                pub_title = request.form.get(f'publications_title_{i}', '').strip()
                pub_link = request.form.get(f'publications_link_{i}', '').strip()
                pub_type1 = request.form.get(f'publications_type_{i}', '').strip()
                pub_type2 = request.form.get(f'other_publications_type_{i}', '').strip()

                date_formatted = convert_to_month_year(date_raw)
                pub_type = pub_type2 if pub_type1 == "Others" else pub_type1


                if pub_title or pub_link or date_formatted :  
                    publications.append({
            "date": date_formatted ,  # Month-Year format
            "type": pub_type,  # Added publication type
            "title": pub_title,
            "link": pub_link
                })


            # Retrieve PhD supervisor data
            research_supervisor = request.form.get('research_supervisor')
            phd_scholars = []
            phd_scholars_produced = None
            phd_scholars_registered = None

            if research_supervisor == 'yes':
                # Get the number of PhD scholars produced and registered
                phd_scholars_produced = request.form.get('phd_scholars_produced')
                phd_scholars_registered = request.form.get('phd_scholars_registered')

                # Loop through dynamic PhD scholar fields
                for i in range(50):
                    scholar_name = request.form.get(f'phd_name_{i}', '').strip()
                    scholar_topic = request.form.get(f'phd_topic_{i}', '').strip()
                    scholar_status = request.form.get(f'phd_status_{i}', '').strip()
                    scholar_years = request.form.get(f'phd_years_{i}', '').strip()

                    if scholar_name or scholar_topic or scholar_status or scholar_years:
                        phd_scholars.append({
                            "name": scholar_name,
                            "topic": scholar_topic,
                            "status": scholar_status,
                            "years_of_completion": scholar_years
                        })
            else:
                # If "No" is selected, PhD scholars data should be cleared
                phd_scholars_produced = None
                phd_scholars_registered = None
                phd_scholars = []

            # Convert lists to JSON strings
            research_ids_json = json.dumps(research_ids)
            administrative_position_json = json.dumps(administrative_position)
            education_json = json.dumps(education)
            funding_json = json.dumps(funding_items)
            publications_json = json.dumps(publications)
            phd_scholars_json = json.dumps(phd_scholars)
            honorary_positions_json = json.dumps(honorary_positions)
            conferences_attended_json = json.dumps(conferences_attended)
            resource_persons_json = json.dumps(resource_persons)
            

            # Debug information
            print("Updating with the following data:")
            print(f"Name: {full_name}, Title: {Title}, Institution: {institution}, Phone: {phone}")
            print(f"Address: {address}, Website: {website}, Department: {department}")
            print(f"Profile Picture Filename: {profile_picture_filename}")
            print(f"Research Areas: {research_areas}")
            print(f"Research IDs JSON: {research_ids_json}")
            print(f"Education JSON: {education_json}")
            print(f"Funding JSON: {funding_json}")
            print(f"Publications JSON: {publications_json}")
            print(f"Career Highlights: {career_highlights}")
            print(f"Research Career: {research_career}")
            print(f"Collab: {collab}")
            print(f"PhD Scholars Produced: {phd_scholars_produced}")
            print(f"PhD Scholars Registered: {phd_scholars_registered}")
            print(f"PhD Scholars JSON: {phd_scholars_json}")
            print(f"adminstrarive position JSON: {administrative_position_json}")
            print("Honorary Positions:", honorary_positions_json)
            print("Conferences Attended:", conferences_attended_json)
            print("Resource Persons:", resource_persons_json)

            # Update database
            connection = get_db_connection()
            cursor = connection.cursor()

            update_query = """
            UPDATE details SET
                name=%s, Title=%s, institution=%s, department_order=%s, phone=%s, address=%s, website=%s,
                profile_picture=%s, department=%s, research_areas=%s, research_ids=%s,
                education=%s, funding=%s, publications=%s, career_highlights=%s, research_career=%s, collab=%s,
                phd_scholars_produced=%s, phd_scholars_registered=%s, phd_scholars=%s, alternative_email=%s,
                consultancy=%s , administrative_position=%s , honorary_positions=%s, conferences=%s, resource_person=%s
            WHERE email=%s
            """
            
            cursor.execute(update_query, (
                full_name, Title, institution,department_order, phone, address, website,
                profile_picture_filename, department, '\n'.join(research_areas), research_ids_json,
                education_json, funding_json, publications_json, '\n'.join(career_highlights),
                '\n'.join(research_career), '\n'.join(collab), phd_scholars_produced, phd_scholars_registered, phd_scholars_json,
                alternative_email, '\n'.join(consultancy),administrative_position_json, honorary_positions_json,
                conferences_attended_json, resource_persons_json,
                email
            ))

            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Profile updated successfully.', 'success')

            # Redirect based on user type
            if session.get('user_type') == 'admin':
                return redirect(url_for('tables'))  # Redirect to the admin dashboard
            else:
                return redirect(url_for('profile', email=email))  # Redirect to user


        except Exception as e:
            
            
            return redirect(url_for('update_profile', email=email))


@app.route('/show_info/<int:id>')
def show_info(id):
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
         # Fetch color settings (Assuming there is a table named color_settings with an id of 1)
        cursor.execute("SELECT header_color, sidebar_color FROM color_settings WHERE id = 1")
        color_settings = cursor.fetchone()
        print("Color Settings:", color_settings)  # Debugging line

        # Query to get details based on ID
        query = "SELECT * FROM details WHERE id = %s"
        cursor.execute(query, (id,))
        info = cursor.fetchone()

        if info:
            # Convert JSON strings back to lists and handle possible errors
            try:
                info['research_ids'] = json.loads(info['research_ids']) if info['research_ids'] else []
            except json.JSONDecodeError as e:
                print("Error decoding research_ids:", e)
                info['research_ids'] = []

            try:
                info['education'] = json.loads(info['education']) if info['education'] else []
            except json.JSONDecodeError as e:
                print("Error decoding education:", e)
                info['education'] = []

            try:
                info['funding'] = json.loads(info['funding']) if info['funding'] else []
            except json.JSONDecodeError as e:
                print("Error decoding funding:", e)
                info['funding'] = []

            try:
                info['publications'] = json.loads(info['publications']) if info['publications'] else []
            except json.JSONDecodeError as e:
                print("Error decoding publications:", e)
                info['publications'] = []

            try:
                info['administrative_position'] = json.loads(info['administrative_position']) if info['administrative_position'] else []
            except json.JSONDecodeError as e:
                print("Error decoding administrative_position:", e)
                info['administrative_position'] = []
                
                
            try:
                info['honorary_positions'] = json.loads(info['honorary_positions']) if info['honorary_positions'] else []
            except json.JSONDecodeError as e:
                print("Error decoding honorary_positions:", e)
                info['honorary_positions'] = []
                
                
            try:
                info['conferences'] = json.loads(info['conferences']) if info['conferences'] else []
            except json.JSONDecodeError as e:
                print("Error decoding conferences:", e)
                info['conferences'] = []
                
                
            try:
                info['resource_person'] = json.loads(info['resource_person']) if info['resource_person'] else []
            except json.JSONDecodeError as e:
                print("Error decoding resource_person:", e)
                info['resource_person'] = []

            if info.get('career_highlights'):
                info['career_highlights'] = [item.strip() for item in info['career_highlights'].split('\n') if item.strip()]
            
            if info.get('research_career'):
                info['research_career'] = [item.strip() for item in info['research_career'].split('\n') if item.strip()]

            if info.get('research_areas'):
                info['research_areas'] = [item.strip() for item in info['research_areas'].split('\n') if item.strip()]
            
            if info.get('collab'):
                info['collab'] = [item.strip() for item in info['collab'].split('\n') if item.strip()]

            if info.get('consultancy'):
                info['consultancy'] = [item.strip() for item in info['consultancy'].split('\n') if item.strip()]
            
            
            cursor.close()
            connection.close()

            return render_template('show_info.html', info=info, colors=color_settings)
        
        else:
            flash('No information found for this ID.', 'warning')
            return redirect(url_for('profile'))
    except Error as e:
        print(f"Database error: {e}")
        flash('An error occurred while fetching data from the database.', 'danger')
        return redirect(url_for('profile'))




@app.route('/logout', methods=['POST'])
def logout():
    # Flash a success message
    flash('Logout successful!', 'success')
    
    # Create a response object and set the cookie to expire
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('email', '', expires=0)  # Clear the email cookie
    
    return response

from flask import Response, send_file
from werkzeug.wsgi import FileWrapper
from io import BytesIO
import pandas as pd
import logging
import json

@app.route('/export', methods=['GET'])
def export_data():
    try:
        logging.info("Connecting to database...")
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get selected columns from the query string
        selected_columns = request.args.getlist('columns')

        if not selected_columns:
            logging.warning("No columns selected for export")
            return 'No columns selected', 400

        # Convert the list of selected columns into a comma-separated string for SQL
        columns_string = ', '.join(selected_columns)

        logging.info(f"Selected columns: {columns_string}")
        # Prepare the dynamic query with only selected columns
        query = f"SELECT {columns_string} FROM details"
        logging.info(f"Executing query: {query}")
        cursor.execute(query)
        results = cursor.fetchall()

        logging.info(f"Number of records fetched: {len(results)}")

        if not results:
            return 'No data found', 404

        # Process fields to format with [] if necessary
        for result in results:

            if 'career_highlights' in result and result['career_highlights']:
                result['career_highlights'] = '[' + ']['.join(result['career_highlights'].split('\n')) + ']'

            if 'research_career' in result and result['research_career']:
                result['research_career'] = ', '.join(result['research_career'].split('\n'))

            if 'collab' in result and result['collab']:
                result['collab'] = ', '.join(result['collab'].split('\n'))

            if 'consultancy' in result and result['consultancy']:
                result['consultancy'] = ', '.join(result['consultancy'].split('\n'))

            if 'research_areas' in result and result['research_areas']:
                result['research_areas'] = ', '.join(result['research_areas'].split('\n'))

            if 'research_ids' in result and result['research_ids']:
                research_ids = json.loads(result['research_ids'])
                result['research_ids'] = '[' + ']['.join([f"{item['title']} - {item['id']}" for item in research_ids]) + ']'

            if 'funding' in result and result['funding']:
                funding = json.loads(result['funding'])
                result['funding'] = '[' + ']['.join([f"Project Title: {item['project_title']} (Agency: {item['funding_agency']}, Year: {item['year']}, Amount: {item['amount']})" for item in funding]) + ']'
            
            if 'publications' in result and result['publications']:
                publications = json.loads(result['publications'])
                result['publications'] = '[' + ']['.join([
                f"{pub['type']} - {pub['title']} - {pub['link']} - {pub['date']}" for pub in publications ]) + ']'
            
            if 'education' in result and result['education']:
                education = json.loads(result['education'])
                result['education'] = '[' + ']['.join([f"{edu['degree']} - {edu['college']} - {edu['duration']}" for edu in education]) + ']'
            
            
            
            # Updated handling for 'administrative_position' with error handling
            if 'administrative_position' in result and result['administrative_position']:
                administrative_position = json.loads(result['administrative_position'])
                result['administrative_position'] = '[' + ']['.join([
            f"{item['position']} ({item.get('year_from', 'N/A')}-{item.get('year_to', 'N/A')})" 
            for item in administrative_position
        ]) + ']'
    
            
            if 'honorary_positions' in result and result['honorary_positions']:
                honorary_positions = json.loads(result['honorary_positions'])
                result['honorary_positions'] = '[' + ']['.join([f"{item['position']} ({item['year']})" for item in honorary_positions]) + ']'
            
            if 'conferences' in result and result['conferences']:
                conferences = json.loads(result['conferences'])
                result['conferences'] = '[' + ']['.join([f"{item['year']} ({item['type']}) - {item['title_of_paper']} - {item['details']} (ISBN: {item['isbn']})" for item in conferences]) + ']'
            
            if 'resource_person' in result and result['resource_person']:
                resource_person = json.loads(result['resource_person'])
                result['resource_person'] = '[' + ']['.join([f"{item['date']} - Topic: {item['topic']} (Department: {item['department_']})" for item in resource_person]) + ']'



        logging.info("Converting data to DataFrame...")
        df = pd.DataFrame(results)

        logging.info("Exporting data to Excel file...")
        output = BytesIO()  # Memory file buffer
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Seek the buffer to the beginning so `send_file` reads from the start
        output.seek(0)

        # Using FileWrapper to avoid `fileno` issue
        logging.info("Returning Excel file to user")
        return Response(
            FileWrapper(output),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': 'attachment; filename=Researcher_data.xlsx'
            }
        )

    except Exception as e:
        logging.error(f"An error occurred during export: {e}")
        return f"An error occurred during export: {e}", 500


@app.route('/phd_details')
def phd_details():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query to get researcher details
    query = """
    SELECT name, department, phd_scholars, phd_scholars_registered, phd_scholars_produced
    FROM details
    """
    cursor.execute(query)
    all_details = cursor.fetchall()

    # Initialize serial numbers
    researcher_serial_number = 1  # For the "PhD Scholars Count" table (by researcher)
    running_serial_number = 1  # For the "PhD Scholars Details" table (by scholar)

    # Variables to store total counts
    total_phd_scholars_registered = 0
    total_phd_scholars_produced = 0

    # Loop through each researcher
    for detail in all_details:
        # Ensure values are integers, default to 0 if None
        phd_scholars_registered = detail['phd_scholars_registered'] or 0
        phd_scholars_produced = detail['phd_scholars_produced'] or 0

        # Assign serial number for the researcher (PhD Scholars Count)
        detail['serial_number'] = researcher_serial_number
        researcher_serial_number += 1

        # Add to total counts
        total_phd_scholars_registered += phd_scholars_registered
        total_phd_scholars_produced += phd_scholars_produced

        # Handle the scholar's details
        if detail['phd_scholars']:
            detail['phd_scholars'] = json.loads(detail['phd_scholars'])
        else:
            detail['phd_scholars'] = []

        # Loop through each scholar and assign the running serial number
        for scholar in detail['phd_scholars']:
            scholar['serial_number'] = running_serial_number
            running_serial_number += 1

    # Render the template and pass the total counts
    return render_template('phd_details.html',
                           all_details=all_details,
                           total_phd_scholars_registered=total_phd_scholars_registered,
                           total_phd_scholars_produced=total_phd_scholars_produced)


# In your Flask app (app.py or main Python file)

def indian_format(value):
    """Formats a number with commas as per the Indian numbering system."""
    try:
        value = int(value)  # Ensure the input is an integer
        # Convert the value to a string to manually format it
        value_str = str(value)
        if len(value_str) <= 3:
            return value_str  # No need for commas if the number is less than 1,000

        # Start formatting from the last three digits
        last_three = value_str[-3:]
        other_digits = value_str[:-3]  # Get the rest of the digits before the last three

        # Insert commas for every two digits in the remaining part
        remaining = ''
        while len(other_digits) > 2:
            remaining = ',' + other_digits[-2:] + remaining
            other_digits = other_digits[:-2]

        # Combine the parts
        return other_digits + remaining + ',' + last_three if other_digits else last_three
    except ValueError:
        return value  # If it's not a valid number, return the value as is

# Register this custom filter in Jinja2
app.jinja_env.filters['indian_format'] = indian_format




if __name__ == '__main__':
    app.run(debug=True, port=5000)
