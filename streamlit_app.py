import streamlit as st
from PIL import Image, ImageOps
import random

if "ingelogd" not in st.session_state: 
    st.session_state.ingelogd = False 

if not st.session_state.ingelogd: 
    wachtwoord = st.text_input("Voer het wachtwoord in om de app te kunnen gebruiken:", type="password") 
    
    if wachtwoord == st.secrets["app_wachtwoord"]: 
        st.session_state.ingelogd = True 
        st.rerun() 
    elif wachtwoord != "": 
        st.error("Verkeerde wachtwoord ingevoerd.") 
    st.stop() 

lijst_caption = []
with open("bestand.csv") as bron:
    for regel in bron:
        foto_caption = regel.strip().split(",")
        lijst_caption.append(foto_caption[3])
lijst_caption.pop(0)

aantal_fotos = len(lijst_caption)

if "teller" not in st.session_state:
    st.session_state.teller = 1

teller = st.session_state.teller
nummer = str(teller)
huidige_foto = "Fotos/Foto (" + nummer + ").jpeg"
huidige_caption = lijst_caption[teller - 1]

st.header("REWIND26", text_alignment="center")

afbeelding = Image.open(huidige_foto)
rechte_afbeelding = ImageOps.exif_transpose(afbeelding)
if rechte_afbeelding.height > rechte_afbeelding.width:
    nieuwe_breedte = rechte_afbeelding.width
    nieuwe_hoogte = int(rechte_afbeelding.width) 
    rechte_afbeelding = ImageOps.fit(rechte_afbeelding, (nieuwe_breedte, nieuwe_hoogte))

links, midden, rechts = st.columns([0.5, 3, 0.5])

with midden:
    st.image(rechte_afbeelding, use_container_width=True)
    st.write(f"{huidige_caption} - ({teller}/{aantal_fotos})")
    
    with st.container(border=False):
        col1, col2, col3 = st.columns(3, gap="xxsmall")

        with col1:
            if st.button("Vorige", use_container_width=True, type="primary"):
                if st.session_state.teller > 1:
                    st.session_state.teller -= 1
                    st.rerun()

        with col2:
            if st.button("Volgende", use_container_width=True, type="primary"):
                if st.session_state.teller < aantal_fotos:
                    st.session_state.teller += 1
                else:
                    st.session_state.teller = 1
                st.rerun()

        with col3:
            if st.button("Random", use_container_width=True, type="primary"):
                st.session_state.teller = random.randint(1, aantal_fotos)
                st.rerun()

    st.caption("Mocht er ergens een fout zijn, stuur een mail naar @mail....")
