import streamlit as st
from sourcecode.main import BankPortfolio

st.set_page_config(page_title="FinTech Risk Analyzer", layout="wide")

with st.sidebar:
    st.header("Bank Legend")
    st.markdown("**JPM**: JPMorgan Chase & Co.")
    st.markdown("**GS**: The Goldman Sachs Group, Inc.")
    st.markdown("**MS**: Morgan Stanley")
    
    st.markdown("---")
    st.header("Data References")
    st.markdown("Historical stock data retrieved from **Kaggle**.")
    st.caption("Files utilized: `jpm.csv`, `GS.csv`, `MS.csv`")

st.title("Banking Sector Risk & Return Dashboard")
st.markdown("### *Interactive quantitative evaluation of asset performance.*")

try:
    portfolio = BankPortfolio(
        folder_path="datacsv", 
        bank_names=['jpm', 'GS', 'MS']
    )
    
    st.markdown("---")
    st.subheader("Executive Summary (Latest Close)")
    
    prices_df = portfolio.get_prices()
    latest_prices = prices_df.iloc[-1]
    prev_prices = prices_df.iloc[-2]
    
    full_names = {
        'jpm': 'JPMorgan Chase',
        'GS': 'Goldman Sachs',
        'MS': 'Morgan Stanley'
    }
    
    kpi_cols = st.columns(3)
    for idx, bank in enumerate(['jpm', 'GS', 'MS']):
        current_price = latest_prices[bank]
        delta_val = current_price - prev_prices[bank]
        delta_pct = (delta_val / prev_prices[bank]) * 100
        
        with kpi_cols[idx]:
            display_key = bank.upper()
            st.metric(
                label=f"{full_names[bank]} ({display_key})", 
                value=f"${current_price:.2f}", 
                delta=f"{delta_pct:.2f}%"
            )
            
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Daily Returns**")
        st.dataframe(portfolio.daily_returns.tail(), width='stretch')
        
    with col2:
        st.warning("**Annualized Volatility (Risk)**")
        st.dataframe(portfolio.calculate_annualized_risk(), width='stretch')

    st.markdown("---")
    st.subheader("Risk vs. Reward Visualization")
    fig = portfolio.plot_performance_and_risk()
    st.pyplot(fig)

    st.markdown("---")
    st.caption("**Project Data Source**: Historical banking sector datasets (`jpm.csv`, `GS.csv`, `MS.csv`) provided by [Kaggle](https://www.kaggle.com/).")
    st.caption("By **Suhaina Ilyas Khan**")

except Exception as e:
    st.error(f"Failed to load data: {e}")
