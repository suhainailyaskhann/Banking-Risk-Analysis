import pandas as pd
import numpy as np
import os
import seaborn as sns

class BankPortfolio:
    def __init__(self, folder_path: str, bank_names: list, start_date=None, end_date=None):
        self.folder_path = folder_path
        self.bank_names = bank_names
        self.start_date = pd.to_datetime(start_date) if start_date else None
        self.end_date = pd.to_datetime(end_date) if end_date else None
        self.__all_prices = self.__combine_csv_files()
        
    def __combine_csv_files(self) -> pd.DataFrame:
        merged_table = pd.DataFrame()
        for bank in self.bank_names:
            file_location = os.path.join(self.folder_path, f"{bank}.csv")
            stock_data = pd.read_csv(file_location, parse_dates=['Date'], index_col='Date')
            stock_data = stock_data[['Close']].rename(columns={'Close': bank})
            
            if merged_table.empty:
                merged_table = stock_data
            else:
                merged_table = merged_table.join(stock_data, how='inner')
                
        df = merged_table.dropna()
        
        if self.start_date:
            df = df[df.index >= self.start_date]
        if self.end_date:
            df = df[df.index <= self.end_date]
            
        return df

    def get_prices(self) -> pd.DataFrame:
        return self.__all_prices.copy()

    @property
    def daily_returns(self) -> pd.DataFrame:
        return self.__all_prices.pct_change().dropna()
        
    def calculate_annualized_risk(self) -> pd.Series:
        return self.daily_returns.std() * np.sqrt(252)

    def plot_performance_and_risk(self):
        sns.set_theme(style="whitegrid", palette="husl")
        
        cumulative_growth = (1 + self.daily_returns).cumprod()
        annualized_return = self.daily_returns.mean() * 252
        annualized_risk = self.calculate_annualized_risk()

        risk_return_df = pd.DataFrame({
            'Risk': annualized_risk,
            'Return': annualized_return,
            'Bank': self.bank_names
        })

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#f8f9fa')
        
        sns.lineplot(data=cumulative_growth, ax=ax1, dashes=False, linewidth=2.5)
        ax1.set_title('Cumulative Return Over Time', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Growth (Base 1.0)')
        
        sns.scatterplot(data=risk_return_df, x='Risk', y='Return', hue='Bank', s=200, ax=ax2, edgecolor='black')
        
        for i in range(risk_return_df.shape[0]):
            ax2.text(risk_return_df['Risk'].iloc[i] + 0.005, 
                     risk_return_df['Return'].iloc[i], 
                     risk_return_df['Bank'].iloc[i], 
                     horizontalalignment='left', weight='bold')
            
        ax2.set_title('Risk vs. Expected Return', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Annualized Risk (Volatility)')
        ax2.set_ylabel('Annualized Return')
        
        plt.tight_layout()
        return fig
