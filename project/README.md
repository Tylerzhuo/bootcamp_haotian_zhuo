# Project: Stock Returns and Market Index Relationship

This project studies the relationship between individual stock returns (e.g., Apple, Microsoft) and the market index (e.g., S&P 500).  

---

## Stage 01 – Problem Framing & Scoping
- **Research Question**: Are individual stock returns strongly correlated with the overall market index?  
- **Hypothesis**: Stocks such as AAPL and MSFT will show a positive correlation with the S&P 500.  
- **Scope**: Use daily closing prices over the past 3–5 years. The project focuses on correlation analysis rather than predictive modeling.

---

## Stage 02 – Tooling Setup

- Project directory structure:

    ```text
    project/
    |-- data/
    |   |-- raw/
    |   `-- processed/
    |-- notebooks/
    |-- src/
    |   |-- __init__.py
    |   `-- utils.py
    |-- .env
    `-- README.md
    ```

- Environment: Python 3, with packages `pandas`, `numpy`, `matplotlib`, `seaborn`, and `yfinance`.

- `.env` file defines `DATA_RAW_PATH` and `DATA_PROCESSED_PATH` for reproducible paths.


---

## Stage 03 – Python Fundamentals
- Utility functions implemented:
  - `daily_return(prices)`: compute daily log returns from adjusted close prices.  
  - `correlation(x, y)`: compute Pearson correlation coefficient between two return series.  
- Tested these functions on small synthetic data to confirm correctness.

---

## Stage 04 – Data Acquisition & Ingestion
- Data source: Yahoo Finance (via `yfinance` package) or pre-downloaded CSVs.  
- Assets: AAPL, MSFT, and S&P 500 (ticker: ^GSPC).  
- Saved raw price data to `data/raw/`.  
- Merged into a single DataFrame with aligned dates.

---

## Stage 05 – Data Storage
- Raw datasets stored in `data/raw/` as CSV.  
- Processed returns stored in `data/processed/` in both CSV and Parquet formats.  
- Implemented helper functions:
  - `write_df(df, path)`  
  - `read_df(path)`  
  to handle saving and loading with friendly error handling.

---

## Stage 06 – Data Preprocessing
- Aligned trading dates across assets.  
- Handled missing values:
  - Forward-filled missing prices if the market was open but the stock did not trade.  
  - Dropped rows where data was missing for all assets.  
- Removed duplicate rows if any.  
- Normalized returns for comparability (min-max scaling to [0,1]).  
- Verified that row counts and column datatypes were consistent after preprocessing.

---

## Stage 07 – Outliers & Risk Assumptions
- Detected outliers in returns using:
  - **IQR rule** (k = 1.5).  
  - **Z-score rule** (|z| > 3).  
- Compared correlation coefficients **with** and **without** outliers.  
- Visualization:
  - Scatter plots of stock vs. index returns.  
  - Boxplots before and after outlier removal.  
- **Reflection**:  
  - Outliers (large crashes or spikes) can distort correlation.  
  - However, in finance, extreme events are often the most important risk signals.  
  - Removing them makes correlation appear “cleaner” but may underestimate risk.  
  - Thresholds are heuristic; in practice, risk models (e.g., VaR) are also used.
  
---

## Stage 08 – Exploratory Data Analysis (EDA)

**Goal:**  
Understand the structure, distribution, and relationships in the processed datasets (MSFT, AAPL, SP500).  

**Steps Performed:**  
- Computed **statistical summaries**: mean, median, standard deviation, skewness.  
- Checked for **missing values** and **outliers** using IQR.  
- Visualized data with:
  - Histograms (close price, volume)
  - Boxplots (close price)
  - Scatter plots (volume vs close)
  - Time-series plots (close price over time)
  - Correlation heatmaps (numeric variables)

**Key Insights:**  
- Volume showed heavy skew and potential outliers.  
- Close prices displayed clear trends and volatility over time.  
- Strong correlations exist between price-related features.  

**Implication for next steps:**  
- Outlier treatment may be required.  
- Skewed variables could benefit from log transformation.  
- Time-aware validation is needed for modeling.

---

## Stage 09 – Feature Engineering

**Goal:**  
Construct new indicators from stock data to support modeling and financial analysis.  

**New Features:**  
1. **Volatility (7-day)**  
   - Rolling standard deviation of closing prices.  
   - Captures short-term uncertainty and market risk.  

2. **Price-to-Volume Ratio**  
   - Closing price ÷ trading volume.  
   - Reflects how much price movement occurs relative to trading activity.  

3. **Momentum (10-day)**  
   - Relative change in close price compared to 10 days ago.  
   - Positive values indicate bullish momentum; negative values suggest bearish trends.  

**Impact:**  
- These engineered features enrich the dataset with risk, liquidity, and trend information.  
- They will be valuable inputs for predictive modeling and financial analysis in subsequent stages.

---


---

## Project Value
- **Educational**: Covers end-to-end data pipeline from raw data to statistical reflection.  
- **Financial Relevance**: Correlation analysis links directly to systematic vs. idiosyncratic risk, and concepts like beta in CAPM.  
- **Practical**: Small, reproducible project with real-world data, suitable for learning and presentation.
