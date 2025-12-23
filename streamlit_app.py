import streamlit as st

# ================= TAX FUNCTIONS =================

def calculate_old_regime_tax(income, deductions):
    steps = []
    taxable_income = max(0, income - deductions)

    steps.append(f"Gross Income              : ₹{income:,.2f}")
    steps.append(f"Less: Chapter VI-A Deduct.: ₹{deductions:,.2f}")
    steps.append(f"Taxable Income            : ₹{taxable_income:,.2f}\n")
    steps.append("Tax Calculation:")

    tax = 0

    if taxable_income > 250000:
        slab = min(taxable_income, 500000) - 250000
        slab_tax = slab * 0.05
        tax += slab_tax
        steps.append(f"• 2,50,001 – 5,00,000 @5%   = ₹{slab_tax:,.2f}")

    if taxable_income > 500000:
        slab = min(taxable_income, 1000000) - 500000
        slab_tax = slab * 0.20
        tax += slab_tax
        steps.append(f"• 5,00,001 – 10,00,000 @20% = ₹{slab_tax:,.2f}")

    if taxable_income > 1000000:
        slab = taxable_income - 1000000
        slab_tax = slab * 0.30
        tax += slab_tax
        steps.append(f"• Above 10,00,000 @30%      = ₹{slab_tax:,.2f}")

    # Section 87A Rebate (Old Regime)
    rebate = 0
    if taxable_income <= 500000 and tax > 0:
        rebate = min(tax, 12500)
        tax -= rebate
        steps.append(f"\nLess: Rebate u/s 87A       : ₹{rebate:,.2f}")

    cess = tax * 0.04
    total_tax = tax + cess

    steps.append(f"\nBasic Tax                 : ₹{tax:,.2f}")
    steps.append(f"Health & Edu Cess @4%     : ₹{cess:,.2f}")
    steps.append(f"Total Tax Payable         : ₹{total_tax:,.2f}")

    return total_tax, steps


def calculate_new_regime_tax(income):
    steps = []
    steps.append(f"Gross Income : ₹{income:,.2f}")
    steps.append("Tax Calculation:")

    tax = 0

    if income > 300000:
        slab = min(income, 600000) - 300000
        slab_tax = slab * 0.05
        tax += slab_tax
        steps.append(f"• 3,00,001 – 6,00,000 @5%   = ₹{slab_tax:,.2f}")

    if income > 600000:
        slab = min(income, 900000) - 600000
        slab_tax = slab * 0.10
        tax += slab_tax
        steps.append(f"• 6,00,001 – 9,00,000 @10%  = ₹{slab_tax:,.2f}")

    if income > 900000:
        slab = min(income, 1200000) - 900000
        slab_tax = slab * 0.15
        tax += slab_tax
        steps.append(f"• 9,00,001 – 12,00,000 @15% = ₹{slab_tax:,.2f}")

    if income > 1200000:
        slab = min(income, 1500000) - 1200000
        slab_tax = slab * 0.20
        tax += slab_tax
        steps.append(f"• 12,00,001 – 15,00,000 @20% = ₹{slab_tax:,.2f}")

    if income > 1500000:
        slab = income - 1500000
        slab_tax = slab * 0.30
        tax += slab_tax
        steps.append(f"• Above 15,00,000 @30%      = ₹{slab_tax:,.2f}")

    # Section 87A Rebate (New Regime)
    rebate = 0
    if income <= 700000 and tax > 0:
        rebate = min(tax, 25000)
        tax -= rebate
        steps.append(f"\nLess: Rebate u/s 87A       : ₹{rebate:,.2f}")

    cess = tax * 0.04
    total_tax = tax + cess

    steps.append(f"\nBasic Tax                 : ₹{tax:,.2f}")
    steps.append(f"Health & Edu Cess @4%     : ₹{cess:,.2f}")
    steps.append(f"Total Tax Payable         : ₹{total_tax:,.2f}")

    return total_tax, steps


# ================= STREAMLIT UI =================

st.set_page_config(page_title="Income Tax Calculator", layout="centered")
st.title("🇮🇳 Income Tax Calculator (India)")

# FY / AY Selection
fy = st.selectbox(
    "Select Financial Year",
    ["FY 2023-24 (AY 2024-25)", "FY 2024-25 (AY 2025-26)"]
)

st.write(f"**Selected:** {fy}")

income = st.number_input("Annual Income (₹)", min_value=0.0, step=5000.0)
age = st.number_input("Age", min_value=18, max_value=100)

regime = st.radio("Select Regime", ["Old Regime", "New Regime", "Compare Both"])

deductions = 0
if regime in ["Old Regime", "Compare Both"]:
    st.subheader("Chapter VI-A Deductions (Old Regime)")
    sec_80c = st.number_input("Section 80C (Max ₹1,50,000)", min_value=0.0)
    sec_80d = st.number_input("Section 80D", min_value=0.0)
    deductions = min(sec_80c, 150000) + sec_80d

if st.button("Calculate Tax"):
    st.divider()

    if regime in ["Old Regime", "Compare Both"]:
        old_tax, old_steps = calculate_old_regime_tax(income, deductions)
        st.subheader("🧾 Old Regime – Tax Calculation Steps")
        for s in old_steps:
            st.write(s)

    if regime in ["New Regime", "Compare Both"]:
        new_tax, new_steps = calculate_new_regime_tax(income)
        st.subheader("🧾 New Regime – Tax Calculation Steps")
        for s in new_steps:
            st.write(s)

    if regime == "Compare Both":
        st.divider()
        st.subheader("✅ Best Regime Recommendation")
        if old_tax < new_tax:
            st.success("Old Regime is more beneficial ✅")
        elif new_tax < old_tax:
            st.success("New Regime is more beneficial ✅")
        else:
            st.info("Both regimes result in the same tax ⚖")
