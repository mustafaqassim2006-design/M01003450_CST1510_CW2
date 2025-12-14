
# Multi-Domain Intelligence Platform (CST1510 Coursework 2)

A Streamlit-based **Multi-Domain Intelligence Platform** developed for **CST1510 Coursework 2**.  
The system integrates multiple IT operational domains into a single authenticated dashboard, backed by an SQLite database and modular service architecture.

The platform supports the following domains:

- Cybersecurity Operations
- Data Governance (Data Catalog)
- IT Service Management (ITSM)
- AI-assisted operational analysis

---

## Key Features

### User Authentication
- User login system with credential validation
- Passwords securely handled using hashing
- User data stored persistently

### Cybersecurity Operations
- Incident tracking with severity, category, and status
- CRUD operations on incident records
- CSV-based data seeding and persistent database storage
- Dashboard visualisation using Streamlit and Pandas

### Data Governance (Data Catalog)
- Dataset metadata management
- Ownership, classification, and descriptive fields
- Structured storage for governance-oriented use cases

### IT Service Management
- Ticket management system
- Priority, category, and status tracking
- Persistent ticket storage and dashboard display

### AI Assistant
- AI helper module for analytical support 
- Uses external API via environment variables
- Integrated into dashboards for operational insights

---

## Technology Stack

- **Python 3**
- **Streamlit** – Web UI framework
- **SQLite** – Persistent relational database
- **Pandas** – Data handling and analysis
- **bcrypt** – Secure password handling
- **CSV files** – Initial data seeding
- **OpenRouter API** – AI assistant integration

---

## Project Structure

```text
M01003450_CST1510_CW2/
│
├── .env                      # Environment variables
├── .gitignore
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── app.py                    # Main Streamlit application entry point
├── ai_helper.py              # AI assistant helper logic
├── auth.py                   # Authentication utilities
├── instructions.txt          # Setup and run instructions
├── MustafaPresentation (1).mp4   # Recorded presentation
├── MustafaReport.pdf         # Final coursework report
├── __init__.py
│
├── DATA/
│   ├── cyber_incidents.csv   # Cyber incident seed data
│   ├── datasets_metadata.csv# Dataset metadata seed data
│   ├── it_tickets.csv        # IT ticket seed data
│   ├── users.txt             # User credentials file
│   └── intelligence_platform.db  # SQLite database
│
├── DB/
│   ├── crud.py               # CRUD database operations
│   ├── db.py                 # Database connection handler
│   ├── load_data.py          # CSV-to-database loader
│   ├── schema.py             # Database schema definitions
│   ├── main.py               # Database initialization script
│   └── __init__.py
│
├── pages/
│   ├── Login.py              # Login interface
│   ├── Cyber_Dashboard.py    # Cybersecurity dashboard
│   ├── Data_Dashboard.py     # Data governance dashboard
│   ├── IT_Dashboard.py       # ITSM dashboard
│   └── __init__.py
│
├── services/
│   ├── users_service.py      # User-related operations
│   ├── incidents_service.py # Cyber incidents service layer
│   ├── datasets_service.py  # Data catalog service layer
│   ├── tickets_service.py   # IT tickets service layer
│   └── __init__.py
│
└── __pycache__/
````

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mustafaqassim2006-design/M01003450_CST1510_CW2.git
cd M01003450_CST1510_CW2
```

---

### 2. Install Dependencies

```bash
pip install streamlit pandas bcrypt
```

If any module is missing later:

```bash
pip install <module_name>
```

---

### 3. Initialize the Database

Run the database initialization script to create tables and load initial data:

```bash
python -m DB.main
```

or

```bash
python3 -m DB.main
```

This step creates the SQLite database and loads CSV data from the `DATA/` directory.

---

### 4. Environment Variables (AI Assistant)

Create a `.env` file in the root directory and add:

```env
OPENROUTER_API_KEY=your_api_key_here
```

This is required for the AI assistant functionality.

---

## Running the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

Alternative commands if needed:

```bash
python -m streamlit run app.py
python3 -m streamlit run app.py
```

The application will open automatically in your browser.

---

## Default Login Credentials

For testing purposes:

* **Username:** `test`
* **Password:** `123456`

---

## Notes & Troubleshooting

### Database Issues

* Ensure the `DATA/` directory exists
* Ensure `DB.main` has been executed before running the app

### CSV Duplication

* Primary keys are enforced
* Duplicate records from CSV files are prevented

### AI Assistant Not Working

* Verify `.env` file exists
* Ensure API key is valid and loaded correctly

---

## Coursework Context

This project demonstrates:

* Secure authentication handling
* Relational database design with SQLite
* Modular service-oriented architecture
* CRUD operations across multiple domains
* Streamlit-based dashboard development
* Integration of AI-assisted analytics

Developed as part of **CST1510 – Coursework 2**.

---

## License

This project is intended for academic submission purposes only.

