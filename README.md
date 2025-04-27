# 🌎 Disaster Relief Organizer

Welcome to the **Disaster Relief Organizer**, a decentralized web application designed to automate fund transfers to victims of major disasters using the Stellar blockchain. It enables real-time disaster monitoring, automated aid distribution based on disaster magnitude and location, and offers chatbot assistance for victims.

## 📑 Table of Contents
- [Overview](#📖-overview)
- [Features](#🚀-features)
- [Installation](#⚙️-installation)
- [Usage](#🛠️-usage)
- [Project Structure](#🗂️-project-structure)
- [Technologies Used](#🛠️-technologies-used)
- [Deployment](#🚀-deployment)
- [Contributing](#🤝-contributing)
- [License](#📄-license)
- [Contact](#📬-contact)
- [Future Plans](#🌟-future-plans)

## 📖 Overview
The Disaster Relief Organizer aims to directly transfer funds to victims in affected areas based on their city and the disaster's magnitude using an automated process. It leverages the Stellar blockchain for secure, decentralized transactions and provides a real-time disaster feed for organizers/admins.

**Target Audience:** Victims of major disasters, offering immediate financial aid and chatbot support.

## 🚀 Features
- **Automated Fund Distribution:**  
  Sends 10 XLM to every registered victim in a disaster-affected city.
- **Stellar Blockchain Integration:**  
  Secure, transparent, and decentralized fund transfers.
- **Real-Time Disaster Feed:**  
  Live disaster updates for organizers and admins.
- **Chatbot Assistance:**  
  Victims get guidance and emergency help via a chatbot (powered by Groq API).
- **Automated Wallet Creation:**  
  Stellar wallet created and pre-funded with 10,000 XLM upon user registration.
- **Location Verification (Coming Soon):**  
  GPS-based verification for real-time victim location confirmation.
- **Scalability:**  
  Future optimization to target specific zones within cities.

## ⚙️ Installation
### Prerequisites
- Python 3.8+
- Node.js and npm (for frontend enhancements)
- Git
- AWS EC2 instance
- Stellar SDK
- PostgreSQL (or compatible database)

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SSarkar0307/Disaster-Relief-Organizer.git
   cd Disaster-Relief-Organizer/BACKEND
   ```
2. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialize the Database:**
   ```bash
   python initialize_db.py
   ```
4. **Set Environment Variables:**

   Create a .env file inside the BACKEND/ directory:
   ```ini
   GROQ_API_KEY=your-groq-api-key
   STELLAR_SECRET_KEY=your-stellar-secret-key
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```
6. **Run Locally:**
   Create a .env file inside the BACKEND/ directory:
   ```bash
   uvicorn main.py --reload
   ```
    Access the app at: http://localhost:8000

## 🛠️ Usage
- Victim Registration: http://localhost:8000/register.html
- Disaster Feed (Admin): http://localhost:8000/disaster-feed
- Aid Transfers: http://localhost:8000/aid-transfer
- Chatbot Assistance: http://localhost:8000/chatbot-page
- API Endpoint for Aid Transfers: [http://localhost:8000/register.html](http://localhost:8000/api/aid-transfers (JSON response))

## 🗂️ Project Structure
```csharp
Disaster-Relief-Organizer/
└── BACKEND/
    ├── __pycache__/
    ├── frontend/              # Static HTML pages (register, about us)
    ├── routes/
    ├── static/                # Static HTML and JS files (disaster feed, chatbot, etc.)
    ├── templates/             # (Optional) Jinja2 templates
    ├── aid_log.json           # Aid transfer data
    ├── aid_logger.py          # Aid logging utilities
    ├── aid_service.py         # Aid distribution logic (Stellar transactions)
    ├── check_balance.py       # Stellar wallet balance checker
    ├── check.py               # General checks
    ├── clean_db.py            # Database cleanup utility
    ├── db.py                  # Database operations (SQLAlchemy)
    ├── disaster_simulator.py  # Disaster event simulator
    ├── fetch_aid_transfers.py # Fetch aid transfer data
    ├── fetch_balance.py       # Fetch Stellar balances
    ├── generate_victims.py    # Test victim data generation
    ├── initialize_db.py       # Database initialization script
    ├── main.py                # FastAPI entry point
    ├── main_backup.py         # Backup of main.py
    ├── main_new.py            # Alternate main.py version
    ├── models.py              # Database models (User, Disaster)
    ├── resetlink_db.py        # Reset database links
    ├── test_db.py             # Database test scripts
    ├── userauth.py            # User authentication module
    ├── wallets.py             # Stellar wallet creation and management
    ├── requirements.txt       # Python dependencies
    └── .gitignore             # Ignored files

```
## 🛠️ Technologies Used
- **Backend**: FastAPI (Python)
- **Frontend**: HTML, JavaScript (static)
- **Blockchain**: Stellar
- **Database**: PostgreSQL (via SQLAlchemy)
- **Dependencies**: fastapi, uvicorn, requests, markdown2, stellar-sdk
- **AI**: Groq API (for chatbot)
- **Deployment**: AWS EC2




## 🌟 Future Plans
- Integrate GPS verification for real-time victim location tracking.

- Optimize fund distribution to specific areas within cities.

- Add multi-language support for the chatbot.

- Upgrade frontend to React.js.

- Implement user authentication and role-based access (Admin/Victim).

# 🌟 Thank you for using Disaster Relief Organizer! 🌟
