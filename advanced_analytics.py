"""
Advanced Analytics Module for AI Opportunity Map
===============================================

This module provides sophisticated analytical capabilities including:
- Predictive modeling for AI trends
- Market correlation analysis
- Investment opportunity scoring
- Risk assessment frameworks
- ROI calculations and projections

Author: Easin Arafat (@mrx-arafat)
Last Updated: June 2025
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class AIMarketAnalytics:
    """Advanced analytics engine for AI market intelligence."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def calculate_opportunity_score(self, market_size, growth_rate, adoption_rate, investment_focus):
        """
        Calculate comprehensive opportunity score using weighted factors.
        
        Args:
            market_size: Market size in billions
            growth_rate: CAGR percentage
            adoption_rate: Current adoption percentage
            investment_focus: Investment priority score (1-10)
            
        Returns:
            Normalized opportunity score (0-100)
        """
        # Normalize inputs
        market_weight = 0.3
        growth_weight = 0.25
        adoption_weight = 0.2
        investment_weight = 0.25
        
        # Log transform market size to handle large variations
        normalized_market = np.log10(market_size + 1) / np.log10(1000)  # Normalize to 0-1
        normalized_growth = min(growth_rate / 50, 1)  # Cap at 50% growth
        normalized_adoption = adoption_rate / 100
        normalized_investment = investment_focus / 10
        
        opportunity_score = (
            normalized_market * market_weight +
            normalized_growth * growth_weight +
            normalized_adoption * adoption_weight +
            normalized_investment * investment_weight
        ) * 100
        
        return min(opportunity_score, 100)
    
    def perform_trend_clustering(self, trends_df):
        """
        Perform K-means clustering on AI trends to identify strategic groups.
        
        Args:
            trends_df: DataFrame with trend data
            
        Returns:
            DataFrame with cluster assignments and analysis
        """
        # Prepare features for clustering
        features = ['Impact_Score', 'Market_Size_Billion', 'Adoption_Rate']
        X = trends_df[features].fillna(0)
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels
        trends_df = trends_df.copy()
        trends_df['Cluster'] = clusters
        
        # Define cluster characteristics
        cluster_names = {
            0: "High Impact Leaders",
            1: "Emerging Opportunities", 
            2: "Mainstream Adoption",
            3: "Niche Specialists"
        }
        
        trends_df['Cluster_Name'] = trends_df['Cluster'].map(cluster_names)
        
        return trends_df, kmeans
    
    def calculate_market_correlations(self, data_df):
        """
        Calculate correlations between market factors.
        
        Args:
            data_df: DataFrame with market data
            
        Returns:
            Correlation matrix and insights
        """
        numeric_cols = data_df.select_dtypes(include=[np.number]).columns
        correlation_matrix = data_df[numeric_cols].corr()
        
        # Find strongest correlations
        correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.3:  # Only significant correlations
                    correlations.append({
                        'Factor_1': correlation_matrix.columns[i],
                        'Factor_2': correlation_matrix.columns[j],
                        'Correlation': corr_value,
                        'Strength': 'Strong' if abs(corr_value) > 0.7 else 'Moderate'
                    })
        
        return correlation_matrix, pd.DataFrame(correlations)
    
    def predict_market_growth(self, historical_data, periods=12):
        """
        Simple trend-based prediction for market growth.
        
        Args:
            historical_data: Time series data
            periods: Number of periods to forecast
            
        Returns:
            Forecast values and confidence intervals
        """
        # Simple linear trend extrapolation
        x = np.arange(len(historical_data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, historical_data)
        
        # Generate predictions
        future_x = np.arange(len(historical_data), len(historical_data) + periods)
        predictions = slope * future_x + intercept
        
        # Calculate confidence intervals (simplified)
        confidence_interval = 1.96 * std_err * np.sqrt(1 + 1/len(historical_data))
        
        return {
            'predictions': predictions,
            'confidence_upper': predictions + confidence_interval,
            'confidence_lower': predictions - confidence_interval,
            'r_squared': r_value**2,
            'trend_strength': 'Strong' if abs(r_value) > 0.8 else 'Moderate' if abs(r_value) > 0.5 else 'Weak'
        }
    
    def calculate_investment_risk_score(self, opportunity_data):
        """
        Calculate investment risk scores based on multiple factors.
        
        Args:
            opportunity_data: DataFrame with opportunity information
            
        Returns:
            DataFrame with risk scores and classifications
        """
        risk_factors = {
            'market_volatility': 0.25,
            'regulatory_risk': 0.20,
            'technology_maturity': 0.20,
            'competition_intensity': 0.15,
            'adoption_uncertainty': 0.20
        }
        
        # Simulate risk scores (in real implementation, these would be calculated from actual data)
        np.random.seed(42)  # For reproducible results
        
        risk_scores = []
        for _, row in opportunity_data.iterrows():
            # Base risk calculation
            market_vol = np.random.uniform(0.2, 0.8)
            reg_risk = 0.8 if 'Governance' in row['Opportunity_Area'] else np.random.uniform(0.1, 0.6)
            tech_maturity = 0.3 if row['Maturity_Level'] == 'Emerging' else 0.6 if row['Maturity_Level'] == 'Early Growth' else 0.8
            competition = np.random.uniform(0.3, 0.9)
            adoption_unc = 1 - (row['Investment_Focus_Score'] / 10)
            
            total_risk = (
                market_vol * risk_factors['market_volatility'] +
                reg_risk * risk_factors['regulatory_risk'] +
                (1 - tech_maturity) * risk_factors['technology_maturity'] +
                competition * risk_factors['competition_intensity'] +
                adoption_unc * risk_factors['adoption_uncertainty']
            )
            
            risk_scores.append(total_risk)
        
        opportunity_data = opportunity_data.copy()
        opportunity_data['Risk_Score'] = risk_scores
        opportunity_data['Risk_Level'] = pd.cut(
            risk_scores, 
            bins=[0, 0.3, 0.6, 1.0], 
            labels=['Low', 'Medium', 'High']
        )
        
        return opportunity_data
    
    def generate_portfolio_recommendations(self, opportunities_df, risk_tolerance='medium', investment_amount=1000000):
        """
        Generate investment portfolio recommendations based on risk tolerance.
        
        Args:
            opportunities_df: DataFrame with opportunity data
            risk_tolerance: 'low', 'medium', or 'high'
            investment_amount: Total investment amount in USD
            
        Returns:
            Portfolio allocation recommendations
        """
        # Calculate opportunity scores
        opp_scores = []
        for _, row in opportunities_df.iterrows():
            score = self.calculate_opportunity_score(
                float(row['Market_Size_2025'].replace('Large ($', '').replace('Medium ($', '').replace('B+)', '')),
                row['Growth_Rate_CAGR'],
                50,  # Assume 50% adoption for calculation
                row['Investment_Focus_Score']
            )
            opp_scores.append(score)
        
        opportunities_df = opportunities_df.copy()
        opportunities_df['Opportunity_Score'] = opp_scores
        
        # Risk-based filtering
        if risk_tolerance == 'low':
            filtered_opps = opportunities_df[opportunities_df['Risk_Level'] == 'Low']
            max_allocation = 0.25
        elif risk_tolerance == 'medium':
            filtered_opps = opportunities_df[opportunities_df['Risk_Level'].isin(['Low', 'Medium'])]
            max_allocation = 0.35
        else:  # high risk tolerance
            filtered_opps = opportunities_df
            max_allocation = 0.50
        
        # Sort by opportunity score
        filtered_opps = filtered_opps.sort_values('Opportunity_Score', ascending=False)
        
        # Allocate investment
        total_score = filtered_opps['Opportunity_Score'].sum()
        allocations = []
        
        for _, row in filtered_opps.head(8).iterrows():  # Top 8 opportunities
            weight = min(row['Opportunity_Score'] / total_score, max_allocation)
            allocation = investment_amount * weight
            
            allocations.append({
                'Opportunity': row['Opportunity_Area'],
                'Allocation_USD': allocation,
                'Allocation_Percent': weight * 100,
                'Expected_Return': row['Growth_Rate_CAGR'],
                'Risk_Level': row['Risk_Level'],
                'Opportunity_Score': row['Opportunity_Score']
            })
        
        return pd.DataFrame(allocations)

def create_advanced_visualizations(trends_df, opportunities_df, analytics_engine):
    """
    Create advanced analytical visualizations.
    
    Args:
        trends_df: Trends data
        opportunities_df: Opportunities data
        analytics_engine: AIMarketAnalytics instance
        
    Returns:
        Dictionary of plotly figures
    """
    figures = {}
    
    # 1. Opportunity Score vs Risk Matrix
    opp_with_risk = analytics_engine.calculate_investment_risk_score(opportunities_df)
    
    # Calculate opportunity scores
    opp_scores = []
    for _, row in opp_with_risk.iterrows():
        score = analytics_engine.calculate_opportunity_score(
            float(row['Market_Size_2025'].replace('Large ($', '').replace('Medium ($', '').replace('B+)', '')),
            row['Growth_Rate_CAGR'],
            50,  # Assume 50% adoption
            row['Investment_Focus_Score']
        )
        opp_scores.append(score)
    
    opp_with_risk['Opportunity_Score'] = opp_scores
    
    fig_risk_return = px.scatter(
        opp_with_risk,
        x='Risk_Score',
        y='Opportunity_Score',
        size='Growth_Rate_CAGR',
        color='Risk_Level',
        hover_name='Opportunity_Area',
        title='Investment Risk vs Opportunity Matrix',
        labels={'Risk_Score': 'Risk Score', 'Opportunity_Score': 'Opportunity Score'},
        color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    )
    fig_risk_return.update_layout(height=500)
    figures['risk_return_matrix'] = fig_risk_return
    
    # 2. Market Size vs Growth Rate Bubble Chart
    # Extract numeric market size
    market_sizes = []
    for size_str in opportunities_df['Market_Size_2025']:
        if 'Large' in size_str:
            market_sizes.append(200)  # Assume $200B for large markets
        else:
            market_sizes.append(75)   # Assume $75B for medium markets
    
    fig_bubble = px.scatter(
        opportunities_df,
        x='Growth_Rate_CAGR',
        y='Investment_Focus_Score',
        size=market_sizes,
        color='Maturity_Level',
        hover_name='Opportunity_Area',
        title='Market Growth vs Investment Priority (Bubble Size = Market Size)',
        labels={'Growth_Rate_CAGR': 'Growth Rate (CAGR %)', 'Investment_Focus_Score': 'Investment Focus Score'}
    )
    fig_bubble.update_layout(height=500)
    figures['growth_investment_bubble'] = fig_bubble
    
    # 3. Trend Clustering Visualization
    clustered_trends, _ = analytics_engine.perform_trend_clustering(trends_df)
    
    fig_clusters = px.scatter_3d(
        clustered_trends,
        x='Impact_Score',
        y='Market_Size_Billion',
        z='Adoption_Rate',
        color='Cluster_Name',
        hover_name='Trend',
        title='AI Trends Strategic Clustering (3D)',
        labels={
            'Impact_Score': 'Impact Score',
            'Market_Size_Billion': 'Market Size ($B)',
            'Adoption_Rate': 'Adoption Rate (%)'
        }
    )
    fig_clusters.update_layout(height=600)
    figures['trend_clusters'] = fig_clusters
    
    # 4. Investment Portfolio Allocation
    portfolio = analytics_engine.generate_portfolio_recommendations(opp_with_risk)
    
    fig_portfolio = px.pie(
        portfolio,
        values='Allocation_Percent',
        names='Opportunity',
        title='Recommended Investment Portfolio Allocation',
        hover_data=['Expected_Return', 'Risk_Level']
    )
    fig_portfolio.update_layout(height=500)
    figures['portfolio_allocation'] = fig_portfolio
    
    # 5. Correlation Heatmap
    correlation_matrix, _ = analytics_engine.calculate_market_correlations(trends_df)
    
    fig_corr = px.imshow(
        correlation_matrix,
        title='Market Factors Correlation Matrix',
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    fig_corr.update_layout(height=500)
    figures['correlation_heatmap'] = fig_corr
    
    return figures

def generate_market_insights(trends_df, opportunities_df):
    """
    Generate key market insights and recommendations.
    
    Args:
        trends_df: Trends data
        opportunities_df: Opportunities data
        
    Returns:
        Dictionary of insights and recommendations
    """
    insights = {
        'market_overview': {
            'total_opportunities': len(opportunities_df),
            'high_growth_opportunities': len(opportunities_df[opportunities_df['Growth_Rate_CAGR'] > 30]),
            'emerging_trends': len(trends_df[trends_df['Time_Horizon'].str.contains('Emerging')]),
            'market_leaders': trends_df.nlargest(3, 'Impact_Score')['Trend'].tolist()
        },
        'investment_recommendations': {
            'top_opportunities': opportunities_df.nlargest(5, 'Investment_Focus_Score')[['Opportunity_Area', 'Investment_Focus_Score']].to_dict('records'),
            'fastest_growing': opportunities_df.nlargest(3, 'Growth_Rate_CAGR')[['Opportunity_Area', 'Growth_Rate_CAGR']].to_dict('records'),
            'emerging_markets': opportunities_df[opportunities_df['Maturity_Level'] == 'Emerging']['Opportunity_Area'].tolist()
        },
        'risk_analysis': {
            'low_risk_high_return': "AI-Powered Software Development, Enterprise AI Integration Services",
            'high_risk_high_return': "Agentic AI Platforms, Multimodal AI Development Tools",
            'stable_investments': "AI in Financial Services, AI-Enhanced Cybersecurity"
        },
        'strategic_recommendations': [
            "Focus on agentic AI platforms for maximum growth potential",
            "Invest in AI governance services due to regulatory requirements",
            "Consider multimodal AI for competitive differentiation",
            "Prioritize workforce reskilling to address talent gaps",
            "Develop sustainable AI infrastructure for long-term viability"
        ]
    }
    
    return insights