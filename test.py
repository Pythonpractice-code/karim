import streamlit as st
import csv
import random
import pandas as pd

def lees_woordjes(bestand):
    woordjes = []
    reader = csv.reader(bestand, delimiter=';')
    next(reader)  # Sla kopregel over
    for rij in reader:
        if len(rij) >= 2:
            woordjes.append((rij[0].strip(), rij[1].strip()))
    return woordjes

st.title("📚 Spaanse Flashcards")

# 🔹 Upload-optie
upload = st.file_uploader("📂 Voeg je eigen woordenlijst toe (CSV)", type="csv")

# 🔹 Gebruik upload of standaardbestand
if upload:
    woordjes = lees_woordjes(upload)
else:
    with open("woordenlijst.csv", encoding="utf-8-sig") as f:
        woordjes = lees_woordjes(f)

# 🔹 Shuffle en sessiestate
if "index" not in st.session_state:
    random.shuffle(woordjes)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.moeilijk = []

# 🔹 Toon flashcard
spaans, nederlands = woordjes[st.session_state.index]
st.header(spaans)

if st.button("Toon antwoord"):
    st.subheader(nederlands)

col1, col2, col3 = st.columns(3)
if col1.button("Ik wist het"):
    st.session_state.score += 1
    st.session_state.index += 1
elif col2.button("Moeilijk"):
    st.session_state.moeilijk.append((spaans, nederlands))
    st.session_state.index += 1
elif col3.button("Volgende"):
    st.session_state.index += 1

st.write(f"Score: {st.session_state.score}")
st.write(f"Woord {st.session_state.index + 1} van {len(woordjes)}")
