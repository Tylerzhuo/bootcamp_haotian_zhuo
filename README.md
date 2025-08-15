# bootcamp_haotian_zhuo
## Folder Structure
- **homework/** → All homework contributions will be submitted here.
- **project/** → All project contributions will be submitted here.
- **class_materials/** → Local storage for class materials. Never pushed to
GitHub.

## Homework Folder Rules
- Each homework will be in its own subfolder (`homework0`, `homework1`, etc.)
- Include all required files for grading.
## Project Folder Rules
- Keep project files organized and clearly named.

# Equity Pricing Error Prediction  
**Stage:** Problem Framing & Scoping (Stage 01)  

## Problem Statement  
Current pricing models show persistent errors averaging vs actual closing prices. This project builds a hybrid model combining Bayesian Model Averaging Approach with attention mechanisms to reduce pricing errors by:  
1) Incorporating spike-and-slab prior to substitute flat prior, in order to improve robustness of the model.
2) Leveraging 118 factors constructed by a lot of financial indexes, which is more comprehensive than Fama-and-French model.
Target: Narrow down the pricing errors and perform better than all the classic models.

## Stakeholder & User  
- **Decision Maker**: Hedge fund pricing committee  
- **Primary User**: Quant trading desk  
- **Workflow Context**:  
  - Pre-market: Generate price corridors  
  - Intraday: Continuous error monitoring  

## Useful Answer & Decision  
**Predictive Framework**:  
- Output: Predicted pricing error bands (+/- 1σ)  
- Deliverables:  
  - Python pricing library (PyPI package)  
  - Streamlit monitoring dashboard   

## Assumptions & Constraints  
- Data Sources:  
  - Bloomberg terminal data (OHLCV + L2 orderbook)  
  - Wind terminal data
  - CSMAR financial data
- Latency: <250ms for EOD pricing  
- Compliance: Reg NMS compliant  

## Known Unknowns / Risks  
- Market microstructure changes  
- News sentiment parsing errors  
- Validation: Walk-forward testing 2007-2023  

## Lifecycle Mapping  
Alpha Research → Model Development → Backtest Report  
Productionization → API Development → CI/CD Pipeline  

## Repo Structure  
- `/data/`
- `/src/` 
- `/notebooks/`
