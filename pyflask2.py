import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine
import datetime
import parsedatetime
from flask import Flask
from flask import request


app = Flask(__name__)



@app.route("/compute/<cmd>")
def parse_request(cmd):
   
    print "cmd is",cmd;
    res = dbcon(cmd)    
    return res

    

def dbcon(text):
    
    tokenizer = EnglishTokenizer()
    trie = Trie()
    tagger = EntityTagger(trie, tokenizer)
    parser = Parser(tokenizer, tagger)
    cal = parsedatetime.Calendar()
    engine = IntentDeterminationEngine()

    category_keyword = [
        "energy",
        "equipment"
    ]

    for ck in category_keyword:
        engine.register_entity(ck, "categoryKeyword")

    command_categories = [
         "show",
         "write",
         "what",
         "display",
         "read"
    ]
    for cc in command_categories:
         engine.register_entity(cc,"commandcategories")

    pmt_categories = [
        "details",
        "status",
        "parameters",
        "requirement",
        "output"
    ]
    for pc in pmt_categories:
        engine.register_entity(pc, "pmtcategories")

    lvl_categories = [
        "level-1",
        "level-2",
        "level-3",
        "level-4",
        "level-5"
    ]
    for lc in lvl_categories:
        engine.register_entity(lc,"lvlcategories")

    intensity_categories = [
        "high",
        "medium",
        "low",
        "normal"

    ]
    for ic in intensity_categories:
        engine.register_entity(ic,"intensitycategories") 
    sub_categories = [
        "consumption",
        "demand",
        "energy consumption tracker",
        "building energy usage category",
        "top five faults",
        "faults by equipment category",
        "chiller system runhour",
        "boiler system runhour"

    ]
    for sc in sub_categories:
        engine.register_entity(sc, "subcategories")

    range_categories = [
        "one month data",
        "two month data",
        "three month data",
        "four month data",
        "five month data",
        "six month data",
        "seven month data",
        "eight month data",
        "nine month data",
        "ten month data"
    ]
    for rc in range_categories:
        engine.register_entity(rc, "rangecategories")

    equipment_intent = IntentBuilder("equipmentIntent")\
        .require("categoryKeyword")\
        .optionally("subcategories")\
        .optionally("commandcategories")\
        .optionally("rangecategories")\
        .optionally("pmtcategories")\
        .optionally("intensitycategories")\
        .optionally("lvlcategories")\
        .build()

    engine.register_intent_parser(equipment_intent)

    #if __name__ == "__main__":
    intent = {}
  	
    for intent in engine.determine_intent(text):
	print"*************************************************"
    	if intent.get('confidence') > 0:
   	       print "intent:",intent
    
    print ("------------------------------------------------------------------")
    print "text: ",text
    print ("------------------------------------------------------------------")
    
    dt_obj = cal.parse(str(text))
   
    print "date:",dt_obj[0][2]
    print "Month:",dt_obj[0][1]
    print "year:",dt_obj[0][0]
 
    ''' 	
    if(dt_obj):
         print 'date:',dt_obj.datetimeString-

         #print intent

         intent['date']=dt_obj.datetimeString
    '''
    	
    intent['date']  = dt_obj[0][2] 
    intent['month'] = dt_obj[0][1]
    intent['year']  = dt_obj[0][0]
    		 
    print intent
    return(json.dumps(intent, indent=4))

    

 


if __name__ == "__main__":
	#app.debug = True
	app.run('127.0.0.1', 8085)
	#app.run(debug = True)	
