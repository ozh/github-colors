import sys
import requests
import re
from bs4 import BeautifulSoup
from time import sleep # sleep(2) # Time in seconds.


def get_soup( url ):
    try:
        r = requests.get( url )
    except:
        sys.exit( "Request fatal error :  %s" % sys.exc_info()[1] )
        
    if r.status_code != 200:
        sys.exit( "Request error at '%s' (status: %s)" % ( url, r.status_code ) )
    return BeautifulSoup( r.text )


def get_links_name_href( url, pattern ):
    """Return array of {"name":"some name", "url":"/some/url"} 

    Keyword arguments:
    url      -- url to parse
    pattern  -- HTML elements to traverse, eg "div.select-menu-list a.select-menu-item-text.js-select-button-text"
                in /trending: div.select-menu-list a.select-menu-item-text.js-select-button-text
                in /trending?l=php: ol.repo-leaderboard-list li a.repository-name
    """
    soup = get_soup( url )
    links = soup.select( pattern )
    # for link in links:
        # print( link.string, link['href'] )
    # result = [ {"name": link.string, "url": link['href'] } for link in links ]
    if links[0].string:
        result = {}
        for link in links:
            result[ link.string ] = { "url" : link['href'] }
    else:
        result = [ link['href'] for link in links ]
    return( result )


def get_colors( url ):
    """Return lang & color
    
    From /owner/repo: match all "ol.repository-lang-stats-numbers li" where each <li> is like: 
    <li>
        <a href="/owner/repo/search?l=php">
            <span style="background-color:#f7df1e;" class="color-block language-color"></span>
            <span class="lang">PHP</span>
            <span class="percent">16.6%</span>
        </a>
    </li>
    """
    soup = get_soup( url )
    stats = soup.select( "ol.repository-lang-stats-numbers li" )
    for stat in stats:
        spans = stat.find_all('span')
        color = re.findall( '\#\w+', spans[0]['style'] )[0]
        lang  = spans[1].string
        print( lang, color )


langs = get_links_name_href( "http://127.0.0.1/fake-trending/trending.html", "div.select-menu-list a.select-menu-item-text.js-select-button-text" )
print( langs['Common Lisp'] )
    
# repos = get_links_name_href( "http://127.0.0.1/fake-trending/trending-php.html", "ol.repo-leaderboard-list li a.repository-name" )
# print( repos )

"""
colors = get_colors( "http://127.0.0.1/fake-trending/repo.html" )
"""
