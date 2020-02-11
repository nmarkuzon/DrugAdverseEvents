# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from collections import defaultdict
import PyGnuplot as gp

def get_results(r):
    return [(x['term'],x['count']) for x in r.json()['results']] # list comprehension

def make_API_call(url):
    r = requests.get(url)
    results = get_results(r)
    return results[:5]

def get_counts(count_field):
    url_tpl = 'https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20191220]&count={}'
    url = url_tpl.format(count_field)
    return make_API_call(url)
    
def get_country_data(country, count_field):
    url_tpl = 'https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20191220]+AND+occurcountry:%22{}%22&count={}'
    url = url_tpl.format(country, count_field)
    return make_API_call(url)

def get_med_data(country, count_field):
    url_tpl = 'https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20191220]+AND+patient.drug.drugindication:DIABETES++AND+occurcountry:%22{}%22&count={}'
    url = url_tpl.format(country, count_field)
    return make_API_call(url)

def get_drug_indication_data(drug_indication, count_field):
    url_tpl = 'https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20191220]+AND+patient.drug.drugindication.exact:%22{}%22&count={}'
    url = url_tpl.format(drug_indication, count_field)
    return make_API_call(url)


def normalize(top_10, total):
    return [(side_effect, count/total) for (side_effect, count) in top_10]


def convert_to_table(data):
    table = [] 
    side_effects = set() 
    for top_10 in data.values():
        for (side_effect, percentage) in top_10:
            side_effects.add(side_effect)
            
    side_effects_list = list(side_effects)
    printable_side_effects_list = ['"'+side_effect+'"' for side_effect in side_effects_list]
    header = ["Country"] + printable_side_effects_list
    table.append(header)
    for country in data:
        side_effects_dict = defaultdict(int)
        for side_effect, percentage in data[country]:
            side_effects_dict[side_effect] = percentage
        row = ['"'+country+'"'] + [side_effects_dict[side_effect] for side_effect in side_effects_list]
        table.append(row)
        
    return table

def graph(table):
    
    gp.c('set style data histogram')
    gp.c('set style histogram cluster gap 1')
    gp.c('set style fill solid border rgb "black"')
    gp.c('set auto x')
    gp.c('set boxwidth 1.4')
    gp.c('set yrange [0:*]')
    gp.s(table)
    gp.c('set xtics rotate')
    gp.c("plot 'tmp.dat' using 2:xtic(1) title col, '' using 3:xtic(1) title col, '' using 4:xtic(1) title col, '' using 5:xtic(1) title col, '' using 6:xtic(1) title col, '' using 7:xtic(1) title col, '' using 8:xtic(1) title col, '' using 9:xtic(1) title col, '' using 10:xtic(1) title col, '' using 11:xtic(1) title col")
    #print(table)
    
def get_table_data(counts, data_function, count_field, norm = False):
    data = {}
    for (by_variable, total) in counts:
        data_elem = data_function(by_variable, count_field)
        data[by_variable] = normalize(data_elem, total) if norm else data_elem
    return data

def main():
    #multiple calls can be un-commented and run separately 
    country_counts = get_counts('occurcountry')
    data = get_table_data(country_counts, get_country_data, 'patient.reaction.reactionmeddrapt.exact', norm = True)
    #data = get_table_data(country_counts, get_country_data, 'patient.reaction.reactionmeddrapt.exact')
    #data = get_table_data(country_counts, get_country_data, 'patient.drug.medicinalproduct.exact')
    #data = get_table_data(country_counts, get_med_data, 'patient.drug.medicinalproduct.exact', norm = True)
    
    #drug_indication_counts = get_counts('patient.drug.drugindication.exact')
    #data = get_table_data(drug_indication_counts, get_drug_indication_data, 'patient.reaction.reactionmeddrapt.exact')
    
    table = convert_to_table(data)
    graph(table)
    

if __name__ == "__main__":
    main()
 
  
