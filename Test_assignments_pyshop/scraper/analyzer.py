'''
Модуль анализа скрапированных данных
'''

import pandas as pd
from scraper import scrap_em


def analyze_distribution(scraped_list):
    '''
    Get distribution of OS versions from list of dicts, return pandas.dataframe in sorted order
        Parameters:
            scraped_list (list[dicts]): list of dicts
        Return:
            dup_values (pandas.dataframe): sorted(descending) dataframe of os version distribution
    '''
    framed_data = pd.DataFrame(scraped_list)
    dup_values = framed_data.groupby('ver').size().to_frame('frequency')
    return dup_values.sort_values(by = 'frequency', ascending = False)

def main():
    '''
    Get distribution of os versions of top 100 smartphones on Ozon
    in sorted manner and print it in console
    '''
    scrap_list = scrap_em(100)
    print(analyze_distribution(scrap_list))

if __name__ == '__main__':
    main()
