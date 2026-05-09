# 📊 Plateforme d’analyse des offres d’emploi

## 🎯 Description

Ce projet consiste à concevoir une plateforme complète de traitement et d’analyse des offres d’emploi à partir de données collectées sur le web.

L’objectif est de mettre en place un pipeline de données moderne permettant :
- la collecte des données
- leur traitement
- leur stockage
- leur analyse
- leur visualisation

---

## 🏗️ Architecture du projet

Le pipeline suit une architecture de type **Data Engineering moderne** :

Scrapy → Kafka → Consumer → MinIO (Data Lake)
                         ↓
                     Airflow
                Silver → Gold
                         ↓
                    MySQL (Data Warehouse)
                         ↓
                   Streamlit (Dashboard)

---

## ⚙️ Technologies utilisées

- 🐍 Python
- 🕷️ Scrapy (Web Scraping)
- 📨 Apache Kafka (Streaming)
- ☁️ MinIO (Data Lake)
- 🔄 Apache Airflow (Orchestration)
- 🗄️ MySQL (Data Warehouse)
- 📊 Streamlit (Dashboard)

---

## 📁 Structure des données

### 🥉 Bronze
- Données brutes issues du scraping
- Stockées dans MinIO

### 🥈 Silver
- Données nettoyées et validées
- Suppression des valeurs manquantes

### 🥇 Gold
- Données agrégées pour l’analyse
- Statistiques (jobs par ville, secteur, date)

---

## 📊 Data Warehouse

Les données analytiques sont stockées dans MySQL :

Tables :
- `jobs_by_city`
- `jobs_by_sector`
- `jobs_by_date`

---

## 📈 Dashboard

Un dashboard interactif a été développé avec Streamlit permettant de visualiser :

- 📈 Tendances des offres d’emploi
- 📍 Répartition géographique
- 🏢 Répartition par secteur
- 🎛️ Filtres interactifs (secteurs, top villes)

---

## 🧪 Qualité des données

Des contrôles ont été mis en place :

### ✔ Tests
- Suppression des articles sans titre
- Suppression des dates manquantes
- Filtrage des contenus trop courts

### ✔ Dimensions
- Complétude
- Cohérence
- Validité

---

## 🏛️ Gouvernance des données

La gouvernance est assurée par :

- Structuration en Bronze / Silver / Gold
- Orchestration via Airflow
- Stockage dans MinIO (traçabilité)
- Partitionnement des données (par date)

---

## 🚀 Lancement du projet

### 1. Lancer Docker
- bash
docker-compose up -d

### 2. Lancer consumer:
    docker exec -it airflow bash
    python /opt/airflow/project/consumer.py

### 3. Lancer Airflow
username : firdaous
mot de pass: firdaous

### 4. Lancer le dashboard
streamlit run dashboard.py

Accès : http://localhost:8501

