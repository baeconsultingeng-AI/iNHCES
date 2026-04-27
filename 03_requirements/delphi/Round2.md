# iNHCES Delphi Round 2 — 38-Item Likert Instrument

> DATA SOURCE: AMBER — Instrument is real; ratings are SYNTHETIC (numpy seed=42).

**Scale**: 1=Strongly Disagree ... 7=Strongly Agree  
**Consensus**: Mean >= 5.0, CV <= 20.0%  
**n**: 20 (synthetic)  

## Category A: Macroeconomic Feature Requirements

**A1**: The NGN/USD exchange rate should be included as a predictive feature in the iNHCES model  
Mean=6.35, SD=0.67, CV=10.6%, Consensus=YES  

**A2**: The CPI/inflation rate (annual %) should be included as a predictive feature in the model  
Mean=6.40, SD=0.50, CV=7.9%, Consensus=YES  

**A3**: Brent crude oil price (USD/barrel) should be included as a predictive feature in the model  
Mean=6.00, SD=0.86, CV=14.3%, Consensus=YES  

**A4**: Nigeria's GDP growth rate (annual %) should be included as a predictive feature  
Mean=5.10, SD=0.85, CV=16.7%, Consensus=YES  

**A5**: The commercial lending interest rate should be included as a predictive feature  
Mean=4.20, SD=1.01, CV=23.9%, Consensus=NO (-> Round 3)  

**A6**: The iNHCES system should use live, automatically updated macroeconomic data, not static historical tables  
Mean=6.00, SD=0.65, CV=10.8%, Consensus=YES  

**A7**: Macroeconomic features in the model should be refreshed at least once per week automatically  
Mean=5.80, SD=1.01, CV=17.3%, Consensus=YES  

## Category B: Project Characteristic Features

**B1**: Gross floor area in square metres (sqm) should be a mandatory input feature for every estimate  
Mean=6.50, SD=0.51, CV=7.9%, Consensus=YES  

**B2**: Number of building storeys (above ground) should be a mandatory input feature  
Mean=6.25, SD=0.64, CV=10.2%, Consensus=YES  

**B3**: Structural system type (masonry/reinforced concrete frame/steel frame) should be a mandatory input feature  
Mean=6.15, SD=0.75, CV=12.1%, Consensus=YES  

**B4**: Project location expressed as geopolitical zone or state should be a mandatory input feature  
Mean=6.40, SD=0.60, CV=9.3%, Consensus=YES  

**B5**: Project type (purely residential / commercial / mixed-use) should be a mandatory input feature  
Mean=6.25, SD=0.64, CV=10.2%, Consensus=YES  

**B6**: Procurement method (direct labour / traditional / design-and-build) should be included as an input feature  
Mean=4.25, SD=1.74, CV=41.0%, Consensus=NO (-> Round 3)  

**B7**: Specification level (standard / medium / luxury finish) should be included as an input feature  
Mean=6.00, SD=0.65, CV=10.8%, Consensus=YES  

**B8**: Number of residential units or bedrooms should be included as an input feature  
Mean=5.20, SD=1.32, CV=25.4%, Consensus=NO (-> Round 3)  

## Category C: ML Model Requirements

**C1**: The deployed iNHCES model should achieve a Mean Absolute Percentage Error (MAPE) of <= 15% on held-out validation data  
Mean=6.20, SD=0.89, CV=14.4%, Consensus=YES  

**C2**: The model must provide SHAP-based feature importance explanations for every estimate generated  
Mean=5.80, SD=1.11, CV=19.1%, Consensus=YES  

**C3**: The model should provide 90% prediction intervals alongside point estimates to communicate uncertainty  
Mean=5.80, SD=1.01, CV=17.3%, Consensus=YES  

**C4**: The model should be automatically retrained at least quarterly as new project cost data becomes available  
Mean=6.10, SD=0.91, CV=14.9%, Consensus=YES  

**C5**: Multiple ML algorithms (e.g. Ridge, RF, XGBoost, LightGBM, MLP) should be benchmarked before the champion model is selected for deployment  
Mean=5.35, SD=1.04, CV=19.4%, Consensus=YES  

**C6**: A stacking ensemble should be selected as the champion model if it outperforms individual models on cross-validated MAPE  
Mean=4.85, SD=1.46, CV=30.1%, Consensus=NO (-> Round 3)  

## Category D: System Performance Requirements

**D1**: Cost estimate generation (model inference + SHAP calculation) should complete within 3 seconds  
Mean=6.05, SD=0.76, CV=12.5%, Consensus=YES  

**D2**: The system should support at least 50 simultaneous active users without performance degradation  
Mean=5.95, SD=0.89, CV=14.9%, Consensus=YES  

**D3**: The iNHCES web system should maintain at least 99.5% uptime (scheduled maintenance excluded)  
Mean=6.30, SD=0.66, CV=10.4%, Consensus=YES  

**D4**: Every estimate should be stored with a full audit trail: user identity, timestamp, all inputs, model version, and outputs  
Mean=6.40, SD=0.68, CV=10.6%, Consensus=YES  

**D5**: The system should automatically generate a professionally formatted PDF cost report for every estimate completed  
Mean=6.05, SD=1.05, CV=17.4%, Consensus=YES  

## Category E: Interface Requirements

**E1**: The user interface should be fully accessible via standard web browser without any software installation  
Mean=6.40, SD=0.60, CV=9.3%, Consensus=YES  

**E2**: A qualified QS professional should be able to complete the estimate input form in under 5 minutes  
Mean=5.80, SD=0.83, CV=14.4%, Consensus=YES  

**E3**: Estimate results should include a visual cost breakdown chart (elemental or trade-by-trade)  
Mean=5.85, SD=0.88, CV=15.0%, Consensus=YES  

**E4**: The interface should display data freshness indicators showing the age of each macroeconomic data source  
Mean=5.20, SD=1.24, CV=23.8%, Consensus=NO (-> Round 3)  

**E5**: The user interface should be fully usable on mobile phones and tablet devices  
Mean=4.75, SD=1.41, CV=29.7%, Consensus=NO (-> Round 3)  

**E6**: Each registered user should be able to save and manage multiple project profiles  
Mean=5.25, SD=1.16, CV=22.2%, Consensus=NO (-> Round 3)  

## Category F: Data Quality Requirements

**F1**: The system should display a warning flag when any macroeconomic data source is more than 7 days old  
Mean=6.00, SD=0.92, CV=15.3%, Consensus=YES  

**F2**: Each estimate should display a DATA SOURCE confidence classification (GREEN/AMBER/RED) indicating data quality  
Mean=5.65, SD=0.93, CV=16.5%, Consensus=YES  

**F3**: Missing or invalid input values should produce clear, user-friendly validation messages — not system crashes  
Mean=6.25, SD=0.64, CV=10.2%, Consensus=YES  

**F4**: All numeric inputs should be validated against plausible real-world range limits before submission  
Mean=5.95, SD=0.83, CV=13.9%, Consensus=YES  

## Category G: Reporting Requirements

**G1**: Generated PDF reports should follow the NIQS (Nigerian Institute of Quantity Surveyors) cost plan format  
Mean=6.10, SD=0.97, CV=15.9%, Consensus=YES  

**G2**: Reports should include a sensitivity analysis showing estimate variation under 3 exchange rate scenarios (base, +15%, -15%)  
Mean=4.95, SD=1.54, CV=31.1%, Consensus=NO (-> Round 3)  

**G3**: Cost reports should be exportable as professionally formatted, branded PDF documents  
Mean=6.70, SD=0.57, CV=8.5%, Consensus=YES  

**G4**: The report format should be acceptable for submission alongside tender documents in Nigerian public procurement  
Mean=6.05, SD=0.83, CV=13.6%, Consensus=YES  

