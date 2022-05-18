def get_charge_time(speed, efficiency, charge_rate, T):
    R = speed * efficiency / charge_rate # no units
    charge_time = T * R / (1+R) # hours
    return charge_time

def miles_per_day(speed, efficiency, charge_rate, T):
    charge_time = get_charge_time(speed, efficiency, charge_rate, T)
    mpd = speed * (T - charge_time)
    kwh = mpd * efficiency
    print("{:3d}  {:3.0f}  {:4.1f}  {:4.1f}  {:4.0f}  {:3.0f}".format(
                speed, 1000*efficiency, T-charge_time, charge_time, mpd, kwh))
    return mpd

def time_traveled(s, e, r, c, d):
    E = d * e
    tc = max(0, (E - c) / r)
    td = d / s
    T = tc + td
    print("{:3d}  {:3.0f}  {:4.1f}  {:4.1f}  {:4.1f}  {:3.0f}  {:3.0f}".format(s, 1000*e, td, tc, T, E, max(0, E-c)))


def main(charge_rate, speed, efficiency, T, dist_travel=372, start_kwh=65):
    print("Travel for {} hours".format(T))
    print("  s    R   t_d   t_c     M  kWh")
    for s, e in zip(speed, efficiency):
        mpd = miles_per_day(s, e, charge_rate, T)

    print("\nDrive {} miles".format(dist_travel))
    print("  s    R   t_d   t_c     T  kWh  sup")
    for s, e in zip(speed, efficiency):
        time_traveled(s, e, charge_rate, start_kwh, dist_travel)

if __name__ == "__main__":
    charge_rate = 8 # kW
    speed = [30, 45, 50, 55, 60, 65, 70, 75, 80, 100] # mph
    efficiency = [.129, .159, .174, .190, .208, .227, .249, .272, .297, .412] # kWh/mi
    # efficiency = [2 * e for e in efficiency] # R1S
    # efficiency = [1.5 * e for e in efficiency] # bikes
    # efficiency = [.97 * e for e in efficiency] # psi
    T = 23 # nb hours per day

    main(charge_rate, speed, efficiency, T)
