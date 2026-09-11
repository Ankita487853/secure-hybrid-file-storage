from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os, time, secrets

from crypto.aes_layer import aes_encrypt, aes_decrypt
from crypto.rsa_layer import generate_rsa_keys, rsa_wrap_key, rsa_unwrap_key
from crypto.chaotic_key import mix_aes_key, unmix_aes_key
from crypto.utils import save_bytes, save_json, load_bytes, load_json

# -------------------- Flask Setup --------------------
app = Flask(__name__)
app.secret_key = "supersecretkey123"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -------------------- Server-Side Private Keys Storage --------------------
PRIVATE_KEYS = {}  # filename -> private key

# -------------------- Security Key --------------------
SECURITY_KEY = "SuperSecret123!"  # User must enter this to decrypt

# ==============================================================
#                          WEB PAGES
# ==============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt')
def encrypt_page():
    return render_template('encrypt.html')


@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')


@app.route('/dashboard')
def dashboard():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('dashboard.html', files=files)


# ==============================================================
#                     ENCRYPTION PROCESS
# ==============================================================

@app.route('/do_encrypt', methods=['POST'])
def do_encrypt():
    f = request.files.get('file')
    if not f:
        flash("Please upload a file!", "danger")
        return redirect(url_for('encrypt_page'))

    data = f.read()

    # AES Encryption
    enc_data, aes_key, iv = aes_encrypt(data)

    # Chaotic Mixing
    seed = secrets.randbits(64) / (2**64)
    mixed_key, chaos_meta = mix_aes_key(aes_key, seed=seed, r=3.99, burn=250)

    # RSA Keys + wrapping
    rsa_private, rsa_public = generate_rsa_keys()
    wrapped_key = rsa_wrap_key(mixed_key, rsa_public)

    # Store private key in memory
    timestamp = str(int(time.time()))
    enc_filename = f"{timestamp}_{f.filename}.enc"
    PRIVATE_KEYS[enc_filename] = rsa_private

    # Save encrypted file
    enc_path = os.path.join(app.config["UPLOAD_FOLDER"], enc_filename)
    save_bytes(enc_path, enc_data)

    # Save metadata (without private key)
    meta = {
        "iv": iv.hex(),
        "wrapped_key": wrapped_key.hex(),
        "rsa_public": rsa_public.decode(),
        "chaos": chaos_meta,
        "original_filename": f.filename
    }
    meta_path = enc_path + ".json"
    save_json(meta_path, meta)

    flash("File encrypted successfully!", "success")
    return redirect(url_for('dashboard'))


# ==============================================================
#                 DASHBOARD & SECURE DECRYPTION
# ==============================================================

# Download
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# Metadata preview (private key hidden)
@app.route('/preview/<filename>')
def preview(filename):
    meta_file = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".json")
    if not os.path.exists(meta_file):
        flash("Metadata not found!", "danger")
        return redirect(url_for('dashboard'))

    meta = load_json(meta_file)
    return render_template("preview.html", meta=meta, filename=filename)


# Auto-decrypt (GET shows security key form, POST decrypts)
@app.route('/auto_decrypt/<filename>', methods=['GET', 'POST'])
def auto_decrypt(filename):
    if request.method == 'POST':
        user_key = request.form.get('security_key')
        if user_key != SECURITY_KEY:
            flash("Incorrect security key! Decryption denied.", "danger")
            return redirect(url_for('dashboard'))

        enc_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        meta_path = enc_path + ".json"
        if not os.path.exists(enc_path) or not os.path.exists(meta_path):
            flash("Encrypted file or metadata missing!", "danger")
            return redirect(url_for('dashboard'))

        enc_data = load_bytes(enc_path)
        meta = load_json(meta_path)
        rsa_private = PRIVATE_KEYS.get(filename)
        if not rsa_private:
            flash("Private key missing on server. Cannot decrypt.", "danger")
            return redirect(url_for('dashboard'))

        iv = bytes.fromhex(meta["iv"])
        wrapped_key = bytes.fromhex(meta["wrapped_key"])
        mixed_key = rsa_unwrap_key(wrapped_key, rsa_private)
        aes_key = unmix_aes_key(mixed_key, meta["chaos"])
        plain = aes_decrypt(enc_data, aes_key, iv)

        outname = "decrypted_" + meta["original_filename"]
        outpath = os.path.join(app.config['UPLOAD_FOLDER'], outname)
        save_bytes(outpath, plain)

        flash(f"Auto-decrypted: {outname}", "success")
        return redirect(url_for('dashboard'))

    # GET request → show security key form
    return render_template("security_key.html", filename=filename)


# Delete
@app.route('/delete/<filename>')
def delete(filename):
    enc_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    meta_path = enc_path + ".json"

    if os.path.exists(enc_path):
        os.remove(enc_path)
    if os.path.exists(meta_path):
        os.remove(meta_path)
    if filename in PRIVATE_KEYS:
        del PRIVATE_KEYS[filename]

    flash("File deleted!", "warning")
    return redirect(url_for('dashboard'))


# ==============================================================
#                       RUN APP
# ==============================================================

if __name__ == "__main__":
    app.run(debug=True)
