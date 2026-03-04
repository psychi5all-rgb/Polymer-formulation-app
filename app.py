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
        background-color: blue;
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
        "PU Prepolymer",
        "Industrial Polyester Designer"
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

# ==========================================================
# PU PREPOLYMER FORMULATION MODULE
# ==========================================================

elif module == "PU Prepolymer":

    st.header("PU Prepolymer Formulation")

    # ------------------------------------------------------
    # ISOCYANATE LIBRARY
    # ------------------------------------------------------

    isocyanate_library = {
        "MDI":  {"mw":250.25, "nco":2},
        "TDI":  {"mw":174.16, "nco":2},
        "IPDI": {"mw":222.30, "nco":2},
    }

    # ------------------------------------------------------
    # INPUT SECTION
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        iso_type = st.selectbox(
            "Select Isocyanate",
            list(isocyanate_library.keys())
        )

        iso_mass = st.number_input(
            "Isocyanate Mass (g)",
            min_value=0.0,
            value=100.0,
            step=10.0
        )

    with col2:
        poly_mass = st.number_input(
            "Polyol Mass (g)",
            min_value=0.0,
            value=300.0,
            step=10.0
        )

        poly_OH = st.number_input(
            "Polyol OH Value (mg KOH/g)",
            min_value=0.0,
            value=200.0
        )

        poly_func = st.number_input(
            "Polyol Functionality",
            min_value=1.0,
            value=2.5,
            step=0.1
        )

    # ------------------------------------------------------
    # CALCULATION
    # ------------------------------------------------------

    if st.button("Calculate Prepolymer"):

        iso_data = isocyanate_library[iso_type]

        MW_iso = iso_data["mw"]
        f_nco = iso_data["nco"]

        # ---- NCO equivalents ----
        moles_iso = iso_mass / MW_iso
        total_nco_eq = moles_iso * f_nco

        # ---- Polyol OH equivalents ----
        total_oh_eq = (poly_OH * poly_mass) / 56100

        residual_nco_eq = total_nco_eq - total_oh_eq

        total_mass = iso_mass + poly_mass

        st.subheader("Results")

        if residual_nco_eq > 0:

            percent_nco = (residual_nco_eq * 42 / total_mass) * 100
            eq_weight = total_mass / residual_nco_eq

            # Polyol molecular weight estimate
            EW_poly = 56100 / poly_OH
            Mn_poly = poly_func * EW_poly

            st.success("Prepolymer Successfully Calculated")

            colA, colB, colC = st.columns(3)

            colA.metric("Residual NCO (eq)", f"{residual_nco_eq:.3f}")
            colB.metric("%NCO", f"{percent_nco:.2f}")
            colC.metric("Eq. Weight", f"{eq_weight:.2f}")

            st.markdown("---")

            st.write("### Polyol Properties")
            st.write("Estimated Polyol Mn:", round(Mn_poly,2))
            st.write("Polyol Equivalent Weight:", round(EW_poly,2))

        elif residual_nco_eq == 0:
            st.warning("System is exactly NCO/OH balanced (Index = 1.00).")

        else:
            st.error("System is OH terminated (Excess Polyol). Increase Isocyanate.")

#revese polyester##
elif module == "Reverse Polyester":

    st.markdown('<div class="title-style">Reverse Polyester Designer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-style">Target OH Controlled Formulation</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        # --------------------------------------------------
        # TARGET OH INPUT
        # --------------------------------------------------

        target_OH = st.number_input("Target OH (mg KOH/g)", value=200.0)

        st.markdown("---")

        # --------------------------------------------------
        # ACIDS (Fixed Mass Input)
        # --------------------------------------------------

        st.subheader("Acids (Fixed Mass)")

        num_acids = st.slider("Number of Acids", 1, 3, 1)

        total_acid_mass = 0
        total_acid_eq = 0
        total_water = 0

        for i in range(num_acids):
            col1, col2 = st.columns(2)

            with col1:
                acid = st.selectbox(
                    f"Acid {i+1}",
                    [k for k in polyester_library if polyester_library[k]["type"]=="acid"],
                    key=f"rev_acid_sel_{i}"
                )

            with col2:
                mass = st.number_input(
                    f"{acid} Mass (g)",
                    value=100.0,
                    key=f"rev_acid_mass_{i}"
                )

            data = polyester_library[acid]
            mol = mass / data["mw"]

            total_acid_mass += mass
            total_acid_eq += mol * data["func"]
            total_water += mol * data["water"] * 18

        st.markdown("---")

        # --------------------------------------------------
        # GLYCOLS (Ratio Input)
        # --------------------------------------------------

        st.subheader("Glycols (Mol Ratio)")

        num_glycols = st.slider("Number of Glycols", 1, 4, 1)

        glycol_ratios = {}
        ratio_sum = 0

        for i in range(num_glycols):
            col1, col2 = st.columns(2)

            with col1:
                glycol = st.selectbox(
                    f"Glycol {i+1}",
                    [k for k in polyester_library if polyester_library[k]["type"]=="glycol"],
                    key=f"rev_glycol_sel_{i}"
                )

            with col2:
                ratio = st.number_input(
                    f"{glycol} Mol Ratio",
                    value=1.0,
                    key=f"rev_glycol_ratio_{i}"
                )

            glycol_ratios[glycol] = ratio
            ratio_sum += ratio

        # --------------------------------------------------
        # SOLVER
        # --------------------------------------------------

        if st.button("Calculate Required Glycols"):

            if ratio_sum == 0:
                st.error("Glycol ratio cannot be zero.")
                st.stop()

            # Solve for glycol scaling

            def compute(scale):
                total_oh_eq = 0
                total_glycol_mass = 0
                branch_moles = 0
                branch_func = 3

                for name, ratio in glycol_ratios.items():
                    mol = scale * (ratio / ratio_sum)
                    data = polyester_library[name]

                    total_oh_eq += mol * data["func"]
                    total_glycol_mass += mol * data["mw"]

                    if data["func"] > 2:
                        branch_moles += mol
                        branch_func = data["func"]

                final_mass = total_acid_mass + total_glycol_mass - total_water
                residual = total_oh_eq - total_acid_eq

                if residual <= 0:
                    return -1, 0, 0, 0

                OH = (56100 * residual) / final_mass
                return OH, branch_moles, final_mass, total_glycol_mass

            # Bisection method
            low, high = 1e-6, 1000

            for _ in range(100):
                mid = (low + high) / 2
                OH_val, branch_moles, final_mass, total_glycol_mass = compute(mid)

                if OH_val < 0:
                    low = mid
                    continue

                if abs(OH_val - target_OH) < 0.01:
                    break

                if OH_val < target_OH:
                    low = mid
                else:
                    high = mid

            OH_val, branch_moles, final_mass, total_glycol_mass = compute(mid)

            if OH_val <= 0:
                st.error("Acid Terminated Polyester — Increase Glycol.")
                st.stop()

            # Chang functionality
            EW = 56100 / OH_val

            if branch_moles > 0:
                Y = final_mass / branch_moles
                f = 2 / (1 - (1) * (EW / Y))
            else:
                Y = None
                f = 2

            Mn = f * EW

            # --------------------------------------------------
            # OUTPUT
            # --------------------------------------------------

            st.success("Calculation Complete")

            st.markdown('<div class="result-box">', unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Achieved OH", f"{OH_val:.2f}")
            c2.metric("Functionality", f"{f:.3f}")
            c3.metric("Mn", f"{Mn:.2f}")

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("### Required Glycol Masses")

            for name, ratio in glycol_ratios.items():
                mol = mid * (ratio / ratio_sum)
                mass = mol * polyester_library[name]["mw"]
                st.write(f"{name}: {mass:.2f} g")

        st.markdown('</div>', unsafe_allow_html=True)

##Industrial Polyester Designer##
elif module == "Industrial Polyester Designer":

    st.markdown('<div class="title-style">Industrial Polyester Designer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-style">Dynamic Polyester Formulation Tool</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        # --------------------------------------------------
        # GLOBAL CONTROLS
        # --------------------------------------------------

        col1,col2,col3 = st.columns(3)

        with col1:
            r_ratio = st.slider("r (OH / COOH)",0.80,2.20,1.08,0.01)

        with col2:
            branch_percent = st.slider("Brancher % (mol)",0.0,0.20,0.05,0.01)

        with col3:
            acid_moles = st.slider("Total Acid Moles",1.0,50.0,10.0,1.0)

        st.markdown("---")

        # --------------------------------------------------
        # ACID SELECTION
        # --------------------------------------------------

        acid_options = [k for k in polyester_library if polyester_library[k]["type"]=="acid"]

        num_acids = st.slider("Number of Acids",1,3,2)

        acids=[]
        acid_ratios=[]
        ratio_sum=0

        for i in range(num_acids):

            colA,colB = st.columns(2)

            with colA:
                acid = st.selectbox(
                    f"Acid {i+1}",
                    acid_options,
                    key=f"acid_ind_{i}"
                )

            with colB:
                ratio = st.slider(
                    f"{acid} Ratio",
                    0.0,1.0,
                    1/num_acids,
                    0.01,
                    key=f"acid_ratio_ind_{i}"
                )

            acids.append(acid)
            acid_ratios.append(ratio)
            ratio_sum+=ratio

        st.markdown("---")

        # --------------------------------------------------
        # GLYCOL SELECTION
        # --------------------------------------------------

        glycol_options = [k for k in polyester_library if polyester_library[k]["type"]=="glycol"]

        num_glycols = st.slider("Number of Glycols",1,4,2)

        glycols=[]
        glycol_ratios=[]
        glycol_sum=0

        for i in range(num_glycols):

            colA,colB = st.columns(2)

            with colA:
                glycol = st.selectbox(
                    f"Glycol {i+1}",
                    glycol_options,
                    key=f"glycol_ind_{i}"
                )

            with colB:
                ratio = st.slider(
                    f"{glycol} Ratio",
                    0.0,1.0,
                    1/num_glycols,
                    0.01,
                    key=f"glycol_ratio_ind_{i}"
                )

            glycols.append(glycol)
            glycol_ratios.append(ratio)
            glycol_sum+=ratio

        st.markdown("---")

        brancher = st.selectbox("Brancher",["Glycerine","TMP"])

        B = polyester_library[brancher]

        # --------------------------------------------------
        # CALCULATION
        # --------------------------------------------------

        total_acid_eq=0
        total_oh_eq=0
        total_mass=0
        total_water=0

        branch_mol = acid_moles*branch_percent
        branch_oh = branch_mol*B["func"]

        for i,acid in enumerate(acids):

            A = polyester_library[acid]

            mol = acid_moles*(acid_ratios[i]/ratio_sum)

            total_acid_eq += mol*A["func"]

            total_mass += mol*A["mw"]

            total_water += mol*A["water"]*18

        total_oh_eq = r_ratio*total_acid_eq

        remaining_oh = total_oh_eq-branch_oh

        for i,glycol in enumerate(glycols):

            G = polyester_library[glycol]

            mol = (remaining_oh*(glycol_ratios[i]/glycol_sum))/G["func"]

            total_mass += mol*G["mw"]

        total_mass += branch_mol*B["mw"]

        final_mass = total_mass-total_water

        residual_oh = total_oh_eq-total_acid_eq

        if residual_oh <= 0:
            st.warning("Acid terminated polyester")

        else:

            OH = (56100*residual_oh)/final_mass

            EW = 56100/OH

            Y = final_mass/branch_mol if branch_mol>0 else None

            if branch_mol>0:

                denom = 1-(B["func"]-2)*(EW/Y)

                if abs(denom)<1e-6:
                    f = float("inf")
                else:
                    f = 2/denom
            else:
                f=2

            Mn = f*EW

            st.markdown('<div class="result-box">', unsafe_allow_html=True)

            c1,c2,c3,c4 = st.columns(4)

            c1.metric("OH",f"{OH:.2f}")
            c2.metric("Functionality",f"{f:.3f}")
            c3.metric("Mn",f"{Mn:.2f}")
            c4.metric("Final Mass",f"{final_mass:.1f}")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


