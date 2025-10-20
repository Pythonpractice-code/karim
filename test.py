import streamlit as st
import csv
import random

def lees_woordjes(bestandsnaam):
    woordjes = []
    with open(bestandsnaam, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for rij in reader:
            if len(rij) >= 2:
                woordjes.append((rij[0].strip(), rij[1].strip()))
    return woordjes

woordjes = lees_woordjes("woordenlijst.csv")
if "index" not in st.session_state:
    st.session_state.index = 0
    random.shuffle(woordjes)
    st.session_state.score = 0
    st.session_state.moeilijk = []

st.title("📚 Spaanse Flashcards")
st.write(f"Woord {st.session_state.index + 1} van {len(woordjes)}")

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