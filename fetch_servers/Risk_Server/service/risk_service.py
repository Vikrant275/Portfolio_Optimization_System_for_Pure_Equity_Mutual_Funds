
import yfinance as yf
import numpy as np


from ETL_Pipeline.entity.data_entity import Trading_data  # -----> simulate as pick date from trading platform


class Risk_Service:
    def __init__(self,stock,start,end):
        self.stock = stock
        self.start = start
        self.end = end

    def get_market_data(self):
        try:
            # dtype_map = {
            #     "Close": "float64",
            #     "Open": "float64",
            #     "Volume": "int64"
            # }
            # stock_df = pd.read_csv('D:\\Stock_Selection_and_Portfolio_Optimization_System_for_Pure_Equity_Mutual_Funds\\data\\Trading_data\\Stock.csv')
            # stock_df = stock_df.iloc[1:]
            # stock_df = stock_df.astype(dtype_map)
            #
            # market_df = pd.read_csv('D:\\Stock_Selection_and_Portfolio_Optimization_System_for_Pure_Equity_Mutual_Funds\\data\\Trading_data\\Index.csv')
            # market_df = market_df.iloc[1:]
            # market_df = market_df.astype(dtype_map)

            stock_df = yf.download(f"{self.stock}.NS", start=self.start, end=self.end)
            market_df = yf.download("^NSEI", start=self.start, end=self.end)

            return stock_df, market_df
        except Exception as e:
            raise e

    def compute_risk(self):
        try:
            stock_df, market_df = self.get_market_data()

            stock_df['returns'] = stock_df['Close'].pct_change()
            market_df['returns'] = market_df['Close'].pct_change()

            df = stock_df[['returns']].join(
                market_df[['returns']],
                how='inner',
                lsuffix='_stock',
                rsuffix='_market'
            ).dropna()

            # Beta
            cov = np.cov(df['returns_stock'], df['returns_market'])
            beta = cov[0][1] / cov[1][1]

            # Volatility
            vol = df['returns_stock'].std() * np.sqrt(252)

            # VaR
            var = np.percentile(df['returns_stock'], 5)

            return {
                "stock": self.stock,
                "beta": float(beta),
                "volatility": float(vol),
                "var": float(var)
            }
        except Exception as e:
            raise e

