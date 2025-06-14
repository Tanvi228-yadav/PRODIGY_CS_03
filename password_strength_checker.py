import streamlit as st
import re

st.set_page_config(page_title="🔒 Password Strength Checker", page_icon=":closed_lock_with_key:")

st.title("🔒 Password Strength Checker")
st.markdown("Check how strong your password is and get instant tips to improve it!")

with st.sidebar:
    st.header("Tips for a Strong Password :bulb:")
    st.markdown("""
    - At least 8 characters
    - Mix uppercase and lowercase letters
    - Include numbers
    - Add special characters (!@#$...)
    """)

password = st.text_input("Enter your password", type="password")

def check_strength(pwd):
    suggestions = []
    score = 0

    if len(pwd) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", pwd):
        score += 1
    else:
        suggestions.append("Include at least one uppercase letter.")

    if re.search(r"[a-z]", pwd):
        score += 1
    else:
        suggestions.append("Include at least one lowercase letter.")

    if re.search(r"\d", pwd):
        score += 1
    else:
        suggestions.append("Include at least one digit.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
        score += 1
    else:
        suggestions.append("Include at least one special character (!@#$%^&* etc.).")

    if len(pwd) == 0:
        return None, []

    if score == 5:
        strength = "Strong 💪"
    elif score >= 3:
        strength = "Medium ⚠️"
    else:
        strength = "Weak ❌"

    return strength, suggestions, score

if password:
    strength, feedback, score = check_strength(password)
    if score == 5:
        st.success(f"**Strength:** {strength}")
    elif score >= 3:
        st.warning(f"**Strength:** {strength}")
    else:
        st.error(f"**Strength:** {strength}")
    if feedback:
        st.markdown("**Suggestions:**")
        for sug in feedback:
            st.markdown(f"- {sug}")
else:
    st.info("Please enter a password to check its strength.")