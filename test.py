import streamlit as st
import csv
import random
import time

# Streamlit app configuratie
st.set_page_config(page_title="📚 Spaanse Flashcards", page_icon="📘", layout="centered")

st.markdown("<h1 style='text-align: center; color: #007acc;'>📘 Spaanse Flashcards</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Oefen je Spaanse woordenschat met interactieve flashcards!</p>", unsafe_allow_html=True)

# Functie om woordjes te lezen uit een standaard CSV-bestand
def lees_standaard_woordjes():
    woordjes = []
    try:
        with open("woordenlijst.csv", newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            for rij in reader:
                if len(rij) >= 2:
                    woordjes.append((rij[0].strip(), rij[1].strip()))
    except Exception as e:
        st.error(f"Fout bij het lezen van de standaard woordenlijst: {e}")
    return woordjes

# Initialiseer sessiestatus
if "woordjes" not in st.session_state:
    st.session_state.woordjes = lees_standaard_woordjes()
    random.shuffle(st.session_state.woordjes)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.moeilijk = []
    st.session_state.toon_antwoord = False
    st.session_state.afgerond = False
    st.session_state.starttijd = time.time()

# Timer berekenen
def get_timer():
    return int(time.time() - st.session_state.starttijd)

# Toon flashcard-interface
if st.session_state.woordjes and not st.session_state.afgerond:
    totaal = len(st.session_state.woordjes)
    index = st.session_state.index

    if index < totaal:
        spaans, nederlands = st.session_state.woordjes[index]

        st.markdown(f"### 📖 Woord {index + 1} van {totaal}")
        st.progress((index + 1) / totaal)

        # Highlight Spaans woord
        st.markdown(
            f"<div style='background-color:#e6f2ff; padding:20px; margin:30px 0; border-radius:10px;'>"
            f"<h2 style='text-align: center; color: #007acc; font-size: 36px;'>{spaans}</h2></div>",
            unsafe_allow_html=True
        )

        # Toon antwoord indien gevraagd
        if st.session_state.toon_antwoord:
            st.markdown(f"<h3 style='text-align: center; color: #333;'>{nederlands}</h3>", unsafe_allow_html=True)

        # Timer
        st.markdown(f"⏱️ Tijd bezig met dit woord: **{get_timer()} seconden**")

        # Knoppen
        toon, goed, moeilijk, volgende = st.columns(4)
        if toon.button("👁️ Toon antwoord"):
            st.session_state.toon_antwoord = True

        if goed.button("✅ Ik wist het"):
            st.session_state.score += 1
            st.session_state.toon_antwoord = True

        if moeilijk.button("❗ Moeilijk"):
            st.session_state.moeilijk.append((spaans, nederlands))
            st.session_state.toon_antwoord = True

        if volgende.button("➡️ Volgende woord"):
            st.session_state.index += 1
            st.session_state.toon_antwoord = False
            st.session_state.starttijd = time.time()

        st.markdown(f"**🎯 Score: {st.session_state.score} / {totaal}**")

    else:
        st.session_state.afgerond = True

# Eindscherm
if st.session_state.afgerond:
    st.success("🎉 Je hebt alle woordjes gehad!")
    totaal = len(st.session_state.woordjes)
    st.markdown("### 📊 Eindstatistieken")
    st.markdown(f"- ✅ Goede antwoorden: {st.session_state.score}")
    st.markdown(f"- ❗ Moeilijke woorden: {len(st.session_state.moeilijk)}")
    st.markdown(f"- 📄 Totaal woordjes: {totaal}")

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
            st.session_state.afgerond = False
            st.session_state.starttijd = time.time()

    if st.button("🔄 Opnieuw beginnen"):
        st.session_state.woordjes = lees_standaard_woordjes()
        random.shuffle(st.session_state.woordjes)
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.moeilijk = []
        st.session_state.toon_antwoord = False
        st.session_state.afgerond = False
        st.session_state.starttijd = time.time()
