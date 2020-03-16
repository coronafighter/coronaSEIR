import json
import world_data

with open('country-by-population.json') as f:
    countryByPopulationJson = json.loads(f.read())

countryPopulation = {}
for item in countryByPopulationJson:
    if not item['population']:
        continue
    countryPopulation[item['country']] = int(item['population'])

# some fixes
countryPopulation['US'] = countryPopulation['United States']
countryPopulation['Czechia'] = countryPopulation["Czech Republic"]
countryPopulation['Korea, South'] = countryPopulation['South Korea']
countryPopulation['Korea, North'] = countryPopulation['North Korea']
countryPopulation['Taiwan*'] = 23574274
countryPopulation['Serbia'] = 7057666
# ...

countries, provinces = world_data.get_countries_provinces()

cp2 = {}
for country in countries:
    if country in countryPopulation:
        cp2[country] = countryPopulation[country]
    else:
        for country2 in countryPopulation:
            if country in country2:
                cp2[country] = countryPopulation[country2]

def get_population(country):
    return cp2[country]

def get_all_population_data():
    return cp2

if __name__ == '__main__':
    
    for country in countries:
        if not country in cp2:
            print(country)
    
    s = ''
    for c in countryPopulation.keys():
        if not c in countries:
            s += " %s " % c
    print(s)

    
# region population from wikipedia

# import wptools

# def get_population(region):
#     page = wptools.page(region)
#     page.get_parse(show=True)
#     global infobox
#     infobox = page.data['infobox']
#     for s in ['population_estimate', 'population']:
#         try:
#             population = infobox[s]
#             continue
#         except KeyError:
#             pass
#     print(region + " p: " + str(population))
#     return population


#for country in countries:
#    get_population(country)
#get_population('China')

