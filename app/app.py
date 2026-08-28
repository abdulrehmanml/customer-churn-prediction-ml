import sys
from pathlib import Path
import streamlit as st

# =========================================================
# PAGE CONFIGURATION (Must be the first st. command)
# =========================================================

st.set_page_config(
    page_title="Customer Churn Prediction", 
    page_icon="📊", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# =========================================================
# PATH CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.predict import (
    load_predictive_engine,
    validate_customer_input,
    predict_customer,
    calculate_risk,
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    /* =====================================================
       GLOBAL PAGE
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 7% 10%,
                rgba(55, 126, 184, 0.18),
                transparent 25%
            ),
            radial-gradient(
                circle at 93% 15%,
                rgba(74, 139, 198, 0.13),
                transparent 24%
            ),
            radial-gradient(
                circle at 50% 95%,
                rgba(39, 98, 145, 0.11),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #11161c 0%,
                #151c24 48%,
                #10151b 100%
            );
        color: #f5f7fa;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.4rem;
        padding-bottom: 3rem;
    }

    /* =====================================================
       HIDE DEFAULT STREAMLIT CHROME
       ===================================================== */

    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* =====================================================
       PAGE TITLE
       ===================================================== */

    .page-title {
        text-align: center;
        color: #ffffff;
        font-size: 2.65rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.035em;
        margin: 0;
    }

    .page-title .accent {
        color: #55a9e8;
    }

    /* =====================================================
       PAGE SUBTITLE
       ===================================================== */

    .page-subtitle {
        max-width: 780px;
        margin: 0.8rem auto 2rem;
        text-align: center;
        color: #bdc8d3;
        font-size: 0.98rem;
        line-height: 1.55;
    }

    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    .section-title {
        color: #ffffff;
        font-size: 1.18rem;
        font-weight: 750;
        margin-top: 0.4rem;
        margin-bottom: 0.25rem;
    }

    .section-description {
        color: #aebbc7;
        font-size: 0.87rem;
        line-height: 1.5;
        margin-bottom: 0.95rem;
    }

    /* =====================================================
       INPUT LABELS
       ===================================================== */

    .stSelectbox label,
    .stSelectbox label p,
    .stNumberInput label,
    .stNumberInput label p {
        color: #f0f4f7 !important;
        opacity: 1 !important;
        font-size: 0.88rem !important;
        font-weight: 650 !important;
    } 

    /* =====================================================
       NATIVE HELP TOOLTIP
       ===================================================== */

    [data-testid="stTooltipIcon"] {
        color: #ffffff !important;
        opacity: 0.65 !important;
    }

    [data-testid="stTooltipIcon"] svg {
        stroke: #ffffff !important;
    }

    [data-testid="stTooltipIcon"]:hover {
        opacity: 1 !important;
    }

    [data-testid="stTooltipIcon"]:hover svg {
        stroke: #55a9e8 !important;
    }

    /* =====================================================
       SELECTBOX
       ===================================================== */

    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-testid="stSelectbox"] div[role="combobox"] {
        background-color: #202b35 !important;
        border: 1px solid #3d4e5d !important;
        border-radius: 10px !important;
        height: 48px !important;
        min-height: 48px !important;
        box-sizing: border-box !important;
        box-shadow: 0 5px 14px rgba(0, 0, 0, 0.12) !important;
    }

    /* Aggressive visible text fix */
    div[data-baseweb="select"] div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Dropdown arrow */
    div[data-baseweb="select"] svg {
        fill: #cbd5de !important;
        color: #cbd5de !important;
    }

    /* =====================================================
       NUMBER INPUT
       ===================================================== */

    div[data-testid="stNumberInput"] {
        color: #ffffff !important;
    }
    
    /* Lock the outer wrapper height */
    div[data-testid="stNumberInput"] > div {
        height: 48px !important;
        min-height: 48px !important;
    }

    /* 1. Target the MAIN WRAPPER */
    div[data-testid="stNumberInput"] div[data-baseweb="input"],
    div[data-testid="stNumberInput"] div[data-baseweb="baseInput"] {
        background-color: #202b35 !important;
        border: 1px solid #3d4e5d !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 14px rgba(0,0,0,0.12) !important;
        overflow: hidden !important; 
    }

    /* 2. Target the INNER TEXT FIELD */
    div[data-testid="stNumberInput"] input {
        background-color: #202b35 !important; /* Forces dark background */
        color: #ffffff !important;
        caret-color: #55a9e8 !important; /* Restores the blue typing cursor */
        border: none !important; 
        height: 48px !important;
        min-height: 48px !important;
        box-sizing: border-box !important;
        font-size: 0.94rem !important;
        font-weight: 500 !important;
        opacity: 1 !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.035) !important;
    }

    div[data-testid="stNumberInput"] input::placeholder {
        color: #aebbc7 !important;
        -webkit-text-fill-color: #aebbc7 !important;
        opacity: 1 !important;
    }

    /* =====================================================
       SELECTED DROPDOWN VALUE
       ===================================================== */

    /* Visible selected text fix */
    div[data-baseweb="select"] div[class*="singleValue"],
    div[data-baseweb="select"] div[class*="ValueContainer"] {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Dropdown arrow */
    div[data-baseweb="select"] svg {
        fill: #cbd5de !important;
        color: #cbd5de !important;
    }

    /* Dropdown menu background */
    div[data-baseweb="popover"], 
    div[data-baseweb="menu"] {
        background: #1c252e !important;
    }

    /* Individual options */
    div[data-baseweb="menu"] [role="option"] {
        background: #1c252e !important;
        color: #f5f7fa !important;
    }

    /* Hovered option */
    div[data-baseweb="menu"] [role="option"]:hover {
        background: #2d3b48 !important;
        color: #ffffff !important;
    }

    /* =====================================================
       NUMBER INPUT STEPPER BUTTONS & CLEAR ICON
       ===================================================== */

    button[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"] {
        background: transparent !important;
        border: none !important;
        margin: 0 !important;
        transition: all 0.2s ease;
    }

    button[data-testid="stNumberInputStepUp"] svg,
    button[data-testid="stNumberInputStepDown"] svg {
        fill: #aebbc7 !important; 
        width: 14px !important;
        height: 14px !important;
    }

    button[data-testid="stNumberInputStepUp"]:not(:disabled):hover,
    button[data-testid="stNumberInputStepDown"]:not(:disabled):hover {
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    button[data-testid="stNumberInputStepUp"]:not(:disabled):hover svg,
    button[data-testid="stNumberInputStepDown"]:not(:disabled):hover svg {
        fill: #55a9e8 !important; 
    }

    button[data-testid="stNumberInputStepUp"]:disabled,
    button[data-testid="stNumberInputStepDown"]:disabled {
        opacity: 0.3 !important;
        background: transparent !important;
        border: none !important;
    }
    
    button[data-testid="stInputClearButton"],
    button[data-testid="stInputClearButton"] * {
        background-color: transparent !important;
    }
    
    button[data-testid="stInputClearButton"] svg {
        fill: #8796a3 !important;
    }

    /* =====================================================
       INPUT FOCUS
       ===================================================== */

    /* 3. Apply blue border directly to wrappers */
    div[data-baseweb="select"]:focus-within,
    div[data-testid="stSelectbox"] div[role="combobox"]:focus-within,
    div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
    div[data-testid="stNumberInput"] div[data-baseweb="baseInput"]:focus-within {

    /* =====================================================
       DIVIDER
       ===================================================== */

    .soft-divider {
        height: 1px;
        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(255,255,255,0.10),
                transparent
            );
        margin: 1.4rem 0;
    }

    /* =====================================================
       INFORMATION CARD
       ===================================================== */

    .info-card {
        background:
            linear-gradient(
                135deg,
                rgba(59,111,150,0.13),
                rgba(255,255,255,0.06)
            );
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px;
        padding: 0.95rem 1.05rem;
        margin-top: 0.15rem;
        box-shadow: 0 9px 23px rgba(0,0,0,0.14);
    }

    .info-title {
        color: #ffffff;
        font-size: 0.88rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .info-text {
        color: #b5c1cc;
        font-size: 0.81rem;
        line-height: 1.5;
    }

    /* =====================================================
       ACTION BUTTONS (SUBMIT & RESET)
       ===================================================== */

    button[kind="primary"] {
        width: 100%;
        min-height: 3.15rem;
        background: linear-gradient(90deg, #2f7fba, #438fc8) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 11px !important;
        font-size: 0.96rem !important;
        font-weight: 750 !important;
        box-shadow: 0 10px 22px rgba(47,127,186,0.18);
        transition: all 0.3s ease !important;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(90deg, #28a745, #34ce57) !important;
        color: #ffffff !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 14px 26px rgba(40,167,69,0.25) !important;
    }

    button[kind="secondary"] {
        width: 100%;
        min-height: 3.15rem;
        background: #202b35 !important;
        color: #c6d0d9 !important;
        border: 1px solid #3d4e5d !important;
        border-radius: 11px !important;
        font-size: 0.96rem !important;
        font-weight: 750 !important;
        transition: all 0.3s ease !important;
    }

    button[kind="secondary"]:hover {
        background: #293640 !important;
        color: #ffffff !important;
        border-color: #536677 !important;
        transform: translateY(-1px) !important;
    }

    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        color: #71808c;
        font-size: 0.74rem;
        margin-top: 2.2rem;
    }

    /* =====================================================
       RESULT DASHBOARD
       ===================================================== */

    .result-section {
        margin-top: 2rem;
    }

    .result-section-title {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 750;
        margin-bottom: 0.3rem;
    }

    .result-section-description {
        color: #aebbc7;
        font-size: 0.86rem;
        margin-bottom: 1rem;
    }

    .result-card {
        min-height: 155px;
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.08),
                rgba(255,255,255,0.035)
            );
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 1.15rem;
        box-shadow: 0 12px 28px rgba(0,0,0,0.20);
    }

    .result-label {
        color: #96a6b4;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.08em;
        margin-bottom: 0.55rem;
    }

    .result-main-value {
        color: #ffffff;
        font-size: 1.55rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .result-secondary {
        color: #aab7c3;
        font-size: 0.81rem;
        margin-top: 0.45rem;
    }

    .probability-track {
        width: 100%;
        height: 9px;
        background: #2a3540;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 0.9rem;
    }

    .probability-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #357eaf, #55a9e8);
    }

    .risk-high { color: #ef7777; }
    .risk-medium { color: #e2b94f; }
    .risk-low { color: #4bc47d; }

    .business-result {
        margin-top: 1rem;
        padding: 1.15rem 1.2rem;
        background:
            linear-gradient(
                135deg,
                rgba(54,111,153,0.12),
                rgba(255,255,255,0.035)
            );
        border: 1px solid rgba(77,158,216,0.18);
        border-left: 4px solid #4d9ed8;
        border-radius: 14px;
    }

    .business-result-title {
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .business-result-text {
        color: #c1ccd5;
        font-size: 0.88rem;
        line-height: 1.6;
    }

    .threshold-note {
        margin-top: 0.8rem;
        color: #8796a3;
        font-size: 0.77rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CACHED MODEL LOADING
# =========================================================

@st.cache_resource
def get_predictive_engine():
    """
    Wrap the imported load function in Streamlit's cache decorator
    so it only runs once and stays in memory.
    """
    return load_predictive_engine()


try:
    pipeline, prediction_threshold = get_predictive_engine()

except FileNotFoundError:
    st.error("The prediction engine is currently unavailable.")
    st.caption("The trained model artifact could not be located. Please verify the application deployment.")
    st.stop()

except Exception as exc:
    st.error("The prediction engine could not be initialized.")
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    """
    <div class="page-title">
        Customer <span class="accent">Churn Prediction</span>
    </div>
    <div class="page-subtitle">
        Estimate a customer's likelihood of leaving based on
        available customer, service, contract, and billing information.
    </div>
    <div style="text-align:center; color:#7f91a0; font-size:0.76rem; margin-top:-1.2rem; margin-bottom:1.7rem;">
        All displayed fields are used by the prediction engine.
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# CUSTOMER PROFILE
# =====================================================

st.markdown('<div class="section-title">Customer Profile</div>', unsafe_allow_html=True)
st.markdown('<div class="section-description">Enter the customer characteristics available to the business.</div>', unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    gender = st.selectbox("Gender", options=["Female", "Male"], index=None, placeholder="Select gender", key="gender")
with row1_col2:
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=72, value=0, step=1, help="Number of months the customer has remained with the company.", key="tenure")
with row1_col3:
    contract = st.selectbox("Contract", options=["Month-to-month", "One year", "Two year"], index=None, placeholder="Select contract", help="Customer's current contract commitment period.", key="contract")

row2_col1, row2_col2, row2_col3 = st.columns(3)
    
with row2_col1:
    senior_citizen = st.selectbox("Senior Citizen", options=[0, 1], format_func=lambda value: "No" if value == 0 else "Yes", index=None, placeholder="Select status", help="Indicates whether the customer is 65 years or older.", key="senior_citizen")
with row2_col2:
    phone_service = st.selectbox("Phone Service", options=["No", "Yes"], index=None, placeholder="Select status", key="phone_service")
with row2_col3:
    paperless_billing = st.selectbox("Paperless Billing", options=["No", "Yes"], index=None, placeholder="Select status", key="paperless_billing")

row3_col1, row3_col2, row3_col3 = st.columns(3)

with row3_col1:
    partner = st.selectbox("Partner", options=["No", "Yes"], index=None, placeholder="Select status", help="Indicates whether the customer has a partner.", key="partner")
with row3_col2:
    if phone_service == "No":
        multiple_lines = st.selectbox("Multiple Lines", options=["No phone service"], disabled=True, key="multiple_lines_disabled")
        st.markdown('<div style="color: #e2b94f; font-size: 0.82rem; margin-top: -0.5rem;">💡 <i>Requires Phone Service</i></div>', unsafe_allow_html=True)
    else:
        multiple_lines = st.selectbox("Multiple Lines", options=["No", "Yes"], index=None, placeholder="Select status", help="Indicates whether the customer has multiple phone lines.", key="multiple_lines")
with row3_col3:
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=0.0, step=1.0, help="Customer's current recurring monthly service charge.", key="monthly_charges")

row4_col1, row4_col2, row4_col3 = st.columns(3)
    
with row4_col1:
    dependents = st.selectbox("Dependents", options=["No", "Yes"], index=None, placeholder="Select status", help="Indicates whether the customer lives with any dependents.", key="dependents")
with row4_col2:
    internet_service = st.selectbox("Internet Service", options=["DSL", "Fiber optic", "No"], index=None, placeholder="Select connection", help="Customer's internet service type.", key="internet_service")
with row4_col3:
    total_charges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=0.0, step=5.0, help="Customer's accumulated charges over the customer relationship.", key="total_charges")


# =====================================================
# SERVICES & SUPPORT
# =====================================================

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Services & Support</div>', unsafe_allow_html=True)
st.markdown('<div class="section-description">Select the services and support options associated with the customer.</div>', unsafe_allow_html=True)

if internet_service == "No":
    st.markdown(
        """
        <div style="background: rgba(243, 156, 18, 0.15); border-left: 4px solid #f39c12; padding: 14px 18px; border-radius: 8px; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <span style="color: #ffffff; font-size: 0.92rem; letter-spacing: 0.3px;">
                💡 <strong style="color: #f39c12;">Internet required:</strong> Internet-dependent services are unavailable because the customer has no internet service. Select <strong>DSL</strong> or <strong>Fiber optic</strong> above to configure these services.
            </span>
        </div>
        """,
        unsafe_allow_html=True
)

serv_row1_col1, serv_row1_col2, serv_row1_col3 = st.columns(3)

with serv_row1_col1:
    if internet_service == "No":
        online_security = "No internet service"
        st.selectbox("Online Security", options=["No internet service"], disabled=True, key="sec_dis")
    else:
        online_security = st.selectbox("Online Security", options=["No", "Yes"], index=None, placeholder="Select status", help="Indicates whether the customer subscribes to online security.", key="online_security")

with serv_row1_col2:
    if internet_service == "No":
        device_protection = "No internet service"
        st.selectbox("Device Protection", options=["No internet service"], disabled=True, key="dev_dis")
    else:
        device_protection = st.selectbox("Device Protection", options=["No", "Yes"], index=None, placeholder="Select status", help="Indicates whether the customer subscribes to device protection.", key="device_protection")

with serv_row1_col3:
    if internet_service == "No":
        streaming_tv = "No internet service"
        st.selectbox("Streaming TV", options=["No internet service"], disabled=True, key="tv_dis")
    else:
        streaming_tv = st.selectbox("Streaming TV", options=["No", "Yes"], index=None, placeholder="Select status", key="streaming_tv")


serv_row2_col1, serv_row2_col2, serv_row2_col3 = st.columns(3)

with serv_row2_col1:
    if internet_service == "No":
        online_backup = "No internet service"
        st.selectbox("Online Backup", options=["No internet service"], disabled=True, key="bak_dis")
    else:
        online_backup = st.selectbox("Online Backup", options=["No", "Yes"], index=None, placeholder="Select status", help="Indicates whether the customer subscribes to an online backup service.", key="online_backup")

with serv_row2_col2:
    if internet_service == "No":
        tech_support = "No internet service"
        st.selectbox("Tech Support", options=["No internet service"], disabled=True, key="tech_dis")
    else:
        tech_support = st.selectbox("Tech Support", options=["No", "Yes"], index=None, placeholder="Select status", help="Indicates whether the customer subscribes to technical support.", key="tech_support")

with serv_row2_col3:
    if internet_service == "No":
        streaming_movies = "No internet service"
        st.selectbox("Streaming Movies", options=["No internet service"], disabled=True, key="mov_dis")
    else:
        streaming_movies = st.selectbox("Streaming Movies", options=["No", "Yes"], index=None, placeholder="Select status", key="streaming_movies")


# =====================================================
# PAYMENT INFORMATION
# =====================================================

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Payment Information</div>', unsafe_allow_html=True)
st.markdown('<div class="section-description">Select the payment method associated with the customer.</div>', unsafe_allow_html=True)

payment_col1, payment_col2 = st.columns([1, 1])

with payment_col1:
    payment_method = st.selectbox(
        "Payment Method",
        options=[
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)",
        ],
        index=None,
        placeholder="Select payment method",
        help="Method currently used by the customer to pay for services.",
        key="payment_method"
    )

with payment_col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">How the prediction works</div>
            <div class="info-text">
                The entered customer information is processed through the trained prediction pipeline to estimate the likelihood of churn.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
   
# =====================================================
# ACTION BUTTONS & LOGIC
# =====================================================

st.markdown(
    """
    <div style="
        color:#91a1af;
        font-size:0.80rem;
        text-align:right; 
        margin:1.5rem 0 0.7rem 0;
    ">
        Review the customer information, then run the prediction.
    </div>
    """,
    unsafe_allow_html=True,
)

spacer, action_col1, action_col2 = st.columns([5, 3, 1.5])

with action_col1:
    submitted = st.button("Analyze Customer Churn Risk", use_container_width=True, type="primary")

with action_col2:
    reset = st.button("Reset Form", use_container_width=True, type="secondary")

# =========================================================
# HANDLE ACTIONS
# =========================================================

if reset:
    st.session_state.clear()
    st.rerun()

if submitted:
    
    # -----------------------------------------------------
    # 1. COMPILE CUSTOMER RECORD
    # -----------------------------------------------------
    
    customer_data = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
    }

    # -----------------------------------------------------
    # 2. INPUT VALIDATION
    # -----------------------------------------------------
    
    validation_errors = validate_customer_input(customer_data)

    if validation_errors:
        st.warning("Please review the following information before running the prediction.")
        for error in validation_errors:
            st.write(f"• {error}")
        st.stop()

    # -----------------------------------------------------
    # 3. MODEL INFERENCE
    # -----------------------------------------------------
    
    try:
        probability, prediction = predict_customer(customer_data, pipeline, prediction_threshold)
    except Exception as exc:
        st.error("The prediction could not be generated.")
        st.caption("Please verify the entered customer information and try again.")
        with st.expander("Technical details"):
            st.code(str(exc))
        st.stop()

    # -----------------------------------------------------
    # 4. RISK CLASSIFICATION
    # -----------------------------------------------------
    
    risk_level = calculate_risk(probability, prediction_threshold)


    # =========================================================
    # RESULT DASHBOARD
    # =========================================================

    prediction_text = "Likely to Churn" if prediction == 1 else "Likely to Stay"

    if risk_level == "High":
        risk_class = "risk-high"
        business_message = (
            "This customer has a high predicted likelihood of churn. "
            "The business may prioritize this customer for retention review or targeted intervention."
        )
    elif risk_level == "Medium":
        risk_class = "risk-medium"
        business_message = (
            "This customer falls within the model's churn-risk range. "
            "The business may consider additional review or targeted customer engagement."
        )
    else:
        risk_class = "risk-low"
        business_message = "This customer has a lower predicted likelihood of churn based on the information provided."

    # =====================================================
    # RESULT HEADER
    # =====================================================

    st.markdown(
        """
        <div class="result-section">
            <div class="result-section-title">Prediction Result</div>
            <div class="result-section-description">A concise assessment of the customer's estimated churn risk.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result_col1, result_col2, result_col3 = st.columns(3)

    # -----------------------------------------------------
    # PROBABILITY
    # -----------------------------------------------------
    with result_col1:
        st.markdown(
            f"""<div class="result-card">
                    <div class="result-label">CHURN PROBABILITY</div>
                    <div class="result-main-value">{probability:.1%}</div>
                    <div class="probability-track">
                        <div class="probability-fill" style="width:{probability * 100:.1f}%;"></div>
                    </div>
                    <div class="result-secondary">Model-estimated likelihood</div>
                </div>
            """,
            unsafe_allow_html=True,  
        )

    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------
    with result_col2:
        st.markdown(
            f"""<div class="result-card">
                    <div class="result-label">MODEL PREDICTION</div>
                    <div class="result-main-value">{prediction_text}</div>
                    <div class="result-secondary">Decision threshold: {prediction_threshold:.0%}</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # RISK
    # -----------------------------------------------------
    with result_col3:
        st.markdown(
            f"""<div class="result-card">
                    <div class="result-label">RISK LEVEL</div>
                    <div class="result-main-value {risk_class}">{risk_level}</div>
                    <div class="result-secondary">Based on predicted probability</div>
                </div>
            """,
            unsafe_allow_html=True,
    )

    # =====================================================
    # BUSINESS INTERPRETATION & THRESHOLD NOTE
    # =====================================================

    st.markdown(
        f"""<div class="business-result">
                <div class="business-result-title">Business Interpretation</div>
                <div class="business-result-text">{business_message}</div>
            </div>
            <div class="threshold-note">
                A probability of {prediction_threshold:.0%} or higher is classified by the model as likely to churn.
            </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    Customer Churn Prediction · Classical Machine Learning · Logistic Regression
    </div>
    """,
    unsafe_allow_html=True,
)
