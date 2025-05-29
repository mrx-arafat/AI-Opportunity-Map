import streamlit as st
import pandas as pd
import plotly.express as px
import time # For simulating updates
import numpy as np # Import numpy

# --- Configuration & Initial Data (Simulated) ---
# Use the full page width
st.set_page_config(layout="wide", page_title="AI Opportunity Map Dashboard")

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
st.title("🌐 Dynamic AI Industry Opportunity Map")
st.markdown("""
Welcome to the AI Opportunity Map. This dashboard provides a conceptual overview of trends,
opportunities, and strategic considerations in the rapidly evolving AI industry.
*Data is illustrative and simulates dynamic updates when the button in the sidebar is clicked.*
""")

# --- Sidebar for Controls ---
st.sidebar.header("⚙️ Controls & Filters")
st.sidebar.info("Future controls could include: Filter by industry, investment level, or specific technology.")
update_button = st.sidebar.button("🔄 Simulate Data Update", help="Click to simulate fetching new data and updating the dashboard.")

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
tab1, tab2, tab3 = st.tabs(["📈 Trend Timeline", "💡 Opportunity Sizing", "🌳 Strategy Decision Trees"])

with tab1:
    st.header("AI Industry Trend Timeline & Impact")
    st.markdown("""
    This section visualizes key AI industry trends, their perceived impact, and their current time horizon.
    *In a fully developed dashboard, clicking on a trend could reveal detailed articles, data sources, or related opportunities.*
    """)

    # Visualization for Trends using Plotly Express
    # Ensure the DataFrame is sorted by Impact_Score for better visualization if desired, or by Time_Horizon
    # For example, to sort by Time_Horizon to group them:
    # sorted_trends_df = st.session_state.trends_df.sort_values(by='Time_Horizon')
    fig_trends = px.bar(
        st.session_state.trends_df,
        x='Trend',
        y='Impact_Score',
        color='Time_Horizon',
        title="AI Industry Trends by Impact and Time Horizon",
        labels={'Impact_Score': 'Perceived Impact Score (1-10)', 'Trend': 'Industry Trend'},
        category_orders={"Time_Horizon": ["Currently Dominant (Now - 1-2 Years)", "Emerging & Growing (1-3 Years)", "Future Outlook (3-5+ Years)"]} # Ensures consistent order in legend
    )
    fig_trends.update_layout(xaxis_tickangle=-45, height=650, legend_title_text='Time Horizon')
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
    st.header("AI Opportunity Sizing & Focus")
    st.markdown("""
    This section identifies potential opportunity areas based on current trends and a qualitative assessment of their size and investment focus.
    *The 'Investment Focus Score' is a simulated metric. Actual market sizing requires dedicated research.*
    """)

    # Treemap visualization for Opportunities
    fig_ops = px.treemap(
        st.session_state.opportunities_df,
        path=[px.Constant("All AI Opportunities"), 'Qualitative_Size', 'Opportunity_Area'], # Defines the hierarchy
        values='Investment_Focus_Score',
        color='Investment_Focus_Score',
        color_continuous_scale='viridis', # Using a different color scale
        title="AI Opportunity Areas by Qualitative Size and Investment Focus Score",
        hover_data={'Related_Trends': True} # Show related trends on hover
    )
    fig_ops.update_layout(height=700, margin = dict(t=50, l=25, r=25, b=25))
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

# --- Footer Information in Sidebar ---
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Dashboard Information**")
st.sidebar.markdown(f"Last Simulated Update: `{st.session_state.last_update_time}`")
st.sidebar.markdown("Source Data: Simulated based on user-provided industry insights.")
st.sidebar.markdown("Developed using [Streamlit](https://streamlit.io).")