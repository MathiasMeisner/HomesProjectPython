# -*- coding: utf-8 -*-

from .homevaluation import calculate_single_home

def main():
    # Define test values
    municipality = '4700 Næstved'
    squaremeters = 100
    constructionyear = 2015
    energylabel = 'A'

    # Call the function
    adjusted_price = calculate_single_home(municipality, squaremeters, constructionyear, energylabel)

    # Print the result
    print(f"Adjusted price for {squaremeters} sqm home in {municipality} (built in {constructionyear} with energy label {energylabel}): {adjusted_price}")

if __name__ == "__main__":
    main()