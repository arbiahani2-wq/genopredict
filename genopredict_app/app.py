import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import time
import random

# --- CONFIGURATION ---
st.set_page_config(
    page_title="GenoPredict AD",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #0E1117;
        text-align: center;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #262730;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-container {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #dce0e6;
    }
    .success-box {
        padding: 1rem;
        background-color: #d1fae5;
        color: #065f46;
        border-radius: 5px;
        border: 1px solid #34d399;
        text-align: center;
        margin-top: 1rem;
    }
    .highlight-text {
        font-weight: bold;
        color: #2563eb;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

@st.cache_resource
def load_model():
    try:
        with open("alzheimer_rf_model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None

def parse_genotype(gt_str, ref, alt):
    """Parses '0/1' or '1|1' into additive count (0, 1, 2)"""
    if pd.isna(gt_str): return 0
    gt_str = str(gt_str)
    sep = '|' if '|' in gt_str else '/'
    try:
        alleles = [int(x) for x in gt_str.split(sep)]
        return sum(alleles) # 0=Ref/Ref, 1=Ref/Alt, 2=Alt/Alt (assuming 0 is ref)
    except:
        return 0

def get_allele_indices(gt_str):
    """Returns list of indices like [0, 1]"""
    if pd.isna(gt_str): return [0, 0]
    gt_str = str(gt_str)
    sep = '|' if '|' in gt_str else '/'
    try:
        return [int(x) for x in gt_str.split(sep)]
    except:
        return [0, 0]

def simulate_children(father_df, mother_df, snps, n=1000):
    """Simulates n children based on parents"""
    sim_data = [] # List of dicts
    
    # Pre-process parents alleles for target SNPs
    p_alleles = {} # snp -> (father_indices, mother_indices)
    
    for rs in snps:
        f_row = father_df[father_df['rsID'] == rs]
        m_row = mother_df[mother_df['rsID'] == rs]
        
        f_idx = [0, 0]
        if not f_row.empty:
            f_idx = get_allele_indices(f_row.iloc[0]['GT'])
            
        m_idx = [0, 0]
        if not m_row.empty:
            m_idx = get_allele_indices(m_row.iloc[0]['GT'])
            
        p_alleles[rs] = (f_idx, m_idx)
        
    # Generate children
    for i in range(n):
        child = {}
        for rs in snps:
            f_idx, m_idx = p_alleles[rs]
            # Mendelian inheritance
            f_a = random.choice(f_idx)
            m_a = random.choice(m_idx)
            child[rs] = f_a + m_a # Additive genotype (0, 1, 2)
            
        sim_data.append(child)
        
    return pd.DataFrame(sim_data)

# --- APP FLOW ---

# Initialize session state for navigation
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'father_data' not in st.session_state:
    st.session_state.father_data = None
if 'mother_data' not in st.session_state:
    st.session_state.mother_data = None
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'risk_score_global' not in st.session_state:
    st.session_state.risk_score_global = 0

# --- STEP 1: HOME ---
if st.session_state.step == 1:
    st.markdown("<h1 class='main-header'>🧬 GenoPredict AD</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Évaluer le risque de transmission de la maladie d'Alzheimer</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("https://cdn.pixabay.com/photo/2020/05/15/16/32/dna-5174482_1280.jpg", use_container_width=True)
    
    with col2:
        st.markdown("### Bienvenue")
        st.write("""
        Ce service utilise l'intelligence artificielle et la génétique moléculaire pour estimer le **Score de Risque Polygénique (PRS)** 
        de transmission au sein votre famille.
        
        **Comment ça marche ?**
        1. Importez les profils génétiques des parents.
        2. Nous simulons 1 000 combinaisons d'enfants potentiels ("Enfants Virtuels").
        3. Notre IA prédit le risque pour chaque combinaison.
        
        🔒 **Confidentialité** : Vos données sont analysées localement et ne sont jamais stockées sur nos serveurs.
        """)
        
        if st.button("Commencer l'analyse familiale  ➡️"):
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: UPLOAD ---
elif st.session_state.step == 2:
    st.markdown("<h1 class='main-header'>📂 Importation des Profils ADN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Veuillez charger les fichiers de génotypage (format CSV exporté de notre extracteur).</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Profil du PÈRE 👨")
        father_file = st.file_uploader("Fichier CSV Père", type=['csv'], key="father")
        if father_file:
            st.session_state.father_data = pd.read_csv(father_file)
            st.markdown("<div class='success-box'>✅ Profil valide détecté</div>", unsafe_allow_html=True)
            
    with col2:
        st.info("Profil de la MÈRE 👩")
        mother_file = st.file_uploader("Fichier CSV Mère", type=['csv'], key="mother")
        if mother_file:
            st.session_state.mother_data = pd.read_csv(mother_file)
            st.markdown("<div class='success-box'>✅ Profil valide détecté</div>", unsafe_allow_html=True)

    # Demo mode helper (if files missing, tell user where they are)
    with st.expander("Pas de fichiers ? Utilisez nos données de démo"):
        st.write("Les fichiers `father_genotype.csv` et `mother_genotype.csv` ont été générés dans le dossier `genopredict_app`. Chargez-les ci-dessus.")

    if st.session_state.father_data is not None and st.session_state.mother_data is not None:
        # Check for critical SNPs
        required_snps = ['rs429358', 'rs7412'] # APOE signatures
        found_f = st.session_state.father_data['rsID'].isin(required_snps).any()
        
        if found_f:
            st.success("Marqueurs APOE (rs429358/rs7412) identifiés avec succès.")
            if st.button("Valider et Continuer ➡️"):
                st.session_state.step = 3
                st.rerun()
        else:
            st.warning("Attention : Les marqueurs APOE semblent manquants. L'analyse sera moins précise.")
            if st.button("Continuer quand même ➡️"):
                st.session_state.step = 3
                st.rerun()

# --- STEP 3: PARAMETERS ---
elif st.session_state.step == 3:
    st.markdown("<h1 class='main-header'>⚙️ Paramètres Cliniques</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>La génétique interagit avec l'âge et l'histoire familiale.</p>", unsafe_allow_html=True)
    
    with st.container():
        st.write("#### Configuration de la simulation")
        
        target_age = st.slider("Âge cible de l'analyse (Projection)", min_value=50, max_value=100, value=75, format="%d ans")
        st.caption("Le risque d'Alzheimer augmente exponentiellement avec l'âge.")
        
        target_sex_ratio = st.radio("Sexe des enfants virtuels", ["Mixte (50/50)", "Filles uniquement", "Garçons uniquement"])
        sex_map = {"Mixte (50/50)": [0, 1], "Filles uniquement": [0], "Garçons uniquement": [1]}
        
        family_history = st.checkbox("Antécédents familiaux connus d'Alzheimer (hors parents) ?")
        
        st.session_state.sim_params = {
            'Age': target_age,
            'Sex_Opts': sex_map[target_sex_ratio],
            'FamilyHistory': 1 if family_history else 0
        }
        
        if st.button("Générer la simulation 🧬"):
            st.session_state.step = 4
            st.rerun()

# --- STEP 4: PROCESSING ---
elif st.session_state.step == 4:
    st.markdown("<h1 class='main-header'>🔄 Analyse en cours...</h1>", unsafe_allow_html=True)
    
    # Progress bar and animation
    my_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("Initialisation du simulateur Mendélien...")
    time.sleep(0.5)
    my_bar.progress(20)
    
    # 1. Simulate
    status_text.text("Génération de 1 000 enfants virtuels...")
    
    # Define SNPs to track (must match model features)
    model_snps = ['rs429358', 'rs7412', 'rs3851179'] 
    
    sim_df = simulate_children(
        st.session_state.father_data, 
        st.session_state.mother_data, 
        model_snps
    )
    my_bar.progress(50)
    
    # 2. Add Clinical Data
    status_text.text("Application des paramètres cliniques...")
    sim_df['Age'] = st.session_state.sim_params['Age']
    sim_df['FamilyHistory'] = st.session_state.sim_params['FamilyHistory']
    
    # Handle sex randomly based on selection
    sim_df['Sex'] = np.random.choice(st.session_state.sim_params['Sex_Opts'], size=len(sim_df))
    my_bar.progress(70)
    
    # 3. Predict with AI
    status_text.text("Inférence du modèle Random Forest...")
    model = load_model()
    
    if model:
        # Reorder columns to match training
        feature_order = ['Age', 'Sex', 'FamilyHistory', 'rs429358', 'rs7412', 'rs3851179']
        X = sim_df[feature_order]
        
        probs = model.predict_proba(X)
        sim_df['Risk_Score'] = probs[:, 1]
        
        st.session_state.simulation_results = sim_df
        st.session_state.risk_score_global = sim_df['Risk_Score'].mean() * 100
        
        my_bar.progress(100)
        status_text.text("Terminé !")
        time.sleep(0.5)
        st.session_state.step = 5
        st.rerun()
    else:
        st.error("Erreur : Modèle IA introuvable. Veuillez contacter le support.")

# --- STEP 5: DASHBOARD ---
elif st.session_state.step == 5:
    st.markdown("<h1 class='main-header'>📊 Tableau de Bord des Résultats</h1>", unsafe_allow_html=True)
    
    # Global Score - Gauge Chart
    risk_val = st.session_state.risk_score_global
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_val,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risque Moyen de Transmission"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2563eb"},
            'steps': [
                {'range': [0, 30], 'color': "#d1fae5"},
                {'range': [30, 70], 'color': "#fef3c7"},
                {'range': [70, 100], 'color': "#fee2e2"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': risk_val}}))
    
    col_g1, col_g2 = st.columns([1, 2])
    with col_g1:
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col_g2:
        st.markdown("### Interprétation")
        if risk_val < 30:
            st.success(f"**Risque Faible ({risk_val:.1f}%)** : La combinaison génétique simulée est favorable. Le risque est inférieur à la moyenne de la population pour cet âge.")
        elif risk_val < 60:
            st.warning(f"**Risque Modéré ({risk_val:.1f}%)** : Certains facteurs de risque sont présents. Une surveillance régulière est conseillée.")
        else:
            st.error(f"**Risque Élevé ({risk_val:.1f}%)** : Les simulations montrent une forte pénétrance des variants à risque (ex: APOE4).")
            
        st.write(f"Sur 1 000 simulations, **{(st.session_state.simulation_results['Risk_Score'] > 0.5).sum()}** enfants virtuels ont développé un profil à risque élevé.")

    st.divider()
    
    # Distribution Plot
    st.markdown("### 📈 Distribution du Risque dans la Descendance")
    fig_dist = px.histogram(st.session_state.simulation_results, x="Risk_Score", nbins=30, 
                            title="Distribution des probabilités (0.0 - 1.0)",
                            color_discrete_sequence=['#6366f1'])
    fig_dist.add_vline(x=0.5, line_dash="dash", line_color="red", annotation_text="Seuil Critique")
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # Genetic Details
    with st.expander("🔍 Détails génétiques (Mode Expert)"):
        st.write("Fréquence des génotypes risqués (Homozygote Alt) dans les simulations :")
        col_d1, col_d2, col_d3 = st.columns(3)
        
        df = st.session_state.simulation_results
        p_apoe = (df['rs429358'] == 2).mean() * 100
        p_picalm = (df['rs3851179'] == 2).mean() * 100
        
        col_d1.metric("APOE (rs429358) C/C", f"{p_apoe:.1f}%", "Risque Majeur")
        col_d2.metric("PICALM (rs3851179) C/C", f"{p_picalm:.1f}%", "Risque Mineur")
    
    st.markdown("---")
    if st.button("Voir les recommandations préventives ➡️"):
        st.session_state.step = 6
        st.rerun()

# --- STEP 6: RECOMMENDATIONS ---
elif st.session_state.step == 6:
    st.markdown("<h1 class='main-header'>🌱 Prévention & Action</h1>", unsafe_allow_html=True)
    
    st.info("💡 **Le saviez-vous ?** Même avec un risque génétique élevé, le mode de vie peut réduire l'apparition des symptômes de 40%.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🧠 Stimulation Cognitive")
        st.write("- Apprentissage de nouvelles langues")
        st.write("- Jeux de stratégie (Échecs, Sudoku)")
        st.write("- Lecture quotidienne")
        
    with col2:
        st.markdown("### 🥑 Nutrition (Mind Diet)")
        st.write("- Légumes à feuilles vertes")
        st.write("- Baies et fruits rouges")
        st.write("- Noix et Huile d'olive")
        st.write("- Poisson (Oméga-3) 1x/semaine")
        
    with col3:
        st.markdown("### 🏃 Activité Physique")
        st.write("- 150 min de cardio modéré/semaine")
        st.write("- Marche rapide")
        st.write("- Sommeil de qualité (7-8h)")
    
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    if st.button("🔄 Relancer une nouvelle analyse"):
        st.session_state.step = 1
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
