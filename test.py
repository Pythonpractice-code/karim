import streamlit as st
import csv
import random
import io

# Streamlit app configuratie
st.set_page_config(page_title="📚 Spaanse Flashcards", page_icon="📘", layout="centered")

st.markdown("<h1 style='text-align: center; color: #007acc;'>📘 Spaanse Flashcards</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Oefen je Spaanse woordenschat met interactieve flashcards!</p>", unsafe_allow_html=True)

# Functie om woordjes te lezen uit een CSV-bestand
def lees_woordjes(uploaded_file):
    woordjes = []
    try:
        content = io.StringIO(uploaded_file.getvalue().decode("utf-8-sig"))
        reader = csv.reader(content, delimiter=';')
        next(reader)  # sla kopregel over
        for rij in reader:
            if len(rij) >= 2:
                woordjes.append((rij[0].strip(), rij[1].strip()))
    except Exception as e:
        st.error(f"Fout bij het lezen van het bestand: {e}")
    return woordjes

# Uploadfunctie voor CSV-bestand
uploaded_file = st.file_uploader("📂 Upload je woordenlijst (CSV met ; als scheidingsteken)", type=["csv"])

# Initialiseer sessiestatus
if "woordjes" not in st.session_state:
    st.session_state.woordjes = []
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.moeilijk = []
    st.session_state.toon_antwoord = False
    st.session_state.herhaling = False

# Als bestand is geüpload, lees de woordjes
if uploaded_file:
    st.session_state.woordjes = lees_woordjes(uploaded_file)
    random.shuffle(st.session_state.woordjes)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.moeilijk = []
    st.session_state.toon_antwoord = False
    st.session_state.herhaling = False

# Toon flashcard-interface als er woordjes zijn
if st.session_state.woordjes:
    totaal = len(st.session_state.woordjes)
    index = st.session_state.index

    if index < totaal:
        spaans, nederlands = st.session_state.woordjes[index]

        st.markdown(f"### 📖 Woord {index + 1} van {totaal}")
        st.progress((index + 1) / totaal)

        st.markdown(f"<h2 style='text-align: center; color: #333;'>{spaans}</h2>", unsafe_allow_html=True)

        if st.session_state.toon_antwoord:
            st.markdown(f"<h3 style='text-align: center; color: #007acc;'>{nederlands}</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        if col1.button("👁️ Toon antwoord"):
            st.session_state.toon_antwoord = True

        if col2.button("✅ Ik wist het"):
            st.session_state.score += 1
            st.session_state.index += 1
            st.session_state.toon_antwoord = False

        if col3.button("❗ Moeilijk"):
            st.session_state.moeilijk.append((spaans, nederlands))
            st.session_state.index += 1
            st.session_state.toon_antwoord = False

        st.markdown(f"**🎯 Score: {st.session_state.score} / {totaal}**")

    else:
        st.success("🎉 Je hebt alle woordjes gehad!")
        st.markdown(f"**Eindscore: {st.session_state.score} / {totaal}**")

        if st.session_state.moeilijk:
            st.markdown("### ❗ Moeilijke woorden")
            for s, n in st.session_state.moeilijk:
                st.write(f"- {s} = {n}")

            if st.button("🔁 Herhaal moeilijke woorden"):
                st.session_state.woordjes = st.session_state.moeilijk.copy()
                random.shuffle(st.session_state.woordjes)
                st.session_state.index = 0
                st.session_state.score = 0
                st.session_state.moeilijk = []
                st.session_state.toon_antwoord = False
                st.session_state.herhaling = True
else:
    st.info("📄 Upload een woordenlijst om te beginnen.")
