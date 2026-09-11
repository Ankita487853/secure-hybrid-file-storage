🔐 Secure Hybrid Encrypted File Storage System
📌 Project Overview

The Secure Hybrid Encrypted File Storage System is a multi-layered security framework designed to protect user files through advanced cryptographic techniques. The system integrates symmetric encryption (AES-256), asymmetric encryption (RSA-2048), chaos-based randomization, hashing, compression, and OTP-based authentication to ensure strong confidentiality, integrity, and controlled access.

This project demonstrates how hybrid encryption can combine performance and security while providing a practical file storage solution.

🚀 Key Features

✅ User Registration & Secure Login
✅ AES-256 File Encryption
✅ RSA-2048 Key Wrapping
✅ Chaos-Based Cipher Diffusion
✅ SHA-256 Integrity Verification
✅ ZIP Compression for Storage Optimization
✅ OTP-Based Secure Decryption
✅ Metadata Generation & Audit Tracking
✅ User-Specific Secure Dashboard

🏗️ System Architecture

The system follows a hybrid encryption workflow:
File Upload
ZIP Compression
AES-256 Encryption
RSA Key Wrapping (AES key encrypted with RSA public key)
Chaos-Based Cipher Transformation
Metadata Generation
Secure Storage

For decryption:
OTP Verification
RSA Private Key Unwrap
Reverse Chaos Diffusion
AES Decryption
Original File Restoration

🧩 Modules

1️⃣ User Authentication Module
Handles user registration, login, password hashing, and session management using Flask-Login.

2️⃣ File Upload & Pre-Processing
Accepts multiple file formats and converts them into binary format for encryption.

3️⃣ AES Encryption Module
Encrypts files using AES-256 with a randomly generated key and IV.

4️⃣ RSA Key Wrapping Module
Secures the AES key using RSA-2048 encryption.

5️⃣ Chaos-Based Security Layer
Applies logistic map-based transformation to increase unpredictability.

6️⃣ Compression Module
Reduces storage size using ZIP compression.

7️⃣ Metadata Storage Module
Stores encryption parameters, file hash, timestamps, and statistics.

8️⃣ OTP-Based Decryption
Adds two-factor authentication before decryption.

🛠️ Technologies Used

Python
Flask
Flask-Login
PyCryptodome
RSA Cryptography
SHA-256 Hashing
ZIP Compression
JSON Metadata Handling

🔒 Security Highlights
Hybrid encryption approach
Multi-layered protection
Secure key exchange mechanism
Protection against brute-force attacks
Integrity verification using hashing
OTP-based access control

📊 Testing Results

Successfully encrypted and decrypted multiple file formats
Verified data integrity using hash comparison
Confirmed failure of decryption with incorrect keys
Achieved secure storage in encrypted form only

📂 Installation
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
pip install -r requirements.txt
python app.py

🖥️ Usage

Register a new account
Login securely
Upload a file
Encrypt and store
Request OTP
Decrypt and download

🎯 Future Improvements

Cloud integration (AWS / Azure)
Multi-factor authentication expansion
Blockchain-based audit logs
File sharing with secure key exchange
