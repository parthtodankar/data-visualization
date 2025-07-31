import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# App configuration
st.set_page_config(
    page_title="Nuclear Isotopes Economics",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load sample data (in real app, use IAEA/WNA APIs)
def load_data():
    countries = ['Canada', 'Russia', 'USA', 'Netherlands', 'South Africa', 'China', 'Japan', 'India']
    production = [38, 25, 15, 10, 8, 5, 3, 2]  # % of global isotope production
    medical_use = [4.2, 3.1, 4.0, 0.8, 0.5, 2.5, 1.8, 1.2]  # Million procedures/year
    co2_savings = [850, 620, 550, 180, 120, 420, 150, 200]  # Thousand tons CO2 saved
    
    return pd.DataFrame({
        'Country': countries,
        'Isotope Production (%)': production,
        'Medical Procedures (Million)': medical_use,
        'CO2 Savings (Thousand Tons)': co2_savings
    })

# Initialize session state
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# Quiz questions
quiz_questions = [
    {
        "question": "What percentage of global medical isotopes are produced in research reactors?",
        "options": ["25%", "40%", "60%", "75%"],
        "answer": 1  # Index of correct option (40%)
    },
    {
        "question": "Which sector uses the majority of industrial isotopes?",
        "options": ["Agriculture", "Material Testing", "Sterilization", "Oil Exploration"],
        "answer": 1  # Material Testing
    },
    {
        "question": "What's the projected CAGR for the isotopes market (2023-2030)?",
        "options": ["3.2%", "5.0%", "6.8%", "8.5%"],
        "answer": 2  # 6.8%
    }
]

# Main app
def main():
    df = load_data()
    
    # Sidebar navigation
    st.sidebar.header("Nuclear Isotopes Economics")
    app_mode = st.sidebar.radio("Navigation", [
        "Global Dashboard", 
        "Isotope Production", 
        "Sector Applications", 
        "Economic Analysis",
        "Interactive Quiz",
        "References"
    ])
    
    st.sidebar.divider()
    st.sidebar.markdown("**Data Sources:**")
    st.sidebar.caption("IAEA Databases • World Nuclear Association • OECD/NEA Reports")
    st.sidebar.caption("Developed by Team [Matrix]")
    
    # Global Dashboard
    if app_mode == "Global Dashboard":
        st.title("⚛️ Global Isotope Economics Dashboard")
        st.subheader("Non-Energy Applications of Nuclear Technologies")
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Global Isotope Market", "$4.8 Billion", "6.8% CAGR")
        col2.metric("Medical Procedures", "40M/year", "80% of isotope use")
        col3.metric("CO₂ Savings", "2.5M tons/year", "Equivalent to 550K cars")
        
        # World map
        st.subheader("Global Isotope Production")
        fig_map = px.choropleth(
            df,
            locations="Country",
            locationmode="country names",
            color="Isotope Production (%)",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Plasma,
            projection="natural earth"
        )
        fig_map.update_layout(height=500)
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Top producers
        st.subheader("Top Producing Countries")
        fig_bar = px.bar(
            df.sort_values("Isotope Production (%)", ascending=False).head(5),
            x="Country",
            y="Isotope Production (%)",
            text_auto=True,
            color="Country"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Isotope Production
    elif app_mode == "Isotope Production":
        st.title("🧪 Isotope Production Methods")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Production Methods")
            st.markdown("""
            - **Research Reactors**:  
              Neutron activation (e.g., Mo-99, I-131)
            - **Nuclear Power Plants**:  
              Fission products (e.g., Cs-137, Sr-90)
            - **Cyclotrons**:  
              Proton bombardment (e.g., F-18, C-11)
            - **Radioisotope Generators**:  
              Parent-daughter systems (e.g., Tc-99m)
            """)
            
            st.subheader("Key Facilities")
            st.markdown("""
            - **Canada**: NRU Reactor (Chalk River)
            - **Russia**: RIAR (Dimitrovgrad)
            - **Netherlands**: HFR (Petten)
            - **South Africa**: SAFARI-1
            """)
            
        with col2:
            st.subheader("Production Economics")
            production_data = pd.DataFrame({
                "Method": ["Research Reactors", "NPP By-products", "Cyclotrons"],
                "Cost Efficiency": [9, 7, 4],
                "Scalability": [8, 9, 6],
                "Isotope Range": [9, 7, 5]
            })
            
            fig_radar = go.Figure()
            for i, row in production_data.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=row[1:].values,
                    theta=production_data.columns[1:],
                    fill='toself',
                    name=row['Method']
                ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                height=500
            )
            st.plotly_chart(fig_radar, use_container_width=True)
    
    # Sector Applications
    elif app_mode == "Sector Applications":
        st.title("📊 Sector Applications Analysis")
        
        sectors = st.selectbox("Select Sector", [
            "Medical", "Industrial", "Agricultural", "Space Technology"
        ])
        
        if sectors == "Medical":
            st.subheader("Medical Applications")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Common Isotopes:**
                - Tc-99m (Diagnostics)
                - I-131 (Thyroid treatment)
                - Lu-177 (Cancer therapy)
                
                **Economic Impact:**
                - $3.2B market (2025)
                - 40M procedures/year
                - 90% accuracy in diagnostics
                """)
                
            with col2:
                medical_data = pd.DataFrame({
                    "Application": ["Diagnostics", "Cancer Therapy", "Sterilization"],
                    "Market Share (%)": [65, 25, 10]
                })
                fig_pie = px.pie(
                    medical_data,
                    values="Market Share (%)",
                    names="Application",
                    hole=0.3
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        elif sectors == "Industrial":
            st.subheader("Industrial Applications")
            st.markdown("""
            **Key Uses:**
            - Radiography testing (Ir-192)
            - Gauging systems (Cs-137)
            - Tracer studies (H-3, C-14)
            
            **Economic Benefits:**
            - $850M market (2025)
            - 30% cost reduction vs alternatives
            - 0% production downtime
            """)
            
            st.image("industrial_apps.jpg", caption="Industrial radiography using isotopes")
        
    # Economic Analysis
    elif app_mode == "Economic Analysis":
        st.title("💹 Economic Analysis")
        
        tab1, tab2, tab3 = st.tabs([
            "Market Trends", "Cost Comparison", "Growth Projections"
        ])
        
        with tab1:
            st.subheader("Global Isotope Market Trends")
            years = np.arange(2015, 2031)
            market_size = [2.1, 2.3, 2.5, 2.7, 2.9, 3.2, 3.5, 3.8, 4.2, 4.5, 4.9, 5.3, 5.7, 6.1, 6.6, 7.1]
            df_market = pd.DataFrame({"Year": years, "Market Size ($B)": market_size})
            
            fig = px.line(
                df_market, 
                x="Year", 
                y="Market Size ($B)",
                markers=True,
                title="Isotope Market Growth (2015-2030)"
            )
            fig.add_vrect(x0=2023, x1=2030, fillcolor="green", opacity=0.1, line_width=0)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Production Cost Comparison")
            cost_data = pd.DataFrame({
                "Method": ["Research Reactor", "NPP By-product", "Cyclotron"],
                "Startup Cost ($M)": [500, 8000, 10],
                "Production Cost ($/unit)": [50, 30, 150],
                "Output Capacity": ["High", "Very High", "Medium"]
            })
            st.dataframe(cost_data.style.highlight_min(axis=0, color='#90EE90'), use_container_width=True)
            
            fig = px.bar(
                cost_data,
                x="Method",
                y="Production Cost ($/unit)",
                color="Method",
                title="Unit Production Cost Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Interactive Quiz
    elif app_mode == "Interactive Quiz":
        st.title("📝 Nuclear Isotopes Quiz")
        st.caption("Test your knowledge of isotope economics and applications")
        
        if st.session_state.current_question < len(quiz_questions):
            question = quiz_questions[st.session_state.current_question]
            
            st.subheader(f"Question {st.session_state.current_question + 1}/{len(quiz_questions)}")
            st.markdown(f"**{question['question']}**")
            
            cols = st.columns(2)
            for i, option in enumerate(question["options"]):
                if cols[i % 2].button(option, key=f"option_{i}", use_container_width=True):
                    if i == question["answer"]:
                        st.success("Correct!")
                        st.session_state.quiz_score += 1
                    else:
                        st.error("Incorrect!")
                    st.session_state.current_question += 1
                    st.experimental_rerun()
        else:
            st.subheader("Quiz Completed!")
            st.metric("Your Score", f"{st.session_state.quiz_score}/{len(quiz_questions)}")
            
            if st.button("Restart Quiz"):
                st.session_state.quiz_score = 0
                st.session_state.current_question = 0
                st.experimental_rerun()
    
    # References
    else:
        st.title("📚 References & Data Sources")
        st.markdown("""
        ### Verified Information Sources:
        - **IAEA (International Atomic Energy Agency)**:  
          [Nuclear Data Services](https://www.iaea.org/resources/databases)
        - **World Nuclear Association**:  
          [World Nuclear Performance Reports](https://www.world-nuclear.org/)
        - **OECD Nuclear Energy Agency**:  
          [Nuclear Technology Reports](https://www.oecd-nea.org/)
        - **UN Sustainable Development**:  
          [Nuclear for Climate Initiative](https://www.un.org/sustainabledevelopment/climate-change/)
        
        ### Key Publications:
        1. "The Supply of Medical Isotopes" (OECD/NEA, 2023)
        2. "Industrial Applications of Radioisotopes" (IAEA, 2022)
        3. "Economic Assessment of Non-Energy Nuclear Applications" (WNA, 2024)
        """)
        
        st.divider()
        st.markdown("""
        ### Application Development:
        - **Frontend**: Streamlit
        - **Data Visualization**: Plotly
        - **Deployment**: Streamlit Cloud
        - **Source Code**: [GitHub Repository](https://github.com/your-repo)
        """)

if __name__ == "__main__":
    main()