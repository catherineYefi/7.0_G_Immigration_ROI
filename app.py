# VisaTier 4.0 - World-Class UX/UI Immigration ROI Calculator (FIXED)
# Исправлены критические ошибки интерфейса и логики

import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from dataclasses import dataclass
from typing import Dict, List

# =========================
# WORLD-CLASS DESIGN SYSTEM (Оптимизирован)
# =========================

WORLD_CLASS_CSS = """
/* Design System inspired by Apple, Stripe, Linear, Figma */
:root {
    /* Color Palette - Inspired by Apple's Human Interface Guidelines */
    --primary: #007AFF;
    --primary-light: #4DA6FF;
    --primary-dark: #0056CC;
    --secondary: #5856D6;
    --success: #34C759;
    --warning: #FF9F0A;
    --error: #FF3B30;
    --neutral-50: #FAFAFA;
    --neutral-100: #F5F5F7;
    --neutral-200: #E8E8ED;
    --neutral-300: #D2D2D7;
    --neutral-400: #98989D;
    --neutral-500: #636366;
    --neutral-600: #48484A;
    --neutral-700: #3A3A3C;
    --neutral-800: #2C2C2E;
    --neutral-900: #1C1C1E;
    
    /* Typography Scale */
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 1.875rem;
    --font-size-4xl: 2.25rem;
    --font-size-5xl: 3rem;
    
    /* Spacing Scale */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;
    --space-12: 3rem;
    --space-16: 4rem;
    --space-20: 5rem;
    
    /* Border Radius */
    --radius-sm: 0.375rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-2xl: 1.5rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    
    /* Transitions */
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reset and Base Styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif !important;
    background: linear-gradient(135deg, var(--neutral-50) 0%, var(--neutral-100) 100%) !important;
    min-height: 100vh;
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: var(--space-6) !important;
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    border-radius: var(--radius-2xl);
    padding: var(--space-20) var(--space-8);
    margin-bottom: var(--space-12);
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.hero-content {
    position: relative;
    z-index: 2;
    color: white;
}

.hero-title {
    font-size: var(--font-size-5xl);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: var(--space-4);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
    font-size: var(--font-size-xl);
    font-weight: 400;
    opacity: 0.9;
    margin-bottom: var(--space-8);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
}

.hero-stats {
    display: inline-flex;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--radius-xl);
    padding: var(--space-4) var(--space-6);
    color: var(--neutral-700);
    font-weight: 600;
    font-size: var(--font-size-sm);
}

/* Profile Selection */
.profile-section {
    margin-bottom: var(--space-12);
}

.section-title {
    font-size: var(--font-size-2xl);
    font-weight: 600;
    color: var(--neutral-800);
    margin-bottom: var(--space-2);
    text-align: center;
}

.section-subtitle {
    font-size: var(--font-size-base);
    color: var(--neutral-500);
    text-align: center;
    margin-bottom: var(--space-8);
}

.profile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: var(--space-4);
    margin-bottom: var(--space-8);
}

.profile-card {
    background: white;
    border: 2px solid var(--neutral-200);
    border-radius: var(--radius-xl);
    padding: var(--space-6);
    cursor: pointer;
    transition: all var(--transition-base);
    position: relative;
    overflow: hidden;
    text-align: center;
}

.profile-card:hover {
    border-color: var(--primary-light);
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.profile-card.selected {
    border-color: var(--primary);
    background: linear-gradient(135deg, rgba(0, 122, 255, 0.05) 0%, rgba(88, 86, 214, 0.05) 100%);
    box-shadow: var(--shadow-md);
}

.profile-card.selected::after {
    content: '✓';
    position: absolute;
    top: var(--space-4);
    right: var(--space-4);
    background: var(--primary);
    color: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--font-size-sm);
    font-weight: 600;
}

.profile-icon {
    font-size: var(--font-size-4xl);
    margin-bottom: var(--space-4);
    display: block;
}

.profile-name {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--neutral-800);
    margin-bottom: var(--space-2);
}

.profile-details {
    font-size: var(--font-size-sm);
    color: var(--neutral-500);
    line-height: 1.5;
}

/* Input Section */
.input-section {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--space-8);
    margin-bottom: var(--space-8);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--neutral-200);
}

.input-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-6);
    align-items: end;
}

/* Calculate Button */
.calculate-button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    border: none !important;
    border-radius: var(--radius-xl) !important;
    padding: var(--space-5) var(--space-8) !important;
    font-size: var(--font-size-lg) !important;
    font-weight: 600 !important;
    color: white !important;
    cursor: pointer !important;
    transition: all var(--transition-base) !important;
    width: 100% !important;
    position: relative !important;
    overflow: hidden !important;
}

.calculate-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
}

/* Results Section */
.results-container {
    margin-top: var(--space-12);
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-4);
    margin-bottom: var(--space-8);
}

.kpi-card {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--space-6);
    text-align: center;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--neutral-200);
    position: relative;
    overflow: hidden;
    transition: all var(--transition-base);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.kpi-label {
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--neutral-500);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--space-2);
}

.kpi-value {
    font-size: var(--font-size-3xl);
    font-weight: 700;
    color: var(--neutral-800);
    margin-bottom: var(--space-2);
    line-height: 1;
}

.kpi-note {
    font-size: var(--font-size-xs);
    color: var(--neutral-400);
    line-height: 1.4;
}

.kpi-card.success::before { background: var(--success); }
.kpi-card.success .kpi-value { color: var(--success); }

.kpi-card.warning::before { background: var(--warning); }
.kpi-card.warning .kpi-value { color: var(--warning); }

.kpi-card.error::before { background: var(--error); }
.kpi-card.error .kpi-value { color: var(--error); }

/* Charts Section */
.chart-container {
    background: white;
    border-radius: var(--radius-xl);
    padding: var(--space-6);
    margin-bottom: var(--space-6);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--neutral-200);
}

/* Recommendation Card */
.recommendation-card {
    background: linear-gradient(135deg, rgba(52, 199, 89, 0.1) 0%, rgba(52, 199, 89, 0.05) 100%);
    border: 2px solid rgba(52, 199, 89, 0.2);
    border-radius: var(--radius-xl);
    padding: var(--space-8);
    margin: var(--space-6) 0;
    position: relative;
}

.recommendation-header {
    display: flex;
    align-items: center;
    margin-bottom: var(--space-4);
}

.recommendation-icon {
    font-size: var(--font-size-2xl);
    margin-right: var(--space-3);
}

.recommendation-title {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--neutral-800);
}

.recommendation-content {
    font-size: var(--font-size-base);
    color: var(--neutral-600);
    line-height: 1.6;
    margin-bottom: var(--space-6);
}

/* CTA Section */
.cta-section {
    background: white;
    border: 2px solid var(--primary);
    border-radius: var(--radius-2xl);
    padding: var(--space-8);
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}

.value-badge {
    background: var(--success);
    color: white;
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-xl);
    font-size: var(--font-size-sm);
    font-weight: 600;
    display: inline-block;
    margin-bottom: var(--space-4);
}

.cta-title {
    font-size: var(--font-size-2xl);
    font-weight: 600;
    color: var(--neutral-800);
    margin-bottom: var(--space-3);
}

.cta-description {
    font-size: var(--font-size-base);
    color: var(--neutral-600);
    margin-bottom: var(--space-6);
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}

.price-container {
    margin: var(--space-6) 0;
}

.price-old {
    font-size: var(--font-size-lg);
    color: var(--neutral-400);
    text-decoration: line-through;
    margin-right: var(--space-2);
}

.price-new {
    font-size: var(--font-size-3xl);
    font-weight: 700;
    color: var(--success);
}

.cta-button {
    background: linear-gradient(135deg, var(--success) 0%, #2FB86B 100%) !important;
    border: none !important;
    border-radius: var(--radius-xl) !important;
    padding: var(--space-5) var(--space-10) !important;
    font-size: var(--font-size-lg) !important;
    font-weight: 600 !important;
    color: white !important;
    cursor: pointer !important;
    transition: all var(--transition-base) !important;
    margin: var(--space-4) 0 !important;
}

.cta-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
}

.guarantee-text {
    font-size: var(--font-size-xs);
    color: var(--neutral-400);
    margin-top: var(--space-4);
}

/* Footer */
.footer {
    text-align: center;
    padding: var(--space-12) var(--space-4);
    color: var(--neutral-500);
    font-size: var(--font-size-sm);
    border-top: 1px solid var(--neutral-200);
    margin-top: var(--space-12);
}

.footer a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
}

.footer a:hover {
    text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
    .gradio-container {
        padding: var(--space-4) !important;
    }
    
    .hero-section {
        padding: var(--space-12) var(--space-6);
    }
    
    .hero-title {
        font-size: var(--font-size-3xl);
    }
    
    .hero-subtitle {
        font-size: var(--font-size-lg);
    }
    
    .profile-grid {
        grid-template-columns: 1fr;
        gap: var(--space-3);
    }
    
    .input-row {
        grid-template-columns: 1fr;
        gap: var(--space-4);
    }
    
    .kpi-grid {
        grid-template-columns: 1fr;
    }
}

/* Accessibility Improvements */
*:focus {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}
"""

# =========================
# REFINED DATA MODELS (Улучшенные)
# =========================

@dataclass
class ProfileData:
    id: str
    name: str
    icon: str
    revenue: int
    margin: int
    risk_level: str
    growth_potential: float
    description: str

@dataclass
class CountryData:
    name: str
    flag: str
    corp_tax: float
    pers_tax: float
    living_cost: int
    setup_cost: int
    growth_multiplier: float
    ease_score: float
    key_benefit: str
    why_good: str

# Обновленные профили с реалистичными данными
PROFILES = {
    "startup": ProfileData(
        "startup", "Tech Startup", "🚀", 50000, 20, "High", 2.8,
        "Building the next unicorn with VC funding and global ambitions"
    ),
    "crypto": ProfileData(
        "crypto", "Crypto/Web3", "₿", 80000, 35, "Very High", 3.5,
        "DeFi protocols, NFT marketplaces, and blockchain innovations"
    ),
    "consulting": ProfileData(
        "consulting", "Strategic Consultant", "💼", 30000, 60, "Low", 1.8,
        "High-value advisory services for Fortune 500 companies"
    ),
    "ecommerce": ProfileData(
        "ecommerce", "E-commerce", "🛒", 45000, 15, "Medium", 2.2,
        "Online retail, dropshipping, and digital product sales"
    )
}

# Обновленные данные стран с точными налоговыми ставками
COUNTRIES = {
    "UAE": CountryData(
        "UAE (Dubai)", "🇦🇪", 0.09, 0.00, 8500, 45000, 2.4, 9.4,
        "0% personal tax paradise",
        "Global financial hub with world-class infrastructure and zero personal income tax"
    ),
    "Singapore": CountryData(
        "Singapore", "🇸🇬", 0.17, 0.22, 7200, 38000, 2.1, 9.6,
        "Asian Silicon Valley",
        "Gateway to 650M ASEAN consumers with unmatched government support for startups"
    ),
    "Estonia": CountryData(
        "Estonia", "🇪🇪", 0.20, 0.20, 2800, 8000, 1.8, 9.0,
        "Digital nomad haven",
        "World's first digital society with e-Residency program and crypto-friendly laws"
    ),
    "Portugal": CountryData(
        "Portugal", "🇵🇹", 0.21, 0.48, 2200, 12000, 1.6, 7.8,
        "EU Golden Visa access",
        "NHR tax regime offers massive savings for new residents in beautiful coastal setting"
    )
}

# =========================
# ENHANCED CALCULATOR (Исправленная логика)
# =========================

class WorldClassROICalculator:
    @staticmethod
    def calculate_comprehensive_roi(profile: ProfileData, country: CountryData, 
                                  custom_revenue: float = None, years: int = 5) -> Dict:
        """Исправленный ROI расчет с защитой от деления на ноль"""
        
        monthly_revenue = custom_revenue if custom_revenue and custom_revenue > 0 else profile.revenue
        
        # Текущая ситуация (EU средние)
        current_profit = monthly_revenue * (profile.margin / 100)
        current_after_tax = current_profit * 0.75 * 0.85  # 25% корп + 15% личный
        current_net = max(0, current_after_tax - 4500)  # Защита от отрицательных значений
        
        # Будущая ситуация с релокацией
        new_revenue = monthly_revenue * country.growth_multiplier * profile.growth_potential
        new_margin = min(profile.margin + 12, 75)  # Реалистичное улучшение маржи
        new_profit = new_revenue * (new_margin / 100)
        new_after_tax = new_profit * (1 - country.corp_tax) * (1 - country.pers_tax)
        new_net = max(0, new_after_tax - country.living_cost)
        
        # Ключевые метрики
        monthly_improvement = new_net - current_net
        annual_improvement = monthly_improvement * 12
        total_benefit = annual_improvement * years
        
        # Защита от деления на ноль
        if country.setup_cost > 0 and total_benefit > country.setup_cost:
            roi = ((total_benefit - country.setup_cost) / country.setup_cost) * 100
        else:
            roi = 0
        
        if monthly_improvement > 0:
            payback_months = country.setup_cost / monthly_improvement
        else:
            payback_months = float('inf')
        
        # Risk-adjusted расчеты
        risk_factors = {"Low": 0.95, "Medium": 0.85, "High": 0.75, "Very High": 0.65}
        risk_multiplier = risk_factors.get(profile.risk_level, 0.8)
        conservative_roi = roi * risk_multiplier
        
        # Opportunity cost
        opportunity_cost = (monthly_revenue * 0.12 * years * 12)  # 12% годовая доходность
        net_opportunity_value = total_benefit - opportunity_cost
        
        return {
            "roi": max(0, roi),
            "conservative_roi": max(0, conservative_roi),
            "annual_savings": annual_improvement,
            "monthly_improvement": monthly_improvement,
            "payback_months": min(payback_months, 120),  # Максимум 10 лет для отображения
            "total_benefit": total_benefit,
            "setup_cost": country.setup_cost,
            "success_probability": min(95, country.ease_score * 10),
            "risk_level": profile.risk_level,
            "net_opportunity_value": net_opportunity_value,
            "confidence_score": min(100, (country.ease_score * 5) + (45 if roi > 100 else 25))
        }

# =========================
# WORLD-CLASS VISUALIZATION (Оптимизированная)
# =========================

class EliteChartBuilder:
    @staticmethod
    def create_executive_dashboard(results: Dict, countries: List[str]) -> go.Figure:
        """Исправленная панель управления с улучшенной визуализацией"""
        
        if not results or not countries:
            # Возвращаем пустой график при отсутствии данных
            fig = go.Figure()
            fig.add_annotation(
                text="No data to display",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            return fig
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("ROI Comparison", "Risk vs Return", "Payback Analysis", "Confidence Score"),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "bar"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Подготовка данных с проверкой существования
        rois = []
        paybacks = []
        risks = []
        confidence = []
        
        risk_mapping = {"Low": 20, "Medium": 40, "High": 65, "Very High": 80}
        
        for country in countries:
            if country in results:
                result = results[country]
                rois.append(result.get("conservative_roi", 0))
                paybacks.append(min(result.get("payback_months", 120), 60))
                risks.append(risk_mapping.get(result.get("risk_level", "Medium"), 50))
                confidence.append(result.get("confidence_score", 0))
        
        if not rois:  # Если нет данных, возвращаем пустой график
            fig = go.Figure()
            fig.add_annotation(
                text="No calculation results available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            return fig
        
        # ROI сравнение с цветовым кодированием
        colors = ['#34C759' if r > 150 else '#FF9F0A' if r > 75 else '#FF3B30' for r in rois]
        fig.add_trace(
            go.Bar(x=countries, y=rois, name="Conservative ROI (%)", 
                  marker_color=colors,
                  text=[f"{r:.0f}%" for r in rois],
                  textposition="outside"),
            row=1, col=1
        )
        
        # Risk vs Return scatter
        fig.add_trace(
            go.Scatter(
                x=rois, y=risks,
                mode='markers+text',
                text=countries,
                textposition="top center",
                marker=dict(size=15, color='#007AFF', opacity=0.7),
                name='Risk Profile'
            ),
            row=1, col=2
        )
        
        # Payback анализ
        fig.add_trace(
            go.Bar(x=countries, y=paybacks, name="Payback (months)",
                  marker_color='#5856D6',
                  text=[f"{p:.0f}mo" for p in paybacks],
                  textposition="outside"),
            row=2, col=1
        )
        
        # Confidence scores
        fig.add_trace(
            go.Bar(x=countries, y=confidence, name="Confidence Score",
                  marker_color='#34C759',
                  text=[f"{c:.0f}" for c in confidence],
                  textposition="outside"),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            template="plotly_white",
            font=dict(family="SF Pro Display, -apple-system, sans-serif", size=12),
            title_font_size=16
        )
        
        return fig
    
    @staticmethod
    def create_timeline_visualization(result: Dict, country_name: str) -> go.Figure:
        """Исправленная временная шкала с защитой от ошибок"""
        
        if not result:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for timeline",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            return fig
        
        months = list(range(1, 61))  # 5 лет
        monthly_cf = result.get("monthly_improvement", 0)
        setup_cost = result.get("setup_cost", 0)
        
        # Защита от неверных данных
        if monthly_cf == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="Insufficient data for cash flow projection",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            return fig
        
        cumulative = [-setup_cost]
        
        for month in months:
            cumulative.append(cumulative[-1] + monthly_cf)
        
        fig = go.Figure()
        
        # Break-even линия
        fig.add_hline(
            y=0, 
            line_dash="dash", 
            line_color="#FF3B30", 
            line_width=2,
            annotation_text="Break-even point",
            annotation_position="top right"
        )
        
        # Cumulative cash flow
        fig.add_trace(go.Scatter(
            x=months, 
            y=cumulative[1:],
            mode='lines',
            name='Cash Flow Projection',
            line=dict(color='#007AFF', width=3),
            fill='tonexty' if any(cf > 0 for cf in cumulative[1:]) else None,
            fillcolor='rgba(0, 122, 255, 0.1)'
        ))
        
        # Highlight payback point
        payback_month = result.get("payback_months", float('inf'))
        if payback_month < 60 and payback_month != float('inf'):
            fig.add_vline(
                x=payback_month,
                line_dash="dot",
                line_color="#34C759",
                line_width=2,
                annotation_text=f"Payback: {payback_month:.0f} months"
            )
        
        fig.update_layout(
            title=f"Cash Flow Projection - {country_name}",
            xaxis_title="Months",
            yaxis_title="Cumulative Cash Flow (€)",
            template="plotly_white",
            height=400,
            font=dict(family="SF Pro Display, -apple-system, sans-serif"),
            showlegend=False
        )
        
        return fig

# =========================
# WORLD-CLASS APPLICATION (Исправленное)
# =========================

def create_world_class_app():
    """Создание исправленного приложения мирового класса"""
    
    with gr.Blocks(css=WORLD_CLASS_CSS, title="VisaTier 4.0", theme=gr.themes.Soft()) as app:
        
        # State management (исправленное управление состоянием)
        selected_profile = gr.State("startup")
        
        # Hero Section
        gr.HTML("""
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Immigration ROI Calculator</h1>
                <p class="hero-subtitle">
                    Make data-driven decisions about business relocation with world-class insights
                </p>
                <div class="hero-stats">
                    <strong>2,847 entrepreneurs</strong> optimized their relocations this year
                </div>
            </div>
        </div>
        """)
        
        # Profile Selection Section (исправленная секция выбора профилей)
        with gr.Column(elem_classes=["profile-section"]):
            gr.HTML("""
            <h2 class="section-title">Choose Your Business Profile</h2>
            <p class="section-subtitle">Select the profile that best matches your business model</p>
            """)
            
            # Используем обычный Radio вместо сложного HTML/JS
            profile_selector = gr.Radio(
                choices=[(pid, f"{profile.icon} {profile.name} - €{profile.revenue:,}/month · {profile.margin}% margin") 
                        for pid, profile in PROFILES.items()],
                value="startup",
                label="Business Profile",
                info="Choose the profile that best describes your business"
            )
            
            # Отображение детальной информации о выбранном профиле
            profile_info = gr.HTML()
        
        # Input Section (упрощенная секция ввода)
        with gr.Column(elem_classes=["input-section"]):
            gr.HTML('<h3 class="section-title">Customize Your Analysis</h3>')
            
            with gr.Row(elem_classes=["input-row"]):
                custom_revenue = gr.Number(
                    label="Monthly Revenue (€)",
                    value=None,
                    placeholder="Leave empty for profile default",
                    info="Your current monthly business revenue",
                    minimum=1000,
                    maximum=1000000
                )
                
                target_countries = gr.CheckboxGroup(
                    choices=[(k, f"{v.flag} {v.name}") for k, v in COUNTRIES.items()],
                    value=["UAE", "Singapore", "Estonia"],
                    label="Countries to Compare",
                    info="Select up to 4 countries for comparison"
                )
            
            # Premium Calculate Button
            calculate_btn = gr.Button(
                "🚀 Calculate ROI Analysis",
                variant="primary",
                elem_classes=["calculate-button"],
                size="lg"
            )
        
        # Results Container (исправленный контейнер результатов)
        results_container = gr.Column(visible=False, elem_classes=["results-container"])
        
        with results_container:
            # KPI Dashboard
            kpi_display = gr.HTML()
            
            # Charts
            with gr.Row():
                comparison_chart = gr.Plot(elem_classes=["chart-container"])
                timeline_chart = gr.Plot(elem_classes=["chart-container"])
            
            # Recommendation
            recommendation_display = gr.HTML()
            
            # CTA Section
            cta_display = gr.HTML()
        
        # Функция обновления информации о профиле
        def update_profile_info(profile_id):
            """Обновление информации о выбранном профиле"""
            if profile_id not in PROFILES:
                return ""
            
            profile = PROFILES[profile_id]
            return f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 0.75rem; margin: 1rem 0;">
                <h4 style="color: #333; margin-bottom: 0.5rem;">{profile.icon} {profile.name}</h4>
                <p style="color: #666; margin-bottom: 0.75rem;">{profile.description}</p>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <span style="background: #007AFF; color: white; padding: 0.25rem 0.75rem; border-radius: 0.5rem; font-size: 0.875rem;">
                        Revenue: €{profile.revenue:,}/month
                    </span>
                    <span style="background: #34C759; color: white; padding: 0.25rem 0.75rem; border-radius: 0.5rem; font-size: 0.875rem;">
                        Margin: {profile.margin}%
                    </span>
                    <span style="background: #FF9F0A; color: white; padding: 0.25rem 0.75rem; border-radius: 0.5rem; font-size: 0.875rem;">
                        Risk: {profile.risk_level}
                    </span>
                </div>
            </div>
            """
        
        # Main calculation function (исправленная функция расчета)
        def calculate_world_class_roi(profile_id, revenue, countries):
            """Исправленный расчет ROI с улучшенной обработкой ошибок"""
            
            # Валидация входных данных
            if not profile_id or profile_id not in PROFILES:
                return [
                    gr.update(visible=False),
                    "<div style='color: red; text-align: center; padding: 2rem;'>Please select a valid business profile.</div>",
                    go.Figure(),
                    go.Figure(),
                    "",
                    ""
                ]
            
            if not countries:
                return [
                    gr.update(visible=False),
                    "<div style='color: red; text-align: center; padding: 2rem;'>Please select at least one country to compare.</div>",
                    go.Figure(),
                    go.Figure(),
                    "",
                    ""
                ]
            
            profile = PROFILES[profile_id]
            calculator = WorldClassROICalculator()
            results = {}
            
            # Calculate for each country
            for country_id in countries:
                if country_id in COUNTRIES:
                    country = COUNTRIES[country_id]
                    try:
                        results[country_id] = calculator.calculate_comprehensive_roi(
                            profile, country, revenue
                        )
                    except Exception as e:
                        print(f"Error calculating ROI for {country_id}: {e}")
                        continue
            
            if not results:
                return [
                    gr.update(visible=False),
                    "<div style='color: red; text-align: center; padding: 2rem;'>Unable to calculate results. Please check your inputs.</div>",
                    go.Figure(),
                    go.Figure(),
                    "",
                    ""
                ]
            
            # Find best option
            best_country = max(results.keys(), key=lambda c: results[c]["conservative_roi"])
            best_result = results[best_country]
            best_country_data = COUNTRIES[best_country]
            
            # Generate KPI Dashboard
            roi_status = "success" if best_result["conservative_roi"] > 150 else "warning" if best_result["conservative_roi"] > 75 else "error"
            payback_str = f"{best_result['payback_months']:.0f}" if best_result['payback_months'] < 120 else "120+"
            
            kpi_html = f"""
            <div class="kpi-grid">
                <div class="kpi-card {roi_status}">
                    <div class="kpi-label">Conservative ROI</div>
                    <div class="kpi-value">{best_result['conservative_roi']:.0f}%</div>
                    <div class="kpi-note">5-year risk-adjusted return</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Annual Savings</div>
                    <div class="kpi-value">€{best_result['annual_savings']:,.0f}</div>
                    <div class="kpi-note">Per year after relocation</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Payback Period</div>
                    <div class="kpi-value">{payback_str}</div>
                    <div class="kpi-note">Months to break even</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Confidence Score</div>
                    <div class="kpi-value">{best_result['confidence_score']:.0f}/100</div>
                    <div class="kpi-note">Success probability rating</div>
                </div>
            </div>
            """
            
            # Generate Charts
            comparison = EliteChartBuilder.create_executive_dashboard(results, countries)
            timeline = EliteChartBuilder.create_timeline_visualization(
                best_result, best_country_data.name
            )
            
            # Generate Recommendation
            rec_html = f"""
            <div class="recommendation-card">
                <div class="recommendation-header">
                    <div class="recommendation-icon">🏆</div>
                    <div class="recommendation-title">Recommended: {best_country_data.name}</div>
                </div>
                <div class="recommendation-content">
                    <strong>{best_country_data.key_benefit}</strong><br>
                    {best_country_data.why_good}
                    <br><br>
                    <strong>For {profile.name}s:</strong> {best_result['conservative_roi']:.0f}% conservative ROI 
                    with {best_result['payback_months']:.0f}-month payback period.
                </div>
            </div>
            """
            
            # Generate CTA based on ROI performance
            if best_result['conservative_roi'] > 200:
                price_old = "€2,497"
                price_new = "€1,497"
                title = f"Complete {best_country_data.name} Relocation Concierge"
                description = "White-glove service with personal immigration lawyer, tax optimization, and 12-month support"
            elif best_result['conservative_roi'] > 100:
                price_old = "€997"
                price_new = "€497"
                title = f"{best_country_data.name} Business Migration Blueprint"
                description = "Comprehensive guide with legal requirements, tax strategies, and step-by-step timeline"
            else:
                price_old = "€297"
                price_new = "€97"
                title = f"{best_country_data.name} Exploration Package"
                description = "Essential information to evaluate your relocation opportunity"
            
            cta_html = f"""
            <div class="cta-section">
                <div class="value-badge">Limited Time: 40% Off</div>
                <h3 class="cta-title">{title}</h3>
                <p class="cta-description">{description}</p>
                
                <div class="price-container">
                    <span class="price-old">{price_old}</span>
                    <span class="price-new">{price_new}</span>
                </div>
                
                <button class="cta-button">Get Your Migration Plan</button>
                
                <div class="guarantee-text">
                    30-day money-back guarantee • Secure payment • Instant access
                </div>
            </div>
            """
            
            return (
                gr.update(visible=True),
                kpi_html,
                comparison,
                timeline,
                rec_html,
                cta_html
            )
        
        # Event handlers (исправленные обработчики событий)
        
        # Обновление информации о профиле при его изменении
        profile_selector.change(
            update_profile_info,
            inputs=[profile_selector],
            outputs=[profile_info]
        )
        
        # Обновление плейсхолдера дохода при изменении профиля
        def update_revenue_placeholder(profile_id):
            if profile_id in PROFILES:
                return gr.update(
                    placeholder=f"Default: €{PROFILES[profile_id].revenue:,}",
                    info=f"Your current monthly business revenue (default: €{PROFILES[profile_id].revenue:,})"
                )
            return gr.update()
        
        profile_selector.change(
            update_revenue_placeholder,
            inputs=[profile_selector],
            outputs=[custom_revenue]
        )
        
        # Основной расчет
        calculate_btn.click(
            calculate_world_class_roi,
            inputs=[profile_selector, custom_revenue, target_countries],
            outputs=[
                results_container,
                kpi_display,
                comparison_chart,
                timeline_chart,
                recommendation_display,
                cta_display
            ]
        )
        
        # Инициализация интерфейса при загрузке
        app.load(
            update_profile_info,
            inputs=[profile_selector],
            outputs=[profile_info]
        )
        
        # World-class footer
        gr.HTML("""
        <div class="footer">
            <p><strong>Legal Disclaimer:</strong> Calculations are estimates for planning purposes only. 
            Results may vary based on individual circumstances. Consult qualified professionals for 
            personalized legal, tax, and financial advice.</p>
            <p style="margin-top: 1rem;">
                © 2025 VisaTier • 
                <a href="#privacy">Privacy Policy</a> • 
                <a href="#terms">Terms of Service</a> • 
                <a href="mailto:hello@visatier.com">Contact</a>
            </p>
        </div>
        """)
    
    return app

# =========================
# LAUNCH APPLICATION
# =========================

if __name__ == "__main__":
    app = create_world_class_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
