import streamlit as st
from PIL import Image
from Crypto.Cipher import ChaCha20
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import io
import re
from auth import login_user, register_user, logout

ADMIN_SECRET_KEY = "TopSecret@2025"  # Change if needed

# ===================== Encryption =====================
def derive_key(password, salt):
    return PBKDF2(password, salt, dkLen=32, count=1000000)

def encrypt_message(message, password):
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    nonce = get_random_bytes(12)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(message.encode())
    return base64.b64encode(salt + nonce + ciphertext).decode()

def decrypt_message(enc_data_b64, password):
    enc_data = base64.b64decode(enc_data_b64.encode())
    salt = enc_data[:16]
    nonce = enc_data[16:28]
    ciphertext = enc_data[28:]
    key = derive_key(password, salt)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    try:
        return cipher.decrypt(ciphertext).decode()
    except:
        return "Invalid password or corrupted data."

# ===================== Image Steganography =====================
def get_usable_pixel_count(img, threshold=600):
    img = img.convert("RGB")
    width, height = img.size
    count = 0
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            if r + g + b < threshold:
                count += 1
    return count

def encode_message(img, msg, threshold=600):
    img = img.convert("RGB")
    encoded = img.copy()
    width, height = img.size
    idx = 0
    msg += chr(0)
    for y in range(height):
        for x in range(width):
            if idx >= len(msg):
                return encoded
            r, g, b = img.getpixel((x, y))
            if r + g + b < threshold:
                encoded.putpixel((x, y), (r, g, ord(msg[idx])))
                idx += 1
    return encoded

def decode_message(img):
    img = img.convert("RGB")
    width, height = img.size
    msg = ""
    for y in range(height):
        for x in range(width):
            _, _, b = img.getpixel((x, y))
            if b == 0:
                return msg
            msg += chr(b)
    return msg

# ===================== Password Strength Checker =====================
def is_strong_password(pwd):
    return (
        len(pwd) >= 8 and
        re.search(r"[A-Z]", pwd) and
        re.search(r"[a-z]", pwd) and
        re.search(r"[0-9]", pwd) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd)
    )

# ===================== Streamlit UI =====================
def main():
    st.set_page_config(page_title="🖼 Secure Image Steganography", layout="wide")

    # Initialize session
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

    if not st.session_state.logged_in:
        st.title("🔐 Login to Access Steganography App")
        login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])

        with login_tab:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = login_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user[0]
                    st.session_state.role = user[2]
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        with register_tab:
            new_user = st.text_input("Choose a username", key="reg_user")
            new_pass = st.text_input("Choose a strong password", type="password", key="reg_pass")
            if new_pass and not is_strong_password(new_pass):
                st.warning("⚠️ Password must include uppercase, lowercase, number, and special char.")
            if st.button("Register"):
                if is_strong_password(new_pass):
                    success = register_user(new_user, new_pass)
                    if success:
                        st.success("✅ Registered successfully. Please login.")
                    else:
                        st.error("❌ Username already exists.")
                else:
                    st.error("❌ Password is too weak.")
    else:
        st.sidebar.success(f"👋 Logged in as: {st.session_state.username} ({st.session_state.role})")
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()

        st.title("🔐 Secure Image Steganography with Visual Stealth")

        tab1, tab2 = st.tabs(["🖼 Hide Message", "🔓 Reveal Message"])

        with tab1:
            st.header("🔒 Hide & Encrypt Text in Image")
            image_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])
            message = st.text_area("Enter the secret message")
            password = st.text_input("Encryption Password", type="password")
            if password and not is_strong_password(password):
                st.warning("⚠️ Weak password. Include upper, lower, number & special char.")

            if image_file:
                img = Image.open(image_file)
                width, height = img.size
                usable_pixels = get_usable_pixel_count(img)
                st.markdown(f"📐 Image size: {width} x {height}")
                st.markdown(f"🧮 Usable pixels: {usable_pixels} → Max characters: {usable_pixels - 1}")

            if st.button("🔏 Encode and Download"):
                if image_file and message and password:
                    if not is_strong_password(password):
                        st.error("❌ Use a strong password.")
                    else:
                        if len(message) + 1 > usable_pixels:
                            st.warning("🚫 Message too long. Use a shorter message or darker image.")
                        else:
                            encrypted = encrypt_message(message, password)
                            encoded_img = encode_message(img, encrypted)
                            buf = io.BytesIO()
                            encoded_img.save(buf, format="PNG")
                            st.success("✅ Message encrypted and embedded successfully!")
                            st.download_button("⬇ Download Encoded Image", data=buf.getvalue(), file_name="encoded_image.png", mime="image/png")
                else:
                    st.error("Please upload an image, enter a message and password.")

        with tab2:
            st.header("🔍 Extract & Decrypt Text from Image")
            image_file2 = st.file_uploader("Upload encoded image", type=["png", "jpg", "jpeg"], key="decode")
            password2 = st.text_input("Enter password to decrypt", type="password", key="pwd")
            if password2 and not is_strong_password(password2):
                st.warning("⚠️ Weak password.")

            if st.button("🔓 Decode Message"):
                if image_file2 and password2:
                    img2 = Image.open(image_file2)
                    secret_enc = decode_message(img2)
                    secret_dec = decrypt_message(secret_enc, password2)
                    if "Invalid password" in secret_dec:
                        st.error(secret_dec)
                    else:
                        st.success("🎉 Secret message:")
                        st.code(secret_dec)
                else:
                    st.error("Upload an image and provide a password.")

if __name__ == '__main__':
    main()

