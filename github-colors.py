import sys
import requests
import re
import collections
import json
from bs4 import BeautifulSoup
from time import sleep

langs = {}

def get_soup( url ):
    """Return beautifulsoup object from URL body, or False if page not found

    Keyword arguments:
    url -- url to parse
    """
    try:
        r = requests.get( url )
        # Delay to avoid getting banned
        sleep( 2 )
    except:
        sys.exit( "Request fatal error :  %s" % sys.exc_info()[1] )
        
    if r.status_code != 200:
        # some repo, although listed as "Trending", can be actual 404
        return False

    return BeautifulSoup( r.text )


def get_links_name_href( url, pattern ):
    """Return array of {"name":"some name", "url":"/some/url"} 

    Keyword arguments:
    url      -- url to parse
    pattern  -- HTML elements to traverse, eg "div.select-menu-list a.select-menu-item-text.js-select-button-text"
                1) in /trending: div.select-menu-list a.select-menu-item-text.js-select-button-text
                2) in /trending?l=php: ol.repo-leaderboard-list li a.repository-name
    """
    soup = get_soup( url )
    if soup == False:
        print( "No repo found!" );
        return False

    links = soup.select( pattern )
    if links == []:
        print( "No repo found!" );
        return False
    
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
    global langs
    
    soup = get_soup( url )
    stats = soup.select( "ol.repository-lang-stats-numbers li" )
    found = False
    for stat in stats:
        spans = stat.find_all('span')
        try:
            # this block will throw an exception if the regexp fails, meaning probably "Other" lang
            color = re.findall( '\#\w+', spans[0]['style'] )
            if color == []:
                color = "#CCCCCC"
            else:
                color = color[0]
            lang  = spans[1].string
            if lang not in langs:
                langs[lang] = {}
            langs[lang]["color"] = color
            found = True
            print( "   %s: %s " % ( lang, color ) )
        except:
            pass
    return found


def run():
    global langs

    # Get list of all langs
    print( "Getting list of languages ..." )
    langs = get_links_name_href( "http://github.com/trending", "div.select-menu-list a.select-menu-item-text.js-select-button-text" )
    lang_count = len( langs )
    print( "Found %d languages" % lang_count )

    # For each lang, get a couple trending repo if we don't have its color already
    i = 0
    for lang in langs:
        i += 1
        print( "[%d/%d] What is the color for '%s' ?" % ( i, lang_count, lang ) )
        try:
            # if we already know the color, do nothing
            i_can_haz_color = langs[lang]["color"]
            print( "   I already know %s color" % lang )
        except:
            # otherwise, fetch it
            print( "   Searching a couple '%s' repos" % lang )
            repos = get_links_name_href( langs[lang]['url'], "ol.repo-leaderboard-list li a.repository-name" )
            if repos != False:
                for repo in repos:
                    repo_url = "https://github.com" + repo
                    print( "   Fetching colors from %s" % repo_url )
                    if get_colors( repo_url ) == True:
                        print( "   Nice colors!" )
                        break;
                    else:
                        print( "   No color found here, searching next repo" )

    langs = order_by_keys( langs )
    print( "Writing a new JSON file ..." )
    write_json( langs )
    print( "Updating the README ..." )
    write_readme( langs )
    print( "All done!" )


def order_by_keys( dict ):
    """
    Sort a dictionary by keys, case insensitive ie [ Ada, eC, Fortran ]
    Default ordering, or using json.dump with sort_keys=True, produces [ Ada, Fortran, eC ]
    """
    from collections import OrderedDict
    return OrderedDict( sorted( dict.items(), key=lambda s: s[0].lower() ) )


def write_json( dict, filename = 'colors.json' ):
    """
    Write a JSON file from a dictionary
    """
    from collections import OrderedDict
    dict = order_by_keys( dict )
    f = open( filename, 'w' )
    f.write( json.dumps( dict, indent=4 ) + '\n' )
    f.close()


def write_readme( dict, filename = 'README.md' ):
    f = open( filename, 'w' )
    f.write( "# Colors of programming languages on Github \n\n" )

    colorless = {}

    for lang in dict:
        if "color" not in dict[lang]:
            colorless[lang] =  dict[lang]["url"]
        else:
            # dict[lang]["color"][1:] : remove first char ("#") from the color ("#fefefe")
            f.write( "[![](http://www.placehold.it/150/%s/ffffff&text=%s)](%s)" % ( dict[lang]["color"][1:], lang, dict[lang]["url"] ) )
            
    if colorless != {}:
        f.write( "\n\nA few other languages don't have their own color on Github :( \n" )
        for lang in colorless:
            f.write( "* [%s](%s)\n" % ( lang, colorless[lang] ) )

    f.write( "\n\nCurious about all this? Check `ABOUT.md`\n" )
    
    f.close

# #
# now do stuff
# #

run()

