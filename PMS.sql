-- 1. Departments table
-- Must be created first because other tables reference it.
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL UNIQUE
);

-- 2. Employees table
-- This table references the 'departments' table via a foreign key.
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    department_id INT NOT NULL,
    job_title VARCHAR(255),
    salary DECIMAL(10, 2),
    hire_date DATE,
    gender VARCHAR(50),
    profile_photo TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 3. Update the Departments table with the 'head_of_department_id' foreign key.
-- This is a separate step because 'employees' must exist before it can be referenced.
ALTER TABLE departments
ADD COLUMN head_of_department_id INT,
ADD CONSTRAINT fk_head_of_department
FOREIGN KEY (head_of_department_id) REFERENCES employees(employee_id);

-- 4. Tasks table
-- This table references the 'employees' table.
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    task_description TEXT NOT NULL,
    due_date DATE,
    status VARCHAR(50) DEFAULT 'To Do', -- 'To Do', 'In Progress', 'Completed'
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- 5. Performance Ratings table
-- This table references the 'employees' table for both the employee and the manager.
CREATE TABLE performance_ratings (
    rating_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    reporting_manager_id INT NOT NULL,
    rating INT,
    feedback TEXT,
    rating_date DATE,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (reporting_manager_id) REFERENCES employees(employee_id)
);

-- 6. Deleted Employees table
-- This table stores archived data of employees who have been soft-deleted.
CREATE TABLE deleted_employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    deletion_date TIMESTAMP DEFAULT NOW()
);

-- 7. Recruitment table
-- This table references the 'departments' table.
CREATE TABLE recruitment (
    recruitment_id SERIAL PRIMARY KEY,
    department_id INT NOT NULL,
    job_description TEXT,
    job_specification TEXT,
    yield_ratio DECIMAL(5, 2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 8. Add initial data
-- It's crucial to insert data in the correct order to respect foreign key constraints.
INSERT INTO departments (department_name) VALUES ('HR'), ('Engineering'), ('Marketing'), ('Finance');

INSERT INTO employees (name, email, phone, department_id, job_title, salary, hire_date, gender) VALUES
('John Doe', 'john.doe@example.com', '123-456-7890', 2, 'Software Engineer', 80000.00, '2023-01-15', 'Male'),
('Jane Smith', 'jane.smith@example.com', '098-765-4321', 1, 'HR Manager', 90000.00, '2022-05-20', 'Female'),
('Peter Jones', 'peter.jones@example.com', '555-123-4567', 2, 'Senior Developer', 120000.00, '2021-09-10', 'Male'),
('Shreya Nayak', 'shreya.nayak@example.com', '111-222-3333', 1, 'HR Analyst', 75000.00, '2023-03-01', 'Female');

-- Update the 'departments' table with the head of department now that employees exist.
UPDATE departments SET head_of_department_id = 2 WHERE department_name = 'Engineering';
UPDATE departments SET head_of_department_id = 4 WHERE department_name = 'HR';

-- Add some tasks
INSERT INTO tasks (employee_id, task_description, due_date, status) VALUES
(2, 'Complete Q3 performance reviews', '2025-09-30', 'In Progress'),
(4, 'Update employee handbook', '2025-09-25', 'To Do'),
(1, 'Refactor user authentication module', '2025-09-20', 'Completed');

-- Add some ratings
INSERT INTO performance_ratings (employee_id, reporting_manager_id, rating, feedback, rating_date) VALUES
(1, 3, 5, 'Excellent performance this quarter.', '2025-09-01'),
(2, 4, 4, 'Met all targets, good work.', '2025-09-02');

INSERT INTO employees (name, email, phone, department_id, job_title, salary, hire_date, gender, profile_photo, is_active) VALUES
('Priya Sharma', 'priya.sharma@example.com', '123-111-2222', 1, 'HR Manager', 95000.00, '2022-01-10', 'Female', 'https://randomuser.me/api/portraits/women/1.jp', TRUE),
('Rahul Kumar', 'rahul.kumar@example.com', '123-222-3333', 1, 'Recruitment Specialist', 78000.00, '2022-03-15', 'Male', 'https://randomuser.me/api/portraits/men/2.jpg', TRUE),
('Neha Singh', 'neha.singh@example.com', '123-333-4444', 1, 'HR Generalist', 70000.00, '2022-05-20', 'Female', 'https://randomuser.me/api/portraits/women/3.jpg', TRUE),
('Sanjay Gupta', 'sanjay.gupta@example.com', '123-444-5555', 1, 'Benefits Coordinator', 65000.00, '2022-07-25', 'Male', 'https://randomuser.me/api/portraits/men/4.jpg', TRUE),
('Ananya Patel', 'ananya.patel@example.com', '123-555-6666', 1, 'HR Analyst', 82000.00, '2022-09-30', 'Female', 'https://randomuser.me/api/portraits/women/5.jpg', TRUE),
('Vikram Joshi', 'vikram.joshi@example.com', '123-666-7777', 1, 'Learning & Development', 75000.00, '2023-02-05', 'Male', 'https://randomuser.me/api/portraits/men/6.jpg', TRUE),
('Divya Rao', 'divya.rao@example.com', '123-777-8888', 1, 'HR Assistant', 58000.00, '2023-04-10', 'Female', 'https://randomuser.me/api/portraits/women/7.jpg', TRUE),
('Akash Mishra', 'akash.mishra@example.com', '123-888-9999', 1, 'HR Consultant', 110000.00, '2023-06-15', 'Male', 'https://randomuser.me/api/portraits/men/8.jpg', TRUE),
('Sneha Reddy', 'sneha.reddy@example.com', '123-999-0000', 1, 'Recruitment Coordinator', 68000.00, '2023-08-20', 'Female', 'https://randomuser.me/api/portraits/women/9.jpg', TRUE),
('Aditya Sharma', 'aditya.sharma@example.com', '123-000-1111', 1, 'Compensation Analyst', 85000.00, '2023-10-25', 'Male', 'https://randomuser.me/api/portraits/men/10.jpg', TRUE),
('Meera Krishnan', 'meera.krishnan@example.com', '123-111-2233', 1, 'HR Specialist', 72000.00, '2024-01-05', 'Female', 'https://randomuser.me/api/portraits/women/11.jpg', TRUE),
('Ganesh Das', 'ganesh.das@example.com', '123-222-3344', 1, 'Employee Relations', 88000.00, '2024-03-10', 'Male', 'https://randomuser.me/api/portraits/men/12.jpg', TRUE);

-- Insert 18 employees for Engineering (12 Male, 6 Female)
-- Engineering department_id = 2
INSERT INTO employees (name, email, phone, department_id, job_title, salary, hire_date, gender, profile_photo, is_active) VALUES
('Rohan Mehta', 'rohan.mehta@example.com', '456-111-2222', 2, 'Software Engineer', 110000.00, '2021-02-15', 'Male', 'https://randomuser.me/api/portraits/men/13.jpg', TRUE),
('Aisha Khan', 'aisha.khan@example.com', '456-222-3333', 2, 'Data Scientist', 130000.00, '2021-04-20', 'Female', 'https://randomuser.me/api/portraits/women/14.jpg', TRUE),
('Kiran Kumar', 'kiran.kumar@example.com', '456-333-4444', 2, 'Senior Developer', 150000.00, '2021-06-25', 'Male', 'https://randomuser.me/api/portraits/men/15.jpg', TRUE),
('Pooja Shah', 'pooja.shah@example.com', '456-444-5555', 2, 'QA Analyst', 85000.00, '2021-08-30', 'Female', 'https://randomuser.me/api/portraits/women/16.jpg', TRUE),
('Vijay Singh', 'vijay.singh@example.com', '456-555-6666', 2, 'DevOps Engineer', 125000.00, '2021-11-05', 'Male', 'https://randomuser.me/api/portraits/men/17.jpg', TRUE),
('Nidhi Aggarwal', 'nidhi.aggarwal@example.com', '456-666-7777', 2, 'Product Manager', 140000.00, '2022-01-10', 'Female', 'https://randomuser.me/api/portraits/women/18.jpg', TRUE),
('Amit Sharma', 'amit.sharma@example.com', '456-777-8888', 2, 'Full Stack Developer', 105000.00, '2022-03-15', 'Male', 'https://randomuser.me/api/portraits/men/19.jpg', TRUE),
('Preeti Desai', 'preeti.desai@example.com', '456-888-9999', 2, 'UI/UX Designer', 90000.00, '2022-05-20', 'Female', 'https://randomuser.me/api/portraits/women/20.jpg', TRUE),
('Manish Rao', 'manish.rao@example.com', '456-999-0000', 2, 'System Analyst', 98000.00, '2022-07-25', 'Male', 'https://randomuser.me/api/portraits/men/21.jpg', TRUE),
('Saurabh Dube', 'saurabh.dube@example.com', '456-000-1111', 2, 'Backend Engineer', 115000.00, '2022-09-30', 'Male', 'https://randomuser.me/api/portraits/men/22.jpg', TRUE),
('Gaurav Singh', 'gaurav.singh@example.com', '456-111-2233', 2, 'Frontend Developer', 100000.00, '2022-11-05', 'Male', 'https://randomuser.me/api/portraits/men/23.jpg', TRUE),
('Ankit Verma', 'ankit.verma@example.com', '456-222-3344', 2, 'Database Administrator', 120000.00, '2023-01-10', 'Male', 'https://randomuser.me/api/portraits/men/24.jpg', TRUE),
('Kavita Nair', 'kavita.nair@example.com', '456-333-4455', 2, 'Data Analyst', 92000.00, '2023-03-15', 'Female', 'https://randomuser.me/api/portraits/women/25.jpg', TRUE),
('Rajesh Kumar', 'rajesh.kumar@example.com', '456-444-5566', 2, 'Network Engineer', 105000.00, '2023-05-20', 'Male', 'https://randomuser.me/api/portraits/men/26.jpg', TRUE),
('Vivek Gupta', 'vivek.gupta@example.com', '456-555-6677', 2, 'Software Architect', 180000.00, '2023-07-25', 'Male', 'https://randomuser.me/api/portraits/men/27.jpg', TRUE),
('Deepak Sharma', 'deepak.sharma@example.com', '456-666-7788', 2, 'QA Engineer', 87000.00, '2023-09-30', 'Male', 'https://randomuser.me/api/portraits/men/28.jpg', TRUE),
('Ritika Singh', 'ritika.singh@example.com', '456-777-8899', 2, 'Business Analyst', 95000.00, '2023-11-05', 'Female', 'https://randomuser.me/api/portraits/women/29.jpg', TRUE),
('Arjun Das', 'arjun.das@example.com', '456-888-9900', 2, 'Project Manager', 145000.00, '2024-01-10', 'Male', 'https://randomuser.me/api/portraits/men/30.jpg', TRUE);

-- Insert 11 employees for Marketing (7 Male, 4 Female)
-- Marketing department_id = 3
INSERT INTO employees (name, email, phone, department_id, job_title, salary, hire_date, gender, profile_photo, is_active) VALUES
('Ritesh Jain', 'ritesh.jain@example.com', '789-111-2222', 3, 'Marketing Manager', 120000.00, '2021-03-20', 'Male', 'https://randomuser.me/api/portraits/men/31.jpg', TRUE),
('Pooja Verma', 'pooja.verma@example.com', '789-222-3333', 3, 'Content Strategist', 85000.00, '2021-05-25', 'Female', 'https://randomuser.me/api/portraits/women/32.jpg', TRUE),
('Alok Sharma', 'alok.sharma@example.com', '789-333-4444', 3, 'Digital Marketing Specialist', 90000.00, '2021-08-01', 'Male', 'https://randomuser.me/api/portraits/men/33.jpg', TRUE),
('Sonal Gupta', 'sonal.gupta@example.com', '789-444-5555', 3, 'SEO Analyst', 75000.00, '2021-10-06', 'Female', 'https://randomuser.me/api/portraits/women/34.jpg', TRUE),
('Manav Desai', 'manav.desai@example.com', '789-555-6666', 3, 'Social Media Manager', 88000.00, '2022-01-11', 'Male', 'https://randomuser.me/api/portraits/men/35.jpg', TRUE),
('Vivek Kumar', 'vivek.kumar@example.com', '789-666-7777', 3, 'Brand Manager', 105000.00, '2022-03-16', 'Male', 'https://randomuser.me/api/portraits/men/36.jpg', TRUE),
('Sunita Rao', 'sunita.rao@example.com', '789-777-8888', 3, 'Content Writer', 68000.00, '2022-05-21', 'Female', 'https://randomuser.me/api/portraits/women/37.jpg', TRUE),
('Rohit Sharma', 'rohit.sharma@example.com', '789-888-9999', 3, 'Graphic Designer', 72000.00, '2022-07-26', 'Male', 'https://randomuser.me/api/portraits/men/38.jpg', TRUE),
('Kunal Dube', 'kunal.dube@example.com', '789-999-0000', 3, 'Market Research Analyst', 95000.00, '2022-10-01', 'Male', 'https://randomuser.me/api/portraits/men/39.jpg', TRUE),
('Tarun Mehta', 'tarun.mehta@example.com', '789-000-1111', 3, 'Email Marketing Specialist', 80000.00, '2022-12-06', 'Male', 'https://randomuser.me/api/portraits/men/40.jpg', TRUE),
('Sakshi Joshi', 'sakshi.joshi@example.com', '789-111-2233', 3, 'Social Media Analyst', 70000.00, '2023-02-11', 'Female', 'https://randomuser.me/api/portraits/women/41.jpg', TRUE);

-- Insert 9 employees for Finance (5 Male, 4 Female)
-- Finance department_id = 4
INSERT INTO employees (name, email, phone, department_id, job_title, salary, hire_date, gender, profile_photo, is_active) VALUES
('Suresh Patil', 'suresh.patil@example.com', '987-111-2222', 4, 'Finance Manager', 130000.00, '2021-04-10', 'Male', 'https://randomuser.me/api/portraits/men/42.jpg', TRUE),
('Anjali Desai', 'anjali.desai@example.com', '987-222-3333', 4, 'Financial Analyst', 95000.00, '2021-06-15', 'Female', 'https://randomuser.me/api/portraits/women/43.jpg', TRUE),
('Rohit Verma', 'rohit.verma@example.com', '987-333-4444', 4, 'Accountant', 80000.00, '2021-08-20', 'Male', 'https://randomuser.me/api/portraits/men/44.jpg', TRUE),
('Kirti Shah', 'kirti.shah@example.com', '987-444-5555', 4, 'Auditor', 88000.00, '2021-11-25', 'Female', 'https://randomuser.me/api/portraits/women/45.jpg', TRUE),
('Amit Dube', 'amit.dube@example.com', '987-555-6666', 4, 'Financial Planner', 105000.00, '2022-02-01', 'Male', 'https://randomuser.me/api/portraits/men/46.jpg', TRUE),
('Priya Singh', 'priya.singh@example.com', '987-666-7777', 4, 'Risk Analyst', 92000.00, '2022-04-06', 'Female', 'https://randomuser.me/api/portraits/women/47.jpg', TRUE),
('Sachin Gupta', 'sachin.gupta@example.com', '987-777-8888', 4, 'Tax Consultant', 98000.00, '2022-06-11', 'Male', 'https://randomuser.me/api/portraits/men/48.jpg', TRUE),
('Sonali Kumari', 'sonali.kumari@example.com', '987-888-9999', 4, 'Bookkeeper', 75000.00, '2022-08-16', 'Female', 'https://randomuser.me/api/portraits/women/49.jpg', TRUE),
('Harish Naik', 'harish.naik@example.com', '987-999-0000', 4, 'Chief Financial Officer', 250000.00, '2021-01-01', 'Male', 'https://randomuser.me/api/portraits/men/50.jpg', TRUE);

-- Task for HR employees (department_id = 1)
INSERT INTO tasks (employee_id, task_description, due_date, status) VALUES
(1, 'Prepare quarterly performance review report', '2025-10-15', 'To Do'),
(2, 'Organize new hire orientation for Q4', '2025-11-01', 'In Progress'),
(3, 'Update company policy on remote work', '2025-10-20', 'To Do'),
(4, 'Review and approve leave requests for November', '2025-10-30', 'Completed'),
(5, 'Analyze employee satisfaction survey results', '2025-11-10', 'In Progress'),
(6, 'Schedule team-building event for December', '2025-11-15', 'To Do'),
(7, 'Process new employee onboarding paperwork', '2025-10-10', 'Completed'),
(8, 'Develop a training program for junior staff', '2025-11-25', 'In Progress'),
(9, 'Screen resumes for open positions', '2025-10-12', 'Completed'),
(10, 'Plan compensation review for next fiscal year', '2025-12-05', 'To Do'),
(11, 'Draft internal communication about policy changes', '2025-10-18', 'In Progress'),
(12, 'Conduct exit interview for a departing employee', '2025-10-22', 'Completed');

-- Tasks for Engineering employees (department_id = 2)
INSERT INTO tasks (employee_id, task_description, due_date, status) VALUES
(13, 'Refactor user authentication module', '2025-10-25', 'In Progress'),
(14, 'Build a new data pipeline for sales analytics', '2025-11-05', 'To Do'),
(15, 'Code review for new feature release', '2025-10-14', 'Completed'),
(16, 'Write unit tests for the main application', '2025-10-28', 'In Progress'),
(17, 'Configure CI/CD pipeline in Jenkins', '2025-11-12', 'Completed'),
(18, 'Update production server documentation', '2025-10-18', 'To Do'),
(19, 'Migrate old microservice to new framework', '2025-11-30', 'In Progress'),
(20, 'Design UI/UX for the mobile application', '2025-10-21', 'Completed'),
(21, 'Debug a critical production bug', '2025-10-11', 'Completed'),
(22, 'Optimize database queries for performance', '2025-11-08', 'In Progress'),
(23, 'Develop the new dashboard feature', '2025-12-01', 'To Do'),
(24, 'Deploy the latest bug fixes to staging', '2025-10-23', 'Completed'),
(25, 'Analyze system logs for anomalies', '2025-11-03', 'In Progress'),
(26, 'Set up a new VPC in AWS', '2025-11-18', 'To Do'),
(27, 'Architect the new scalable architecture', '2025-12-15', 'In Progress'),
(28, 'Fix memory leak in the core service', '2025-10-26', 'Completed'),
(29, 'Create a business requirements document', '2025-11-09', 'To Do'),
(30, 'Lead the daily stand-up meeting', '2025-10-13', 'Completed');

-- Tasks for Marketing employees (department_id = 3)
INSERT INTO tasks (employee_id, task_description, due_date, status) VALUES
(31, 'Plan Q4 marketing campaign', '2025-10-28', 'In Progress'),
(32, 'Write blog post on new product launch', '2025-10-17', 'Completed'),
(33, 'Optimize Google Ads campaigns', '2025-11-02', 'To Do'),
(34, 'Conduct keyword research for SEO', '2025-10-19', 'Completed'),
(35, 'Manage social media content calendar', '2025-11-07', 'In Progress'),
(36, 'Develop new brand guidelines', '2025-11-20', 'To Do'),
(37, 'Draft newsletter for customer base', '2025-10-24', 'In Progress'),
(38, 'Design new landing page banners', '2025-10-16', 'Completed'),
(39, 'Analyze competitor marketing strategies', '2025-11-04', 'To Do'),
(40, 'Send out a promotional email blast', '2025-10-29', 'In Progress'),
(41, 'Create a new campaign report', '2025-11-11', 'Completed');

-- Tasks for Finance employees (department_id = 4)
INSERT INTO tasks (employee_id, task_description, due_date, status) VALUES
(42, 'Prepare monthly budget report', '2025-10-10', 'Completed'),
(43, 'Analyze Q3 financial performance', '2025-10-25', 'In Progress'),
(44, 'Reconcile accounts payable', '2025-10-15', 'Completed'),
(45, 'Conduct internal audit on expenses', '2025-11-05', 'To Do'),
(46, 'Forecast Q4 revenue projections', '2025-11-18', 'In Progress'),
(47, 'Evaluate new investment opportunities', '2025-12-01', 'To Do'),
(48, 'Prepare tax documentation for filing', '2025-10-29', 'In Progress'),
(49, 'Update financial statements', '2025-10-21', 'Completed'),
(50, 'Review Q3 financial report with management', '2025-10-13', 'Completed');

-- Insert performance ratings for all 50 employees

-- Assuming some employees are reporting managers:
-- Jane Smith (ID: 2), Kiran Kumar (ID: 15), Ritesh Jain (ID: 31), Suresh Patil (ID: 42)

-- HR Ratings
INSERT INTO performance_ratings (employee_id, reporting_manager_id, rating, feedback, rating_date) VALUES
(1, 2, 4, 'Strong leadership in managing the team and key initiatives.', '2025-09-01'),
(3, 2, 3, 'Meets expectations. Can improve on process documentation.', '2025-09-02'),
(4, 2, 5, 'Excellent communication and problem-solving skills.', '2025-09-03'),
(5, 2, 4, 'Very good analytical skills. Provides valuable insights.', '2025-09-04'),
(6, 2, 3, 'Good progress on development projects.', '2025-09-05'),
(7, 2, 4, 'Efficient and a great team player.', '2025-09-06'),
(8, 2, 5, 'Exceptional strategic thinking. Exceeds expectations.', '2025-09-07'),
(9, 2, 4, 'Solid performance in a high-volume recruitment period.', '2025-09-08'),
(10, 2, 3, 'Consistent and reliable work, with room for growth.', '2025-09-09'),
(11, 2, 4, 'Demonstrates strong initiative and attention to detail.', '2025-09-10'),
(12, 2, 5, 'Outstanding skills in conflict resolution and support.', '2025-09-11');

-- Engineering Ratings
INSERT INTO performance_ratings (employee_id, reporting_manager_id, rating, feedback, rating_date) VALUES
(13, 15, 4, 'Consistent code quality and strong problem-solving.', '2025-09-01'),
(14, 15, 5, 'Excellent at deriving actionable insights from complex data.', '2025-09-02'),
(16, 15, 3, 'Meets expectations. More proactive bug-hunting is encouraged.', '2025-09-03'),
(17, 15, 5, 'Exceptional work in automating our deployment process.', '2025-09-04'),
(18, 15, 4, 'Thorough documentation and reliable system maintenance.', '2025-09-05'),
(19, 15, 4, 'Strong grasp of new technologies. A key contributor.', '2025-09-06'),
(20, 15, 5, 'Designs are highly intuitive and user-friendly.', '2025-09-07'),
(21, 15, 3, 'Solid coding and good team collaboration.', '2025-09-08'),
(22, 15, 4, 'Proactive in identifying and resolving bottlenecks.', '2025-09-09'),
(23, 15, 3, 'Good foundational work. Needs to improve on project timelines.', '2025-09-10'),
(24, 15, 5, 'Flawless deployments and excellent knowledge of system architecture.', '2025-09-11'),
(25, 15, 4, 'Quick to adapt and provides clear, concise analysis.', '2025-09-12'),
(26, 15, 3, 'Meets job requirements, but can show more initiative.', '2025-09-13'),
(27, 15, 5, 'A visionary architect. Drives innovation within the team.', '2025-09-14'),
(28, 15, 4, 'Consistently delivers high-quality work.', '2025-09-15'),
(29, 15, 3, 'Good at understanding requirements, needs to be more vocal.', '2025-09-16'),
(30, 15, 5, 'Excellent project management. Projects are always on track.', '2025-09-17');

-- Marketing Ratings
INSERT INTO performance_ratings (employee_id, reporting_manager_id, rating, feedback, rating_date) VALUES
(31, 31, 5, 'Outstanding leadership. Drove a successful Q3 campaign.', '2025-09-01'),
(32, 31, 4, 'Content is highly engaging and well-researched.', '2025-09-02'),
(33, 31, 3, 'Meets targets. Needs to experiment with new campaign strategies.', '2025-09-03'),
(34, 31, 5, 'Exceptional at identifying high-value keywords and boosting traffic.', '2025-09-04'),
(35, 31, 4, 'Consistent social media presence and engagement.', '2025-09-05'),
(36, 31, 4, 'Developed a strong and cohesive brand image.', '2025-09-06'),
(37, 31, 3, 'Good writing skills, but can improve on audience targeting.', '2025-09-07'),
(38, 31, 5, 'Designs are innovative and capture the brand perfectly.', '2025-09-08'),
(39, 31, 4, 'Provides insightful market research that informs our strategy.', '2025-09-09'),
(40, 31, 3, 'Campaigns are functional but could be more creative.', '2025-09-10'),
(41, 31, 4, 'Excellent at analyzing data to improve social media performance.', '2025-09-11');

-- Finance Ratings
INSERT INTO performance_ratings (employee_id, reporting_manager_id, rating, feedback, rating_date) VALUES
(42, 42, 5, 'Exemplary leadership. The team is running smoothly.', '2025-09-01'),
(43, 42, 4, 'Accurate and timely analysis. A key member of the team.', '2025-09-02'),
(44, 42, 5, 'Meticulous and reliable. All accounts are in order.', '2025-09-03'),
(45, 42, 4, 'Provides thorough and actionable audit reports.', '2025-09-04'),
(46, 42, 3, 'Forecasts are accurate, but can improve on presenting data.', '2025-09-05'),
(47, 42, 5, 'Identifies great investment opportunities that have yielded high returns.', '2025-09-06'),
(48, 42, 4, 'Highly knowledgeable in tax laws. Very reliable.', '2025-09-07'),
(49, 42, 3, 'Meets all requirements, but can speed up the process.', '2025-09-08'),
(50, 42, 5, 'Exceptional strategic oversight. A true asset to the company.', '2025-09-09');

-- Insert data into the 'recruitment' table
-- This data helps populate the workforce planning section of the dashboard.
INSERT INTO recruitment (department_id, job_description, job_specification, yield_ratio) VALUES
(1, 'Lead and manage the HR department. Oversee talent acquisition, performance management, and employee relations.', 'Bachelor’s degree in Human Resources, 10+ years of experience in a leadership role.', 0.25),
(2, 'Design and develop complex software systems and applications. Guide the engineering team in technical decisions.', 'Master’s degree in Computer Science, 15+ years of experience, expertise in multiple programming languages.', 0.20),
(3, 'Create and execute comprehensive marketing strategies to promote products and services. Manage brand identity.', 'Bachelor’s degree in Marketing, 8+ years of experience, strong background in digital and content marketing.', 0.30),
(4, 'Oversee all financial operations, including budgeting, forecasting, and financial reporting.', 'Master’s degree in Finance or Accounting, CPA certification, 12+ years of experience in financial management.', 0.28);
