# World War Bot

Dumb algorithm for finding the ultimate warmonger

I stole the country data from https://github.com/lorey/list-of-countries

The procedure works as follows:

        - Pick a random country
        - Pick a random neighbour of that country
        - Choose a probability of victory for the countries based on relative population
        - Choose a winner based on a random number choice and the calculated probability of victory
        - Transfer the loser's population and borders to the winner

    Repeat until only one country remains.



Performing this procedure 10,000 times returns the following rankings:

China: 6907
India: 2419
United States: 539
Brazil: 59
Russia: 12
Nigeria: 7
Germany: 7
Pakistan: 7
Ethiopia: 6
United Kingdom: 5
Egypt: 5
Dominican Republic: 4
Democratic Republic of the Congo: 4
Guadeloupe: 3
France: 3
Colombia: 3
Iran: 2
Ivory Coast: 1
Sint Maarten: 1
Poland: 1
South Africa: 1
Turkey: 1
Spain: 1
Kenya: 1
Argentina: 1
