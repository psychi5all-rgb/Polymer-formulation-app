import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Polymer Formulation Suite",
    layout="wide",
    page_icon="🧪"
)

# ==========================================================
# CUSTOM CSS (Professional Styling)
# ==========================================================

st.markdown("""
<style>
    .main {
        background-color: #f4f6f9;
    }

    .stApp {
        font-family: "Segoe UI", sans-serif;
    }

    .section-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .title-style {
        font-size: 26px;
        font-weight: 600;
        color: #1f2937;
    }

    .subtitle-style {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 20px;
    }

    .result-box {
        background-color: #eef2ff;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown("## 🧪 Polymer Engineering Suite")
st.sidebar.markdown("Advanced Formulation Dashboard")

module = st.sidebar.radio(
    "Select Module",
    [
        "Forward Polyester",
        "Reverse Polyester",
        "Polyether Designer",
        "PU Prepolymer"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("© 2026 Polymer Engineering Tools")

# ==========================================================
# MATERIAL LIBRARIES
# ==========================================================

polyester_library = {
    "Adipic Acid": {"mw":146.14,"func":2,"type":"acid","water":2},
    "Sebacic Acid": {"mw":202.25,"func":2,"type":"acid","water":2},
    "Phthalic Anhydride": {"mw":148.12,"func":2,"type":"acid","water":1},
    "MEG": {"mw":62.07,"func":2,"type":"glycol"},
    "DEG": {"mw":106.12,"func":2,"type":"glycol"},
    "1,4-BDO": {"mw":90.12,"func":2,"type":"glycol"},
    "1,3-Propanediol": {"mw":76.09,"func":2,"type":"glycol"},
    "1,6-Hexanediol": {"mw":118.17,"func":2,"type":"glycol"},
    "Propylene Glycol": {"mw":76.09,"func":2,"type":"glycol"},
    "Glycerine": {"mw":92.09,"func":3,"type":"glycol"},
    "TMP": {"mw":134.17,"func":3,"type":"glycol"},
}

polyether_starters = {
    "MEG": {"mw":62.07,"func":2},
    "DEG": {"mw":106.12,"func":2},
    "Glycerine": {"mw":92.09,"func":3},
    "Neopentyl Glycol": {"mw":104.15,"func":2},
    "Propylene Glycol": {"mw":76.09,"func":2},
    "Hexanediol": {"mw":118.17,"func":2},
    "Castor Oil": {"mw":933,"func":3},
    "1,3-Propanediol": {"mw":76.09,"func":2},
}

MW_EO = 44
MW_PO = 58

# ==========================================================
# FORWARD POLYESTER MODULE
# ==========================================================

if module == "Forward Polyester":

    st.markdown('<div class="title-style">Forward Polyester Designer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-style">Stoichiometric Calculation with Chang Functionality</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        total_acid_eq = 0
        total_oh_eq = 0
        total_mass = 0
        total_water = 0
        branch_moles = 0
        branch_func = 3

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Acids")
            acids = st.multiselect(
                "Select Acids",
                [k for k in polyester_library if polyester_library[k]["type"] == "acid"]
            )

            for acid in acids:
                mass = st.number_input(f"{acid} mass (g)", value=0.0, step=0.1)
                data = polyester_library[acid]
                mol = mass / data["mw"]
                total_acid_eq += mol * data["func"]
                total_water += mol * data["water"] * 18
                total_mass += mass

        with col2:
            st.subheader("Glycols")
            glycols = st.multiselect(
                "Select Glycols",
                [k for k in polyester_library if polyester_library[k]["type"] == "glycol"]
            )

            for glycol in glycols:
                mass = st.number_input(f"{glycol} mass (g)", value=0.0, step=0.1)
                data = polyester_library[glycol]
                mol = mass / data["mw"]
                total_oh_eq += mol * data["func"]
                total_mass += mass

                if data["func"] > 2:
                    branch_moles += mol
                    branch_func = data["func"]

        if total_mass > 0:
            final_mass = total_mass - total_water
            residual = total_oh_eq - total_acid_eq

            if residual > 0:
                OH = (56100 * residual) / final_mass
                EW = 56100 / OH
                f = 2
                Y = None

                if branch_moles > 0:
                    Y = final_mass / branch_moles
                    f = 2 / (1 - (branch_func - 2) * (EW / Y))

                Mn = f * EW

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("OH", f"{OH:.2f}")
                m2.metric("Functionality", f"{f:.3f}")
                m3.metric("Equivalent Weight", f"{EW:.2f}")
                m4.metric("Mn", f"{Mn:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error("Acid terminated system.")

        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# POLYETHER DESIGNER MODULE
# ==========================================================

elif module == "Polyether Designer":

    st.markdown('<div class="title-style">Polyether Polyol Designer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-style">Alkoxylation Calculation (EO / PO)</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        starter = st.selectbox("Base Polyol", list(polyether_starters.keys()))
        starter_moles = st.number_input("Starter moles", value=1.0)
        target_OH = st.number_input("Target OH", value=200.0)
        EO_fraction = st.slider("EO Fraction", 0.0, 1.0, 0.5)

        data = polyether_starters[starter]
        MW_starter = data["mw"]
        f = data["func"]

        EW_starter = MW_starter / f
        EW_target = 56100 / target_OH

        if EW_target > EW_starter:

            delta_EW = EW_target - EW_starter
            total_AO_mass = delta_EW * f * starter_moles

            EO_mass = total_AO_mass * EO_fraction
            PO_mass = total_AO_mass * (1 - EO_fraction)

            Mn = (MW_starter * starter_moles + EO_mass + PO_mass) / starter_moles

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("EO Required (g)", f"{EO_mass:.2f}")
            c2.metric("PO Required (g)", f"{PO_mass:.2f}")
            c3.metric("Final Mn", f"{Mn:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error("Target OH too high for this starter.")

        st.markdown('</div>', unsafe_allow_html=True)