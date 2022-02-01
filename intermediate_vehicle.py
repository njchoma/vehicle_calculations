
def get_selling_amt(purchase_cost, depreciation_coef, years_own):
    depreciation_amt = depreciation_coef**years_own
    return purchase_cost * depreciation_amt

def get_fuel_cost(mpg, total_miles, fuel_price_per_gal, mpkw, elec_cost, elec_pct):
    if elec_pct < 1.0:
        gallons_used = (1.0*total_miles) / mpg
        fuel_cost = fuel_price_per_gal * gallons_used * (1.0-elec_pct)
    else:
        fuel_cost = 0.0

    elec_cost = total_miles / mpkw * elec_cost * elec_pct

    return fuel_cost + elec_cost

def compute_loan_cost(P, r, n):
    '''
    P, principal
    r, monthly APR
    n, total number of months
    '''
    monthly_payment = P * (r * (1+r)**n) / ((1+r)**n - 1)
    interest = monthly_payment * n - P
    return interest

def get_costs(all_cars,
              name,
              purchase_cost_no_tax,
              tax_rate,
              miles_per_year,
              insurance_rate,
              starting_mileage,
              mpg,
              fuel_price,
              vehicle_life_in_miles,
              maintenance_per_year,
              apr = 0.02,
              loan_term = 36,
              elec_cost = 1.0,
              elec_pct = 0.0,
              mpkw = 0.1):

    purchase_cost_with_tax = purchase_cost_no_tax * tax_rate
    interest_cost = compute_loan_cost(purchase_cost_with_tax, apr / 12, loan_term)

    insurance_cost = insurance_rate * 2
    fuel_cost = get_fuel_cost(mpg, miles_per_year, fuel_price, mpkw, elec_cost, elec_pct)

    initial_cost = purchase_cost_with_tax + interest_cost
    usage_cost = fuel_cost + maintenance_per_year + insurance_cost

    all_cars[name] = [initial_cost, usage_cost]


def select_car(all_cars, name):
    try:
        initial_cost, usage_cost = all_cars[name]
        return initial_cost, usage_cost
    except Exception as e:
        print(e)
        print("name \"{}\" not found".format(name))
        exit()

def cost_compare(all_cars, carA, carB, loan_term, num_years, opp_cost_rate):
    '''
    ica is initial cost A
    uca is usage cost A
    '''
    assert (loan_term%12) == 0 # loan term must be year multiple

    ica, uca = select_car(all_cars, carA)
    icb, ucb = select_car(all_cars, carB)


    net_gain_a = 0.0

    pct_accrue_per_year = 12.0 / loan_term
    ica_year = ica * pct_accrue_per_year
    icb_year = icb * pct_accrue_per_year

    a_accrued = 0.0
    b_accrued = 0.0

    for i in range(num_years):
        if i*12 >= loan_term:
            ica_year = 0
            icb_year = 0

        year_cost_a = ica_year + uca
        year_cost_b = icb_year + ucb

        year_ab_diff = year_cost_a - year_cost_b
        year_accrued_interest = (opp_cost_rate-1) * (net_gain_a + year_ab_diff/2)
        year_total = year_ab_diff + year_accrued_interest

        net_gain_a += year_total

        print("{:4d}:  {:5.1f} {:6.1f}  {:6.1f} {:5.1f}  {:7.1f} {:6.1f}".format(
                i+1,
                year_cost_a/1000,
                year_cost_b/1000,
                year_ab_diff/1000,
                year_accrued_interest/1000,
                year_total/1000,
                net_gain_a/1000))

        a_accrued = a_accrued*opp_cost_rate + year_cost_a
        b_accrued = b_accrued*opp_cost_rate + year_cost_b

    n = max(len(carA), len(carB))

    print("\nTotal Cost:")
    print("{1:{0}}:  ${2:5.1f}k".format(n, carA, a_accrued/1000))
    print("{1:{0}}:  ${2:5.1f}k".format(n, carB, b_accrued/1000))

    print("\nAvg cost / year:")
    print("{1:{0}}:  ${2:5.1f}k".format(n, carA, a_accrued/1000/num_years))
    print("{1:{0}}:  ${2:5.1f}k".format(n, carB, b_accrued/1000/num_years))


if __name__ == "__main__":

    miles_per_year = 20000
    base_vehicle_life = 300000
    fuel_cost = 4.95
    electricity_cost = 0.16
    tax_rate = 1.07
    loan_term = 72
    apr = 0.0275
    carA = "Model 3"
    carB = "Model 3 SR"

    print("Car A:", carA)
    print("Car B:", carB)
    print("\nUnits: $1/1000")
    print("{:<4} {:>7} {:>6}  {:>5} {:>4}  {:>7} {:>6}".format(
                            'Year',
                            'Ayr',
                            'Byr',
                            'diffYr',
                            'intYr',
                            'YearTot',
                            'Totl'))

    all_cost = []
    all_summary = []


    all_cars = {}
    get_costs(
        all_cars = all_cars,
        name = "Mach E",
        purchase_cost_no_tax = 39000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 600,
        starting_mileage = 0,
        mpg = 1,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        elec_pct = 1.0,
        mpkw = (300 / 91.0),
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 200)

    get_costs(
        all_cars = all_cars,
        name = "Model 3",
        purchase_cost_no_tax = 48000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 600,
        starting_mileage = 0,
        mpg = 1,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        elec_pct = 1.0,
        mpkw = (350 / 82.0),
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 200)

    get_costs(
        all_cars = all_cars,
        name = "Model 3 SR",
        purchase_cost_no_tax = 43000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 600,
        starting_mileage = 0,
        mpg = 1,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        elec_pct = 1.0,
        mpkw = (272 / 50.0),
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 200)

    get_costs(
        all_cars = all_cars,
        name = "Model Y",
        purchase_cost_no_tax = 56000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 600,
        starting_mileage = 0,
        mpg = 1,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        elec_pct = 1.0,
        mpkw = (330 / 82.0),
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 200)

    get_costs(
        all_cars = all_cars,
        name = "Model S",
        purchase_cost_no_tax = 94000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 650,
        starting_mileage = 0,
        mpg = 1,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        elec_pct = 1.0,
        mpkw = (405 / 100.0),
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 200)

    get_costs(
        all_cars = all_cars,
        name = "Cayman",
        purchase_cost_no_tax = 61000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 650,
        starting_mileage = 0,
        mpg = 27,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 500)

    get_costs(
        all_cars = all_cars,
        name = "Prius",
        purchase_cost_no_tax = 32000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 550,
        starting_mileage = 0,
        mpg = 52,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 400)

    get_costs(
        all_cars = all_cars,
        name = "Prius Prime",
        purchase_cost_no_tax = 33000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 550,
        starting_mileage = 0,
        mpg = 52,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        elec_pct = 0.2,
        mpkw = (25.0 / 6.3),
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 400)

    get_costs(
        all_cars = all_cars,
        name = "Ioniq 5",
        purchase_cost_no_tax = 43000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 550,
        starting_mileage = 0,
        mpg = 1,
        fuel_price = electricity_cost,
        elec_cost = electricity_cost,
        elec_pct = 1.0,
        mpkw = (310 / 77.0),
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 200)

    get_costs(
        all_cars = all_cars,
        name = "Rav4 Prime",
         purchase_cost_no_tax = 42000,
         tax_rate = tax_rate,
         miles_per_year = miles_per_year,
         insurance_rate = 600,
         starting_mileage = 0,
         mpg = 40,
         fuel_price = fuel_cost,
         elec_cost = electricity_cost,
         elec_pct = 0.5,
         mpkw = (42.0 / 15),
         vehicle_life_in_miles = base_vehicle_life,
         loan_term = loan_term,
         apr = apr,
         maintenance_per_year = 500)


    get_costs(
        all_cars = all_cars,
        name = "Honda Clarity",
         purchase_cost_no_tax = 21500,
         tax_rate = tax_rate,
         miles_per_year = miles_per_year,
         insurance_rate = 550,
         starting_mileage = 0,
         mpg = 40,
         fuel_price = fuel_cost,
         elec_cost = electricity_cost,
         elec_pct = 0.2,
         mpkw = (47.0 / 16),
         vehicle_life_in_miles = base_vehicle_life,
         loan_term = loan_term,
         apr = apr,
         maintenance_per_year = 500)

    get_costs(
        all_cars = all_cars,
        name = "Civic used",
        purchase_cost_no_tax = 25000,
        tax_rate = 1.00,
        miles_per_year = miles_per_year,
        insurance_rate = 550,
        starting_mileage = 30000,
        mpg = 35,
        fuel_price = fuel_cost+.5,
        elec_cost = electricity_cost,
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 550)

    get_costs(
        all_cars = all_cars,
        name = "Rav4",
        purchase_cost_no_tax = 30000,
        tax_rate = tax_rate,
        miles_per_year = miles_per_year,
        insurance_rate = 600,
        starting_mileage = 0,
        mpg = 40,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 500)

    get_costs(
        all_cars = all_cars,
        name = "Rav4 used",
        purchase_cost_no_tax = 36000,
        tax_rate = 1.0,
        miles_per_year = miles_per_year,
        insurance_rate = 600,
        starting_mileage = 25000,
        mpg = 40,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 500)

    get_costs(
        all_cars = all_cars,
        name = "Civic used old",
        purchase_cost_no_tax = 10000,
        tax_rate = 1.0,
        miles_per_year = 8000,
        insurance_rate = 400,
        starting_mileage = 180000,
        mpg = 38,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        vehicle_life_in_miles = 250000,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 600)

    get_costs(
        all_cars = all_cars,
        name = "Tacoma",
        purchase_cost_no_tax = 11000,
        tax_rate = 1.0,
        miles_per_year = miles_per_year,
        insurance_rate = 600,
        starting_mileage = 0,
        mpg = 18,
        fuel_price = fuel_cost,
        elec_cost = electricity_cost,
        vehicle_life_in_miles = base_vehicle_life,
        loan_term = loan_term,
        apr = apr,
        maintenance_per_year = 800)

    cost_compare(all_cars,
                 carA,
                 carB,
                 loan_term,
                 num_years = int(base_vehicle_life/miles_per_year),
                 opp_cost_rate = 1.04)

