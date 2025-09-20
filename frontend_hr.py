import streamlit as st
import pandas as pd
import backend_hr as db
import altair as alt
from datetime import date
from collections import defaultdict

# --- Page Configuration ---
st.set_page_config(
    page_title="HR Employee Manager",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS Styling for a beautiful app ---
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color:#4682B4;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color:#4682B4;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    .stSelectbox > div > div > div > span {
        font-size: 1.1em;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: nowrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 10px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4682B4;
        color: white;
    }
    .centered-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def display_company_info():
    """Displays company vision, mission, etc."""
    st.header("🏢 Company Details 25406")
    st.markdown("""
        **Vision:** To be the leading innovator in our industry, fostering a culture of excellence and sustainability.
        **Mission:** We empower our employees to achieve their full potential and deliver exceptional value to our customers.
        **Core Competency:** We excel in collaborative problem-solving and leveraging cutting-edge technology.
        **Goal:** To grow our market share by 20% in the next fiscal year through strategic talent development.
    """)
    st.image("C:/Users/SHREYA/Desktop/DBDWBI End/pms HR/header.webp", use_container_width=True)


def display_business_insights():
    """Displays various business insights using charts."""
    st.header("📊 Business Insights")
    insights = db.get_business_insights()

    if insights:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Max Salary", f"₹{insights['max_salary']:,}" if insights['max_salary'] else "N/A")
        with col2:
            st.metric("Min Salary", f"₹{insights['min_salary']:,}" if insights['min_salary'] else "N/A")
        with col3:
            st.metric("Avg Salary", f"₹{insights['avg_salary']:.2f}" if insights['avg_salary'] else "N/A")

        st.subheader("Gender & Diversity Ratio")
        gender_df = pd.DataFrame(list(insights['gender_ratio'].items()), columns=['Gender', 'Ratio'])
        if not gender_df.empty:
            gender_chart = alt.Chart(gender_df).mark_arc(outerRadius=120).encode(
                theta=alt.Theta("Ratio", stack=True),
                color=alt.Color("Gender", scale=alt.Scale(range=['#cc79a7', '#4293c5', '#63b179'])),
                order=alt.Order("Ratio", sort="descending"),
                tooltip=["Gender", alt.Tooltip("Ratio", format=".1%")]
            ).properties(
                title="Gender Ratio"
            )
            st.altair_chart(gender_chart, use_container_width=True)
        else:
            st.info("No gender data available.")


        st.subheader("Employees per Department")
        if insights['employees_by_dept']:
            dept_count_df = pd.DataFrame(list(insights['employees_by_dept'].items()), columns=['Department', 'Count'])
            dept_count_chart = alt.Chart(dept_count_df).mark_bar(color="#7b2bf2").encode(
                x=alt.X('Department', sort='-y'),
                y='Count',
                tooltip=['Department', 'Count']
            ).properties(title="Number of Employees per Department")
            st.altair_chart(dept_count_chart, use_container_width=True)
        else:
            st.info("No employee count data by department available.")

        st.subheader("Task Status Distribution")
        if insights['task_status_data']:
            task_status_df = pd.DataFrame(list(insights['task_status_data'].items()), columns=['Status', 'Count'])
            task_status_chart = alt.Chart(task_status_df).mark_arc(outerRadius=120).encode(
                theta=alt.Theta("Count", stack=True),
                color=alt.Color("Status", scale=alt.Scale(range=['#FFD700', '#1E90FF', '#32CD32'])),
                order=alt.Order("Count", sort="descending"),
                tooltip=["Status", "Count"]
            ).properties(title="Task Status")
            st.altair_chart(task_status_chart, use_container_width=True)
        else:
            st.info("No task status data available.")

def display_employee_management():
    """Manages the employee CRUD operations."""
    st.header("🧑‍💼 Employee Management")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["List/Search", "Create", "Update", "Delete", "Deleted Employees"])

    with tab1: # List/Search
        search_query = st.text_input("🔍 Search employees by name or email")
        if search_query:
            employees = db.search_employees(search_query)
        else:
            employees = db.get_all_employees()

        if employees:
            employees_df = pd.DataFrame(employees)
            employees_df['Profile Photo'] = employees_df['profile_photo'].apply(lambda x: f"![Profile]({x})" if x else "No Photo")
            
            # Reordering columns to show employee_id
            cols_to_display = ['employee_id', 'name', 'email', 'department_name', 'job_title', 'salary', 'Profile Photo']
            st.markdown(employees_df[cols_to_display].to_html(escape=False), unsafe_allow_html=True)
        else:
            st.info("No employees found.")

    with tab2: # Create
        st.subheader("Add a New Employee")
        with st.form("create_employee_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            departments = db.get_departments()
            dept_name = st.selectbox("Department", list(departments.keys()))
            department_id = departments[dept_name]
            job_title = st.text_input("Job Title")
            salary = st.number_input("Salary", min_value=0.0, format="%.2f")
            hire_date = st.date_input("Hire Date", date.today())
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            profile_photo_url = st.text_input("Profile Photo URL")

            submitted = st.form_submit_button("Add Employee")
            if submitted:
                if not name or not email:
                    st.error("Name and Email are required fields.")
                else:
                    employee_data = {
                        'name': name, 'email': email, 'phone': phone, 'department_id': department_id,
                        'job_title': job_title, 'salary': salary, 'hire_date': hire_date,
                        'gender': gender, 'profile_photo': profile_photo_url
                    }
                    if db.create_employee(employee_data):
                        st.success("Employee added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add employee. Email may already exist.")

    with tab3: # Update
        st.subheader("Update Employee Details")
        employees = db.get_all_employees()
        employee_map = {f"ID:{emp['employee_id']} - {emp['name']}": emp['employee_id'] for emp in employees}
        selected_employee_name = st.selectbox("Select Employee to Update", list(employee_map.keys()))

        if selected_employee_name:
            selected_id = employee_map[selected_employee_name]
            emp_details = [emp for emp in employees if emp['employee_id'] == selected_id][0]

            with st.form("update_employee_form"):
                new_name = st.text_input("Name", value=emp_details['name'])
                new_email = st.text_input("Email", value=emp_details['email'])
                new_phone = st.text_input("Phone", value=emp_details['phone'])
                departments = db.get_departments()
                dept_name = st.selectbox("Department", list(departments.keys()), index=list(departments.keys()).index(emp_details['department_name']))
                new_department_id = departments[dept_name]
                new_job_title = st.text_input("Job Title", value=emp_details['job_title'])
                new_salary = st.number_input("Salary", value=float(emp_details['salary']), min_value=0.0)
                new_hire_date = st.date_input("Hire Date", value=pd.to_datetime(emp_details['hire_date']))
                new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(emp_details['gender']))
                new_profile_photo = st.text_input("Profile Photo URL", value=emp_details['profile_photo'])

                submitted = st.form_submit_button("Update Employee")
                if submitted:
                    updated_data = {
                        'name': new_name, 'email': new_email, 'phone': new_phone,
                        'department_id': new_department_id, 'job_title': new_job_title,
                        'salary': new_salary, 'hire_date': new_hire_date,
                        'gender': new_gender, 'profile_photo': new_profile_photo
                    }
                    if db.update_employee(selected_id, updated_data):
                        st.success("Employee details updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update employee.")

    with tab4: # Delete
        st.subheader("Delete an Employee")
        employees = db.get_all_employees()
        employee_map = {f"ID:{emp['employee_id']} - {emp['name']}": emp['employee_id'] for emp in employees}
        employee_to_delete = st.selectbox("Select Employee to Delete", list(employee_map.keys()))
        if st.button("Permanently Delete Employee"):
            if employee_to_delete:
                selected_id = employee_map[employee_to_delete]
                if db.delete_employee(selected_id):
                    st.success("Employee deleted successfully and archived.")
                    st.rerun()
                else:
                    st.error("Failed to delete employee.")

    with tab5: # Deleted Employees
        st.subheader("Archived (Deleted) Employees")
        deleted_employees = db.get_deleted_employees()
        if deleted_employees:
            deleted_df = pd.DataFrame(deleted_employees)
            st.dataframe(deleted_df)
        else:
            st.info("No employees have been deleted yet.")

def display_task_management():
    """Manages tasks for HR department employees."""
    st.header("📝 Task Management")

    tab1, tab2 = st.tabs(["View All Tasks", "Assign Task (HR Dept)"])

    with tab1: # View All Tasks
        st.subheader("All Employee Tasks (Sorted by Due Date)")
        tasks = db.get_tasks_by_due_date()
        if tasks:
            tasks_df = pd.DataFrame(tasks)
            st.dataframe(tasks_df)

            st.subheader("Update Task Status")
            task_ids = {f"{task['task_id']} - {task['task_description']}": task['task_id'] for task in tasks}
            if task_ids:
                selected_task_name = st.selectbox("Select Task to Update", list(task_ids.keys()))
                new_status = st.radio("New Status", ['To Do', 'In Progress', 'Completed'])
                if st.button("Update Status"):
                    selected_task_id = task_ids[selected_task_name]
                    if db.update_task_status(selected_task_id, new_status):
                        st.success("Task status updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update task status.")
        else:
            st.info("No tasks found.")

    with tab2: # Assign Task (HR Dept)
        st.subheader("Assign a New Task to HR Department Employee")
        hr_employees = db.get_hr_employees()
        hr_employee_names = list(hr_employees.values())
        if hr_employee_names:
            selected_employee_name = st.selectbox("Select HR Employee", hr_employee_names)
            selected_employee_id = list(hr_employees.keys())[list(hr_employees.values()).index(selected_employee_name)]

            with st.form("assign_task_form"):
                task_description = st.text_area("Task Description")
                due_date = st.date_input("Due Date", date.today())
                submitted = st.form_submit_button("Assign Task")

                if submitted:
                    if not task_description:
                        st.error("Task description is required.")
                    else:
                        if db.assign_task(selected_employee_id, task_description, due_date):
                            st.success("Task assigned successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to assign task.")
        else:
            st.warning("No employees found in the HR department.")

def display_performance_management():
    """Manages employee ratings and feedback."""
    st.header("⭐ Performance Management")

    tab1, tab2, tab3 = st.tabs(["View All Ratings", "Rate HR Employee", "Feedback/Recognition"])

    with tab1: # View All Ratings
        st.subheader("All Employee Ratings")
        ratings = db.get_all_ratings()
        if ratings:
            ratings_df = pd.DataFrame(ratings)
            st.dataframe(ratings_df)
        else:
            st.info("No ratings have been submitted yet.")

    with tab2: # Rate HR Employee
        st.subheader("Give Rating to an HR Department Employee")
        hr_employees = db.get_hr_employees()
        hr_employee_names = list(hr_employees.values())
        if hr_employee_names:
            selected_employee_name = st.selectbox("Select HR Employee to Rate", hr_employee_names)
            selected_employee_id = list(hr_employees.keys())[list(hr_employees.values()).index(selected_employee_name)]

            with st.form("give_rating_form"):
                rating = st.slider("Rating (1-5)", 1, 5, 3)
                feedback = st.text_area("Feedback")
                shreya_nayak_id = 4
                
                submitted = st.form_submit_button("Submit Rating")
                if submitted:
                    if db.give_rating_to_employee(selected_employee_id, shreya_nayak_id, rating, feedback):
                        st.success("Rating submitted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to submit rating.")
        else:
            st.warning("No employees found in the HR department to rate.")

    with tab3: # Feedback/Recognition
        st.subheader("Rewards and Recognition")
        st.info("This section allows HR to recognize employees based on their performance.")

        employees = db.get_all_employees()
        employee_map = {f"ID:{emp['employee_id']} - {emp['name']}": emp['employee_id'] for emp in employees}
        selected_employee_name_id = st.selectbox("Select Employee for Recognition", list(employee_map.keys()))

        if selected_employee_name_id:
            selected_id = employee_map[selected_employee_name_id]
            selected_employee_name = selected_employee_name_id.split(' - ')[1]
            st.markdown("---")
            st.subheader(f"Performance Metrics for {selected_employee_name}")

            tasks = [t for t in db.get_tasks_by_due_date() if t['employee_name'] == selected_employee_name]
            st.markdown("#### Task Completion Status")
            if tasks:
                tasks_df = pd.DataFrame(tasks)
                tasks_df = tasks_df[['task_description', 'status', 'due_date']]
                st.dataframe(tasks_df)
            else:
                st.info("No tasks found for this employee.")

            ratings = db.get_employee_ratings(selected_id)
            st.markdown("#### Performance Ratings")
            if ratings:
                ratings_df = pd.DataFrame(ratings)
                ratings_df['rating_date'] = pd.to_datetime(ratings_df['rating_date']).dt.date
                st.dataframe(ratings_df)
            else:
                st.info("No ratings found for this employee.")

            st.markdown("---")
            recognition_text = st.text_area("Write a message for recognition")
            if st.button("Give Recognition"):
                if recognition_text:
                    st.success(f"Recognition message sent to {selected_employee_name}: '{recognition_text}'")
                else:
                    st.warning("Please write a recognition message.")

# --- Workforce Planning ---
def display_workforce_planning():
    """Displays workforce planning and recruitment details."""
    st.header("👥 Workforce Planning & Recruitment")

    # Session state for managing edit mode and data
    if 'recruitment_data' not in st.session_state:
        st.session_state.recruitment_data = pd.DataFrame({
            'Department': ['Engineering', 'Marketing', 'Finance', 'HR', 'Operations', 'Sales'],
            'Applicants': [250, 400, 300, 350, 200, 450],
            'Interviews': [150, 300, 210, 230, 110, 360],
            'Offers': [140, 250, 180, 220, 100, 320],
            'Hires': [100, 210, 150, 190, 80, 280]
        })
        
    st.subheader("Workforce Planning")
    st.info("Forecast hiring needs for specific roles and departments.")
    
    col1, col2, col3 = st.columns(3)
    
    departments = db.get_departments()
    dept_names = sorted(list(departments.keys()))
    
    with col1:
        selected_dept_name = st.selectbox("Select Department", dept_names)
    
    roles_by_dept = {
        "Engineering": ["Software Engineer", "Senior Developer", "QA Analyst", "Data Scientist"],
        "Marketing": ["Marketing Specialist", "Digital Marketing Manager", "Content Creator", "SEO Analyst"],
        "Finance": ["Financial Analyst", "Accountant", "Finance Manager", "Auditor"],
        "HR": ["HR Manager", "HR Analyst", "Recruitment Specialist", "Benefits Coordinator"],
        "Operations": ["Operations Manager", "Supply Chain Analyst", "Project Manager"],
        "Sales": ["Sales Manager", "Account Executive", "Business Development Representative"]
    }

    with col2:
        roles_for_dept = roles_by_dept.get(selected_dept_name, ["Select a role"])
        selected_role = st.selectbox("Select Role", roles_for_dept)

    with col3:
        all_employees = db.get_all_employees()
        current_employees = len([emp for emp in all_employees if emp['department_name'] == selected_dept_name and emp['job_title'] == selected_role])
        st.metric("Current Employees", current_employees)
    
    hiring_needed = st.number_input(f"Enter Number of Positions to Hire for {selected_role}", min_value=0, value=0, key='hiring_needed')

    if st.button("Plan Recruitment"):
        st.session_state['show_recruitment_plan'] = True

    if st.session_state.get('show_recruitment_plan', False) and hiring_needed > 0:
        st.markdown("---")
        st.subheader("Recruitment Plan")
        selected_dept_row = st.session_state.recruitment_data[st.session_state.recruitment_data['Department'] == selected_dept_name]

        if not selected_dept_row.empty and selected_dept_row['Hires'].iloc[0] > 0:
            # Calculate ratios
            applicants_per_hire = selected_dept_row['Applicants'].iloc[0] / selected_dept_row['Hires'].iloc[0]
            interviews_per_hire = selected_dept_row['Interviews'].iloc[0] / selected_dept_row['Hires'].iloc[0]
            offers_per_hire = selected_dept_row['Offers'].iloc[0] / selected_dept_row['Hires'].iloc[0]
            
            # Forecast
            applicants_needed = int(hiring_needed * applicants_per_hire)
            interviews_needed = int(hiring_needed * interviews_per_hire)
            offers_needed = int(hiring_needed * offers_per_hire)

            st.markdown(f"""
            To hire **{hiring_needed}** new **{selected_role}**s in the **{selected_dept_name}** department, you will need to:
            - **Get approximately {applicants_needed} applicants**.
            - **Conduct approximately {interviews_needed} interviews**.
            - **Extend approximately {offers_needed} job offers**.
            """)
        else:
            st.info("No recruitment data available for this department to create a plan.")


    st.markdown("---")
    st.subheader("Recruitment Data Table")
    st.info("Edit the raw recruitment funnel data below. Values represent counts, not percentages.")
    
    # Using st.data_editor to allow direct editing
    st.session_state.recruitment_data = st.data_editor(st.session_state.recruitment_data, hide_index=True)
            
    st.markdown("---")
    st.subheader("Job Descriptions (JD) & Specifications (JS)")
    
    jd_js_data = {
        "Software Engineer": {
            "JD": "Develop, test, and maintain software applications using Python, JavaScript, and other relevant technologies. Collaborate with cross-functional teams to define, design, and ship new features.",
            "JS": "Bachelor's degree in Computer Science or a related field. 3+ years of experience in software development. Strong proficiency in Python, JavaScript, and database management."
        },
        "Senior Developer": {
            "JD": "Lead the design and implementation of complex software solutions. Mentor junior developers, conduct code reviews, and ensure high-quality code standards are met. Drive technical innovation and architectural decisions.",
            "JS": "Master's degree in a technical field preferred. 7+ years of hands-on experience in full-stack development. Proven leadership skills and a track record of successful project delivery."
        },
        "QA Analyst": {
            "JD": "Design and execute test plans to ensure the quality of software products. Identify, document, and track bugs. Work with development teams to resolve issues and improve product quality.",
            "JS": "Bachelor's degree in a technical field or equivalent experience. 2+ years of experience in software quality assurance. Familiarity with automated testing tools and a strong attention to detail."
        },
        "Data Scientist": {
            "JD": "Develop and implement statistical models, machine learning algorithms, and data analysis pipelines to uncover actionable insights. Communicate findings to stakeholders and support data-driven decision-making.",
            "JS": "Master's or PhD in a quantitative field (e.g., Data Science, Statistics, Computer Science). Expertise in Python/R and libraries like scikit-learn, TensorFlow. Experience with data visualization tools like Tableau or Power BI."
        },
        "Marketing Specialist": {
            "JD": "Execute marketing campaigns across various channels, manage social media presence, and analyze campaign performance metrics to optimize ROI. Assist in content creation and market research.",
            "JS": "Bachelor's degree in Marketing, Communications, or a related field. 2+ years of experience in digital marketing. Proficiency with digital marketing platforms (e.g., Google Ads, Meta Ads) and analytics tools."
        },
        "Digital Marketing Manager": {
            "JD": "Develop and oversee the company's digital marketing strategy. Manage a team of marketing specialists, analyze market trends, and implement data-driven campaigns to achieve business goals.",
            "JS": "Bachelor's degree in Marketing. 5+ years of experience in digital marketing, with 2+ years in a leadership role. Strong project management and analytical skills."
        },
        "Content Creator": {
            "JD": "Produce engaging and informative content for blogs, social media, and websites. Research industry-related topics and create content that drives audience engagement and brand growth.",
            "JS": "Bachelor's degree in English, Journalism, or a related field. Proven experience as a content creator with a strong portfolio. Excellent writing, editing, and communication skills."
        },
        "SEO Analyst": {
            "JD": "Optimize website content and structure for search engines to improve organic rankings and traffic. Conduct keyword research, technical audits, and competitor analysis.",
            "JS": "2+ years of experience in SEO. Proficiency with SEO tools like SEMrush, Ahrefs, and Google Analytics. Strong analytical and problem-solving skills."
        },
        "Financial Analyst": {
            "JD": "Analyze financial data, prepare reports, and forecast business performance. Support budgeting, financial modeling, and investment analysis to guide strategic decisions.",
            "JS": "Bachelor's degree in Finance, Accounting, or Economics. 3+ years of experience in financial analysis. Strong knowledge of financial software and advanced Excel skills."
        },
        "Accountant": {
            "JD": "Manage all financial transactions, including ledger entries, bank reconciliations, and payroll. Prepare financial statements and ensure compliance with accounting standards.",
            "JS": "Bachelor's degree in Accounting. Certified Public Accountant (CPA) license is a plus. 2+ years of experience in a similar role. Proficiency with accounting software like QuickBooks."
        },
        "Finance Manager": {
            "JD": "Oversee the finance department, manage financial reporting, and develop strategies to improve financial health. Lead budgeting and forecasting processes.",
            "JS": "Master's degree in Finance or MBA. 7+ years of experience in finance, with 3+ years in a management position. Strong leadership and strategic planning skills."
        },
        "Auditor": {
            "JD": "Examine financial records and statements to ensure accuracy and compliance with laws and regulations. Identify financial risks and make recommendations for improvement.",
            "JS": "Bachelor's degree in Accounting or Finance. Certified Internal Auditor (CIA) or Certified Public Accountant (CPA) license required. 3+ years of experience in auditing."
        },
        "HR Manager": {
            "JD": "Lead the HR department, develop and implement HR policies, and manage employee relations. Oversee recruitment, training, and performance management processes.",
            "JS": "Bachelor's degree in Human Resources or Business Administration. 5+ years of experience in HR, with 2+ years in a management role. Strong knowledge of labor laws and regulations."
        },
        "HR Analyst": {
            "JD": "Analyze HR data, create reports, and support the HR team with strategic initiatives related to compensation, benefits, and employee engagement.",
            "JS": "Bachelor's degree in Human Resources or Business, with a strong background in data analysis and Excel. Experience with HRIS systems is a plus."
        },
        "Recruitment Specialist": {
            "JD": "Manage the end-to-end recruitment process, from sourcing to onboarding. Build and maintain talent pipelines, conduct interviews, and ensure a positive candidate experience.",
            "JS": "Bachelor's degree in HR, Business, or a related field. 3+ years of experience in recruitment, with strong communication and negotiation skills."
        },
        "Benefits Coordinator": {
            "JD": "Administer employee benefits programs, including health insurance, retirement plans, and leave policies. Communicate benefits information to employees and resolve related inquiries.",
            "JS": "Associate's or Bachelor's degree in HR. 1+ years of experience in benefits administration. Strong organizational skills and attention to detail."
        },
        "Operations Manager": {
            "JD": "Oversee daily business operations, implement efficient processes, and manage a team of operations staff. Ensure the company's operational activities are optimized for productivity.",
            "JS": "Bachelor's degree in Business or Operations Management. 5+ years of experience in an operations role, with a proven track record of process improvement."
        },
        "Supply Chain Analyst": {
            "JD": "Analyze supply chain data to identify areas for improvement and cost reduction. Monitor inventory levels, track shipments, and forecast demand to optimize supply chain efficiency.",
            "JS": "Bachelor's degree in Supply Chain Management, Logistics, or a related field. 2+ years of experience in supply chain analysis. Proficiency with supply chain management software."
        },
        "Project Manager": {
            "JD": "Lead projects from conception to completion, defining project scope, setting deadlines, and managing resources. Ensure projects are delivered on time and within budget.",
            "JS": "Bachelor's degree in Business or a related field. Project Management Professional (PMP) certification is a plus. 3+ years of experience in project management."
        },
        "Sales Manager": {
            "JD": "Lead and motivate the sales team to achieve targets. Develop sales strategies, analyze market trends, and build strong client relationships to drive revenue growth.",
            "JS": "Bachelor's degree in Business or a related field. 5+ years of experience in sales, with a proven track record of meeting or exceeding targets. Strong leadership and communication skills."
        },
        "Account Executive": {
            "JD": "Manage a portfolio of client accounts, build strong relationships, and identify new business opportunities. Present products and services to clients and negotiate contracts.",
            "JS": "Bachelor's degree in Business or Sales. 2+ years of experience as an Account Executive. Excellent interpersonal and presentation skills."
        },
        "Business Development Representative": {
            "JD": "Identify and qualify new business leads through research and outreach. Schedule meetings and demonstrations for the sales team and assist in building the sales pipeline.",
            "JS": "Bachelor's degree in a related field. 1+ years of experience in a sales or business development role. Strong prospecting and communication skills."
        }
    }
    
    if selected_role in jd_js_data:
        st.markdown(f"#### JD for {selected_role}")
        st.info(jd_js_data[selected_role]["JD"])
        st.markdown(f"#### JS for {selected_role}")
        st.info(jd_js_data[selected_role]["JS"])
    else:
        st.info("No specific JD/JS available for this role yet.")

# --- Main Application Logic ---
def main():
    """Main function to run the Streamlit app."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("💼 HR Employee Manager Login")
        st.write("Please enter your credentials to log in.")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                if submitted:
                    if db.authenticate_user(username, password):
                        st.session_state.logged_in = True
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
    else:
        st.sidebar.title("HR Dashboard")
        st.sidebar.markdown(f"Welcome, **Shreya**!")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        st.title("💼 HR Employee Manager PMS")

        menu = st.sidebar.radio("Navigation", [
            "Employee Dashboard",
            "Employee Management",
            "Task Management",
            "Performance Management",
            "Workforce & Recruitment"
        ])

        st.markdown("---")

        if menu == "Employee Dashboard":
            display_company_info()
            st.markdown("---")
            display_business_insights()
        elif menu == "Employee Management":
            display_employee_management()
        elif menu == "Task Management":
            display_task_management()
        elif menu == "Performance Management":
            display_performance_management()
        elif menu == "Workforce & Recruitment":
            display_workforce_planning()

if __name__ == "__main__":
    main()