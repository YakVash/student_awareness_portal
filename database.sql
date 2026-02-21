CREATE TABLE schemes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scheme_name VARCHAR(100),
    education_level VARCHAR(50),
    min_income INT,
    category VARCHAR(50),
    gender VARCHAR(20),
    min_age INT,
    max_age INT,
    benefits TEXT,
    documents TEXT
);

ALTER TABLE schemes
CHANGE min_income max_income INT;

INSERT INTO schemes 
(scheme_name, education_level, max_income, category, gender, min_age, max_age, benefits, documents)
VALUES
('Tamil Nadu Post Matric Scholarship', 'UG', 250000, 'SC', 'Any', 17, 25,
 'Tuition Fee Reimbursement', 
 'Income Certificate, Community Certificate'),

('Free Education Scheme for Girls', 'UG', 300000, 'Any', 'Female', 17, 23,
 'Full Tuition Fee Waiver',
 'Income Certificate, Aadhaar');