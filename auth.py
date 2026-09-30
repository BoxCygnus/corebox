import os
import json
import streamlit as st
from typing import Optional, Dict, Any
import config
from database import db, fix_mojibake

def get_current_user_email() -> Optional[str]:
    """
    Retrieves current user email.
    1. First checks Cloudflare Access HTTP header: Cf-Access-Authenticated-User-Email
    2. Checks Streamlit session_state
    3. Checks active_session.json
    4. Checks URL query param 'u' if available
    """
    # Cloudflare Access header detection if running in server with headers accessible
    try:
        if hasattr(st, "context") and hasattr(st.context, "headers"):
            cf_email = st.context.headers.get("cf-access-authenticated-user-email")
            if cf_email:
                return cf_email.strip().lower()
    except Exception:
        pass

    # Check session state
    if "user_email" in st.session_state and st.session_state["user_email"]:
        return st.session_state["user_email"].strip().lower()

    # Check active_session.json
    try:
        sess_file = os.path.join(os.path.dirname(__file__), "active_session.json")
        if os.path.exists(sess_file):
            with open(sess_file, "r", encoding="utf-8") as sf:
                s_data = json.load(sf)
                if s_data.get("email"):
                    norm_e = s_data["email"].strip().lower()
                    u = db.get_user(norm_e)
                    if u:
                        st.session_state["user_email"] = norm_e
                        st.session_state["user_name"] = u.get("full_name", norm_e.split("@")[0])
                        st.session_state["user_role"] = u.get("role", "user")
                        st.session_state["user_status"] = u.get("status", "pending")
                        return norm_e
    except Exception:
        pass

    # Check URL query param 'u' if present
    try:
        q_u = st.query_params.get("u")
        if q_u and "@" in q_u:
            norm_q_u = q_u.strip().lower()
            user = db.get_user(norm_q_u)
            if user:
                st.session_state["user_email"] = norm_q_u
                st.session_state["user_name"] = user.get("full_name", norm_q_u.split("@")[0])
                st.session_state["user_role"] = user.get("role", "user")
                st.session_state["user_status"] = user.get("status", "pending")
                return norm_q_u
    except Exception:
        pass

    return None

def get_current_user() -> Optional[Dict[str, Any]]:
    email = get_current_user_email()
    if not email:
        return None
    return db.get_user(email)

def login_user(email: str, full_name: str = ""):
    email = email.strip().lower()
    clean_name = fix_mojibake(full_name)
    user = db.register_or_get_user(email, clean_name)
    st.session_state["user_email"] = email
    st.session_state["user_name"] = user.get("full_name", email.split("@")[0])
    st.session_state["user_role"] = user.get("role", "user")
    st.session_state["user_status"] = user.get("status", "pending")
    # Save to active_session.json in root
    try:
        sess_file = os.path.join(os.path.dirname(__file__), "active_session.json")
        with open(sess_file, "w", encoding="utf-8") as sf:
            json.dump({"email": email}, sf)
    except Exception:
        pass
    return user

def decode_and_verify_google_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and verifies a Google OAuth 2.0 Identity Token (JWT):
    - Aud (Audience) must match config.GOOGLE_CLIENT_ID
    - Iss (Issuer) must match accounts.google.com
    - Exp (Expiry) must be in the future
    - Email must be verified by Google
    """
    import base64
    import json
    import time
    if not token or not isinstance(token, str):
        return None
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            return None
        payload_b64 = parts[1]
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += "=" * (4 - rem)
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        data = json.loads(payload_bytes.decode("utf-8"))

        expected_client_id = config.GOOGLE_CLIENT_ID.strip()
        aud = str(data.get("aud", ""))
        if aud != expected_client_id and not aud.startswith(expected_client_id.split("-")[0]):
            return None

        iss = data.get("iss", "")
        if iss not in ["accounts.google.com", "https://accounts.google.com"]:
            return None

        exp = data.get("exp", 0)
        if exp < time.time() - 600:
            return None

        email = data.get("email")
        if not email or "@" not in email:
            return None

        return data
    except Exception:
        return None

def verify_and_login_google_token(token: str) -> Optional[Dict[str, Any]]:
    data = decode_and_verify_google_jwt(token)
    if not data:
        return None
    email = data.get("email", "").strip().lower()
    name = data.get("name", "")
    picture = data.get("picture", "")
    if picture:
        st.session_state["user_picture"] = picture
    return login_user(email, name)

def logout_user():
    st.session_state.pop("user_email", None)
    st.session_state.pop("user_name", None)
    st.session_state.pop("user_role", None)
    st.session_state.pop("user_status", None)
    st.session_state.pop("user_picture", None)
    try:
        if "u" in st.query_params:
            del st.query_params["u"]
    except Exception:
        pass

def is_admin() -> bool:
    email = get_current_user_email()
    if not email:
        return False
    user = db.get_user(email)
    if not user:
        return False
    return (
        user.get("status") == "active"
        and (user.get("role") == "admin" or email == config.ADMIN_EMAIL)
    )

def is_active() -> bool:
    email = get_current_user_email()
    if not email:
        return False
    user = db.get_user(email)
    if not user:
        return False
    return user.get("status") == "active"

def is_pending() -> bool:
    email = get_current_user_email()
    if not email:
        return False
    user = db.get_user(email)
    if not user:
        return False
    return user.get("status") == "pending"
