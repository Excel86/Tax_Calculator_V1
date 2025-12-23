# ================== TAX CALCULATOR WITH DETAILED BREAKUP ==================

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
        steps.append(f"• 2,50,001 – 5,00,000 @5%  = ₹{slab_tax:,.2f}")

    if taxable_income > 500000:
        slab = min(taxable_income, 1000000) - 500000
        slab_tax = slab * 0.20
        tax += slab_tax
        steps.append(f"• 5,00,001 – 10,00,000 @20% = ₹{slab_tax:,.2f}")

    if taxable_income > 1000000:
        slab = taxable_income - 1000000
        slab_tax = slab * 0.30
        tax += slab_tax
        steps.append(f"• Above 10,00,000 @30%     = ₹{slab_tax:,.2f}")

    # Rebate u/s 87A (Old Regime)
    rebate = 0
    if taxable_income <= 500000 and tax > 0:
        rebate = min(tax, 12500)
        tax = tax - rebate
        steps.append(f"\nLess: Rebate u/s 87A      : ₹{rebate:,.2f}")


    cess = tax * 0.04
    total_tax = tax + cess

    steps.append(f"\nBasic Tax                : ₹{tax:,.2f}")
    steps.append(f"Health & Edu Cess @4%    : ₹{cess:,.2f}")
    steps.append(f"Total Tax Payable        : ₹{total_tax:,.2f}")

    return taxable_income, tax, cess, total_tax, steps


def calculate_new_regime_tax(income):
    steps = []
    steps.append(f"Gross Income : ₹{income:,.2f}")
    steps.append("Tax Calculation:")

    tax = 0

    if income > 300000:
        slab = min(income, 600000) - 300000
        slab_tax = slab * 0.05
        tax += slab_tax
        steps.append(f"• 3,00,001 – 6,00,000 @5%  = ₹{slab_tax:,.2f}")

    if income > 600000:
        slab = min(income, 900000) - 600000
        slab_tax = slab * 0.10
        tax += slab_tax
        steps.append(f"• 6,00,001 – 9,00,000 @10% = ₹{slab_tax:,.2f}")

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

    # Rebate u/s 87A (New Regime)
    rebate = 0
    if income <= 700000 and tax > 0:
        rebate = min(tax, 25000)
        tax = tax - rebate
        steps.append(f"\nLess: Rebate u/s 87A      : ₹{rebate:,.2f}")

    cess = tax * 0.04
    total_tax = tax + cess

    steps.append(f"\nBasic Tax             : ₹{tax:,.2f}")
    steps.append(f"Health & Edu Cess @4% : ₹{cess:,.2f}")
    steps.append(f"Total Tax Payable     : ₹{total_tax:,.2f}")

    return tax, cess, total_tax, steps


# ================== MAIN PROGRAM ==================

try:

    print("\nSelect Financial Year:")
    print("1. FY 2023-24 (AY 2024-25)")
    print("2. FY 2024-25 (AY 2025-26)")

    fy_choice = int(input("Enter your choice (1/2): "))

    if fy_choice == 1:
        financial_year = "2023-24"
        assessment_year = "2024-25"
    elif fy_choice == 2:
        financial_year = "2024-25"
        assessment_year = "2025-26"
    else:
        print("Invalid FY selection")
        exit()

    income = float(input("Enter Annual Income (₹): "))
    age = int(input("Enter Age: "))

    print("\n1. Old Regime\n2. New Regime\n3. Compare Both")
    choice = int(input("Select option (1/2/3): "))

    deductions = 0
    if choice in [1, 3]:
        sec_80c = float(input("Section 80C: "))
        sec_80d = float(input("Section 80D: "))
        deductions = min(sec_80c, 150000) + sec_80d

    if choice in [1, 3]:
        old_data = calculate_old_regime_tax(income, deductions)

    if choice in [2, 3]:
        new_data = calculate_new_regime_tax(income)


    print(f"\nFINANCIAL YEAR : {financial_year}")
    print(f"ASSESSMENT YEAR: {assessment_year}")

    print("\n================ TAX CALCULATION REPORT ================")

    if choice in [1, 3]:
        print("\n--- OLD REGIME TAX CALCULATION STEPS ---")
        for step in old_data[4]:
            print(step)

    if choice in [2, 3]:
        print("\n--- NEW REGIME TAX CALCULATION STEPS ---")
        for step in new_data[3]:
            print(step)

    if choice == 3:
        print("\n--- BEST OPTION ---")
        if old_data[3] < new_data[2]:
            print("✅ Old Regime is more beneficial")
        elif new_data[2] < old_data[3]:
            print("✅ New Regime is more beneficial")
        else:
            print("⚖ Both regimes are equal")

except ValueError:
    print("Invalid input! Please enter valid numbers.")
