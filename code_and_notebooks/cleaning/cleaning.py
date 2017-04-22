from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz, process
from nltk.tokenize import wordpunct_tokenize
from pandas_profiling import ProfileReport
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import re

stop_words = set(stopwords.words('english')) # srop words list
sns.set_style('whitegrid')
IT_stop = stop_words.copy()
IT_stop.discard('it')


def fuzzy_match(city,matchs_list):
    """returns the the most likely matching value if not, it returns the city_name asis"""
    match = process.extractOne(city, matchs_list)
    if match[1] > 60:
        return match[0]
    else:
        return city


def parse_html(html_doc):
    """returns a string of parsed html with all stop words removed"""
    warnings.filterwarnings("ignore")
    try:
        soup = BeautifulSoup(html_doc, 'html.parser')
        list_of_words = [i for i in wordpunct_tokenize(
        re.sub(r'\d+|[^\w\s]', '', (soup.text.lower()))) if i not in stop_words ]
        return ' '.join(map(lambda x: '%s' % x, list_of_words))
    except TypeError:
        return np.NaN


def clean_text(row,  tech_list):
    """returns a string of parsed html with all stop words removed"""
    row = str(row)
    try:
        list_of_words = [i for i in wordpunct_tokenize(
        re.sub(r'\d+|[^\w\s]', ' ', (row.lower()))) if i in tech_list]
        astring = ' '.join(map(lambda x: '%s' % x, list_of_words))
        return astring
    except TypeError:
        return np.NaN


def mean_exper(row):
    if fuzz.partial_ratio(row,['123456789']) > 0:
        try:
            _min = list(re.findall('\d+',row))[0]
        except IndexError:
            return np.nan
        try:
            _max = list(re.findall('\d+',row))[1]
        except IndexError:
            return int(_min)
        return (int(_min)+int(_max))/2


def clean_expr_years(row):
    if fuzz.partial_ratio(row,['123456789']) > 0:
        try:
            _min = list(re.findall('\d+',row))[0]
        except IndexError:
            return np.nan
        try:
            _max = list(re.findall('\d+',row))[1]
        except IndexError:
            return _min
        return '{}-{}'.format(_min,_max)


def min_max_salary(to_mach,thresh=60):
    listo = []
    for i in data.displayed_job_title:
        if fuzz.partial_ratio(to_mach,i) > thresh:
            listo.append(i)
    sub3 = data[data.displayed_job_title.isin(listo)]
    _shape = sub3.shape
    _min = sub3.salary_min.mean()
    _max = sub3.salary_max.mean()
    return """based on {} results the min salary is {} and the max is {} for jobs the contains {} keyword""".format(_shape[0],_min,_max,to_mach)


def rec(job,num,match_list):
    matches = process.extract(query=job,limit=num, choices=match_list, scorer=fuzz.partial_ratio)
    return pd.DataFrame(matches).ix[:,0]


def job_plot(data,variable,cat_num=10):
    """this function takes a categorical variable and the dataframe it's in and the number of levels
    and it returns a barplot visualization """
    my_colors = [(x/12.0, x/25.0, 0.5) for x in range(cat_num)]
    return data[variable].value_counts().head(cat_num).plot(kind='bar',
                                                            figsize=(15,6),
                                                            color=my_colors,
                                                            title = 'the most frequent {} classes of the {} variable'.format(cat_num,variable))
