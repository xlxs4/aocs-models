from skyfield.api import load


def main():
    stations_url = 'http://celestrak.org/NORAD/elements/stations.txt'
    satellites = load.tle_file(stations_url)

    by_name = {sat.name: sat for sat in satellites}

    eph = load('de421.bsp')
    satellite = by_name['ISS (ZARYA)']

    ts = load.timescale()
    two_hours = ts.utc(2024, 7, 1, 0, range(0, 120, 20))
    sunlit = satellite.at(two_hours).is_sunlit(eph)

    for ti, sunlit_i in zip(two_hours, sunlit):
        print(
            '{}  {} is in {}'.format(
                ti.utc_strftime('%Y-%m-%d %H:%M'),
                satellite.name,
                'sunlight' if sunlit_i else 'shadow',
            )
        )


if __name__ == "__main__":
    main()
