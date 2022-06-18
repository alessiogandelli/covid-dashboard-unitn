## data source 
url_tot = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
url_region = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv'
url_latest = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv'
# constants
drop_stats = ['stato','casi_da_sospetto_diagnostico', 'casi_da_screening', 
                'note', 'note_test', 'note_casi', 'codice_nuts_1', 'codice_nuts_2']
drop_age = ['zone','sigla','cn1', 'cn2', 'region_name', 'lat', 'long']

col_stats = ['date', 'region_id', 'region_name', 'lat', 'long', 'recovered', 'intensive_care', 
            'hospitalized', 'domestic_isolation', 'total_positive', 'variation_total_positive', 
            'new_positive', 'dimessi_guariti', 'deaths', 'total_cases', 'test', 'tested_cases',
               'new_intensive_care', 'tot_positive_pcr', 'tot_positive_antigenic', 'test_pcr', 'test_antigenic']

col_region = ['region_id', 'cn1', 'zone', 'cn2','region_name', 'sigla', 'lat', 'long', 'age_group', 'population_males', 'population_females', 'population']

group_by_region = ['region_id', 'zone', 'region_name', 'lat', 'long']