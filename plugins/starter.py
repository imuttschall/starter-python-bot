import time
import re
import random
import logging
crontable = []
outputs = []
attachments = []
typing_sleep = 0

secrets   = [ "I know secrets...",
              "If you have 3 quarters, 4 dimes, and 4 pennies, you have $1.19. You also have the largest amount of money in coins without being able to make change for a dollar.",
              "The numbers '172' can be found on the back of the U.S. $5 dollar bill in the bushes at the base of the Lincoln Memorial.",
              "President Kennedy was the fastest random speaker in the world with upwards of 350 words per minute.",
              "In the average lifetime, a person will walk the equivalent of 5 times around the equator.",
              "Odontophobia is the fear of teeth.",
              "The 57 on Heinz ketchup bottles represents the number of varieties of pickles the company once had.",
              "In the early days of the telephone, operators would pick up a call and use the phrase, 'Well, are you there?'. It wasn't until 1895 that someone suggested answering the phone with the phrase 'number please?'",
              "The surface area of an average-sized brick is 79 cm squared.",
              "According to suicide statistics, Monday is the favored day for self-destruction.",
              "Cats sleep 16 to 18 hours per day. I don't know how Kit has enough time to play Minecraft...",
              "The most common name in the world is Mohammed.",
              "It is believed that Shakespeare was 46 around the time that the King James Version of the Bible was written. In Psalms 46, the 46th word from the first word is shake and the 46th word from the last word is spear.",
              "Karoke means 'empty orchestra' in Japanese.",
              "The Eisenhower interstate system requires that one mile in every five must be straight. These straight sections are usable as airstrips in times of war or other emergencies.",
              "The first known contraceptive was crocodile dung, used by Egyptians in 2000 B.C.",
              "Rhode Island is the smallest state with the longest name. The official name, used on all state documents, is 'Rhode Island and Providence Plantations.'",
              "When you die your hair still grows for a couple of months.",
              "There are two credit cards for every person in the United States.",
              "Isaac Asimov is the only author to have a book in every Dewey-decimal category.",
              "The newspaper serving Frostbite Falls, Minnesota, the home of Rocky and Bullwinkle, is the Picayune Intellegence.",
              "It would take 11 Empire State Buildings, stacked one on top of the other, to measure the Gulf of Mexico at its deepest point.",
              "The first person selected as the Time Magazine Man of the Year - Charles Lindbergh in 1927.",
              "The most money ever paid for a cow in an auction was $1.3 million.",
              "It took Leo Tolstoy six years to write 'War & Peace'.",
              "The Neanderthal's brain was bigger than yours is.",
              "On the new hundred dollar bill the time on the clock tower of Independence Hall is 4:10.",
              "Each of the suits on a deck of cards represents the four major pillars of the economy in the middle ages: heart represented the Church, spades represented the military, clubs represented agriculture, and diamonds represented the merchant class.",
              "The names of the two stone lions in front of the New York Public Library are Patience and Fortitude. They were named by then-mayor Fiorello LaGuardia.",
              "The Main Library at Indiana University sinks over an inch every year because when it was built, engineers failed to take into account the weight of all the books that would occupy the building.",
              "The sound of E.T. walking was made by someone squishing her hands in jelly.",
              "Lucy and Linus (who where brother and sister) had another little brother named Rerun. (He sometimes played left-field on Charlie Brown's baseball team, [when he could find it!]).",
              "The pancreas produces Insulin.",
              "1 in 5,000 north Atlantic lobsters are born bright blue.",
              "There are 10 human body parts that are only 3 letters long (eye hip arm leg ear toe jaw rib lip gum).",
              "A skunk's smell can be detected by a human a mile away.",
              "The word 'lethologica' describes the state of not being able to remember the word you want.",
              "The king of hearts is the only king without a moustache.",
              "Henry Ford produced the model T only in black because the black paint available at the time was the fastest to dry.",
              "Mario, of Super Mario Bros. fame, appeared in the 1981 arcade game, Donkey Kong. His original name was Jumpman, but was changed to Mario to honor the Nintendo of America's landlord, Mario Segali.",
              "The three best-known western names in China: Jesus Christ, Richard Nixon, and Elvis Presley.",
              "Every year about 98% of the atoms in your body are replaced.",
              "Elephants are the only mammals that can't jump.",
              "The international telephone dialing code for Antarctica is 672.",
              "World Tourist day is observed on September 27.",
              "Women are 37% more likely to go to a psychiatrist than men are.",
              "The human heart creates enough pressure to squirt blood 30 feet (9 m).",
              "Diet Coke was only invented in 1982.",
              "There are more than 1,700 references to gems and precious stones in the King James translation of the Bible.",
              "When snakes are born with two heads, they fight each other for food.",
              "American car horns beep in the tone of F.",
              "Turning a clock's hands counterclockwise while setting it is not necessarily harmful. It is only damaging when the timepiece contains a chiming mechanism.",
              "There are twice as many kangaroos in Australia as there are people. The kangaroo population is estimated at about 40 million.",
              "Police dogs are trained to react to commands in a foreign language; commonly German but more recently Hungarian.",
              "The Australian $5 to $100 notes are made of plastic.",
              "St. Stephen is the patron saint of bricklayers.",
              "The average person makes about 1,140 telephone calls each year.",
              "Stressed is Desserts spelled backwards.",
              "If you had enough water to fill one million goldfish bowls, you could fill an entire stadium.",
              "Mary Stuart became Queen of Scotland when she was only six days old.",
              "Charlie Brown's father was a barber.",
              "Flying from London to New York by Concord, due to the time zones crossed, you can arrive 2 hours before you leave.",
              "Dentists have recommended that a toothbrush be kept at least 6 feet (2 m) away from a toilet to avoid airborne particles resulting from the flush.",
              "You burn more calories sleeping than you do watching TV.",
              "A lion's roar can be heard from five miles away.",
              "The citrus soda 7-UP was created in 1929; "7" was selected because the original containers were 7 ounces. 'UP' indicated the direction of the bubbles.",
              "Canadian researchers have found that Einstein's brain was 15% wider than normal.",
              "The average person spends about 2 years on the phone in a lifetime.",
              "The fist product to have a bar code was Wrigleys gum.",
              "The largest number of children born to one woman is recorded at 69. From 1725-1765, a Russian peasant woman gave birth to 16 sets of twins, 7 sets of triplets, and 4 sets of quadruplets.",
              "Beatrix Potter created the first of her legendary 'Peter Rabbit' children's stories in 1902.",
              "In ancient Rome, it was considered a sign of leadership to be born with a crooked nose.",
              "The word 'nerd' was first coined by Dr. Seuss in 'If I Ran the Zoo.'",
              "A 41-gun salute is the traditional salute to a royal birth in Great Britain.",
              "The bagpipe was originally made from the whole skin of a dead sheep.",
              "The roar that we hear when we place a seashell next to our ear is not the ocean, but rather the sound of blood surging through the veins in the ear. Any cup-shaped object placed over the ear produces the same effect.",
              "Revolvers cannot be silenced because of all the noisy gasses which escape the cylinder gap at the rear of the barrel.",
              "Liberace Museum has a mirror-plated Rolls Royce; jewel-encrusted capes, and the largest rhinestone in the world, weighing 59 pounds and almost a foot in diameter.",
              "A car that shifts manually gets 2 miles more per gallon of gas than a car with automatic shift.",
              "Cats can hear ultrasound.",
              "Dueling is legal in Paraguay as long as both parties are registered blood donors.",
              "The highest point in Pennsylvania is lower than the lowest point in Colorado.",
              "The United States has never lost a war in which mules were used.",
              "Children grow faster in the springtime.",
              "On average, there are 178 sesame seeds on each McDonalds BigMac bun.",
              "Paul Revere rode on a horse that belonged to Deacon Larkin.",
              "The Baby Ruth candy bar was actually named after Grover Cleveland's baby daughter, Ruth.",
              "Minus 40 degrees Celsius is exactly the same as minus 40 degrees Fahrenheit.",
              "Clans of long ago that wanted to get rid of unwanted people without killing them used to burn their houses down -- hence the expression 'to get fired'",
              "Nobody knows who built the Taj Mahal. The names of the architects, masons, and designers that have come down to us have all proved to be latter-day inventions, and there is no evidence to indicate who the real creators were.",
              "Every human spent about half an hour as a single cell.",
              "7.5 million toothpicks can be created from a cord of wood.",
              "The plastic things on the end of shoelaces are called aglets.",
              "A 41-gun salute is the traditional salute to a royal birth in Great Britain.",
              "The earliest recorded case of a man giving up smoking was on April 5, 1679, when Johan Katsu, Sheriff of Turku, Finland, wrote in his diary 'I quit smoking tobacco.' He died one month later.",
              "'Goodbye' came from 'God bye' which came from 'God be with you.'",
              "February is Black History Month.",
              "Jane Barbie was the woman who did the voice recordings for the Bell System.",
              "The first drive-in service station in the United States was opened by Gulf Oil Company - on December 1, 1913, in Pittsburgh, Pennsylvania.",
              "The elephant is the only animal with 4 knees.",
              "Kansas state law requires pedestrians crossing the highways at night to wear tail lights." ]

greetings = ['Hi friend!', 'Hello there.', 'Howdy!', 'Wazzzup!!!', 'Hi!', 'Hey.']
help_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
    "I will respond to the following messages: ",
    "`lemonbot hi` for a random greeting.",
    "`lemonbot joke` for a question, typing indicator, then answer style joke.",
    "`lemonbot attachment` to see a Slack attachment message.",
    "`@<your bot's name>` to demonstrate detecting a mention.",
    "`lemonbot help` to see this again.")

# regular expression patterns for string matching
p_bot_hi = re.compile("lemonbot[\s]*hi")
p_bot_joke = re.compile("lemonbot[\s]*joke")
p_bot_attach = re.compile("lemonbot[\s]*attachment")
p_bot_help = re.compile("lemonbot[\s]*help")
p_bot_dance = re.compile("lemonbot[\s]*dance")

p_bot_secret = re.compile("lemonbot[\s]*secret")
p_bot_fact = re.compile("lemonbot[\s]*fact")

p_bot_on = re.compile( "lemonbot[\s]*on" )
p_bot_off = re.compile( "lemonbot[\s]*shutup" )
 

bot_on = True

def process_message(data):
    logging.debug("process_message:data: {}".format(data))

    
    
    if( bot_on or data['text'].startswith("lemonbot") ):
        
        bot_on = True
    
        if( p_bot_off.match( data['text' ] ):
            bot_on = False
    
        elif p_bot_hi.match(data['text']):
            outputs.append([data['channel'], "{}".format(random.choice(greetings))])

        elif p_bot_joke.match(data['text']):
            outputs.append([data['channel'], "Why did the python cross the road?"])
            outputs.append([data['channel'], "__typing__", 5])
            outputs.append([data['channel'], "To eat the chicken on the other side! :laughing:"])

        elif p_bot_attach.match(data['text']):
            txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
            attachments.append([data['channel'], txt, build_demo_attachment(txt)])

        elif p_bot_help.match(data['text']):
            outputs.append([data['channel'], "{}".format(help_text)])

        elif p_bot_joke.match(data['text']):
            outputs.append([data['channel'], "Hello, I'm the BeepBoop python starter bot.\n{}".format(help_text)])

        elif p_bot_secret.match(data['text'] or  p_bot_fact.match(data['text']):
            outputs.append( [ data[ 'channel' ], "{}".format( random.choice( secrets ) ) ] )

        # leave at end 
        elif data['text'].startswith("lemonbot"):
            outputs.append([data['channel'], "I'm sorry, I don't know how to: `{}`".format(data['text'])])

        elif data['channel'].startswith("D"):  # direct message channel to the bot
            outputs.append([data['channel'], "Hello, I'm the BeepBoop python starter bot.\n{}".format(help_text)])
          
def process_mention(data):
    logging.debug("process_mention:data: {}".format(data))
    outputs.append([data['channel'], "You really do care about me. :heart:"])

def build_demo_attachment(txt):
    return {
        "pretext" : "We bring bots to life. :sunglasses: :thumbsup:",
		"title" : "Host, deploy and share your bot in seconds.",
		"title_link" : "https://beepboophq.com/",
		"text" : txt,
		"fallback" : txt,
		"image_url" : "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
		"color" : "#7CD197",
    }
