import streamlit as st
import mysql.connector
import pandas as pd
from collections import Counter

# =========================
# 🎨 CONFIG UI
# =========================
st.set_page_config(
    page_title="Job Market Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Plateforme d'analyse des offres d'emploi")
st.markdown("### Analyse interactive du marché de l'emploi")

# =========================
# 🔗 Connexion MySQL
# =========================
conn = mysql.connector.connect(
    host="localhost",   # ⚠️ PC local
    user="root",
    password="root123",
    database="job_datawarehouse"
)

# 📥 Charger données
df_city = pd.read_sql("SELECT * FROM jobs_by_city", conn)
df_sector = pd.read_sql("SELECT * FROM jobs_by_sector", conn)
df_date = pd.read_sql("SELECT * FROM jobs_by_date", conn)

conn.close()

# =========================
# 📊 KPI (haut)
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("🏙️ Nombre de villes", len(df_city))
col2.metric("🏢 Nombre de secteurs", len(df_sector))
col3.metric("💼 Nombre total des offres", df_date["total"].sum())

st.divider()

# =========================
# 🎛️ FILTRES (SELECT ALL FIX FINAL PRO)
# =========================
st.sidebar.header("🎛️ Filtres")

top_n = st.sidebar.slider("Top N villes", 5, 20, 10)

all_sectors = list(df_sector["sector"].unique())

st.sidebar.subheader("🏢 Secteurs")

# =========================
# 🧠 INIT STATE
# =========================
default_sectors = ["informatique", "banque / finance", "comptabilité / audit", "btp / génie civil", " hôtellerie / restauration"]  # 🔥 modifie selon ton dataset

if "sector_state" not in st.session_state:
    st.session_state.sector_state = {
        s: (s in default_sectors) for s in all_sectors
    }

if "checkbox_version" not in st.session_state:
    st.session_state.checkbox_version = 0
if "checkbox_version" not in st.session_state:
    st.session_state.checkbox_version = 0

# =========================
# 🎯 BOUTONS
# =========================

col1, col2 = st.sidebar.columns(2)

if col1.button("✅ Tout"):
    for s in all_sectors:
        st.session_state.sector_state[s] = True
    st.session_state.checkbox_version += 1
    st.rerun()

if col2.button("❌ Aucun"):
    for s in all_sectors:
        st.session_state.sector_state[s] = False
    st.session_state.checkbox_version += 1
    st.rerun()

# =========================
# ✅ CHECKBOX (clé dynamique)
# =========================
selected_sectors = []

for sector in all_sectors:
    key = f"{sector}_{st.session_state.checkbox_version}"

    checked = st.sidebar.checkbox(
        sector,
        value=st.session_state.sector_state[sector],
        key=key
    )

    st.session_state.sector_state[sector] = checked

    if checked:
        selected_sectors.append(sector)

# 📊 info utilisateur
st.sidebar.markdown(f"✅ {len(selected_sectors)} secteurs sélectionnés")
# =========================
# 🧠 FILTRAGE
# =========================
df_sector_filtered = df_sector[
    df_sector["sector"].isin(selected_sectors)
].sort_values(by="total", ascending=False)

df_city_sorted = df_city.sort_values(by="total", ascending=False).head(top_n)

df_date_sorted = df_date.sort_values(by="date")

# =========================
# 📊 GRID 2x2
# =========================
col1, col2 = st.columns(2)

# 📈 Tendances
with col1:
    st.subheader("📍 Top villes")
    st.bar_chart(df_city_sorted.set_index("city"))

    

# 📍 Villes
with col2:
    st.subheader("🏆 Top secteurs")

    top_sectors = df_sector.sort_values(
        by="total", ascending=False
    ).head(5)

    st.bar_chart(top_sectors.set_index("sector"))

col3, col4 = st.columns(2)

# 🏢 Secteurs
with col3:
    st.subheader("🏢 Répartition par secteur")
    st.bar_chart(df_sector_filtered.set_index("sector"))

# 🔥 Top secteurs
with col4:
    st.subheader("📈 Offres par jour")
    st.line_chart(df_date_sorted.set_index("date"))

# =========================
# 📋 TABLEAU FINAL
# =========================
#st.subheader("📋 Données détaillées")

#st.dataframe(df_city_sorted)

# =========================
# 🎉 FIN
# =========================
#st.success("Dashboard prêt 🚀")