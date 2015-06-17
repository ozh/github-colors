import yaml
import json
import requests
import io
import urllib
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
from collections import OrderedDict
from time import sleep

def ordered_load( stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict ):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python Orderered Dictionary.
    """
    class OrderedLoader( Loader ):
        pass
    OrderedLoader.add_constructor( yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        lambda loader, node: object_pairs_hook( loader.construct_pairs( node ) ) )

    return yaml.load( stream, OrderedLoader )


def order_by_keys( dict ):
    """
    Sort a dictionary by keys, case insensitive ie [ Ada, eC, Fortran ]
    Default ordering, or using json.dump with sort_keys=True, produces [ Ada, Fortran, eC ]
    """
    from collections import OrderedDict
    return OrderedDict( sorted( dict.items(), key=lambda s: s[0].lower() ) )


def get_file( url ):
    """
    Return the URL body, or False if page not found

    Keyword arguments:
    url -- url to parse
    """
    try:
        r = requests.get( url )
    except:
        sys.exit( "Request fatal error :  %s" % sys.exc_info()[1] )

    if r.status_code != 200:
        return False

    return r.text


def run():
    # Get list of all langs
    print( "Getting list of languages ..." )
    yml = get_file( "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml" )
    langs_yml = ordered_load( yml )
    langs_yml = order_by_keys( langs_yml )

    # List construction done, count keys
    lang_count = len( langs_yml )
    print( "Found %d languages" % lang_count )

    # Construct the wanted list
    langs = OrderedDict()
    for lang in langs_yml.keys():
        if ("type" not in langs_yml[lang]) or ("color" in langs_yml[lang]) or (langs_yml[lang]["type"] == "programming"):
            print( "   Parsing the color for '%s' ..." % ( lang ) )
            langs[lang] = OrderedDict()
            langs[lang]["color"] = langs_yml[lang]["color"] if "color" in langs_yml[lang] else None
            langs[lang]["url"] = "https://github.com/trending?l=" + ( langs_yml[lang]["search_term"] if "search_term" in langs_yml[lang] else lang )
    print( "Writing a new JSON file ..." )
    write_json( langs )
    print( "Updating the README ..." )
    write_readme( langs )
    print( "All done!" )


def write_json( text, filename = 'colors.json' ):
    """
    Write a JSON file from a dictionary
    """
    with open( filename, 'w' ) as f:
        f.write( json.dumps( text, indent=4 ) + '\n' )


def write_readme( text, filename = 'README.md' ):
    """
    Write a README file from a dictionary
    """
    with open( filename, 'w' ) as f:
        f.write( "# Colors of programming languages on Github \n\n" )

        colorless = OrderedDict()

        for lang in text:
            if None == text[lang]["color"]:
                colorless[lang] =  text[lang]["url"]
            else:
                # text[lang]["color"][1:] : remove first char ("#") from the color ("#fefefe")
                f.write( "[![](http://www.placehold.it/150/%s/ffffff&text=%s)](%s)" % ( text[lang]["color"][1:], quote(lang), text[lang]["url"] ) )

        if colorless != {}:
            f.write( "\n\nA few other languages don't have their own color on Github :( \n" )
            for lang in colorless:
                f.write( "* [%s](%s)\n" % ( lang, colorless[lang] ) )

        f.write( "\n\nCurious about all this? Check `ABOUT.md`\n" )


# #
# now do stuff
# #
run()

