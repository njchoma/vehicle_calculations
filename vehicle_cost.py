def get_selling_amt(purchase_cost,
                    depreciation_coef,
                    years_own,
                    mileage_deprec_importance,
                    selling_mileage,
                    vehicle_life_miles):
    deprec_age = depreciation_coef**years_own
    deprec_mileage = 1 - min(1.0, selling_mileage*1.0 / vehicle_life_miles)


    deprec_factor = deprec_age * (1-mileage_deprec_importance) + deprec_mileage * mileage_deprec_importance
    
    sell_price = purchase_cost * deprec_factor
    return sell_price


def get_fuel_cost(mpg, total_miles, fuel_price_per_gal, miles_per_kwh, elec_cost, elec_pct):
    if elec_pct < 1.0:
        gallons_used = (1.0*total_miles) / mpg
        fuel_cost = fuel_price_per_gal * gallons_used * (1.0-elec_pct)
    else:
        fuel_cost = 0.0

    elec_cost = total_miles / miles_per_kwh * elec_cost * elec_pct

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

def main(all_cost,
         all_summary,
         name,
         purchase_cost_no_tax,
         tax_rate,
         depreciation_coef,
         miles_per_year,
         insurance_rate,
         starting_mileage,
         mpg,
         fuel_price,
         selling_mileage,
         maintenance_per_year,
         mileage_deprec_importance = 0.3,
         apr = 0.03,
         loan_term = 60,
         elec_cost = 1.0,
         elec_pct = 0.0,
         miles_per_kwh = 0.1,
         full_maintenance_age = 15,
         selling_amt = None,
         is_new = False,
         vehicle_life_miles = 250000):
    miles_driven = selling_mileage - starting_mileage
    years_own = (miles_driven) / (1.0 * miles_per_year)

    purchase_cost_with_tax = purchase_cost_no_tax * tax_rate
    if selling_amt is None:
        selling_amt = get_selling_amt(purchase_cost_no_tax,
                                      depreciation_coef,
                                      years_own,
                                      mileage_deprec_importance,
                                      selling_mileage,
                                      vehicle_life_miles)

    insurance_cost = insurance_rate * 2 * years_own


    pct_mileage_maintenance_done = min(1.0, float(selling_mileage-starting_mileage) / vehicle_life_miles)
    mileage_maintenance_cost = full_maintenance_age * maintenance_per_year * pct_mileage_maintenance_done

    time_maintenance_cost = maintenance_per_year * years_own
    maintenance_cost = (time_maintenance_cost + mileage_maintenance_cost) / 2

    fuel_cost = get_fuel_cost(mpg, miles_driven, fuel_price, miles_per_kwh, elec_cost, elec_pct)
    interest_cost = compute_loan_cost(purchase_cost_with_tax, apr / 12, loan_term)

    total_cost = ( purchase_cost_with_tax 
                 + insurance_cost
                 + fuel_cost
                 + maintenance_cost
                 + interest_cost
                 - selling_amt)
    cost_per_mile = total_cost / miles_driven
    cost_per_year = total_cost / years_own


    constant_costs = fuel_cost + maintenance_cost + insurance_cost
    cost_at_loan_payoff = purchase_cost_with_tax + interest_cost + (constant_costs * (loan_term/12) / years_own)


    new_indicator = '*' if is_new else ' '
    summary = "{:>3}  {:<20}  {:5.2f}  {:5.1f}  {:4.0f}  {:6.0f}  {:5.1f}  {:5.1f} {:5.1f}".format(
                                                     new_indicator,
                                                     name,
                                                     cost_per_mile,
                                                     cost_per_year/1000,
                                                     cost_per_year/12,
                                                     years_own,
                                                     selling_amt/1000,
                                                     cost_per_year/1000 * 10,
                                                     cost_at_loan_payoff/1000)
    all_cost.append(cost_per_mile)
    all_summary.append(summary)
    print(name, int(purchase_cost_no_tax * (tax_rate-1)), fuel_cost / years_own)
    return all_cost, all_summary

def print_summary(all_cost, all_summary):
    sorted_keys = sorted(range(len(all_cost)), key=all_cost.__getitem__)
    for k in sorted_keys:
        print(all_summary[k])

if __name__ == "__main__":

    miles_per_year = 10000
    base_depreciation = 0.88 # add'l deprec. vals based on caredge.com
    base_selling_mileage = 100000
    fuel_cost = 3.05
    electricity_cost = 0.10

    print("{:>3}  {:<20} {:>6} {:>6} {:>5} {:>7} {:>6} {:>6} {:>6}".format(
                            'new',
                            'NAME',
                            '$/mi',
                            '$k/yr',
                            '$/mo',
                            'yr own',
                            '$sell',
                            '$10yr',
                            '$edln'))

    all_cost = []
    all_summary = []

    all_cost, all_summary = main(all_cost,
         all_summary,
         'tesla',
         purchase_cost_no_tax = 47000,
         tax_rate = 1.09,
         depreciation_coef = .89,
         miles_per_year = miles_per_year,
         insurance_rate = 650,
         starting_mileage = 0,
         mpg = 1,
         fuel_price = electricity_cost,
         elec_cost = electricity_cost,
         elec_pct = 1.0,
         miles_per_kwh = (300 / 85.0),
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'civic',
         purchase_cost_no_tax = 21718,
         tax_rate = 1.09,
         depreciation_coef = .89,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 38,
         fuel_price = fuel_cost + 0.4,
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'civic_short_term',
         purchase_cost_no_tax = 21718,
         tax_rate = 1.09,
         depreciation_coef = .95,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 38,
         fuel_price = fuel_cost + 0.4,
         selling_mileage = 25000,
         is_new = True,
         maintenance_per_year = 300)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'civic_value',
         purchase_cost_no_tax = 20500,
         tax_rate = 1.00,
         depreciation_coef = .89,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 25000,
         mpg = 38,
         fuel_price = fuel_cost + 0.4,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 450)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'prius',
         purchase_cost_no_tax = 24000,
         tax_rate = 1.09,
         depreciation_coef = .876,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 54,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'fit',
         purchase_cost_no_tax = 17000,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 34,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'clarity',
         purchase_cost_no_tax = 19500,
         tax_rate = 1.13,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 550,
         starting_mileage = 0,
         mpg = 42,
         fuel_price = fuel_cost,
         elec_cost = electricity_cost,
         elec_pct = 0.3,
         miles_per_kwh = (47.0 / 16),
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 500)

#     all_cost, all_summary = main(all_cost,
#          all_summary,
#          'scion',
#          purchase_cost_no_tax = 3000,
#          tax_rate = 1.00,
#          depreciation_coef = base_depreciation,
#          miles_per_year = miles_per_year,
#          insurance_rate = 450,
#          starting_mileage = 150000,
#          mpg = 27,
#          fuel_price = fuel_cost,
#          selling_mileage = base_selling_mileage,
#          maintenance_per_year = 1500)
# 
#     all_cost, all_summary = main(all_cost,
#          all_summary,
#          'tercel',
#          purchase_cost_no_tax = 3000,
#          tax_rate = 1.09,
#          depreciation_coef = base_depreciation,
#          miles_per_year = miles_per_year,
#          insurance_rate = 450,
#          starting_mileage = 150000,
#          mpg = 35,
#          fuel_price = fuel_cost,
#          selling_mileage = base_selling_mileage,
#          maintenance_per_year = 1200)
# 
#     all_cost, all_summary = main(all_cost,
#          all_summary,
#          'cruze',
#          purchase_cost_no_tax = 4000,
#          tax_rate = 1.00,
#          depreciation_coef = base_depreciation,
#          miles_per_year = miles_per_year,
#          insurance_rate = 500,
#          starting_mileage = 150000,
#          mpg = 37,
#          fuel_price = fuel_cost,
#          selling_mileage = 200000,
#          maintenance_per_year = 1500)

#     all_cost, all_summary = main(all_cost,
#          all_summary,
#          'd21',
#          purchase_cost_no_tax = 1200,
#          tax_rate = 1.09,
#          depreciation_coef = .97,
#          miles_per_year = miles_per_year,
#          insurance_rate = 500,
#          starting_mileage = 180000,
#          mpg = 24,
#          fuel_price = fuel_cost,
#          selling_mileage = base_selling_mileage,
#          maintenance_per_year = 1100)

    all_cost, all_summary = main(all_cost,
         all_summary,
         '86',
         purchase_cost_no_tax = 29000,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 600,
         starting_mileage = 0,
         mpg = 30,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 500)

#     all_cost, all_summary = main(all_cost,
#          all_summary,
#          'tacoma_99',
#          purchase_cost_no_tax = 12000,
#          tax_rate = 1.09,
#          depreciation_coef = 0.98,
#          miles_per_year = miles_per_year,
#          insurance_rate = 600,
#          starting_mileage = 205000,
#          mpg = 19,
#          fuel_price = fuel_cost,
#          selling_mileage = base_selling_mileage+100000,
#          maintenance_per_year = 1000)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'sienna',
         purchase_cost_no_tax = 25000,
         tax_rate = 1.09,
         depreciation_coef = .862,
         miles_per_year = miles_per_year,
         insurance_rate = 550,
         starting_mileage = 30000,
         mpg = 26,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'cayman',
         purchase_cost_no_tax = 59000,
         tax_rate = 1.09,
         depreciation_coef = .875,
         miles_per_year = miles_per_year,
         insurance_rate = 650,
         starting_mileage = 0,
         mpg = 28,
         fuel_price = fuel_cost+0.3,
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 1400)

#     all_cost, all_summary = main(all_cost,
#          all_summary,
#          'bmw',
#          purchase_cost_no_tax = 10000,
#          tax_rate = 1.09,
#          depreciation_coef = .845,
#          miles_per_year = miles_per_year,
#          insurance_rate = 550,
#          starting_mileage = 100000,
#          mpg = 28,
#          fuel_price = fuel_cost+0.3,
#          selling_mileage = base_selling_mileage,
#          maintenance_per_year = 2000)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'caym usd',
         purchase_cost_no_tax = 20000,
         tax_rate = 1.09,
         depreciation_coef = .896,
         miles_per_year = miles_per_year,
         insurance_rate = 600,
         starting_mileage = 60000,
         mpg = 28,
         fuel_price = fuel_cost+0.3,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 2200)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'mustang gt',
         purchase_cost_no_tax = 30000,
         tax_rate = 1.06,
         depreciation_coef = .897,
         miles_per_year = miles_per_year,
         insurance_rate = 650,
         starting_mileage = 0,
         mpg = 24,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 650)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'focus',
         purchase_cost_no_tax = 18500,
         tax_rate = 1.06,
         depreciation_coef = base_depreciation-0.05,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 38,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 550)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'miata',
         purchase_cost_no_tax = 25700,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 33,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 450)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'crosstrek',
         purchase_cost_no_tax = 22000,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 525,
         starting_mileage = 0,
         mpg = 34,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 500)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'impreza',
         purchase_cost_no_tax = 18000,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 36,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 500)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'yaris',
         purchase_cost_no_tax = 17000,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 38,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'crv_hybrid',
         purchase_cost_no_tax = 30870,
         apr=0.0001,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 38,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'rav4_hybrid',
         purchase_cost_no_tax = 27550,
         tax_rate = 1.09,
         depreciation_coef = .889,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 38,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'rav4_non_hybrid',
         purchase_cost_no_tax = 26700,
         tax_rate = 1.09,
         depreciation_coef = .889,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 30,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'camry_hybrid',
         purchase_cost_no_tax = 23070,
         tax_rate = 1.09,
         depreciation_coef = .865,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 48,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'corolla_hybrid',
         purchase_cost_no_tax = 20620,
         tax_rate = 1.09,
         depreciation_coef = .90,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 50,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'corolla_non_hybrid',
         purchase_cost_no_tax = 16422,
         tax_rate = 1.09,
         depreciation_coef = .902,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 36,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'accord_hybrid',
         purchase_cost_no_tax = 26600,
         apr=0.009,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 48,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'niro_phev_no_plug',
         purchase_cost_no_tax = 26500-4500,
         apr=0.009,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 45,
         fuel_price = fuel_cost,
         is_new = True,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 550)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'niro_phev_with_plug',
         purchase_cost_no_tax = 26500-4500,
         tax_rate = 1.09,
         depreciation_coef = base_depreciation,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 45,
         fuel_price = fuel_cost,
         elec_cost = electricity_cost,
         elec_pct = 0.2,
         miles_per_kwh = (26.0 / 8),
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 550)

#     all_cost, all_summary = main(all_cost,
#          all_summary,
#          'old_accord',
#          purchase_cost_no_tax = 300,
#          apr=0.000001,
#          tax_rate = 1.09,
#          depreciation_coef = base_depreciation,
#          miles_per_year = miles_per_year,
#          insurance_rate = 500,
#          starting_mileage = 150000,
#          mpg = 23,
#          fuel_price = fuel_cost,
#          selling_mileage = base_selling_mileage,
#          maintenance_per_year = 1250)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'corolla_hatch',
         purchase_cost_no_tax = 21600,
         tax_rate = 1.09,
         depreciation_coef = .902,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 0,
         mpg = 38,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 400)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'civic_2013',
         purchase_cost_no_tax = 10600,
         tax_rate = 1.09,
         depreciation_coef = .91,
         miles_per_year = miles_per_year,
         insurance_rate = 550,
         starting_mileage = 94000,
         mpg = 35,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 650)

    all_cost, all_summary = main(all_cost,
         all_summary,
         '2016_corolla',
         purchase_cost_no_tax = 11700,
         tax_rate = 1.09,
         depreciation_coef = .917,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 70000,
         mpg = 35,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 650)

    all_cost, all_summary = main(all_cost,
         all_summary,
         '2014_corolla',
         purchase_cost_no_tax = 9000,
         tax_rate = 1.09,
         depreciation_coef = .917,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 85000,
         mpg = 35,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 700)

    all_cost, all_summary = main(all_cost,
         all_summary,
         '2017_civic',
         purchase_cost_no_tax = 12000,
         tax_rate = 1.09,
         depreciation_coef = .91,
         miles_per_year = miles_per_year,
         insurance_rate = 500,
         starting_mileage = 55000,
         mpg = 38,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         maintenance_per_year = 700)

    all_cost, all_summary = main(all_cost,
         all_summary,
         'tacoma',
         purchase_cost_no_tax = 34600,
         tax_rate = 1.09,
         depreciation_coef = .927,
         miles_per_year = miles_per_year,
         insurance_rate = 550,
         starting_mileage = 0,
         mpg = 20,
         fuel_price = fuel_cost,
         selling_mileage = base_selling_mileage,
         is_new = True,
         maintenance_per_year = 500)

    # all_cost, all_summary = main(all_cost,
    print_summary(all_cost, all_summary)

