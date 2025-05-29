import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np
from datetime import datetime, timedelta

# --- Configuration & Initial Data (Simulated) ---
st.set_page_config(
    layout="wide",
    page_title="AI Opportunity Map Dashboard",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }

    .metric-card h3 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    .metric-card p {
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }

    .trend-card {
        background: rgba(255, 255, 255, 0.95);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }

    .trend-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border-left-color: #764ba2;
    }

    .opportunity-highlight {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(17, 153, 142, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }

    .opportunity-highlight:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(17, 153, 142, 0.4);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 0 24px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        font-weight: 500;
        transition: all 0.3s ease;
        color: #333;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }

    .sidebar-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .feature-highlight {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 1rem 0;
    }

    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }

    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to load initial trend data
# In a real application, this data would come from a database, API, or external file.
def load_trend_data():
    """Loads simulated AI trend data."""
    data = {
        'Trend': [
            "Evolution to Agentic AI", "Democratization of B2B AI", "Redundancy of 'First-Wave' AI",
            "AI IPOs Explosion", "Increasing Demand for AI", "AI Augmentation Focus",
            "AI in Software Development", "AI in Finance", "AI in Healthcare",
            "Privacy Concerns", "AI Regulation Efforts", "Workplace Changes",
            "Environmental & Energy Concerns of AI", "Talent Stack Collapsing", "Continuous Learning Imperative"
        ],
        'Impact_Score': [9, 8, 6, 7, 9, 8, 7, 8, 9, 7, 6, 8, 7, 8, 9], # Subjective score 1-10
        'Time_Horizon': [
            "Emerging & Growing (1-3 Years)", "Currently Dominant (Now - 1-2 Years)", "Currently Dominant (Now - 1-2 Years)",
            "Future Outlook (3-5+ Years)", "Currently Dominant (Now - 1-2 Years)", "Emerging & Growing (1-3 Years)",
            "Currently Dominant (Now - 1-2 Years)", "Currently Dominant (Now - 1-2 Years)", "Emerging & Growing (1-3 Years)",
            "Emerging & Growing (1-3 Years)", "Emerging & Growing (1-3 Years)", "Currently Dominant (Now - 1-2 Years)",
            "Future Outlook (3-5+ Years)", "Emerging & Growing (1-3 Years)", "Currently Dominant (Now - 1-2 Years)"
        ],
        'Description': [
            "AI evolving beyond simple chatbots into sophisticated, embedded strategic partners for real-time insights and complex process automation.",
            "LLMs, AI-as-a-service, and user-friendly software making advanced AI accessible to companies of all sizes, not just large enterprises.",
            "Organizations consolidating AI tech stacks, moving away from unreliable or single-purpose tools towards solutions with deep expertise.",
            "Mature AI companies demonstrating ROI and monetization potential, leading to an expected increase in IPOs and M&A activity.",
            "Broad business recognition of AI's value in enhancing productivity, solving complex problems, and improving customer experiences.",
            "A shift towards using AI to enhance human capabilities and processes, with humans remaining key in decision-making and oversight.",
            "AI becoming a powerful tool in software development for code generation, environment setup, and developer assistance.",
            "Transformation of the finance sector through autonomous applications like chatbots, automated forecasting, fraud detection, and risk management.",
            "Increased adoption of AI in healthcare for diagnostics, treatment planning, pharmaceutical development, and data analysis.",
            "Growing concerns as AI systems become capable of analyzing vast amounts of personal data, potentially compromising individual privacy.",
            "Governments and regulatory bodies actively discussing and developing frameworks to govern AI development and deployment.",
            "Fundamental changes in the workplace as AI automates traditional tasks, highlighting the need for new skills and human-AI collaboration.",
            "Increasing computational demands of AI driving concerns about energy consumption and the need for sustainable data centers.",
            "The value of skills shifting, rewarding fast learners, strong pattern finders, and those with good judgment over traditional credentials.",
            "The rapid evolution of AI necessitates ongoing education and skill development through online resources, communities, and projects."
        ]
    }
    return pd.DataFrame(data)

# Function to load initial opportunity data
def load_opportunity_data():
    """Loads simulated AI opportunity data."""
    data = {
        'Opportunity_Area': [
            "Agentic AI Solutions Platforms", "AI-as-a-Service for SMEs", "Specialized Vertical AI Solutions",
            "AI Augmentation & Human-AI Teaming Tools", "AI Ethics, Governance & Compliance Services",
            "Sustainable AI Infrastructure & Green Computing", "AI Skilling & Reskilling Platforms",
            "AI-Powered Software Development Tools"
        ],
        'Qualitative_Size': [
            "Large & Growing", "Large & Rapidly Growing", "Medium & Consolidating",
            "Large & Foundational", "Medium & Critical Growth", "Medium & Emerging Urgently",
            "Large & Continuous", "Large & Embedded"
        ],
        'Related_Trends': [
            "Evolution to Agentic AI, Increasing Demand for AI",
            "Democratization of B2B AI, Increasing Demand for AI",
            "Redundancy of 'First-Wave' AI, AI in Finance, AI in Healthcare",
            "AI Augmentation Focus, Workplace Changes, Fear of AI",
            "Privacy Concerns, AI Regulation Efforts, Trust in AI",
            "Environmental & Energy Concerns of AI",
            "Talent Stack Collapsing, Continuous Learning Imperative, Workplace Changes",
            "AI in Software Development, Increasing Demand for AI"
        ],
        'Investment_Focus_Score': [8, 9, 7, 8, 6, 7, 9, 8] # Simulated focus score 1-10
    }
    return pd.DataFrame(data)

# --- Dashboard Layout ---
st.markdown('<h1 class="main-header">🤖 AI Opportunity Map 2025</h1>', unsafe_allow_html=True)

# Hero section with enhanced metrics
st.markdown("""
<div class="feature-highlight">
    <h2 style="text-align: center; margin-bottom: 1rem; color: #333;">🎯 Strategic AI Intelligence Dashboard</h2>
    <p style="text-align: center; font-size: 1.1rem; color: #666; margin-bottom: 0;">
        Navigate the AI revolution with data-driven insights, trend analysis, and strategic decision-making tools
    </p>
</div>
""", unsafe_allow_html=True)

# Enhanced metrics with better readability
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>15+</h3>
        <p>AI Trends Tracked</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>8</h3>
        <p>Investment Areas</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>$2.6T</h3>
        <p>Market Size 2030</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>Real-time</h3>
        <p>Data Insights</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
### 🎯 **Strategic AI Intelligence Dashboard**

Explore the dynamic landscape of artificial intelligence opportunities, trends, and strategic pathways.
This interactive dashboard provides data-driven insights for businesses and individuals navigating the AI revolution.

**🔥 Key Features:**
- **Real-time Trend Analysis** - Track emerging AI patterns and their market impact
- **Opportunity Mapping** - Identify high-potential investment and business areas
- **Strategic Decision Trees** - Navigate complex AI adoption and career decisions
- **Interactive Visualizations** - Explore data through modern, responsive charts

*Data updates dynamically - use the sidebar controls to refresh insights.*
""")

# --- Sidebar for Controls ---
st.sidebar.markdown("## ⚙️ Dashboard Controls")

# Data refresh section
st.sidebar.markdown("### 🔄 Data Management")
update_button = st.sidebar.button(
    "🔄 Refresh Data",
    help="Simulate fetching new data and updating the dashboard",
    type="primary"
)

# Filters section
st.sidebar.markdown("### 🎛️ Filters & Views")

# Time horizon filter
time_horizons = ["All", "Currently Dominant (Now - 1-2 Years)",
                "Emerging & Growing (1-3 Years)", "Future Outlook (3-5+ Years)"]
selected_horizon = st.sidebar.selectbox(
    "Time Horizon Filter:",
    time_horizons,
    help="Filter trends by their time horizon"
)

# Impact score filter
min_impact = st.sidebar.slider(
    "Minimum Impact Score:",
    min_value=1,
    max_value=10,
    value=1,
    help="Show only trends with impact score above this threshold"
)

# Investment focus filter
min_investment = st.sidebar.slider(
    "Minimum Investment Focus:",
    min_value=1,
    max_value=10,
    value=1,
    help="Show only opportunities with investment focus above this threshold"
)

# Display options
st.sidebar.markdown("### 📊 Display Options")
show_descriptions = st.sidebar.checkbox("Show detailed descriptions", value=True)
chart_theme = st.sidebar.selectbox(
    "Chart Theme:",
    ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn"],
    index=1
)

# Initialize or load data into session state to persist across interactions
if 'trends_df' not in st.session_state or 'opportunities_df' not in st.session_state:
    st.session_state.trends_df = load_trend_data()
    st.session_state.opportunities_df = load_opportunity_data()
    st.session_state.last_update_time = "Initial Load"

# Simulate update if button is pressed
if update_button:
    with st.spinner("⏳ Simulating new data fetch..."):
        time.sleep(1.5) # Simulate network delay
        # In a real application, you would re-fetch from APIs or databases here.
        # For this simulation, we'll slightly modify existing data to show changes.
        trends_df_updated = st.session_state.trends_df.copy()
        opportunities_df_updated = st.session_state.opportunities_df.copy()

        # Simulate minor random changes in scores
        # Corrected: Use np.random.randn instead of pd.np.random.randn
        trends_df_updated['Impact_Score'] = (trends_df_updated['Impact_Score'] * (1 + (np.random.randn(len(trends_df_updated)) * 0.02))).clip(1, 10) # Small random fluctuation
        opportunities_df_updated['Investment_Focus_Score'] = (opportunities_df_updated['Investment_Focus_Score'] * (1 + (np.random.randn(len(opportunities_df_updated)) * 0.03))).clip(1, 10)

        st.session_state.trends_df = trends_df_updated
        st.session_state.opportunities_df = opportunities_df_updated
        st.session_state.last_update_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        st.success("✅ Data updated successfully!")
        # No explicit rerun needed if widgets are directly tied to session state values that are updated.
        # Streamlit automatically reruns if a widget's key changes or if input changes.
        # However, if complex logic doesn't trigger a rerun, st.experimental_rerun() can be used.

# --- Main Content Area with Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trend Analysis", "💡 Opportunity Map", "🌳 Strategy Trees", "📊 Analytics"])

with tab1:
    st.header("🚀 AI Industry Trend Analysis")

    # Apply filters to trends data
    filtered_trends = st.session_state.trends_df.copy()

    # Apply time horizon filter
    if selected_horizon != "All":
        filtered_trends = filtered_trends[filtered_trends['Time_Horizon'] == selected_horizon]

    # Apply impact score filter
    filtered_trends = filtered_trends[filtered_trends['Impact_Score'] >= min_impact]

    if len(filtered_trends) == 0:
        st.warning("No trends match the current filters. Please adjust your filter settings.")
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            **📊 Showing {len(filtered_trends)} of {len(st.session_state.trends_df)} trends**

            Explore AI industry trends by their impact potential and timeline. Use the sidebar filters to focus on specific areas of interest.
            """)

        with col2:
            avg_impact = filtered_trends['Impact_Score'].mean()
            st.metric("Average Impact Score", f"{avg_impact:.1f}", f"{avg_impact - st.session_state.trends_df['Impact_Score'].mean():.1f}")

        # Enhanced visualization with modern styling
        fig_trends = px.bar(
            filtered_trends,
            x='Trend',
            y='Impact_Score',
            color='Time_Horizon',
            title="AI Industry Trends by Impact and Time Horizon",
            labels={'Impact_Score': 'Impact Score (1-10)', 'Trend': 'AI Trend'},
            category_orders={"Time_Horizon": ["Currently Dominant (Now - 1-2 Years)", "Emerging & Growing (1-3 Years)", "Future Outlook (3-5+ Years)"]},
            template=chart_theme,
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
        )

        fig_trends.update_layout(
            xaxis_tickangle=-45,
            height=650,
            legend_title_text='Time Horizon',
            font=dict(size=12),
            title_font_size=16,
            showlegend=True
        )

        st.plotly_chart(fig_trends, use_container_width=True)

    st.subheader("🔍 Explore Trend Details")
    # Allow user to select a trend to see more details
    selected_trend = st.selectbox(
        "Select a Trend to view its description:",
        st.session_state.trends_df['Trend'],
        key='trend_selectbox' # Unique key for the widget
    )
    if selected_trend:
        trend_info = st.session_state.trends_df[st.session_state.trends_df['Trend'] == selected_trend].iloc[0]
        st.markdown(f"**Description:** {trend_info['Description']}")
        st.markdown(f"**Time Horizon:** {trend_info['Time_Horizon']}")
        st.markdown(f"**Perceived Impact Score:** {trend_info['Impact_Score']:.2f}")

with tab2:
    st.header("💰 AI Opportunity Landscape")

    # Apply filters to opportunities data
    filtered_opportunities = st.session_state.opportunities_df.copy()
    filtered_opportunities = filtered_opportunities[filtered_opportunities['Investment_Focus_Score'] >= min_investment]

    if len(filtered_opportunities) == 0:
        st.warning("No opportunities match the current filters. Please adjust your filter settings.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            total_opportunities = len(filtered_opportunities)
            st.metric("Opportunities", total_opportunities, f"{total_opportunities - len(st.session_state.opportunities_df)}")

        with col2:
            avg_focus = filtered_opportunities['Investment_Focus_Score'].mean()
            st.metric("Avg Investment Focus", f"{avg_focus:.1f}", f"{avg_focus - st.session_state.opportunities_df['Investment_Focus_Score'].mean():.1f}")

        with col3:
            high_focus_count = len(filtered_opportunities[filtered_opportunities['Investment_Focus_Score'] >= 8])
            st.metric("High-Focus Areas", high_focus_count, f"{high_focus_count}/{total_opportunities}")

        st.markdown("""
        **🎯 Strategic Opportunity Analysis**

        Explore high-potential AI business areas based on market trends, investment focus, and growth potential.
        The treemap visualization shows relative opportunity sizes and investment attractiveness.
        """)

        # Enhanced treemap visualization
        fig_ops = px.treemap(
            filtered_opportunities,
            path=[px.Constant("AI Opportunities"), 'Qualitative_Size', 'Opportunity_Area'],
            values='Investment_Focus_Score',
            color='Investment_Focus_Score',
            color_continuous_scale='RdYlBu_r',
            title="AI Opportunity Areas by Size and Investment Focus",
            hover_data={'Related_Trends': True},
            template=chart_theme
        )

        fig_ops.update_layout(
            height=700,
            margin=dict(t=50, l=25, r=25, b=25),
            font=dict(size=12),
            title_font_size=16
        )

        st.plotly_chart(fig_ops, use_container_width=True)

    st.subheader("🔍 Explore Opportunity Details")
    selected_opportunity = st.selectbox(
        "Select an Opportunity Area to view details:",
        st.session_state.opportunities_df['Opportunity_Area'],
        key='opportunity_selectbox' # Unique key
    )
    if selected_opportunity:
        opp_info = st.session_state.opportunities_df[st.session_state.opportunities_df['Opportunity_Area'] == selected_opportunity].iloc[0]
        st.markdown(f"**Qualitative Size:** {opp_info['Qualitative_Size']}")
        st.markdown(f"**Related Trends:** {opp_info['Related_Trends']}")
        st.markdown(f"**Simulated Investment Focus Score:** {opp_info['Investment_Focus_Score']:.2f}")

with tab3:
    st.header("Conceptual Strategy Decision Trees")
    st.markdown("""
    The decision trees below are conceptual representations using Graphviz. In a fully interactive application,
    clicking through these options would dynamically filter and display relevant information, data, and specific opportunities
    from the other sections of the dashboard.
    """)

    st.subheader("For Businesses: Navigating AI Adoption")
    # Using Graphviz for the decision tree visualization
    # Ensure Graphviz is installed on your system if running locally and it's not rendering: `conda install python-graphviz` or `pip install graphviz`
    # And the Graphviz binaries: https://graphviz.org/download/
    business_strategy_dot = """
    digraph BusinessStrategy {
        rankdir=LR; // Left to Right layout
        node [shape=box, style="rounded,filled", fillcolor="#E6F7FF", fontname="Arial", fontsize=10]; // Node styling
        edge [fontname="Arial", fontsize=9]; // Edge styling

        A [label="Start: How to strategically leverage AI?"];
        B [label="What is our primary business goal with AI?"];
        C [label="Enhance Operational Efficiency & Reduce Costs"];
        D [label="Drive Innovation & Develop New Revenue Streams"];
        E [label="Improve Customer Experience & Engagement"];

        F [label="Preferred AI Sourcing Model?"];
        G [label="Buy/Subscribe (AI-as-a-Service, Off-the-shelf tools)"];
        H [label="Build (Custom AI solutions, Invest in AI talent & MLOps)"];

        I [label="Key Focus Area for Innovation?"];
        J [label="Develop Novel AI-Powered Products/Services"];
        K [label="Enter or Disrupt New Markets using AI Capabilities"];

        L [label="Primary Approach for CX Enhancement?"];
        M [label="Hyper-Personalization at Scale"];
        N [label="Proactive & Predictive Customer Support"];

        // Connections
        A -> B;
        B -> C [label=" Efficiency"];
        B -> D [label=" Innovation"];
        B -> E [label=" CX"];

        C -> F;
        F -> G [label=" Buy/Subscribe"];
        F -> H [label=" Build Custom"];
        G -> "Opportunity: Agentic AI for Automation, AI Augmentation";
        H -> "Opportunity: Specialized Vertical AI, Proprietary Models";


        D -> I;
        I -> J [label=" New Products"];
        I -> K [label=" New Markets"];
        J -> "Opportunity: Agentic AI Platforms, Niche AI Solutions";
        K -> "Opportunity: AI for Underserved Segments (Democratization)";


        E -> L;
        L -> M [label=" Personalization"];
        L -> N [label=" Proactive Support"];
        M -> "Consider: Agentic AI for CX, Data Privacy Implications";
        N -> "Tools: Advanced Chatbots, Predictive Analytics for Churn/Needs";
    }
    """
    st.graphviz_chart(business_strategy_dot)
    st.info("ℹ️ In an interactive version, clicking nodes (e.g., 'Buy/Subscribe') would filter opportunities in Tab 2 or highlight relevant trends in Tab 1.")

    st.subheader("For Individuals: Adapting to the AI Era")
    individual_strategy_dot = """
    digraph IndividualStrategy {
        rankdir=LR;
        node [shape=box, style="rounded,filled", fillcolor="#E8F5E9", fontname="Arial", fontsize=10];
        edge [fontname="Arial", fontsize=9];

        A [label="Start: How do I navigate my career in the AI era?"];
        B [label="What is my primary interest or desired role regarding AI?"];
        C [label="Technical Development & Building AI Systems (AI Builder)"];
        D [label="Using & Applying AI Tools in a Domain (AI Operator/User)"];
        E [label="Focus on Strategy, Ethics, Governance & Impact of AI"];

        F [label="Preferred Technical Specialization?"];
        G [label="AI Model Development (ML, Deep Learning)"];
        H [label="AI Infrastructure & MLOps (Deployment, Scaling)"];
        I [label="Applied AI (NLP, Computer Vision, Robotics)"];

        J [label="Level of Technical Engagement as User?"];
        K [label="Non-technical User (Focus on Prompting, Domain Expertise)"];
        L [label="Semi-technical Power User (Customization, Basic Scripting, Data Analysis)"];

        M [label="Area of Strategic Impact?"];
        N [label="AI Ethics & Responsible AI Development"];
        O [label="AI Policy, Regulation & Public Governance"];
        P [label="AI Product Management & Business Strategy"];

        // Connections
        A -> B;
        B -> C [label=" Builder Path"];
        B -> D [label=" Operator Path"];
        B -> E [label=" Strategist Path"];

        C -> F;
        F -> G [label=" Model Dev."];
        F -> H [label=" Infra/MLOps"];
        F -> I [label=" Applied AI"];
        G -> "Skills: Advanced Math, Python, PyTorch/TensorFlow, Research";
        H -> "Skills: Cloud Platforms (AWS,GCP,Azure), Kubernetes, CI/CD";
        I -> "Skills: Domain-specific Libraries, Data Handling, System Integration";


        D -> J;
        J -> K [label=" Non-Technical"];
        J -> L [label=" Power User"];
        K -> "Skills: Prompt Engineering, Critical Thinking, Domain Knowledge, Adaptability";
        L -> "Skills: Data Literacy, API Usage, Workflow Automation, Low-code/No-code tools";

        E -> M;
        M -> N [label=" Ethics Focus"];
        M -> O [label=" Policy Focus"];
        M -> P [label=" Product/Biz Focus"];
        N -> "Study: Philosophy, Law, Social Sciences, Bias Detection";
        O -> "Study: Legal Frameworks, Public Policy Analysis, International Relations";
        P -> "Study: Business Acumen, Market Analysis, AI Capabilities, User Research";
    }
    """
    st.graphviz_chart(individual_strategy_dot)
    st.info("ℹ️ Clicking paths like 'AI Builder' could link to relevant skilling platforms (from Opportunities) or highlight 'Continuous Learning' (from Trends).")

with tab4:
    st.header("📊 Advanced Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Trend Impact Distribution")

        # Create impact distribution chart
        impact_counts = st.session_state.trends_df['Impact_Score'].value_counts().sort_index()
        fig_impact = px.bar(
            x=impact_counts.index,
            y=impact_counts.values,
            title="Distribution of Impact Scores",
            labels={'x': 'Impact Score', 'y': 'Number of Trends'},
            template=chart_theme,
            color=impact_counts.values,
            color_continuous_scale='Blues'
        )
        fig_impact.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_impact, use_container_width=True)

        # Time horizon breakdown
        st.subheader("⏰ Time Horizon Analysis")
        horizon_counts = st.session_state.trends_df['Time_Horizon'].value_counts()
        fig_horizon = px.pie(
            values=horizon_counts.values,
            names=horizon_counts.index,
            title="Trends by Time Horizon",
            template=chart_theme,
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
        )
        fig_horizon.update_layout(height=400)
        st.plotly_chart(fig_horizon, use_container_width=True)

    with col2:
        st.subheader("💰 Investment Focus Analysis")

        # Investment focus vs qualitative size
        fig_scatter = px.scatter(
            st.session_state.opportunities_df,
            x='Investment_Focus_Score',
            y='Qualitative_Size',
            size='Investment_Focus_Score',
            color='Investment_Focus_Score',
            hover_name='Opportunity_Area',
            title="Investment Focus vs Market Size",
            template=chart_theme,
            color_continuous_scale='RdYlBu_r'
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Top opportunities
        st.subheader("🏆 Top Investment Opportunities")
        top_opportunities = st.session_state.opportunities_df.nlargest(5, 'Investment_Focus_Score')

        for idx, row in top_opportunities.iterrows():
            st.markdown(f"""
            <div class="opportunity-highlight">
                <h4>{row['Opportunity_Area']}</h4>
                <p><strong>Focus Score:</strong> {row['Investment_Focus_Score']}/10</p>
                <p><strong>Market Size:</strong> {row['Qualitative_Size']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- Enhanced Footer Information in Sidebar ---
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-section">
    <h3>📊 Dashboard Statistics</h3>
    <p><strong>Last Update:</strong> <code>{}</code></p>
    <p><strong>Trends Analyzed:</strong> {}</p>
    <p><strong>Opportunities Mapped:</strong> {}</p>
</div>
""".format(st.session_state.last_update_time, len(st.session_state.trends_df), len(st.session_state.opportunities_df)), unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-section">
    <h3>👨‍💻 Developer</h3>
    <p><strong>Created by:</strong> Easin Arafat</p>
    <p><strong>GitHub:</strong> <a href="https://github.com/mrx-arafat" target="_blank">@mrx-arafat</a></p>
    <p><strong>Repository:</strong> <a href="https://github.com/mrx-arafat/AI-Opportunity-Map" target="_blank">AI-Opportunity-Map</a></p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p><strong>Built with ❤️ using Streamlit</strong></p>
    <p style="font-size: 0.8rem; opacity: 0.7;"><em>Data is simulated for demonstration purposes</em></p>
</div>
""", unsafe_allow_html=True)