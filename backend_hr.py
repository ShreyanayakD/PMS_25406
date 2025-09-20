import psycopg2
import pandas as pd
from typing import List, Dict

# --- Database Connection and Configuration ---
DB_CONFIG = {
    "dbname": "pms",
    "user": "postgres",
    "password": "Nayak",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establishes and returns a database connection."""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# --- Authentication ---
def authenticate_user(username, password):
    """Authenticates the HR user."""
    # Hardcoded for simplicity as per request
    return username == "Shreya" and password == "Nayak"

# --- Employee Management (CRUD) ---

# C - Create
def create_employee(employee_data):
    """Adds a new employee to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO employees (name, email, phone, department_id, job_title, salary, hire_date, gender, profile_photo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            employee_data['name'], employee_data['email'], employee_data['phone'],
            employee_data['department_id'], employee_data['job_title'], employee_data['salary'],
            employee_data['hire_date'], employee_data['gender'], employee_data['profile_photo']
        ))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# R - Read
def get_all_employees():
    """Fetches all employees and their department names."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT e.employee_id, e.name, e.email, e.phone, d.department_name,
               e.job_title, e.salary, e.hire_date, e.gender, e.profile_photo
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        WHERE e.is_active = TRUE
        ORDER BY e.employee_id;
        """
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        employees = cursor.fetchall()
        
        # Correcting department names to be title case
        employee_list = []
        for row in employees:
            row_dict = dict(zip(columns, row))
            if 'department_name' in row_dict and row_dict['department_name'] is not None:
                row_dict['department_name'] = row_dict['department_name'].title()
            employee_list.append(row_dict)
            
        return employee_list
    finally:
        cursor.close()
        conn.close()

def search_employees(search_term):
    """Searches employees by name or email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT e.employee_id, e.name, e.email, e.phone, d.department_name,
               e.job_title, e.salary, e.hire_date, e.gender, e.profile_photo
        FROM employees e
        JOIN departments d ON e.department_id = d.department_id
        WHERE (LOWER(e.name) LIKE %s OR LOWER(e.email) LIKE %s)
          AND e.is_active = TRUE;
        """
        search_term = f"%{search_term.lower()}%"
        cursor.execute(query, (search_term, search_term))
        columns = [desc[0] for desc in cursor.description]
        employees = cursor.fetchall()
        
        employee_list = []
        for row in employees:
            row_dict = dict(zip(columns, row))
            if 'department_name' in row_dict and row_dict['department_name'] is not None:
                row_dict['department_name'] = row_dict['department_name'].title()
            employee_list.append(row_dict)
            
        return employee_list
    finally:
        cursor.close()
        conn.close()

# U - Update
def update_employee(employee_id, employee_data):
    """Updates an existing employee's details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        UPDATE employees
        SET name = %s, email = %s, phone = %s, department_id = %s, job_title = %s, salary = %s,
            hire_date = %s, gender = %s, profile_photo = %s
        WHERE employee_id = %s
        """
        cursor.execute(query, (
            employee_data['name'], employee_data['email'], employee_data['phone'],
            employee_data['department_id'], employee_data['job_title'], employee_data['salary'],
            employee_data['hire_date'], employee_data['gender'], employee_data['profile_photo'], employee_id
        ))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# D - Delete
def delete_employee(employee_id):
    """Soft-deletes an employee and moves their info to a 'deleted' table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get employee info for the deleted_employees table
        cursor.execute("SELECT name, email FROM employees WHERE employee_id = %s", (employee_id,))
        employee_info = cursor.fetchone()
        if not employee_info:
            return False

        name, email = employee_info

        # Insert into deleted_employees table
        cursor.execute("INSERT INTO deleted_employees (employee_id, name, email) VALUES (%s, %s, %s)",
                       (employee_id, name, email))

        # Soft delete from the main employees table
        cursor.execute("UPDATE employees SET is_active = FALSE WHERE employee_id = %s", (employee_id,))

        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_deleted_employees():
    """Fetches a list of soft-deleted employees."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT employee_id, name, email, deletion_date FROM deleted_employees ORDER BY deletion_date DESC;")
        columns = [desc[0] for desc in cursor.description]
        deleted_employees = cursor.fetchall()
        return [dict(zip(columns, row)) for row in deleted_employees]
    finally:
        cursor.close()
        conn.close()

# --- Task Management ---
def get_tasks_by_due_date():
    """Fetches all tasks, ordered by due date."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT t.task_id, e.name as employee_name, t.task_description, t.due_date, t.status
        FROM tasks t
        JOIN employees e ON t.employee_id = e.employee_id
        ORDER BY t.due_date;
        """
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        tasks = cursor.fetchall()
        return [dict(zip(columns, row)) for row in tasks]
    finally:
        cursor.close()
        conn.close()

def assign_task(employee_id, task_description, due_date):
    """Assigns a task to an employee."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (employee_id, task_description, due_date) VALUES (%s, %s, %s)",
            (employee_id, task_description, due_date)
        )
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_task_status(task_id, new_status):
    """Updates the status of a task."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE tasks SET status = %s WHERE task_id = %s",
            (new_status, task_id)
        )
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# --- Business Insights ---
def get_business_insights():
    """Calculates and returns various business insights."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(salary), MIN(salary), AVG(salary) FROM employees WHERE is_active = TRUE")
        max_sal, min_sal, avg_sal = cursor.fetchone()

        cursor.execute("SELECT gender, COUNT(*) FROM employees WHERE is_active = TRUE GROUP BY gender")
        gender_data = dict(cursor.fetchall())
        total_employees = sum(gender_data.values())
        gender_ratio = {k: v / total_employees for k, v in gender_data.items()} if total_employees > 0 else {}

        cursor.execute("""
            SELECT d.department_name, AVG(e.salary) as avg_salary
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE e.is_active = TRUE
            GROUP BY d.department_name;
        """)
        avg_salary_by_dept = dict(cursor.fetchall())
        # Correcting department names
        avg_salary_by_dept_corrected = {k.title(): v for k, v in avg_salary_by_dept.items()}

        cursor.execute("""
            SELECT d.department_name, COUNT(e.employee_id)
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE e.is_active = TRUE
            GROUP BY d.department_name;
        """)
        employees_by_dept = dict(cursor.fetchall())
        # Correcting department names
        employees_by_dept_corrected = {k.title(): v for k, v in employees_by_dept.items()}

        cursor.execute("""
            SELECT status, COUNT(*)
            FROM tasks
            GROUP BY status;
        """)
        task_status_data = dict(cursor.fetchall())

        return {
            "max_salary": max_sal,
            "min_salary": min_sal,
            "avg_salary": avg_sal,
            "gender_ratio": gender_ratio,
            "avg_salary_by_dept": avg_salary_by_dept_corrected,
            "employees_by_dept": employees_by_dept_corrected,
            "task_status_data": task_status_data,
        }
    finally:
        cursor.close()
        conn.close()

def get_departments():
    """Fetches all departments and ensures department names are title-cased."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT department_id, department_name FROM departments;")
        departments = cursor.fetchall()
        return {name.title(): id for id, name in departments}
    finally:
        cursor.close()
        conn.close()


def get_hr_employees():
    """Fetches all employees from the HR department."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT employee_id, name FROM employees WHERE department_id = (SELECT department_id FROM departments WHERE department_name = 'HR')")
        return dict(cursor.fetchall())
    finally:
        cursor.close()
        conn.close()

# --- Performance Management ---
def get_all_ratings():
    """Fetches all employee ratings and feedback."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT pr.rating_id, e.name AS employee_name, rm.name AS reporting_manager_name, pr.rating, pr.feedback, pr.rating_date
        FROM performance_ratings pr
        JOIN employees e ON pr.employee_id = e.employee_id
        JOIN employees rm ON pr.reporting_manager_id = rm.employee_id
        ORDER BY pr.rating_date DESC;
        """
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        ratings = cursor.fetchall()
        return [dict(zip(columns, row)) for row in ratings]
    finally:
        cursor.close()
        conn.close()

def get_employee_ratings(employee_id):
    """Fetches ratings for a specific employee."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT pr.rating, pr.feedback, pr.rating_date
        FROM performance_ratings pr
        WHERE pr.employee_id = %s;
        """
        cursor.execute(query, (employee_id,))
        columns = [desc[0] for desc in cursor.description]
        ratings = cursor.fetchall()
        return [dict(zip(columns, row)) for row in ratings]
    finally:
        cursor.close()
        conn.close()

def give_rating_to_employee(employee_id, manager_id, rating, feedback):
    """Gives a performance rating to an employee."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO performance_ratings (employee_id, reporting_manager_id, rating, feedback, rating_date) VALUES (%s, %s, %s, %s, NOW())",
            (employee_id, manager_id, rating, feedback)
        )
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()