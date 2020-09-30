import spacy
from selenium.webdriver.chrome.options import Options
import random
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import time
nlp = spacy.load('de_core_news_sm') #loaded once

def parse_city(body):
    doc = nlp(body)
    for ent in doc.ents:
        if ent.label_ == 'LOC':
            return ent.text
    return ""


def parse_street(body):
    found = re.findall('\s+\S [0-9]{1,3}', body)
    if len(found) > 0:
        found = found[0]
    else:
        return ""
    if found:
        return found
    return ""


def get_by_text(elems, text):
    for elem in elems:
        if elem.text == text:
            return elem
    return None


def extract_individual(text):
    email = ''
    plz = ''

    for word in text.split(' '):
        if '@'in word:
            email = word
        if len(word) == 5:
            try:
                plz = int(word)
                plz = word
            except:
                pass
    city = parse_city(text)
    street = parse_street(text)
    return email, plz, city, street


def extract_data(driver, link):
    driver.get(link)
    try:
        elem = driver.find_element_by_class_name('iconlist-text')
    except NoSuchElementException:
        time.sleep(1)
        elem = driver.find_element_by_class_name('iconlist-text')
    name = elem.find_element_by_tag_name('span').text
    name = name.split(' ')
    if len(name) > 0:
        first_name = name[0]
    else:
        first_name = ''
    last_name = ''
    if len(name) > 1:
        last_name = ' '.join(name[1:])
    angaben = driver.find_element_by_link_text('Rechtliche Angaben')
    driver.execute_script("arguments[0].click();", angaben)
    
    angaben = driver.find_element_by_id('viewad-imprint-text')
    description = angaben.get_attribute('innerHTML')
    text = angaben.text.replace('\n', ' ')
    email, plz, city, street = extract_individual(text)
    try:
        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'description': description,
            'link': link,
            'plz': plz,
            'city': city,
            'street': street,
        }
    except Exception as e:
        print(e)
        return None


def acquire_data(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # '/home/chromedriver'
    driver = webdriver.Chrome('/home/chromedriver', chrome_options=chrome_options)
    #driver = webdriver.Chrome('/home/aliwo/PycharmProjects/ebaycrawler/chromedriver', chrome_options=chrome_options)
    driver.get(url)
    elems = driver.find_elements_by_class_name('ellipsis')
    # get links
    elems = [elem.get_attribute('href') for elem in elems]
    results = list()
    for elem in elems:
        results.append(extract_data(driver, elem))
    return results


def acquire_links():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # '/home/chromedriver'
    driver = webdriver.Chrome('/home/chromedriver', chrome_options=chrome_options)
    #driver = webdriver.Chrome('/home/aliwo/PycharmProjects/ebaycrawler/chromedriver', chrome_options=chrome_options)
    print("start acquiring links")
    ebay = driver.get('https://www.ebay-kleinanzeigen.de/')
    dienstleistungen = "Dienstleistungen"
    a = driver.find_elements_by_css_selector('a.treelist-headline')
    elem = get_by_text(a, dienstleistungen)
    driver.execute_script("arguments[0].click();", elem)
    elems = driver.find_elements_by_css_selector('a')
    gewerblich = 'Gewerblich'
    elem = get_by_text(elems, gewerblich)
    try:
        driver.execute_script("arguments[0].click();", elem)
    except JavascriptException:
        time.sleep(1)
        driver.execute_script("arguments[0].click();", elem)
    next = driver.find_element_by_class_name('pagination-next')
    next.click()
    # https://www.ebay-kleinanzeigen.de/s-dienstleistungen/anbieter:gewerblich/seite:2/c297
    sites = list()
    url = driver.current_url
    url = url.split('/')
    url[-2] = 'seite:{page}'
    url = '/'.join(url)
    while len(sites) < 10:
        new_page = random.randint(1, 50)
        new_url = url.format(page=new_page)
        if not new_url in sites:
            print("link {new_url} added".format(new_url=str(new_url)))
            sites.append(new_url)
    from joblib import Parallel, delayed
    results = Parallel(n_jobs=-1)(delayed(acquire_data)(url) for url in sites)
    return results[0]
        # new_user = EbayUser(first_name=first_name, last_name=last_name,
        #                     email=email, description=description, link=link,
        #                     plz=plz, city=city, street=street)
        # new_user.save()
        # return new_user


def acquire():
    length = EbayUser.objects.filter(sent=False, cleaned=False, blacklisted=False).count()
    while length < 500:
        try:
            acquire_data()
        except Exception as e:
            print(e)
            pass
        length = EbayUser.objects.filter(sent=False, cleaned=False, blacklisted=False).count()




