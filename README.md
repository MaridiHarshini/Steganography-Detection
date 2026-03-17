# Steganography-Detection
This project is a Secure Image Steganography Web Application built using Python and Streamlit. It allows users to hide encrypted messages inside images and later extract them using a password.
The system uses ChaCha20 encryption to secure the message before embedding it in the image.
Features
User login and registration system
Password strength validation
Encrypt messages using ChaCha20
Hide encrypted text inside images
Extract and decrypt hidden messages
Image upload and download support
Simple web interface using Streamlit
Encryption algorithm comparison (ChaCha20, AES, Blowfish)
Technologies Used
Python
Streamlit
PyCryptodome
Pillow (PIL)
SQLite
Matplotlib

Project Structure
project-folder
│
├── main.py           # Main Streamlit application
├── auth.py           # Login and registration functions
├── db_init.py        # Database initialization
├── algo_benchmark.py # Encryption comparison
├── users.db          # SQLite database
└── README.md

The authentication system is implemented in auth.py.
The main application logic and encryption system are implemented in main.py.
The database initialization script is in db_init.py.
The encryption benchmark tool is in algo_benchmark.py.
Installation
Clone the repository

git clone https://github.com/yourusername/project-name.git
cd project-name

Install dependencies

pip install streamlit
pip install pycryptodome
pip install pillow
pip install matplotlib

Initialize database

python db_init.py

Run the application

streamlit run main.py
How It Works

Encoding Process

Upload an image

Enter a secret message

Provide a password

The message is encrypted and embedded into the image

Download the encoded image

Decoding Process

Upload the encoded image

Enter the password

The system extracts and decrypts the hidden message
