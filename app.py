# app.py
# VisaTier 4.0 — The Ultimate Immigration ROI Simulator
import math
import numpy as np
import pandas as pd
import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import io
import base64
import hashlib
import random
import re
from fastapi import FastAPI
from pydantic import BaseModel

# --- ENHANCED CSS & DESIGN SYSTEM ---
CSS = """
:root {
    --vt-primary: #2563EB; --vt-accent: #10B981; --vt-danger: #EF4444;
    --vt-warning: #F59E0B; --vt-ink: #0F172A; --vt-muted: #64748B;
    --vt-success: #10B981; --vt-purple: #8B5CF6; --radius: 16px;
    --vt-bg-color: #F8FAFC; --vt-card-bg: #FFFFFF;
}
.gradio-container { max-width: 1400px !important; margin: 0 auto; background: var(--vt-bg-color); }
.vt-header {
    display: flex; justify-content: space-between; align-items: center;
    background: var(--vt-ink); color: #CBD5E1; padding: 16px; border-radius: 12px;
}
.vt-header .title { font-size: 24px; font-weight: 700; color: #FFFFFF; }
.vt-header .nav-links { display: flex; gap: 16px; align-items: center; }
.vt-header .nav-links a { color: #CBD5E1; text-decoration: none; transition: color 0.2s; }
.vt-header .nav-links a:hover { color: #FFFFFF; }
.vt-footer {
    background: var(--vt-ink); color: #94A3B8; padding: 32px 16px; margin-top: 40px;
    border-radius: 12px; text-align: center; font-size: 14px;
}
.vt-footer .footer-links a { color: #94A3B8; margin: 0 10px; text-decoration: none; }
.vt-footer .footer-links a:hover { color: #FFFFFF; }
.vt-footer .social-icons { margin-top: 15px; }
.vt-footer .social-icons a { margin: 0 8px; color: #94A3B8; font-size: 20px; transition: color 0.2s; }
.vt-footer .social-icons a:hover { color: #FFFFFF; }
.lead-capture-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.8); z-index: 1000; display: none;
    align-items: center; justify-content: center;
}
.lead-capture-modal {
    background: white; padding: 32px; border-radius: 20px; max-width: 500px;
    margin: 20px; box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    animation: slideIn 0.3s ease-out;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}
.profile-selector {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 12px; margin: 16px 0;
}
.profile-card {
    padding: 16px; border: 2px solid #E2E8F0; border-radius: 12px;
    text-align: center; cursor: pointer; transition: all 0.3s ease;
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
}
.profile-card:hover {
    border-color: var(--vt-primary); transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15);
}
.profile-card.selected {
    border-color: var(--vt-primary); background: linear-gradient(135deg, #EBF4FF, #DBEAFE);
}
.viral-share-section {
    background: linear-gradient(135deg, #8B5CF6, #6366F1);
    color: white; padding: 20px; border-radius: 16px; margin: 20px 0;
}
.share-buttons {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px; margin: 16px 0;
}
.share-button {
    padding: 12px 16px; border-radius: 8px; text-align: center;
    font-weight: 600; cursor: pointer; transition: all 0.3s ease;
    border: none; color: white;
}
.share-linkedin { background: #0077B5; }
.share-twitter { background: #1DA1F2; }
.share-whatsapp { background: #25D366; }
.share-telegram { background: #0088cc; }
.kpi-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px; margin: 20px 0;
}
.kpi-card {
    background: #FFFFFF; border-radius: 12px; padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.kpi-card .label {
    font-size: 14px; color: var(--vt-muted); margin-bottom: 8px;
}
.kpi-card .value {
    font-size: 24px; font-weight: 700; color: var(--vt-ink); margin-bottom: 4px;
}
.kpi-card .vt-note {
    font-size: 12px; color: var(--vt-muted);
}
.kpi-card.exceptional { border-left: 4px solid var(--vt-success); }
.kpi-card.exceptional .value { color: var(--vt-success); }
.kpi-card.good { border-left: 4px solid var(--vt-warning); }
.kpi-card.good .value { color: var(--vt-warning); }
.kpi-card.moderate { border-left: 4px solid var(--vt-muted); }
.kpi-card.moderate .value { color: var(--vt-muted); }
.kpi-card.error { border-left: 4px solid var(--vt-danger); }
.kpi-card.error .value { color: var(--vt-danger); }
.success-alert {
    text-align: center; padding: 20px; margin: 20px 0;
    border-radius: 12px; border: 2px solid currentColor; font-weight: 600;
}
.success-alert.exceptional { color: var(--vt-success); background: rgba(16,185,129,0.05); }
.success-alert.good { color: var(--vt-warning); background: rgba(245,158,11,0.05); }
.success-alert.moderate { color: var(--vt-muted); background: rgba(107,114,128,0.05); }
.insight-card {
    background: linear-gradient(135deg, rgba(37,99,235,0.05), rgba(16,185,129,0.05));
    border: 1px solid rgba(37,99,235,0.2); border-radius: 12px;
    padding: 20px; margin: 12px 0; position: relative;
}
.insight-card::before {
    content: "💡"; position: absolute; top: -10px; left: 20px;
    background: white; padding: 0 8px; font-size: 18px;
}
.cta-button {
    background: linear-gradient(135deg, #10B981, #059669);
    color: white; padding: 16px 32px; border-radius: 50px;
    font-weight: 700; font-size: 16px; border: none;
    cursor: pointer; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}
.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}
.progress-bar {
    width: 100%; height: 8px; background: #E2E8F0;
    border-radius: 4px; margin: 16px 0; overflow: hidden;
}
.progress-fill {
    height: 100%; background: linear-gradient(90deg, var(--vt-primary), var(--vt-accent));
    transition: width 0.5s ease;
}
.user-journey-step {
    display: flex; align-items: center; margin: 16px 0;
    padding: 16px; background: white; border-radius: 12px;
    border-left: 4px solid var(--vt-primary);
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.notification-toast {
    position: fixed; top: 20px; right: 20px; z-index: 1001;
    background: linear-gradient(135deg, #10B981, #059669);
    color: white; padding: 16px 24px; border-radius: 12px;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    display: none; animation: slideInRight 0.3s ease-out;
}
@keyframes slideInRight {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}
.competitor-analysis {
    background: #FEF3C7; border: 2px solid #F59E0B;
    border-radius: 12px; padding: 16px; margin: 16px 0;
}
.urgency-indicator {
    background: linear-gradient(135deg, #EF4444, #DC2626);
    color: white; padding: 8px 16px; border-radius: 20px;
    font-size: 12px; font-weight: 600; display: inline-block;
    animation: pulse 2s infinite;}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
.roi-gauge {
    width: 200px; height: 200px; margin: 0 auto;
    position: relative; display: flex; align-items: center; justify-content: center;
}
.testimonial-slider {
    background: #F1F5F9; padding: 20px; border-radius: 12px;
    margin: 16px 0; text-align: center;
}
.country-card {
    background: var(--vt-card-bg); border-radius: var(--radius); padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 2px solid transparent;
    transition: all 0.3s ease;
}
.country-card h4 { font-size: 18px; margin-top: 0; }
.country-card p { margin: 8px 0; font-size: 14px; }
.country-card .flag { font-size: 24px; }
.country-card .score { font-size: 20px; font-weight: bold; color: var(--vt-primary); }

@media (max-width: 768px) {
    .profile-selector { grid-template-columns: repeat(2, 1fr); }
    .share-buttons { grid-template-columns: 1fr; }
    .lead-capture-modal { margin: 10px; padding: 20px; }
    .vt-header { flex-direction: column; text-align: center; }
    .nav-links { margin-top: 12px; }
}
"""
THEME = gr.themes.Soft()

# --- FINANCIAL DATA & CONFIGURATIONS ---
LEGAL_DISCLAIMERS = {
    "tax": "This tool does not provide tax advice. Consult a qualified tax professional.",
    "immigration": "This tool does not provide immigration advice. Consult a licensed immigration professional.",
    "investment": "Investment projections are for educational purposes only and are not investment advice."
}

USER_PROFILES = {
    "startup_founder": {
        "name": "Startup Founder", "icon": "🚀", "typical_revenue": 15000,
        "typical_margin": 20, "risk_tolerance": 65, "success_multiplier": 1.2, "color": "#2563EB"
    },
    "crypto_entrepreneur": {
        "name": "Crypto Entrepreneur", "icon": "₿", "typical_revenue": 75000,
        "typical_margin": 60, "risk_tolerance": 85, "success_multiplier": 1.5, "color": "#F59E0B"
    },
    "consulting_expert": {
        "name": "Consulting Expert", "icon": "💼", "typical_revenue": 35000,
        "typical_margin": 45, "risk_tolerance": 45, "success_multiplier": 0.9, "color": "#10B981"
    },
    "saas_founder": {
        "name": "SaaS Founder", "icon": "💻", "typical_revenue": 50000,
        "typical_margin": 75, "risk_tolerance": 75, "success_multiplier": 1.3, "color": "#8B5CF6"
    },
    "real_estate": {
        "name": "Real Estate Investor", "icon": "🏠", "typical_revenue": 25000,
        "typical_margin": 35, "risk_tolerance": 35, "success_multiplier": 0.8, "color": "#DC2626"
    }
}

PROFILE_WEIGHTS = {
    "startup_founder": {"tax": 0.2, "cost": 0.15, "growth": 0.25, "ease": 0.2, "banking": 0.1, "partnership": 0.1},
    "crypto_entrepreneur": {"tax": 0.3, "cost": 0.05, "growth": 0.1, "ease": 0.1, "banking": 0.3, "partnership": 0.15},
    "consulting_expert": {"tax": 0.25, "cost": 0.2, "growth": 0.15, "ease": 0.2, "banking": 0.1, "partnership": 0.1},
    "saas_founder": {"tax": 0.2, "cost": 0.1, "growth": 0.3, "ease": 0.2, "banking": 0.1, "partnership": 0.1},
    "real_estate": {"tax": 0.25, "cost": 0.25, "growth": 0.1, "ease": 0.1, "banking": 0.1, "partnership": 0.2}
}

COUNTRY_CONFIG_ENHANCED = {
    "UAE (Dubai)": {
        "flag": "🇦🇪", "language": "Arabic, English", "visa": "Golden Visa",
        "corp_tax": 0.09, "pers_tax": 0.00, "rev_mult": 3.0, "margin_delta_pp": 5.0,
        "living_month": 9000.0, "ongoing_month": 1500.0, "setup_once": 35000.0,
        "currency": "AED", "inflation": 2.5, "market_growth": 8.5, "ease_business": 9.2,
        "tax_treaties": 95, "banking_score": 8.8, "legal_system": "Civil Law",
        "risk_factor": 0.9, "partnership_score": 95,
        "market_insights": {
            "startup_founder": "🚀 World-class startup ecosystem with 0% personal tax",
            "crypto_entrepreneur": "₿ Crypto-friendly regulations and banking",
            "consulting_expert": "💼 Hub for MENA market access",
            "saas_founder": "💻 Growing tech talent pool and government support",
            "real_estate": "🏠 Strong property market with freehold options"
        }
    },
    "Singapore": {
        "flag": "🇸🇬", "language": "English, Malay", "visa": "Employment Pass",
        "corp_tax": 0.17, "pers_tax": 0.22, "rev_mult": 2.8, "margin_delta_pp": 4.0,
        "living_month": 8500.0, "ongoing_month": 1800.0, "setup_once": 45000.0,
        "currency": "SGD", "inflation": 2.3, "market_growth": 6.2, "ease_business": 9.4,
        "tax_treaties": 85, "banking_score": 9.5, "legal_system": "Common Law",
        "risk_factor": 0.85, "partnership_score": 90,
        "market_insights": {
            "startup_founder": "🚀 Asia's startup capital with world-class infrastructure",
            "crypto_entrepreneur": "₿ Clear crypto regulations and fintech leadership",
            "consulting_expert": "💼 Gateway to 4 billion people in ASEAN",
            "saas_founder": "💻 Top talent hub with government innovation support",
            "real_estate": "🏠 Stable market with foreign investment options"
        }
    },
    "UK": {
        "flag": "🇬🇧", "language": "English", "visa": "Innovator Visa",
        "corp_tax": 0.25, "pers_tax": 0.27, "rev_mult": 1.5, "margin_delta_pp": 2.0,
        "living_month": 6200.0, "ongoing_month": 1100.0, "setup_once": 18000.0,
        "currency": "GBP", "inflation": 4.2, "market_growth": 2.1, "ease_business": 8.1,
        "tax_treaties": 130, "banking_score": 9.1, "legal_system": "Common Law",
        "risk_factor": 0.75, "partnership_score": 75,
        "market_insights": {
            "startup_founder": "🚀 Strong fintech ecosystem, easier post-Brexit setup",
            "crypto_entrepreneur": "₿ Developing crypto framework, banking challenges",
            "consulting_expert": "💼 English-speaking market, established network",
            "saas_founder": "💻 Deep tech talent, government R&D support",
            "real_estate": "🏠 Mature market with Brexit opportunities"
        }
    },
    "Estonia": {
        "flag": "🇪🇪", "language": "Estonian, Russian", "visa": "E-Residency",
        "corp_tax": 0.20, "pers_tax": 0.20, "rev_mult": 1.8, "margin_delta_pp": 3.5,
        "living_month": 3500.0, "ongoing_month": 800.0, "setup_once": 12000.0,
        "currency": "EUR", "inflation": 2.8, "market_growth": 4.5, "ease_business": 8.8,
        "tax_treaties": 65, "banking_score": 8.2, "legal_system": "Civil Law",
        "risk_factor": 0.8, "partnership_score": 85,
        "market_insights": {
            "startup_founder": "🚀 Digital-first country, e-Residency program",
            "crypto_entrepreneur": "₿ Crypto paradise with clear regulations",
            "consulting_expert": "💼 EU market access at lower costs",
            "saas_founder": "💻 Tech-savvy population, government digitization",
            "real_estate": "🏠 Emerging market with EU citizenship path"
        }
    },
    "Portugal": {
        "flag": "🇵🇹", "language": "Portuguese, English", "visa": "NHR, Golden Visa",
        "corp_tax": 0.21, "pers_tax": 0.48, "rev_mult": 1.6, "margin_delta_pp": 2.5,
        "living_month": 2800.0, "ongoing_month": 700.0, "setup_once": 15000.0,
        "currency": "EUR", "inflation": 3.2, "market_growth": 3.8, "ease_business": 7.4,
        "tax_treaties": 75, "banking_score": 7.9, "legal_system": "Civil Law",
        "risk_factor": 0.7, "partnership_score": 80,
        "market_insights": {
            "startup_founder": "🚀 Growing tech hub with NHR tax benefits for 10 years",
            "crypto_entrepreneur": "₿ Friendly crypto regulations with tax optimization",
            "consulting_expert": "💼 Gateway to European and Lusophone markets",
            "saas_founder": "💻 Affordable tech talent with high quality of life",
            "real_estate": "🏠 Golden visa program with attractive yields"
        }
    },
    "Netherlands": {
        "flag": "🇳🇱", "language": "Dutch, English", "visa": "30% Ruling",
        "corp_tax": 0.25, "pers_tax": 0.49, "rev_mult": 1.7, "margin_delta_pp": 3.0,
        "living_month": 4500.0, "ongoing_month": 1200.0, "setup_once": 22000.0,
        "currency": "EUR", "inflation": 2.9, "market_growth": 4.2, "ease_business": 8.6,
        "tax_treaties": 90, "banking_score": 9.3, "legal_system": "Civil Law",
        "risk_factor": 0.8, "partnership_score": 85,
        "market_insights": {
            "startup_founder": "🚀 Innovation hub with 30% ruling tax benefit",
            "crypto_entrepreneur": "₿ Balanced regulatory approach to crypto",
            "consulting_expert": "💼 Gateway to European corporate market",
            "saas_founder": "💻 Highly digitized market with English proficiency",
            "real_estate": "🏠 Stable market with international appeal"
        }
    },
}

SEASONALITY_FACTORS = {
    "UAE (Dubai)": [1.0, 0.9, 0.9, 0.8, 0.7, 0.6, 0.5, 0.6, 0.8, 1.0, 1.1, 1.2],
    "Singapore": [0.9, 0.8, 0.9, 1.0, 1.0, 1.1, 1.1, 1.2, 1.1, 1.0, 1.0, 1.1],
    "UK": [1.1, 1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.1, 1.2, 1.3, 1.4],
    "Estonia": [1.2, 1.1, 1.0, 0.9, 0.9, 0.9, 0.9, 1.0, 1.1, 1.1, 1.2, 1.3],
    "Portugal": [1.0, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.3, 1.1, 1.0, 0.9, 1.0],
    "Netherlands": [1.1, 1.0, 1.1, 1.1, 1.2, 1.2, 1.1, 1.0, 1.1, 1.2, 1.2, 1.3]
}

TESTIMONIALS = [
    {"name": "Alex R.", "profile": "Startup Founder", "text": "VisaTier gave me the confidence to make the leap. The ROI analysis was spot-on and helped me choose the right country."},
    {"name": "Maria K.", "profile": "Crypto Entrepreneur", "text": "The detailed tax analysis was a game-changer. I saved thousands by choosing a country with a clear crypto framework. Highly recommend!"},
    {"name": "Tom W.", "profile": "SaaS Founder", "text": "I used VisaTier to compare talent pools and market access. The insights were invaluable and led me to the perfect location for my business expansion."},
]

# --- FINANCIAL MODELING ---
def calculate_financials(
    current_rev, current_margin, current_corp_tax, current_pers_tax, current_living,
    current_ongoing, reloc_dest, reloc_rev_mult, reloc_margin_delta,
    analysis_horizon, discount_rate, profile_id
):
    try:
        current_rev = float(current_rev)
        current_margin = float(current_margin) / 100
        current_corp_tax = float(current_corp_tax) / 100
        current_pers_tax = float(current_pers_tax) / 100
        current_living = float(current_living)
        current_ongoing = float(current_ongoing)
        analysis_horizon = int(analysis_horizon)
        discount_rate = float(discount_rate) / 100

        profile_data = USER_PROFILES.get(profile_id, {})
        success_multiplier = profile_data.get("success_multiplier", 1.0)
        
        dest_config = COUNTRY_CONFIG_ENHANCED.get(reloc_dest, {})
        reloc_corp_tax = dest_config.get("corp_tax", 0.0)
        reloc_pers_tax = dest_config.get("pers_tax", 0.0)
        reloc_setup_once = dest_config.get("setup_once", 0.0)
        reloc_ongoing_month = dest_config.get("ongoing_month", 0.0)
        reloc_living_month = dest_config.get("living_month", 0.0)
        
        df_months = pd.DataFrame(index=range(analysis_horizon))
        
        # --- "Current Situation" Model ---
        inflation_rate = 0.03 / 12  # Simple monthly inflation
        df_months['inflation_factor'] = [(1 + inflation_rate)**i for i in range(analysis_horizon)]
        
        df_months['Current_Revenue'] = current_rev * df_months['inflation_factor']
        df_months['Current_Profit'] = df_months['Current_Revenue'] * current_margin
        df_months['Current_Corp_Tax_Cost'] = df_months['Current_Profit'] * current_corp_tax
        df_months['Current_Net_Profit'] = df_months['Current_Profit'] - df_months['Current_Corp_Tax_Cost']
        df_months['Current_Personal_Tax_Cost'] = df_months['Current_Net_Profit'] * current_pers_tax
        df_months['Current_Total_Taxes'] = df_months['Current_Corp_Tax_Cost'] + df_months['Current_Personal_Tax_Cost']
        df_months['Current_Living_Cost'] = current_living * df_months['inflation_factor']
        df_months['Current_Ongoing_Cost'] = current_ongoing * df_months['inflation_factor']
        df_months['Current_Cash_Flow'] = df_months['Current_Net_Profit'] - df_months['Current_Personal_Tax_Cost'] - (df_months['Current_Living_Cost'] + df_months['Current_Ongoing_Cost'])

        # --- "Post-Relocation" Model ---
        df_months['Reloc_Revenue_Base'] = current_rev * reloc_rev_mult * success_multiplier
        df_months['Reloc_Revenue'] = [
            df_months.loc[i, 'Reloc_Revenue_Base'] * (min(1.0, (i + 1) / 12.0)) * SEASONALITY_FACTORS.get(reloc_dest, [1.0] * 12)[i % 12]
            for i in range(analysis_horizon)
        ]
        df_months['Reloc_Profit'] = df_months['Reloc_Revenue'] * (current_margin + reloc_margin_delta)
        df_months['Reloc_Corp_Tax_Cost'] = df_months['Reloc_Profit'] * reloc_corp_tax
        df_months['Reloc_Net_Profit'] = df_months['Reloc_Profit'] - df_months['Reloc_Corp_Tax_Cost']
        df_months['Reloc_Personal_Tax_Cost'] = df_months['Reloc_Net_Profit'] * reloc_pers_tax
        df_months['Reloc_Total_Taxes'] = df_months['Reloc_Corp_Tax_Cost'] + df_months['Reloc_Personal_Tax_Cost']
        df_months['Reloc_Living_Cost'] = reloc_living_month * df_months['inflation_factor']
        df_months['Reloc_Ongoing_Cost'] = reloc_ongoing_month * df_months['inflation_factor']
        df_months['Reloc_Cash_Flow'] = df_months['Reloc_Net_Profit'] - df_months['Reloc_Personal_Tax_Cost'] - (df_months['Reloc_Living_Cost'] + df_months['Reloc_Ongoing_Cost'])

        # --- ROI and Payback Period Calculations ---
        df_months['Cash_Flow_Difference'] = df_months['Reloc_Cash_Flow'] - df_months['Current_Cash_Flow']
        df_months.loc[0, 'Cash_Flow_Difference'] -= reloc_setup_once
        
        df_months['Cumulative_Cash_Flow'] = df_months['Cash_Flow_Difference'].cumsum()
        
        payback_period_months = df_months['Cumulative_Cash_Flow'][df_months['Cumulative_Cash_Flow'] > 0].index.min()
        payback_period_years = payback_period_months / 12 if pd.notna(payback_period_months) else float('inf')

        initial_investment = reloc_setup_once
        total_benefit = df_months['Cumulative_Cash_Flow'].iloc[-1] + initial_investment
        roi = (total_benefit / initial_investment) * 100 if initial_investment > 0 else float('inf')

        # Risk-adjusted NPV
        df_months['Discount_Factor'] = [1 / (1 + discount_rate/12)**i for i in range(analysis_horizon)]
        df_months['NPV_Difference'] = df_months['Cash_Flow_Difference'] * df_months['Discount_Factor']
        
        risk_factor = dest_config.get("risk_factor", 0.8)
        risk_adjusted_npv = df_months['NPV_Difference'].sum() * risk_factor
        
        taxes_saved_1y = df_months['Current_Total_Taxes'].head(12).sum() - df_months['Reloc_Total_Taxes'].head(12).sum()
        net_profit_increase = df_months['Reloc_Net_Profit'].sum() - df_months['Current_Net_Profit'].sum()
        
        return {
            "roi": roi,
            "payback_years": payback_period_years,
            "taxes_saved_1y": taxes_saved_1y,
            "net_profit_increase": net_profit_increase,
            "risk_adjusted_npv": risk_adjusted_npv,
            "cash_flow_data": {
                "difference": df_months['Cash_Flow_Difference'].tolist(),
                "cumulative": df_months['Cumulative_Cash_Flow'].tolist()
            },
            "dest_config": dest_config
        }

    except Exception as e:
        print(f"Error during calculation: {e}")
        return {
            "roi": 0, "payback_years": float('inf'), "taxes_saved_1y": 0,
            "net_profit_increase": 0, "risk_adjusted_npv": 0,
            "cash_flow_data": {"difference": [], "cumulative": []},
            "dest_config": {}
        }

# --- VISUALIZATIONS ---
def create_roi_gauge(roi_value, profile_id):
    """Create an ROI gauge with color indicators based on profile theme"""
    roi_value = max(0, min(500, roi_value))
    profile_color = USER_PROFILES.get(profile_id, {}).get("color", "#2563EB")
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=roi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "5-Year ROI (%)", 'font': {'size': 24}},
        delta={'reference': 100, 'increasing': {'color': profile_color}},
        gauge={
            'axis': {'range': [0, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': profile_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 100], 'color': '#EF4444'},
                {'range': [100, 200], 'color': '#F59E0B'},
                {'range': [200, 500], 'color': '#10B981'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_financial_dashboard(cash_flow_data, horizon, reloc_dest, roi, risk_npv):
    """Generates a 4-panel dashboard of financial metrics."""
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=(
                            "Monthly Cash Flow Difference", "Cumulative Cash Flow",
                            "ROI vs. Risk", "Profitability & Taxes"
                        ),
                        horizontal_spacing=0.1, vertical_spacing=0.2)
    
    # Chart 1: Monthly Cash Flow
    if cash_flow_data.get("difference"):
        months = list(range(1, horizon + 1))
        fig.add_trace(go.Bar(x=months, y=cash_flow_data['difference'],
                             name='Monthly Delta', marker_color=['green' if x > 0 else 'red' for x in cash_flow_data['difference']]),
                      row=1, col=1)
    
    # Chart 2: Cumulative Cash Flow
    if cash_flow_data.get("cumulative"):
        months = list(range(1, horizon + 1))
        fig.add_trace(go.Scatter(x=months, y=cash_flow_data['cumulative'],
                                 name='Cumulative Delta', mode='lines+markers', line=dict(color='blue')),
                      row=1, col=2)
    
    # Chart 3: Risk vs. Return Scatter Plot
    countries = list(COUNTRY_CONFIG_ENHANCED.keys())
    risk_scores = [COUNTRY_CONFIG_ENHANCED[c]["risk_factor"] for c in countries]
    roic_values = [calculate_financials(30000, 25, 20, 10, 4000, 500, c, 3.0, 5.0, 60, 10, "startup_founder")['roi'] for c in countries]
    
    selected_index = countries.index(reloc_dest)
    colors = ['#2563EB'] * len(countries)
    colors[selected_index] = '#EF4444'
    
    fig.add_trace(go.Scatter(x=risk_scores, y=roic_values, mode='markers+text',
                             marker=dict(size=12, color=colors, line=dict(width=2, color='DarkSlateGrey')),
                             text=countries, textposition='bottom center',
                             name='Country Comparison'),
                  row=2, col=1)
    
    fig.update_xaxes(title_text="Risk Factor", row=2, col=1)
    fig.update_yaxes(title_text="5-Year ROI (%)", row=2, col=1)
    
    # Chart 4: Profitability & Taxes
    # This is a placeholder, a more complex graph could be integrated here
    data_labels = ['Total Revenue', 'Net Profit', 'Taxes Paid']
    
    current_values = [
        calculate_financials(30000, 25, 20, 10, 4000, 500, reloc_dest, 3.0, 5.0, 60, 10, "startup_founder")['Current_Revenue'].sum(),
        calculate_financials(30000, 25, 20, 10, 4000, 500, reloc_dest, 3.0, 5.0, 60, 10, "startup_founder")['Current_Net_Profit'].sum(),
        calculate_financials(30000, 25, 20, 10, 4000, 500, reloc_dest, 3.0, 5.0, 60, 10, "startup_founder")['Current_Total_Taxes'].sum()
    ]
    
    reloc_values = [
        calculate_financials(30000, 25, 20, 10, 4000, 500, reloc_dest, 3.0, 5.0, 60, 10, "startup_founder")['Reloc_Revenue'].sum(),
        calculate_financials(30000, 25, 20, 10, 4000, 500, reloc_dest, 3.0, 5.0, 60, 10, "startup_founder")['Reloc_Net_Profit'].sum(),
        calculate_financials(30000, 25, 20, 10, 4000, 500, reloc_dest, 3.0, 5.0, 60, 10, "startup_founder")['Reloc_Total_Taxes'].sum()
    ]

    fig.add_trace(go.Bar(x=data_labels, y=current_values, name='Current', marker_color='#64748B'), row=2, col=2)
    fig.add_trace(go.Bar(x=data_labels, y=reloc_values, name='Post-Relocation', marker_color='#10B981'), row=2, col=2)
    
    fig.update_layout(height=800, title_text="Detailed Financial Dashboard")
    return fig

TIMELINE_DATA = {
    "UAE (Dubai)": [{"name": "Company Setup", "duration": 30}, {"name": "Visa Processing", "duration": 20}],
    "Singapore": [{"name": "ACRA Registration", "duration": 14}, {"name": "Employment Pass", "duration": 28}],
    "UK": [{"name": "Company Formation", "duration": 10}, {"name": "Visa Processing", "duration": 60}],
    "Estonia": [{"name": "e-Residency", "duration": 21}, {"name": "Company Registration", "duration": 1}],
    "Portugal": [{"name": "Company Formation", "duration": 30}, {"name": "Visa/Residence Permit", "duration": 90}],
    "Netherlands": [{"name": "Company Registration", "duration": 14}, {"name": "30% Ruling", "duration": 60}]
}

def create_timeline_visualization(dest):
    country_stages = TIMELINE_DATA.get(dest, [])
    if not country_stages: return go.Figure()
    
    stages_df = pd.DataFrame(country_stages)
    stages_df['end_date'] = stages_df['duration'].cumsum()
    stages_df['start_date'] = stages_df['end_date'].shift(1).fillna(0)
    stages_df['text'] = stages_df['name'] + ' (' + stages_df['duration'].astype(str) + ' days)'
    
    fig = px.timeline(stages_df, x_start="start_date", x_end="end_date", y="name",
                      text="duration", color="name",
                      title=f"Estimated Relocation Timeline to {dest}")
    fig.update_yaxes(categoryorder="total ascending")
    fig.update_traces(texttemplate='%{text} days', textposition='inside')
    fig.update_layout(showlegend=False, height=400,
                      xaxis_title="Days from Start",
                      yaxis_title="Process Stage")
    return fig

def create_country_comparison_chart(selected_country):
    countries = list(COUNTRY_CONFIG_ENHANCED.keys())
    metrics = {
        "Corporate Tax Rate (%)": [c["corp_tax"] * 100 for c in COUNTRY_CONFIG_ENHANCED.values()],
        "Ease of Doing Business": [c["ease_business"] for c in COUNTRY_CONFIG_ENHANCED.values()],
        "Setup Cost (€)": [c["setup_once"] for c in COUNTRY_CONFIG_ENHANCED.values()],
        "Living Cost (€/month)": [c["living_month"] for c in COUNTRY_CONFIG_ENHANCED.values()]
    }
    
    fig = make_subplots(rows=2, cols=2, subplot_titles=list(metrics.keys()),
                        vertical_spacing=0.2, horizontal_spacing=0.1)
    
    for i, (metric_name, metric_values) in enumerate(metrics.items()):
        row = (i // 2) + 1
        col = (i % 2) + 1
        colors = ['#2563EB' if c == selected_country else '#64748B' for c in countries]
        
        fig.add_trace(go.Bar(x=countries, y=metric_values, name=metric_name, marker_color=colors), row=row, col=col)
        fig.update_yaxes(title_text=metric_name, row=row, col=col)
        fig.update_xaxes(showgrid=False, row=row, col=col)
        
    fig.update_layout(title_text=f"Comparison of Key Business Metrics", showlegend=False, height=700)
    return fig

# --- LOGIC & HELPERS ---
def calculate_match_score(profile_id, country_id):
    profile_weights = PROFILE_WEIGHTS.get(profile_id, {})
    country_metrics = COUNTRY_CONFIG_ENHANCED.get(country_id, {})
    
    if not profile_weights or not country_metrics:
        return 0
    
    score = 0
    # Example scoring logic, can be refined
    score += profile_weights.get("tax", 0) * (100 - (country_metrics.get("corp_tax", 0) * 100))
    score += profile_weights.get("cost", 0) * (100 - (country_metrics.get("living_month", 0) / 100))
    score += profile_weights.get("growth", 0) * country_metrics.get("market_growth", 0)
    score += profile_weights.get("ease", 0) * country_metrics.get("ease_business", 0) * 10
    score += profile_weights.get("banking", 0) * country_metrics.get("banking_score", 0) * 10
    score += profile_weights.get("partnership", 0) * country_metrics.get("partnership_score", 0)
    
    return min(100, max(0, int(score / 10)))

def get_insights(roi_value, taxes_saved, reloc_dest, user_profile_name):
    dest_config = COUNTRY_CONFIG_ENHANCED.get(reloc_dest, {})
    insight_text = ""
    if roi_value > 200:
        insight_text = f"**Exceptional ROI!** Your projected 5-year ROI is **{roi_value:.1f}%**. This indicates an outstanding opportunity to relocate your business to {reloc_dest}."
    elif roi_value > 100:
        insight_text = f"**Great ROI.** Your projected 5-year ROI is **{roi_value:.1f}%**. Relocating to {reloc_dest} is a solid strategic move for your business."
    else:
        insight_text = f"**Moderate Potential.** Your projected 5-year ROI is **{roi_value:.1f}%**. While there is a positive return, it's crucial to optimize your relocation strategy."
    market_insight = dest_config.get("market_insights", {}).get(user_profile_name, "")
    if market_insight:
        insight_text += f"\n\n**Market Insight for your profile ({user_profile_name}):** {market_insight}"
    return insight_text

def update_ui_from_profile(profile_id):
    """
    Updates the UI input fields based on the selected user profile.
    This no longer attempts to update CSS.
    """
    profile_data = USER_PROFILES.get(profile_id, {})
    if profile_data:
        return (
            profile_id,
            profile_data.get("typical_revenue"),
            profile_data.get("typical_margin"),
        )
    return gr.update(value=None), gr.update(value=None), gr.update(value=None)


def generate_referral_code(email):
    if not email: return "Not available"
    return hashlib.sha1(email.encode('utf-8')).hexdigest()[:8].upper()

def run_calculations(
    profile_state, current_rev, current_margin, current_corp_tax, current_pers_tax,
    current_living, current_ongoing, reloc_dest, reloc_rev_mult, reloc_margin_delta,
    analysis_horizon, discount_rate
):
    results = calculate_financials(
        current_rev, current_margin, current_corp_tax, current_pers_tax, current_living,
        current_ongoing, reloc_dest, reloc_rev_mult, reloc_margin_delta,
        analysis_horizon, discount_rate, profile_state
    )
    roi = results.get("roi", 0)
    payback_years = results.get("payback_years", float('inf'))
    taxes_saved_1y = results.get("taxes_saved_1y", 0)
    net_profit_increase = results.get("net_profit_increase", 0)
    risk_adjusted_npv = results.get("risk_adjusted_npv", 0)
    
    roi_gauge = create_roi_gauge(roi, profile_state)
    dashboard_chart = create_financial_dashboard(results.get("cash_flow_data", {}), analysis_horizon, reloc_dest, roi, risk_adjusted_npv)
    timeline_chart = create_timeline_visualization(reloc_dest)
    comparison_chart = create_country_comparison_chart(reloc_dest)
    insight_text = get_insights(roi, taxes_saved_1y, reloc_dest, USER_PROFILES[profile_state]['name'])
    
    roi_class = "exceptional" if roi > 200 else ("good" if roi > 100 else "moderate")
    taxes_class = "exceptional" if taxes_saved_1y > 10000 else ("good" if taxes_saved_1y > 0 else "error")
    payback_class = "exceptional" if payback_years < 2 else ("good" if payback_years < 4 else "moderate")
    payback_text = f"{payback_years:.1f} years" if math.isfinite(payback_years) else "Never"
    
    match_score = calculate_match_score(profile_state, reloc_dest)
    
    # Return updated components and show lead capture modal
    return (
        gr.update(visible=True), # Show modal
        gr.update(value=roi_gauge),
        gr.update(value=f"{roi:.1f}%", elem_classes=[roi_class]),
        gr.update(value=f"€{taxes_saved_1y:,.0f}", elem_classes=[taxes_class]),
        gr.update(value=payback_text, elem_classes=[payback_class]),
        gr.update(value=f"€{net_profit_increase:,.0f}"),
        gr.update(value=f"€{risk_adjusted_npv:,.0f}"),
        gr.update(value=dashboard_chart),
        gr.update(value=timeline_chart),
        gr.update(value=comparison_chart),
        gr.update(value=insight_text),
        gr.update(value=f"<h4 class='flag'>{COUNTRY_CONFIG_ENHANCED[reloc_dest]['flag']}</h4><p>Language: {COUNTRY_CONFIG_ENHANCED[reloc_dest]['language']}</p><p>Key Visa: {COUNTRY_CONFIG_ENHANCED[reloc_dest]['visa']}</p><p>Match Score: <span class='score'>{match_score}%</span></p>", visible=True),
        gr.update(value=f"### Ready for the next step? Get your personalized relocation guide for {reloc_dest}!"),
    )

def clear_results():
    return (
        gr.update(visible=False), # Hide modal
        gr.update(value=create_roi_gauge(0, "startup_founder")),
        gr.update(value="—"), gr.update(value="—"), gr.update(value="—"), gr.update(value="—"), gr.update(value="—"),
        gr.update(value=gr.Plot()), gr.update(value=gr.Plot()), gr.update(value=gr.Plot()),
        gr.update(value=""),
        gr.update(visible=False), gr.update(visible=False)
    )

def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        referral_code = generate_referral_code(email)
        return gr.update(visible=False), gr.update(value=f"Thank you! Your referral code is: `{referral_code}`", visible=True)
    else:
        return gr.update(visible=True), gr.update(value="Please enter a valid email address.", visible=True)

def update_button_styles(selected_profile):
    """Dynamically updates the CSS classes of all profile buttons."""
    updates = []
    for profile_id in USER_PROFILES.keys():
        if profile_id == selected_profile:
            updates.append(gr.update(elem_classes=["profile-card", "selected"]))
        else:
            updates.append(gr.update(elem_classes=["profile-card"]))
    return updates

# --- GRADIO INTERFACE ---
with gr.Blocks(theme=THEME, css=CSS) as demo:
    email_state = gr.State("")
    
    with gr.Row(elem_classes="vt-header"):
        gr.HTML("""<div class="title">VisaTier: Immigration ROI Simulator</div>""")
        with gr.Column(elem_classes="nav-links", scale=0):
            gr.HTML("""<a href="#">Pricing</a> <a href="#">About</a> <a href="#">Contact</a>""")
    
    with gr.Column(elem_classes="lead-capture-overlay", visible=False) as lead_capture_modal:
        with gr.Box(elem_classes="lead-capture-modal"):
            gr.Markdown("### 👋 One more step!")
            gr.Markdown("Please enter your email to get your personalized report and unlock all features.")
            email_input = gr.Textbox(label="Email Address")
            email_error = gr.Markdown("", visible=False)
            submit_button = gr.Button("Get Report & Insights", elem_classes="cta-button")
            
    gr.Markdown("## **Step 1: Choose Your Profile**")
    profile_selector_row = gr.Row(elem_classes="profile-selector")
    
    # Store buttons in a list to use in the update function
    profile_buttons = []
    with profile_selector_row:
        for profile_id, profile_data in USER_PROFILES.items():
            button_classes = ["profile-card", "selected"] if profile_id == "startup_founder" else ["profile-card"]
            btn = gr.Button(f"{profile_data['icon']} {profile_data['name']}",
                          elem_id=f"profile_{profile_id}",
                          elem_classes=button_classes,
                          scale=1)
            profile_buttons.append(btn)
    profile_state = gr.State("startup_founder")

    gr.Markdown("## **Step 2: Your Current Business Situation**")
    with gr.Column(elem_classes="vt-card"):
        with gr.Row():
            with gr.Column(min_width=300):
                current_rev = gr.Slider(
                    label="💰 Monthly Revenue (€)", value=15000, minimum=100, maximum=500000,
                    step=1000, info="Your current monthly business revenue."
                )
                current_margin = gr.Slider(
                    label="📈 EBITDA Margin (%)", value=20, minimum=0, maximum=70, step=1,
                    info="Your profit before taxes and depreciation."
                )
            with gr.Column(min_width=300):
                current_corp_tax = gr.Slider(
                    label="🏛️ Corporate Tax (%)", value=20, minimum=0, maximum=50, step=1,
                    info="Your current corporate tax rate."
                )
                current_pers_tax = gr.Slider(
                    label="🧍 Personal Tax (%)", value=10, minimum=0, maximum=50, step=1,
                    info="Your personal tax rate on dividends or salary."
                )
        with gr.Row():
            with gr.Column(min_width=300):
                current_living = gr.Slider(
                    label="🏠 Living Costs (€/month)", value=4000, minimum=500, maximum=20000,
                    step=100, info="Your monthly personal living expenses."
                )
            with gr.Column(min_width=300):
                current_ongoing = gr.Slider(
                    label="💼 Business Operating Costs (€/month)", value=500, minimum=100, maximum=10000,
                    step=100, info="Other monthly business expenses."
                )
    
    gr.Markdown("## **Step 3: Choose Your Dream Destination**")
    with gr.Column(elem_classes="vt-card"):
        with gr.Row():
            with gr.Column(min_width=300):
                reloc_dest = gr.Dropdown(
                    label="🌍 Choose a Country",
                    choices=list(COUNTRY_CONFIG_ENHANCED.keys()),
                    value="UAE (Dubai)",
                    info="Where do you want to relocate?"
                )
            with gr.Column(min_width=300):
                reloc_rev_mult = gr.Slider(
                    label="🚀 Revenue Growth Multiplier (x)", value=3.0, minimum=0.5, maximum=5.0, step=0.1,
                    info="How much do you expect your revenue to grow after relocation? (e.g., 2.0x)"
                )
                reloc_margin_delta = gr.Slider(
                    label="🎯 Margin Increase (pp)", value=5.0, minimum=0, maximum=20, step=0.1,
                    info="By how many percentage points will your margin increase?"
                )
    
    gr.Markdown("## **Step 4: Advanced Parameters**")
    with gr.Column(elem_classes="vt-card"):
        with gr.Row():
            analysis_horizon = gr.Slider(
                label="⏳ Analysis Horizon (months)", value=60, minimum=12, maximum=120, step=12,
                info="How many months do you want to project?"
            )
            discount_rate = gr.Slider(
                label="📉 Annual Discount Rate (%)", value=10, minimum=0, maximum=30, step=1,
                info="Rate to calculate the present value of future cash flows."
            )

    gr.Markdown("---")
    
    calculate_button = gr.Button("💰 Calculate My ROI", elem_classes="cta-button")
    
    gr.Markdown("## **Calculation Results**")
    
    with gr.Column(elem_classes="vt-card"):
        with gr.Row(elem_classes="kpi-grid"):
            with gr.Column(elem_classes="kpi-card"):
                gr.Markdown("<p class='label'>🚀 5-Year ROI</p>")
                roi_value = gr.Markdown("<p class='value'>—</p>", elem_classes="moderate")
                gr.Markdown("<p class='vt-note'>Projected return on investment over 5 years.</p>")
            with gr.Column(elem_classes="kpi-card"):
                gr.Markdown("<p class='label'>💸 Taxes Saved (1 year)</p>")
                taxes_saved_1y = gr.Markdown("<p class='value'>—</p>", elem_classes="moderate")
                gr.Markdown("<p class='vt-note'>Projected tax savings in the first year.</p>")
            with gr.Column(elem_classes="kpi-card"):
                gr.Markdown("<p class='label'>🔄 Payback Period</p>")
                payback_period = gr.Markdown("<p class='value'>—</p>", elem_classes="moderate")
                gr.Markdown("<p class='vt-note'>Time required to recoup the initial investment.</p>")
            with gr.Column(elem_classes="kpi-card"):
                gr.Markdown("<p class='label'>💰 Net Profit Growth (5 years)</p>")
                net_profit_increase = gr.Markdown("<p class='value'>—</p>", elem_classes="moderate")
                gr.Markdown("<p class='vt-note'>Total increase in net profit.</p>")
            with gr.Column(elem_classes="kpi-card"):
                gr.Markdown("<p class='label'>🏦 Risk-Adjusted NPV</p>")
                risk_adjusted_npv_val = gr.Markdown("<p class='value'>—</p>", elem_classes="moderate")
                gr.Markdown("<p class='vt-note'>Value of future cash flows considering risk.</p>")

        with gr.Row():
            with gr.Column():
                roi_gauge = gr.Plot(create_roi_gauge(0, "startup_founder"))
            with gr.Column(scale=2, min_width=300):
                country_card_info = gr.Markdown(visible=False, elem_classes="country-card")
                insight_card = gr.Markdown(
                    """<div class='insight-card'><p>💡 **Insight**</p><p>Fill in your business data and click 'Calculate My ROI' to get a personalized analysis.</p></div>"""
                )
    
    with gr.Tabs() as tabs:
        with gr.TabItem("📊 Detailed ROI Analysis"):
            dashboard_chart = gr.Plot()
        with gr.TabItem("🌍 Country Comparison"):
            comparison_chart = gr.Plot()
        with gr.TabItem("📅 Implementation Plan"):
            timeline_chart = gr.Plot()
    
    with gr.Column(elem_classes="viral-share-section"):
        gr.Markdown("### 🤝 Refer a Friend and Share Your Success!")
        gr.Markdown("Share your personalized ROI results with a unique link. When your friends sign up, you get rewards!", elem_classes="vt-note")
        referral_code_text = gr.Textbox(label="Your Referral Code", interactive=False)
        with gr.Row(elem_classes="share-buttons"):
            gr.Button("Share on LinkedIn", elem_classes="share-button share-linkedin")
            gr.Button("Share on Twitter", elem_classes="share-button share-twitter")
            gr.Button("Share on WhatsApp", elem_classes="share-button share-whatsapp")
    
    with gr.Column(elem_classes="testimonial-slider"):
        gr.Markdown("### What Our Users Say")
        gr.Markdown(""""VisaTier helped me choose the perfect country for my startup. The ROI analysis was incredibly accurate!""" - Alex R., Startup Founder")
    
    gr.HTML("""
        <div class="vt-footer">
            <p>&copy; 2024 VisaTier. All Rights Reserved.</p>
            <div class="footer-links">
                <a href="#">Privacy Policy</a> |
                <a href="#">Terms of Service</a> |
                <a href="#">Contact Us</a>
            </div>
        </div>
        """)

    # --- Event Binding ---
    inputs = [
        profile_state, current_rev, current_margin, current_corp_tax, current_pers_tax,
        current_living, current_ongoing, reloc_dest, reloc_rev_mult, reloc_margin_delta,
        analysis_horizon, discount_rate
    ]
    outputs = [
        lead_capture_modal, roi_gauge, roi_value, taxes_saved_1y, payback_period, net_profit_increase,
        risk_adjusted_npv_val, dashboard_chart, timeline_chart, comparison_chart, insight_card,
        country_card_info, referral_code_text
    ]
    
    for profile_id, btn in zip(USER_PROFILES.keys(), profile_buttons):
        # Update button classes and UI values
        btn.click(
            fn=update_button_styles,
            inputs=gr.State(profile_id),
            outputs=profile_buttons
        ).then(
            fn=update_ui_from_profile,
            inputs=gr.State(profile_id),
            outputs=[profile_state, current_rev, current_margin]
        )
    
    calculate_button.click(
        fn=run_calculations,
        inputs=inputs,
        outputs=outputs
    )
    
    submit_button.click(
        fn=validate_email,
        inputs=email_input,
        outputs=[lead_capture_modal, referral_code_text]
    )

demo.launch()
