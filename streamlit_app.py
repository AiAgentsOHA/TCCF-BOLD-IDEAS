import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="TCCF Bold Ideas Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0f2847 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #0a1628, #0f2847);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #ff6b4a, #00d4aa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4aa;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #8ba3c7;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .applicant-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .applicant-card:hover {
        background: rgba(255,255,255,0.08);
        border-color: #00d4aa;
    }
    
    .venture-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .yc-oneliner {
        color: #ff8a6e;
        font-style: italic;
        margin-bottom: 0.5rem;
    }
    
    .science-stars {
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    
    .science-stars.strong { color: #00d4aa; }
    .science-stars.good { color: #4fffdb; }
    .science-stars.some { color: #fbbf24; }
    
    .rec-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .rec-strongly { background: #00d4aa; color: #0a1628; }
    .rec-recommend { background: #4fffdb; color: #0a1628; }
    .rec-shortlist { background: #7dd3fc; color: #0a1628; }
    .rec-consider { background: #fbbf24; color: #0a1628; }
    .rec-maybe { background: #fb923c; color: #0a1628; }
    .rec-low { background: #f87171; color: white; }
    
    .country-chip {
        display: inline-block;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 100px;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        font-size: 0.8rem;
        cursor: pointer;
    }
    
    .score-bar {
        height: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 4px;
        overflow: hidden;
        margin-top: 0.25rem;
    }
    
    .score-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #00d4aa, #4fffdb);
        border-radius: 4px;
    }
    
    div[data-testid="stSidebar"] {
        background: rgba(10, 22, 40, 0.95);
    }
    
    .stSelectbox label, .stMultiSelect label {
        color: #8ba3c7 !important;
    }
</style>
""", unsafe_allow_html=True)

# Country flags
FLAGS = {
    'Nigeria': '🇳🇬', 'Kenya': '🇰🇪', 'Tanzania': '🇹🇿', 'Uganda': '🇺🇬',
    'Ghana': '🇬🇭', 'South Africa': '🇿🇦', 'Rwanda': '🇷🇼', 'Ethiopia': '🇪🇹',
    'Egypt': '🇪🇬', 'DRC': '🇨🇩', 'Congo': '🇨🇬', 'Cameroon': '🇨🇲', 'Senegal': '🇸🇳',
    'Zambia': '🇿🇲', 'Zimbabwe': '🇿🇼', 'Malawi': '🇲🇼', 'Mozambique': '🇲🇿',
    'Botswana': '🇧🇼', 'Namibia': '🇳🇦', 'Angola': '🇦🇴', 'Mali': '🇲🇱',
    'Burkina Faso': '🇧🇫', "Cote d'Ivoire": '🇨🇮', 'Guinea': '🇬🇳',
    'Burundi': '🇧🇮', 'Madagascar': '🇲🇬', 'Tunisia': '🇹🇳', 'Morocco': '🇲🇦',
    'Benin': '🇧🇯', 'Togo': '🇹🇬', 'South Sudan': '🇸🇸', 'Niger': '🇳🇪',
    'Sierra Leone': '🇸🇱', 'Liberia': '🇱🇷', 'Djibouti': '🇩🇯', 'Chad': '🇹🇩',
    'Eswatini': '🇸🇿', 'Algeria': '🇩🇿'
}

def get_flag(country):
    return FLAGS.get(country, '🌍')

def get_stars(level):
    if '★★★' in str(level): return '★★★'
    if '★★☆' in str(level): return '★★☆'
    if '★☆☆' in str(level): return '★☆☆'
    return '☆☆☆'

def get_star_class(level):
    if '★★★' in str(level): return 'strong'
    if '★★☆' in str(level): return 'good'
    if '★☆☆' in str(level): return 'some'
    return 'conventional'

def get_rec_class(rec):
    rec = str(rec)
    if 'STRONGLY' in rec: return 'strongly'
    if rec == '★ RECOMMEND': return 'recommend'
    if rec == 'SHORTLIST': return 'shortlist'
    if rec == 'CONSIDER': return 'consider'
    if 'MAYBE' in rec: return 'maybe'
    return 'low'

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('TCCF_Bold_Ideas_FINAL_v3.csv')
    return df

df = load_data()

# Sidebar filters
st.sidebar.image("https://i.imgur.com/placeholder.png", width=200)  # Replace with actual logo
st.sidebar.markdown("## 🔬 Filters")

# Recommendation filter
rec_options = ['All', '★ STRONGLY RECOMMEND', '★ RECOMMEND', 'SHORTLIST', 'CONSIDER', 'MAYBE', 'LOW PRIORITY']
selected_rec = st.sidebar.selectbox("Recommendation", rec_options)

# Country filter
countries = ['All'] + sorted(df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox("Country", countries)

# Science filter
science_only = st.sidebar.checkbox("🔬 Science-focused only (★★★ or ★★☆)")

# Search
search_term = st.sidebar.text_input("🔍 Search ventures")

# Apply filters
filtered_df = df.copy()

if selected_rec != 'All':
    if 'STRONGLY' in selected_rec:
        filtered_df = filtered_df[filtered_df['Recommendation'].str.contains('STRONGLY', na=False)]
    elif 'MAYBE' in selected_rec:
        filtered_df = filtered_df[filtered_df['Recommendation'].str.contains('MAYBE', na=False)]
    else:
        filtered_df = filtered_df[filtered_df['Recommendation'] == selected_rec]

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

if science_only:
    filtered_df = filtered_df[
        filtered_df['Science_Level'].str.contains('★★★', na=False) | 
        filtered_df['Science_Level'].str.contains('★★☆', na=False)
    ]

if search_term:
    search_lower = search_term.lower()
    filtered_df = filtered_df[
        filtered_df['Venture_Name'].str.lower().str.contains(search_lower, na=False) |
        filtered_df['YC_OneLiner'].str.lower().str.contains(search_lower, na=False) |
        filtered_df['Country'].str.lower().str.contains(search_lower, na=False) |
        filtered_df['Technologies'].str.lower().str.contains(search_lower, na=False)
    ]

# Sort by weighted score
filtered_df = filtered_df.sort_values('Weighted_Score', ascending=False)

# Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
        <span style="font-size: 0.9rem; color: #00d4aa; text-transform: uppercase; letter-spacing: 0.1em;">🔬 Science-Based Innovation Evaluation</span>
    </div>
    <h1>Africa's Boldest Plastic Solutions</h1>
    <p style="color: #8ba3c7; font-size: 1.1rem;">TCCF Bold Ideas Project | The Coca-Cola Foundation × OceanHub Africa</p>
</div>
""", unsafe_allow_html=True)

# Stats row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">$120K</div>
        <div class="stat-label">Available Funding</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{len(filtered_df)}</div>
        <div class="stat-label">Applications Shown</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{filtered_df['Country'].nunique()}</div>
        <div class="stat-label">Countries</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    strongly_rec = len(filtered_df[filtered_df['Recommendation'].str.contains('STRONGLY', na=False)])
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{strongly_rec}</div>
        <div class="stat-label">Strongly Recommended</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Summary cards
st.markdown("### 📊 Recommendation Summary")
rec_counts = {
    '★ STRONGLY RECOMMEND': len(df[df['Recommendation'].str.contains('STRONGLY', na=False)]),
    '★ RECOMMEND': len(df[df['Recommendation'] == '★ RECOMMEND']),
    'SHORTLIST': len(df[df['Recommendation'] == 'SHORTLIST']),
    'CONSIDER': len(df[df['Recommendation'] == 'CONSIDER']),
    'MAYBE': len(df[df['Recommendation'].str.contains('MAYBE', na=False)]),
    'LOW PRIORITY': len(df[df['Recommendation'] == 'LOW PRIORITY'])
}

cols = st.columns(6)
colors = ['#00d4aa', '#4fffdb', '#7dd3fc', '#fbbf24', '#fb923c', '#f87171']
for i, (rec, count) in enumerate(rec_counts.items()):
    with cols[i]:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); 
                    border-radius: 12px; padding: 1rem; text-align: center; border-top: 3px solid {colors[i]};">
            <div style="font-size: 1.8rem; font-weight: 700; color: {colors[i]};">{count}</div>
            <div style="font-size: 0.65rem; color: #8ba3c7; text-transform: uppercase;">{rec.replace('★ ', '')}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### 🌍 Applications by Country")
    country_counts = filtered_df['Country'].value_counts().head(15)
    fig_country = px.bar(
        x=country_counts.values,
        y=[f"{get_flag(c)} {c}" for c in country_counts.index],
        orientation='h',
        color=country_counts.values,
        color_continuous_scale=['#0f2847', '#00d4aa']
    )
    fig_country.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#8ba3c7',
        showlegend=False,
        coloraxis_showscale=False,
        yaxis_title='',
        xaxis_title='Applications',
        height=400,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    fig_country.update_yaxes(tickfont=dict(size=11))
    st.plotly_chart(fig_country, use_container_width=True)

with col_chart2:
    st.markdown("### 📈 Score Distribution")
    fig_scores = px.histogram(
        filtered_df, 
        x='Weighted_Score',
        nbins=20,
        color_discrete_sequence=['#00d4aa']
    )
    fig_scores.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#8ba3c7',
        xaxis_title='Weighted Score',
        yaxis_title='Count',
        height=400,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_scores, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Applicant cards
st.markdown(f"### 🚀 Applications ({len(filtered_df)} shown)")

for idx, row in filtered_df.iterrows():
    stars = get_stars(row['Science_Level'])
    star_class = get_star_class(row['Science_Level'])
    rec_class = get_rec_class(row['Recommendation'])
    flag = get_flag(row['Country'])
    
    with st.expander(f"{stars} **{row['Venture_Name']}** — {flag} {row['Country']} — Score: {row['Weighted_Score']:.2f}"):
        # Header info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <span class="rec-tag rec-{rec_class}">{row['Recommendation']}</span>
            <p class="yc-oneliner">"{row['YC_OneLiner']}"</p>
            <p style="color: #8ba3c7; font-size: 0.85rem;">{row['Science_Level']}</p>
            """, unsafe_allow_html=True)
        with col2:
            st.metric("Weighted Score", f"{row['Weighted_Score']:.2f}")
        
        st.markdown("---")
        
        # Score breakdown
        st.markdown("**📊 Score Breakdown**")
        score_cols = st.columns(5)
        scores = [
            ('Innovation', row['Score_Innovation'], '30%'),
            ('Impact', row['Score_Impact'], '25%'),
            ('Social', row['Score_Social'], '20%'),
            ('Commercial', row['Score_Commercial'], '15%'),
            ('Team', row['Score_Team'], '10%')
        ]
        for i, (name, score, weight) in enumerate(scores):
            with score_cols[i]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 1.5rem; font-weight: 700; color: #00d4aa;">{score}</div>
                    <div style="font-size: 0.7rem; color: #8ba3c7;">{name} ({weight})</div>
                    <div class="score-bar"><div class="score-bar-fill" style="width: {score*20}%;"></div></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Contact info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📧 Contact Information**")
            st.write(f"**Contact:** {row['Contact']}")
            st.write(f"**Email:** {row['Email']}")
            st.write(f"**Location:** {row['Location']}")
            st.write(f"**Stage:** {row['Stage']}")
            st.write(f"**Legal Status:** {row['Legal_Status']}")
        
        with col2:
            st.markdown("**📈 Impact Metrics**")
            st.write(f"**Plastic Impact:** {row['Plastic_Tonnes']} tonnes")
            st.write(f"**Livelihoods:** {row['Livelihoods']} people")
            if pd.notna(row.get('LinkedIn')) and row.get('LinkedIn'):
                st.write(f"**LinkedIn:** [{row['LinkedIn'][:50]}...]({row['LinkedIn']})")
        
        # Technologies
        if pd.notna(row['Technologies']) and row['Technologies']:
            st.markdown("**🔬 Technologies**")
            techs = [t.strip() for t in str(row['Technologies']).split('|') if t.strip() and t.strip() != 'Standard approach']
            if techs:
                st.write(" • ".join(techs[:5]))
        
        # Application content
        if pd.notna(row.get('Science_Inputs')) and row.get('Science_Inputs'):
            with st.expander("🔬 Science & Technical Inputs"):
                st.write(row['Science_Inputs'][:1000])
        
        if pd.notna(row.get('Bold_Characteristics')) and row.get('Bold_Characteristics'):
            with st.expander("💡 Bold Characteristics"):
                st.write(row['Bold_Characteristics'][:800])
        
        # Notion link
        notion_url = f"https://www.notion.so/search?q={row['Email']}"
        st.markdown(f"[📄 View in Notion]({notion_url})")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8ba3c7; padding: 2rem;">
    <p><strong>TCCF Bold Ideas Project</strong></p>
    <p>The Coca-Cola Foundation × OceanHub Africa</p>
</div>
""", unsafe_allow_html=True)
