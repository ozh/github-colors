import yaml
import json
import requests
import json
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

def get_file( url ):
    """
    Return the URL body, or False if page not found

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
        return False

    return r.text

def run():
    # Get list of all langs
    print( "Getting list of languages ..." )
    yml = get_file( "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml" )
    langs_yml = ordered_load( yml )

    # List construction done, count keys
    lang_count = len( langs_yml )
    print( "Found %d languages" % lang_count )

    # Construct the wanted list
    langs = OrderedDict()
    for lang in langs_yml.keys():
        print( "   Parsing the color for '%s' ..." % ( lang ) )
        langs[lang] = {}
        langs[lang]["color"] = langs_yml[lang]["color"] if "color" in langs_yml[lang] else None
        langs[lang]["url"] = "http://github.com/trending?l=" + ( langs_yml[lang]["search_term"] if "search_term" in langs_yml[lang] else lang.lower() )
    print( "Writing a new JSON file ..." )
    write_json( langs )
    print( "Updating the README ..." )
    write_readme( langs )
    print( "All done!" )

def write_json( text, filename = 'colors.json' ):
    """
    Write a JSON file from a dictionary
    """
    from collections import OrderedDict
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

