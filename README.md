# Student Awareness Portal

A web application that helps students discover and explore state-level government schemes and scholarships in one place.

## About

Many students miss out on government schemes simply because they don't know they exist. This portal centralises information on state-level student schemes — making them searchable, readable, and accessible to anyone with a browser.

## Features

- Browse state-level student schemes and scholarships
- Clean, responsive UI built with HTML & CSS
- Backend powered by Python (Flask) with a MySQL database
- Organised by category and eligibility

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS |
| Backend | Python (Flask) |
| Database | MySQL |

## Project Structure

```
student_awareness_portal/
├── app.py              # Flask application & routes
├── database.sql        # Database schema and seed data
├── requirements.txt    # Python dependencies
├── static/             # CSS, images, assets
└── templates/          # HTML templates (Jinja2)
```

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL

### Installation

```bash
# Clone the repository
git clone https://github.com/YakVash/student_awareness_portal.git
cd student_awareness_portal

# Install dependencies
pip install -r requirements.txt

# Set up the database
mysql -u root -p < database.sql

# Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

## Screenshots

<img width="1910" height="827" alt="image" src="https://github.com/user-attachments/assets/878a43d4-6e73-4a67-95b7-33bc12758ef9" />
<img width="1897" height="896" alt="image" src="https://github.com/user-attachments/assets/42e362f0-7c54-43cd-915f-807685ebd507" />
<img width="1888" height="844" alt="image" src="https://github.com/user-attachments/assets/cca95843-4e70-43d6-b1bd-6bf8ce67cf87" />
<img width="1889" height="878" alt="image" src="https://github.com/user-attachments/assets/80fff4ff-eb6b-47ea-b485-2159d776f335" />
<img width="1919" height="909" alt="image" src="https://github.com/user-attachments/assets/b38a735c-76f3-4667-82c0-8118b7025291" />
<img width="1902" height="908" alt="image" src="https://github.com/user-attachments/assets/011ada3a-701d-4da3-a5a2-5812f7544277" />
<img width="1919" height="914" alt="image" src="https://github.com/user-attachments/assets/00254bd2-82e2-460f-86cf-0678bbeab9d6" />




## License

This project is open source and available under the [MIT License](LICENSE).

