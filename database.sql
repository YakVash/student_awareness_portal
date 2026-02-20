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
