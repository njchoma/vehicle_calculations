import matplotlib.pyplot as plt

def compute_energy_per_mile(speeds, powers):
    energy_per_mile = [p*1000/s for s,p in zip(speeds, powers)]
    return energy_per_mile

def compute_range(battery_capacity, power):
    ranges = [battery_capacity*1000/p for p in power]
    return ranges

def compute_charge_time(battery_capacity, charge_speed, pct_battery_used):
    to_charge = battery_capacity * pct_battery_used
    charge_time = to_charge / charge_speed
    return charge_time

def compute_time_to_empty(battery_capacity, pct_battery_used, powers):
    energy_avail = battery_capacity * pct_battery_used
    times = [energy_avail / p for p in powers]
    return times

def compute_dist_traveled(time_traveled, speed):
    distance = [t*s for t, s in zip(time_traveled, speed)]
    return distance

def get_real_speed(charge_time, time_traveled, distance):
    real_speed = [d/(t+charge_time) for d, t in zip(distance, time_traveled)]
    return real_speed

def compute_cost(energy_cost, energy_per_mile):
    cost_per_mile = [energy_cost * epm / 1000 for epm in energy_per_mile]
    return cost_per_mile

def print_results(speed,
                  bat_range,
                  charge_rate,
                  charge_time,
                  pct_charge,
                  real_speed,
                  cost_per_dist,
                  time_traveled,
                  trip_dist):
    print("{:.0f} mins required for {:.0f}% charge at {} kW".format(
                    charge_time*60, pct_charge*100, charge_rate))

    print("Trip dist: {} mi".format(trip_dist))
    print("\nmph   mph   mi   $/trip  batHr   tripHr  $save/Hr")
    prev_trip_time = 200.0
    prev_trip_cost = 150.0
    for (s, rs, dist, c, t) in zip(speed, real_speed, bat_range, cost_per_dist, time_traveled):
        d = dist * pct_charge
        trip_time = trip_dist / rs
        trip_cost = trip_dist * c
        extra_cost_per_hr = (trip_cost - prev_trip_cost) / (prev_trip_time - trip_time)
        print("{:3d}:   {:2.0f}  {:3.0f}     ${:3.0f}   {:4.1f}    {:5.1f}     {:5.1f}".format(s, rs, d, trip_cost, t, trip_time, extra_cost_per_hr))

        prev_trip_time = trip_time
        prev_trip_cost = trip_cost
    print()

def main():
    charge_speed = 175 #kW
    battery_capacity = 82 #kWh
    stop_fixed_cost = 3.0/60 # add'l hours per stop
    pct_battery_used = 0.6 # percent (%)
    energy_cost = 0.26 # $/kWh
    trip_dist = 3000 # mi
    speed = [20, 30, 40, 50, 60, 70, 75, 80, 90, 100] # mph
    power_at_speed = [p*.88 for p in [5.5, 8, 10, 13, 17, 23, 26.6, 31, 41, 55]] # kW

    energy_per_mile = compute_energy_per_mile(speed, power_at_speed)
    full_range = compute_range(battery_capacity, energy_per_mile)

    charge_time = compute_charge_time(battery_capacity, charge_speed, pct_battery_used)

    time_traveled = compute_time_to_empty(battery_capacity, pct_battery_used, power_at_speed)


    distance = compute_dist_traveled(time_traveled, speed)
    real_speed = get_real_speed(charge_time+stop_fixed_cost, time_traveled, distance)

    cost_per_dist = compute_cost(energy_cost, energy_per_mile)

    print_results(speed,
                  full_range,
                  charge_speed,
                  charge_time,
                  pct_battery_used,
                  real_speed,
                  cost_per_dist,
                  time_traveled,
                  trip_dist)

    cost = [c*trip_dist for c in cost_per_dist]
    plt.plot(speed, cost)
    plt.xlabel("Real speed (mph)")
    plt.ylabel("$ / {} mi".format(trip_dist))
    plt.xlim([0, max(speed)*1.10])
    plt.ylim([min(cost)*.9, max(cost)*1.10])
    plt.show()

if __name__ == "__main__":
    main()
