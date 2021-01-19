### Escape ###

opening = """{0}, you look around the cell that you are in. Getting up from the dirty floor, you see that on your left is a row of tall, thick metal bars with narrow spacing, preventing you from leaving. You look in between the bars, angling your head to maximize how much you can see. You see 
an entire row of prison cells directly across from you, streching for at least 10 cells as far as you can see in your limited perspective. Reasonably, you assume that there is an equally long row of cells on your side as well. The hallways in the middle is dimmly lit by lights that create a 
light blue hue to the entire area. The walls of both your cell and the hallway are made of large, white tiles that, when combined with the light, create a turquoise colored environment. Despite it being a prison, you see that there is next to no trash or litter or dirt or any other kind of 
filth anywhere. The hall and the cells are immaculate. Even the uniform you are wearing and that of your fellow prisoners is spotless. A clean, orange jumpsuit combined with a white T shirt below it. On the opposite side of the bars, to your right, is a small window that lets in a small ounce 
of natural light. It is impossible to see out of it so you end up sitting on the cold, hard stone bench, likely a sad excuse for a bed. The only other thing in your cell is a white toilet. You continue to look out into the hallway as footsteps approach."""

footsteps = """Every step produces a loud, heavy sound, exactly that of boots moving on a hard floor. The sound is getting closer and closer and you can tell it is coming from the left of your cell."""

first_options = ["Stop looking into the hall before someone comes", "Continue looking at the hallway"]

stop_looking = """You lie down on the bench and roll over so you are facing the wall, pretending to be asleep. The footsteps move past your cell and you slowly roll over so you can observe the hallway when you hear something like a whimper or a moan a few cells away. Right away, this is followed 
by two loud bangs, as if something was being hit hard on metal. Then a loud {0} voice penetrates the silence of the prison. 

'Hey! Shut up!' 

Another voice, a soft and weak one, responds, 'I'm sorry officer. I feel so weak. I haven't been given food for days.' 

'I didn't ask why you opened your damn mouth! Shut up and be thankful you are even breathing! Next time you do this, I will make you sorry!'

The footsteps continue and you assume the guard continues their patrol."""

guard_description = """You continue to look at the hall and see a person enter your field of view. They are wearing sleek, black armor with red accents on the sides and the shoulder pads. Underneath their body armor is a black undershirt, again with red accents along the length of the arm that 
creates a nearly seemless transition between the armor and the sleeves of the undershirt. The armor has a belt with multiple yet seemingly empty pouches. At the waist is a utility belt with many pouches attached to it, the most noticeable one having a gray baton sitting inside of it. Their 
pants continue the aesthetic trend, being black with red accents along the side of the leg. At the bottom of their legs are large, black boots. Their elbows and knees are covered with elbow and knee pads, respectively. On the hands are black gloves with more red accents. Their head is fully 
enclosed in a large black helmet that has some reflectivity in the light. One side of the helmet has a mounted flashlight. On the helmet's facepiece is a dark visor, one that is tinted so that you cannot see the person on the other side. The guard looks to their left, the cell opposite to 
yours, and then to their right, your cell."""

caught_looking = """'What are you looking at?! Yea you, I'm talking about you {0}! Why are your sorry eyes looking at a hallway you will never walk in again?! You are here for a reason! It's people like you, poor scum, the filth of society, rioting and looting and opposing our glorious 
government! The same god damn government that feeds you and gave you a home! People like you are the reason why our nation will never become perfect, why society will never become perfect! So enjoy your new home, you'll rot away here like the rest of your kind!'"""

caught_looking_options = ["Do nothing", "Look away", "Turn around and stop looking", "'I'm sorry, I will never do this again'", "'Fuck you, you pathetic piece of shit'"]

guard_submit = """'Yea that's right, roll over like a damn dog and accept how pathetic you really are. If more of your kind did so, all of our lives would be easier!' With that line, the guard walks away. So this is how the Federation treats its prisoners. You've heard rumors about how its 
like but no one has ever been able to provide evidence or eye witness accounts of it. It is believed that once you are taken away by Federation officers, you will never return to society. However, this doesn't mean you won't try, not at all. It is not a hard decision to decide if it is 
better to be complacent and live here the rest of your miserable existance, or to try escaping and perish that way. There isn't even a choice."""

guard_offend = """'Do you not know your place?! After I'm done with you, you will wish you never stepped out of line!' The guard quickly unlocks the gate to your cell and leaves it open. They then reach over to a holster on their belt and whip out the baton, pressing a button on it that 
causes the front end of the weapon to spark. You see pulses of electricity travel from the front end of the baton down a metal post and then disappear at the cross guard, where the guard is holding the weapon."""

punish_choices = ["Do nothing", "'My apologies officer! I didn't mean it!'", "Fight the guard"]

guard_punish = """The guard raises their baton and repeatedly strikes you, with each blow filling you with regret. It hurts badly, so badly, and each hit is accompanied with an electric shock that attacks your very spirit. After hitting you multiple times, the guard leaves your cell 
satisfied. You are left alone on the floor of your cell beaten and bruised badly. Every movement hurts and you don't know if something's been broken or not. Next time, you figure that it is best to keep your anger in check, at least for now. However, you have to find your way out of this place 
once you feel more recovered."""

planning = """Days after the incident with the guard, you take time to plan your risky escape, taking time to assess your surroundings. From your meticulous observations of your cell and the part of the prison that you can see, you learn that the door to your cell is controlled by a key card 
reader. After noticing the guards only carry a single key card when they open a cell to torture prisoners, it appears that all the doors are controlled by a single key card. You have also noticed that at most, there are two guards patrolling this part of the prison and it is always the 
exact same people. The guards despise the prisoners and will jump on the opportunity to berate or threaten them, even for the most inconsequential sounds or actions. Occasionally, you see the guards drag prisoners out of their cells but they never return. This happened to the prisoner 
across from you and their cell is still empty after several days. The walls of your cell are very well built and there is no way you would be able to break the tiles or dig through them or anything of that sort. A sad excuse for food is given twice a day via some gloop in a can. Guards 
do not open the cells to deliver food. They merely throw the cans through the spacing between the bars. No spoons or utensils either so you look like a homeless dog trying to lick every morsel of food they can find."""

planning_choices = ["Inspect the toilet", "Inspect the cans of food when it is meal time", "Make a loud noise", "Insult the guard as they walk by"]

inspect_toilet = """The toilet is surprisingly clean and works like a charm. It has no issues so far. You lift the top off of the tank and find nothing out of the ordinary. The components inside the tank are securely screw in and the pipes behind the toilet are impossible to remove as well. 
You replace the tank's lid back on."""

toilet_clog = """While the guards are not by your cell, you gradually add more and more toilet paper into the toilet bowl, eventually preventing the water from escaping when you flush it. You flush the toilet multiple times, causing the water to overflow from the bowl and eventually cover 
the floor with a thin layer of water. Due to the tile flooring, you find that the floor is now slippery, almost falling over youself. A guard takes notice of the water flowing out of your cell and rushing on over. 'What the fuck are you doing? Taking a massive shit? I'm going to make 
you regret that!' The guard swipes the key card on the reader and takes out their baton and presses a button, causing the front half of the weapon to pulse with electricity. However, as they approach you, the guard slips on the floor and lands head first on the ground."""

throw_water = """As disgusting as the thought of it is, it beats a future of suffering in this hell hole. You wait for a guard to pass by your cell on their patrol, quickly cup your hands inside the bowl, scoop out some water, and throw it on the guard. 'What the...! I'm going to beat your 
sorry ass and drown you in that toilet myself!' The guard swipes the key card on the reader and takes out their baton and presses a button, causing the front half of the weapon to pulse with electricity. However, as they approach you, the guard slips on the floor and lands head first on 
the ground."""

guard_beat = """You jump on top of the guard and repeatedly pummel your fists into the guard's chest and neck. They attempt to fight back and block your strikes but your time on the streets of New Hope has taught you how to fight better than any classroom training. Over and over, you slam 
your fists into the guard and finally, put your hands around their throat and tightly squeeze on it. Slowly, the guard stops trying to defend themselves, eventually giving a final sigh before ceasing to move."""

guard_smash = """While the guard is down, you quickly rip off the face piece of the helmet and then take off the rest of the helmet entirely. The guard attempts to shrug you off but your time on the streets of New Hope has allowed you to hone your skills in hand to hand fighting. You proceed 
to grab the guard by the next, lift their head up high, and then use all your strength to smash their head on the stone bench. Blood runs down the large gash on the guard's forehead and there is a large pool of red on the bench. The guard ceases to move or say anything. Did you really just 
kill them? Honestly, why should you even care at this point?"""

inspect_food = """Since trash disposal only occurs once a week, you have many cans of food lying around in your cell. You look at one and find that it is nothing more than an ordinary rectangular tin can with a pull back top for easy opening. However, the sides of the lid are still sharp, 
sharp enough that you've almost cut your hand on it one time. There are still bits of 'food' in the can but you would rather avoid eating any more of that stuff than you need."""

food_lid = """You take off the sharpest lid of a can and when the guards are not nearby, try to sharpen it on the edges of other cans in your cell. You eventually get one side sharp enough to where you believe you may cut yourself if you just simply touch the edge. You hide this 
weapon in your cell in a location where you can quickly access it."""

act_insane = """You go up to one of your cell's walls and start punching it while screaming gibberish loudly. You stand there, trashing your body around and looking like a maniac who lost all cognitive ability. Then, you start running around your cell erratically, continuing to make as much 
noise as possbile. A guard runs up to your cell."""

moaning = """You lie down on your bench, turn to face the wall, and start making a loud moaning noise as if you had a very dull pain. You slowly increase the sound of your moans until you hear footsteps quickly approaching your cell. 'Hey, shut up! No one gives a damn what you are feeling!' 
Upon hearing those words, you roll around to face the guard, directly look at them, and moan once more. 'Ok that's it! You think it's funny to act like that to me? I'll show you what's funny! You'll be moaning more than you ever wanted after I'm done with you!'"""

guard_insult = """The guard comes rushing over to your cell. 'You think you are funny you piece of shit?! I'll show you how funny it is when every bone is your body is turned to dust!'"""

first_fight = """The guard swipes the key card on the scanner and enters your cell. Once they step foot inside, they take out a baton and press a button, causing the front half of the weapon to have pulses of electricity. You prepare to fight. 'What the... You really think you can kill me?!'"""

escape = """You know for a fact that your little victory is going to be short lived. Your shuffle made a lot of noise and the second guard must have heard something. Hearing a second set of footsteps rushing towards you, you quickly try to put on the first guard's armor and ditch your shank 
in favor of the stun baton."""

### Lower Levels ###

spotted = """The second guard falls over, beaten senseless by your fighting skills. No other guards are in your vicinity and you attempt to try taking our outfit to sneak your weak out of here. However, out of the corner of your eye, you see the blinking light of a security camera staring right 
at you over two motionless bodies. Then, you hear microphone feedback followed by a loud booming voice over the PA system."""

pa_voice = """'Attention all personnel! A prisoner on Level D, Wing 8 is escaping their cell and has overpowered both guards of the section! All units are to respond immediately and subdue the prisoner for execution! Remember, these people are here because they are a stain on the bright future 
of our Federation and its mission for humanity! Do not let the prisoner escape and corrupt the rest of society! For the glory of the Federation! Prisoner, you have made a grave mistake!'"""

alarm_sounded = """An alarm then starts blaring all throughout the hallway and you can hear many footsteps approaching the only door leading into your wing of the prison, Wing 8. You also have access to the key card that opens all the cells in your wing. Most of the prisoners seem still 
young and healthy and they look eager to escape and take revenge. Quickly, you have to make a decision before the guards arrive."""

free_wing8 = """You swipe the key card on as many cells as you can, earning gratitude from many of the cell's participants. They stand alongside you as guards begin to funnel into Wing 8 and start picking their own fights with the guards. Some prisoners continue to open cells while others 
are engaged in furious hand to hand combat with them. It is clear that all of you have significantly better fighting skills than your oppressors. The prisoners take some of the heat off of you, allowing you to fight less guards at a time."""

forget_wing8 = """With guards rushing you fast, you know that you need to maximize your own chances of survival, as grim as that sounds. You strap on as much of the guards' armor, including their vest and helmet, as you can. Your orange jumpsuit still shows on your arms and legs, defeating 
any chance of your sneaking past. As the first guard enters, you prepare yourself for the brawl ahead."""

lower_section_solo = """You escape the clutches of Wing 8 and find yourself in a wide, two-story central area. The area is shaped like a circle, with entrances to each wing on the outer wall. It appears that there are 10 wings total, evidenced from a Wing 10 sign above one of the doors. 
Furthermore, you notice that some parts of the outer wall have a large 'Level D' painted on it. In the center is a tower that seems to elevate a small circular room with many large windows high above the floor you are on. A spiral staircase connects this observation room to the ground so you 
ascend these stairs and enter the room. There is a desk with many monitors, all showing camera feeds from the various wings. You can see many more prisoners, all in environments similar to that of your wing. There is also a small rack of stun batons, not that you need another one right 
now. Most important, you find a map of the entire prison complex and it amazes you how big it truly is! From what you can gather, you are currently at Level D, the lowest level. Levels D to B are all underground while Level A is above the surface. Level D is visually smaller on the map than 
Levels C and B. You find handwriting next to each level.

'A - Intake and Surface Peacekeeping Base'

'B - Labs and Medical Research'

'C - Regular Prisoners, some deserve to be at D'

'D - Lowest Filth'

You also find a smaller map of Level D, showing that there is both an elevator and a set of stairs connecting D to Level C. There is nothing else noteworthy about this level so you descend the stairs back down. However, you hear a shuffling coming from the direction of where you killed the 
guards."""

lower_section_report = """'Command, this is Matthews. Prisoner has escaped their cell and has overpowered all units in the area! It's too late for us but prepare the other units at Level C and cut power to the elevator! Glory to the Federation!'"""

lower_section_ascend_solo = """On that final shout, the guard named Matthews slums over and stops moving. With the prison alerted to your escape, you decide there is no time left. You hustle up the stairs towards Level C."""

lower_section_revolt = """You escape the clutches of Wing 8 and find yourself in a wide, two-story central area. Your fellow prisoners, now a sizeable amount, have already started raiding the other wing and freeing more captives. The area is shaped like a circle, with entrances to each wing 
on the outer wall. It appears that there are 10 wings total, evidenced from a Wing 10 sign above one of the doors. Furthermore, you notice that some parts of the outer wall have a large 'Level D' painted on it. In the center is a tower that seems to elevate a small circular room with many large 
windows high above the floor you are on. A spiral staircase connects this observation room to the ground so you ascend these stairs and enter the room. There is a desk with many monitors, all showing camera feeds from the various wings. You can see many prisoners being freed, hugging their 
saviors and moving towards the center area as well. There is also a small rack of stun batons, not that you need another one right now. Most important, you find a map of the entire prison complex and it amazes you how big it truly is! From what you can gather, you are currently at Level D, 
the lowest level. Levels D to B are all underground while Level A is above the surface. Level D is visually smaller on the map than Levels C and B. You find handwriting next to each level.

'A - Intake and Surface Peacekeeping Base'

'B - Labs and Medical Research'

'C - Regular Prisoners, some deserve to be at D'

'D - Lowest Filth'

You also find a smaller map of Level D, showing that there is both an elevator and a set of stairs connecting D to Level C. There is nothing else noteworthy about this level so you descend the stairs back to where the other prisoners are. All are eager, some encouraging others while others 
chat about how they will take on the other guards. Then, another very loud voice booms over the crowd."""

lower_section_pa = """'Prisoners, your escape is impossible. We have cut power to the elevator and we have heavily armed units waiting to greet you in the event you scum try to use the stairs. Enjoy your freedom, you might as well kill youselves now! Glory to the Federation!'"""

lower_section_ascend_revolt = """The prisoners start yelling and chanting and in their fury, storm the stairs towards Level C. You hurry to join the mob."""

### Level C ###

levelc_intro = """From the large prison diagram you saw, Level C is used to house the bulk of prisoners and is multiple stories of cells upon cells. It is also tied with Level B for being the largest levels, being extremely large horizontally. The diagram also seemed to show that the stairs 
to reach Level B are on the opposite side as those connecting D and C, meaning you will have plently of ground to cover before ascending once again. As you reach the top of the stairs and enter Level C, you find that the diagrams are indeed correct. The level is laid out so that there are 
many aisles of cells, each aisle three layers tall. Wide corridors separate the aisles and the entire level seems to be one long room. You can barely make out the elevator entrance on the other side when looking down the middle corridor. This place was at least as long as a football field, 
back when football was still a thing. You also notice that the lighting here was much brighter and whiter than in Level D. However, you have no time right now to admire the engineering and construction that went into this place. You hear and see guards fast approaching you and prepare to fight!"""

guards_retreat = """{0} The guards shuffle back as much as they can but then turn around and break into a sprint, dashing towards the stairs to Level B. 'Command, command, this is Sergeant Ryder! We need reinforcements! The {1} too much for us to handle! My unit and I are retreating to Level B!' 
The Sergeant's yelling echoes throughout Level C and then all is quiet."""

levelc_rest_solo = """Using this down time, you scavenge the bodies of the fallen guards, finding some armor but no new weapons or equipment that can help you. You also notice the cells on this level and examine one closely. The cells, similar to the rest of the prison thus far, have the same 
white tile aesthetic. However, each cell also has a table, a bed with pillows instead of a stone bench, blankets, and shelves. Some even have personal items like toys, pictures, drawings, or even laptops. It is clear that equality isn't a principle of this prison and, from your experiences 
above ground, isn't one in society either. There is no key card for these cells, only a slot for a key. You were unable to find any keys on the guards during your searching so you will have to leave these prisoners behind. Not that they should complain since their lives are miles better than 
anything in Level D."""

levelc_rest_revolt = """Using this down time, you scavenge the bodies of the fallen guards, finding some armor but no new weapons or equipment that can help you. You also notice the cells on this level and examine one closely. The cells, similar to the rest of the prison thus far, have the same 
white tile aesthetic. However, each cell also has a table, a bed with pillows instead of a stone bench, blankets, and shelves. Some even have personal items like toys, pictures, drawings, or even laptops. It is clear that equality isn't a principle of this prison and, from your experiences 
above ground, isn't one in society either. There is no key card for these cells, only a slot for a key. As the prisoners loot the guards, one yells 'Y'all I found the key!' and begins unlocking as many cells as possible. Others attempt to lockpick the cells open with success. The revolt is 
expotentially growing in size. The newly freed prisoners showering the Level D saviors with praise and promising to spread the word of how honorable they are."""

levelc_reinforcements = """As you prepare to move on, having only at most five minutes to rest, you hear multiple pops in front of you. Then, clouds of white smoke form a barrier in front of you, making {0} cough and forcing you to retreat a few feet. Out of the smoke steps out a multiple 
heavily armored figures. However, they look even more prepared than the guards you just faced! Many of them are covered head to toe in armor and padding, including flak jackets, ballistic vests, and additional ceramic plates. Their helmets only cover the top and sides of their heads, exposing 
their faces. Some wear balaclavas, masking their entire face except for their eyes. Others wear caps or hoods instead of helmets and only wear chest pieces similar to the guards fought previously. On some vests, you see grenades, belts of ammo, and other pouches of who knows what? Most of them 
are carrying some sort of rifle or firearm while a select few have large, towering glass shields that say 'Federation' on their front. When standing together, they look like one unit, wearing all black with red accents. Every member seems to have their own patches on their armor and sleeves, 
perhaps to show ranks and their accomplishments."""

reinforcement_intimidation = """'Attention {0}, your efforts are brave but they must now come to an end. The Federation has placed great effort in providing you shelter and refugee away from society so you will not corrupt it with your rebellious views. However, it appears you reject their 
kindness and would rather spread your traitorous ideals. This ends now! My name is Commander Leonidas 'Volk' Volkov and before you stand the heroic men and women of the 48th Rapid Response Regiment, 11th Platoon, a unit that is ready to fight at a moment's notice! They have vowed to give up their 
lives, their very own lives, to end your threat to the free and wonderful people of New Hope. Farewell and good luck surviving. Glory to the Federation! 11th Platoon, advance!'"""

volk_intro_solo = """You manage to overpower all the soldiers in your way, an extremely difficult battle. You imagine how much nicer it would have been if you had help from the prisoners down below. Behind you is a pile of dead and dying members of the Federation's forces. However, one foe 
still remains: Volkov himself. Having stood back from the fighting, he steps forward, fully dressed in riot gear himself and armed with something that looks like a flamethrower. You can see drops of some sort of flammable liquid dripping from the weapon's barrel. His armor is also much more 
decorated than that of the shielders, having both red and gray accents. His helmet has his an insignia showing his rank, two horizontal gold bars with a row of three silver stars in between. The helmet also encloses most of his head with a face piece that can be lifted up for more vision."""

volk_intro_revolt = """You and your fellow prisoners outnumber the Federation's forces and while it was a tough fight, you guys have beaten them. You imagine how much harder it would have been if you did not have help from these people. Behind you are piles of dead and dying people, both from 
the Federation but also your fellow prisoners. However, one foe still remains: Volkov himself. Having stood back from the fighting, he steps forward, fully dressed in riot gear himself and armed with something that looks like a flamethrower. You can see drops of some sort of flammable liquid 
dripping from the weapon's barrel. His armor is also much more decorated than that of the shielders, having both red and gray accents. His helmet has his an insignia showing his rank, two horizontal gold bars with a row of three silver stars in between. The helmet also encloses most of his head 
with a face piece that can be lifted up for more vision."""

volk_massacre = """Suddenly, he aims his flamethrower down your corridor and unleashes a torrent of bright orange fire. Enclosed within the confines of the hall, the flames quickly rush down towards you and the rest of the prisoners. 'Oh shit, take cover!' one of them yells. You spot a cell 
that was opened and dive straight in. You hear gun fire being exchanged but the screams of people writhing in pain as they are cooked alive is much louder. Over the span of thirty seconds and four more burst of fire, Volk has single handedly managed to eliminate every single prisoner alive. 
You hear him reload his weapon and move out of your cell to face him, perhaps the final obstacle in your way to freedom. It is a shame what happened to the others but if you mourn now, you might as well give up and kill yourself."""

volk_option = """'I see that you are the only one left alive. You surely are a quick thinker, doing whatever it takes to survive and get out of here. I mean, just look at how many of my own forces you have defeated, it's incredible! If only I didn't have to kill you. You would have made a 
fine addition to my unit, perhaps might even be one of the best fighters we could have ever seen. But you would never turn on your own kind would you? No, no, I wil give you one chance to live despite going against my orders. Surrender now and I will allow you to live. Otherwise, I will 
have to incinerate you and having someone with your skill perish would be a waste don't you think?'"""

volk_dialogue = ["'Are you kidding? Forget my 'kind!' I'll serve under you even if I had to pay you!'", "'Hmmm, you drive a hard bargin but I accept. I surrender!'", "'What kind of spineless trash do you think I am? I'll never surrender!'", "'Fuck you, just try to kill me!'"]

volk_surrender = """Following your surrender, Volk honored his promise and didn't waste any time placing you in the unit's recruit training camp. With your experiences on the dangerous streets in the slums of the city, you proved to be an extremely capable warrior, passing test after test 
with the highest rankings. During weapons training, you showed your superiors how deadly you could be with anything, including knives, grenades, pistols, rifles, and heavy weapons. When it was time for field exercises and the final grueling weeks long testing, your bravery and leadership skills 
earned the respect of all your peers. Soon after graduation as a marksman of the 48th Rapid Response Regiment, you are promoted to Corporal and given a small squad of soldiers to command during your regular patrols of New Hope. You all get along well and become solid comrades over your months 
and years of duty. When given assignments to stop riots from the filth of the ghettos and slums, you and your team show no hesitation, making critical moves that stop the rebellion dead in its tracks and retain peace in society. Eventually, you earn enough to have a nice home in the nice part 
of the city and are able to live to your heart's content. You have earned your freedom...at the expense of others."""

volk_fight = """'Very well, it is a shame that someone like you would not like an opportunity like this. Many of your fellow prisoners wouldn't even think there was a choice. It seems you really do embody the traitorous ideals that harm the stability of the Federation. Always resisting, always 
asking for more, never knowing your place in life. You know, I looked into your prison record before coming here. The gentlemen at the CCTV room advised me to. What did you expect would happen if you tried to take part in a riot? And what's worse is that the riot was pointless too, asking for 
more food and medicine and housing when the Federation has given you more than you deserve. My men got injured in that riot, good people too. I guess this is payback for all the fine people you have hurt and killed in your sad attempt to change our perfect society! Now prepare to burn!'"""

### The Machine Labs ###

labs_intro = """You arrive at the entrance to a large building with the words 'Machine Labs' above the front door in Latin. From the outside, the building is not very tall, but it is extremely long. It eventually turns right and continues to stretch down, eventually going into the part of the 
city that was not destroyed. Machine Labs? What goes on in here and what warrents having a building that is this large? The Romans didn't have complex technology in ancient times so what could they be making here? Did they learn from the outside world? Maybe they saw how humanity was progressing 
and using this knowledge, started experiementation and research on their own. There building itself has the same aesthetic as the rest of the city, with clean and polished white concrete walls with a sloped roof. You smell something that reminds you of oil or gasoline. The only way to figure out 
what happens here is to go in."""

### Event dialogues ###

# Dodge #

dodge_text = """The tunnel is pitch black but you hear sounds approaching you and dive towards the darkest spot you can find. As the sounds come closer, you realize that it is the sound of Legionary armor clinking during motion. You slow down your breathing and cease to move, hiding as still 
as a statue. No matter how nervous you have be, you must be quiet. Clinging to darkness, you patiently wait for the sounds to mvoe past you. All that is protecting you is the darkness of the tunnel. Every second feels like an hour but eventually, the sounds move past you and fade into the 
distance. It is fortunate that their torches are not very bright. Perhaps luck is on yout side. You breath once more, slip out of the darkness, and continue on your path."""

# Statues #

statues_intro = """You walk into a room in a bizzare condition. The walls and floor are polished and clean, aside from a few specks of dirt and grim. Two large pillars lay toppled on the ground in front of you, beautifully etched with engravings of Legionaries marching into battle and of
the Roman people celebrating a good harvest. A red carpet streches across the length of the whole room, from the entrance where you stand all the way to the exit on the other side. Just like the walls, it is also almost immaculate except for the crumbled remains of the pillars on it.
Above you, you notice that the roof has broken down for some reason, causing the sunlight to pour into the room and shower the main attractions: gigantic statues of the legendary {0}, {1}, and {2}. 

You climb over the pillars and walk in front of the statues to examine them. They are expertly crafted and have little signs of wear. It's incredible how they survived so long yet who is maintaining this room? In fact, are you the only person who has made it here? You take out your 
Latin to English dictionary and decipher the worn out messages engraved on the base of each statue. 'Place hand here to...' The rest is suspiciously worn away on each statue. Should you place your hand where it tells you too? What will happen? You stand there, wondering what to do 
as three looming giants judge you with their stone cold gazes."""

statues_exit = """Having recieved a gift from one of the statues, the text at the base of each statue fades away. You try to place your hand on their bases but nothing happens."""

mercury = """You walk up to and place your hand at the base of the statue of Mercury bent over in a sprint. An airy feeling overcomes you, making you feel as light as a feather. All the weight of being an adventurer, the stress of fending off creatures for your survival, the doubt of making it 
back home in one piece is lifted off of your shoulders. It feels as if you are merely existing but it is an enjoyable kind of existance. Gone with the worries of the world, it seems like you could just enjoy the feeling of being alive! You close your eyes to savor this moment. Slowly, 
this euphoric feeling goes away and you return to reality. You open your eyes and in front of you are a pair of chrome colored boots. You slip them on and immediately notice that they are almost weightless."""

mars = """You walk up to the towering statue of Mars in full armor and place your hand at its polished base. Suddenly, how feel your body heat up to an immense degree. It's hot, painfully hot! The sweat running down your skin feels like a knife being dragged through your skin! You start jumping 
and skipping about the room, intensely wiping off your sweat and screaming at the pain. You close your eyes, you want to die and end this suffering. However, the pain suddenly stops. You open your eyes and gasp for breath. What just happened?! You check your entire body yet there are no signs
of damage and all your clothes have dry as ever. You are relieved. However, you also feel an incredible power inside of you now. It courses through every vessel in your body and you feel stronger than ever."""

apollo = """You walk up to the statue of Apollo singing gracefully with his lyre and place your hand at its base. The one quiet room starts to fill with the sound of ancient Roman singing, slowly becoming louder and louder. A playful rhythm accompanies a steady beat and lyrics about the wonders
of Roman life. The voices sing of a wonderful harvet and plentiful hunt, thanking the Gods for their mercy and blessings. The mystical bard moves on to tell of the glory of the Roman military, how graceful the men march into battle and the mercy they show their foes. The focus then turns to
life in the city, encapsulating with descriptions of the town square, the political discussions occuring in the Senate, and the cheers of the crowd in the Colusseum. The music flows all around you and uplifts your spirit, making it as full of joy as the melody itself. You close your eyes to
turn inwards and fully imagine what the song is saying. Then, the voices and music slowly fade away and you are left in the silence of the room once more. Upon opening your eyes, you find a beautiful lyre in front of you, a treasure for you to keep."""

vejovis = """You walk up to the statue of Vejovis holding pilums standing next to a goat and place your hand at its base. You feel a quick rush of energy overcome you but then it quickly dissipates. However, when you take a drink of your water, you feel more refreshed than you were expecting. 
The same feeling occurs when you try eating a snack from your backpack. Everything you consume invigorates you with more energy than ever before. """

diana = """You walk up to the statue of Diana, crouched aiming her bow, and place your hand at its base. Immediately, you notice a whistle come from behind you and you whip around, ready to take on another foe. However, what was once a white room has now become an expansive forest. You turn
back around to face the statue but that's gone as well, replace by more tall trees and short shrubs. You turn around once more, hearing a rustling in the bushes behind you. Out of the shrubs jumps a large, fat boar that immediately starts grazing in front of you. You don't know what you 
should do. That thing has the speed and strength to rip your guts out with its tusks. Despite being frozen, you notice out of the corner of your right eye a graceful and silent archer crouching next to you. She has a finely crafted bow in hand but no quiver in sight. She sees you and puts her
finger up to her lips. 'Sssshhhh, don't alert him,' she whispers. In one smooth motion, she loads one of her three arrows, draws her bow, and fires it directly into the boar. In rapid succession, she fires her other two. In less than a second, the boar goes down to the ground. The archer gives 
you her thanks for staying quiet and goes forth to secure her kill. The forest vanishes around you and the room returns back to normal. You feel as if you learned something valuable from that experience: how to use a bow to its full potential. A skill that you think will come in handy."""

# Legendary Items #

legit_intro = """You encounter a worn down gray stone wall with a human skeleton peacefully resting on it, sitting on the ground with its back on the cold stone. Something tells you that this skeleton has been sitting here for years as time rolled by. Surprisingly, there is still a hat
perched on its head, a worn down jacket on its torso, and trousers on its legs. You check the canteen lying nearby. No water. No food either, probably eaten by the occupants of this place or nature's own animals. There are so many ways this person could have perished. Maybe its your mind
placing you in the skeleton's shoes but you imagine that this brave and foolish soul stopped moving forward for whatever reason. No more food, water, equipment, willpower, or whatever it may be. You imagine that they just sat down in this room, resting their back on this wall. Perhaps they
cried or thrashed around in anger and frustration. Eventually, they made peace with the idea of death and slowly let their life slip away from them. At least, that is how you would like to die, accepting the end of your life if it came down to this."""

ross_rifle_text = """You notice that the skeleton was craddling something in its arms, almost like a baby. You gently and respectfully slip it out of the skeleton's arms. Brushing off the dust and polishing it a bit with a rag, you find that it's bolt action rifle in a usable condition. You
operate the bolt, pulling it back and sliding it forward once again. It still feels incredibly smooth and a little grease would make it flawless. There are still some bullets left in the chamber of the rifle. You throughly inspect the rifle and determine that while old, it is still a usable
machine. However, this is not just any rifle. It's the Ross Rifle, legendary Canadian bolt action rifle renowned for its accuracy and power! It became known after its performance with Canadian troops during the Great War, becoming a precision weapon in the hands of a skilled user. If only
there was a scope you could attach to this. That would make this the perfect rifle."""

# Ghostly Vision #

ghosts_banquet = """You walk into a place and see a bunch of apparitions appear in front of you. They are dressed in formal attire, chatting excitedly about life, the weather, politics, or whatever is on their mind. There is a long table adorned with an amazing amount of food, enough to
make your mouth water. The room around you consists of polished while columns decorated with colorful banners and intricate symbols. The floor has a beautiful carpet that stretches the length of the shiny marble tiles. The laughter, the conversations, the music, the footsteps all flood your
ears."""

ghosts_banquet_end = """A team of musicians plays their instruments, producing a beautiful melody as a singer produces a song with their powerful voice. You stand there and take all of this in. So this was what a wealthy Roman gathering was, seems like a joyous occasion. There is respect that
have to give to the Romans, they knew what elegance was. You take a walk around. The ghostly guests pay no heed to your presence, even when you pass through them. You smell the wonderful odor of the food yet unfortunately, when you attempt to take something, your hand passes through it.
No matter, this experience was a wonderful one. It's a shame that whatever is left of the Roman empire is trying to kill you. Perhaps you might have enjoyed living in this society. Slowly, the sounds and sights fade away, along with the guests. You are left by yourself, with only your
memory of that event as evidence of its existance."""

ghosts_battle = """You walk into a room and see are taken aback by what is in front of you. Many apparitions appear in front of you, Roman legionaries maintaining a shield wall against Gallic barbarians. You hear the smashing of shields, the clash of metal, and the slamming of bodies against
one another. The sky is a firey orange, colored by the flames and smoke litering the battlefield. The field in front of the Romans is littered with bodies and blood, a truly gruesome sight. Above you, a hail of arrows wizz past, cutting the barbarians down."""

ghosts_battle_end = """You are encapsulated, continuing to watch the battle unfold. A tall man in gleaming armor and a helmet adorned with a striking red feather plume. 'Legionaries, we must turn this battle around. The barbarians are fierce, hungry to kill us and harm our friends, families,
and legacies. However, we are not mere raiders, bandits, or soldiers from a lesser empire. We are Romans! We are from the strongest empire backed by the Gods themselves! How can we let ourselves be defeated by people who have no dignity, no honor, no morals?! Assemble the shield wall and
advance!' At that moment, the ranks behind the front line of Legionaries placed their shields above their heads, forming an inpenetrable fortess of Roman might. They unit slowly creeped towards the barbarians, their shields fending off the arrows. On their flanks, their auxilliary archers
peppered the enemy. When they clashed with the barbarian warriors, the Legionaries showed their skill and strength, cutting down their foes and whittling the enemy's numbers. A charge from their cavalry finished off the survivors, leaving the Romans the victors. You are in awe of their
might and shocked by their determination. The vision fades away and you are left in an empty place. It's a shame that you have to go against these powerful foes. No wonder they were a legendary fighting force. The event left no evidence but left a lasting memory inside you."""

ghosts_run = """Fear has a vice grip on you and your heart is beating as hard as it can. Adrenaline surges through you and your leg muscles are bursting with energy. Whatever is happening, it's best to get out of there! Good or bad or whatever, you don't care enough to find out. But, but, but,
you were here to push on, to move towards the treasure. You summon up all your courage and run through this paranormal scene as fast as you can, dashing out of the room until its exit was out of your sight. Exhausted from that sprint, you lean back on a rock and catch your breath, collecting
youself back together. All you think about is that this treasure better be damn worth it!"""

# Merchant Event #

merchant_intro = """You come across a mysterious figure standing inside in what appears to look like a type of makeshift stand or shop. A sign in the front reads 'Merchant' in Latin but this place also gives a bad feeling. You can't see the merchant's face, shrouded in darkness by the hood
over their head. The inside of the shop is extremely dark as well, allowing you to only see the merchant leaning over the front counter. Even though there's light all around you, it's as if the light is averted once it attempts to enter the shop. Despite the peculiar nature of this shop, 
the likes of which you've never seem before, the merchant notices your presence and gestures for you to come over. 'Weeeeeelcome traveler, needs some...wares?' said a gruff, crackled voice. Even the way this merchant spoke sounds like someone trying to lure you into a back alley to rob
you. But this may also be the only chance you have to resupply on your travels, especially in a place so removed from normal civilization."""

# Encounters #

abandoned_village = """You come across a small collection of worn down houses. It is eerily quiet, not even the sound of the wind could be heard. You guess that this place is some sort of village or encampment. However, the most defining feature of a place like this was missing: the people.
There is not a soul in sight. Not even any of the bizzare enemies or creatures you have encountered, if those even have a soul in the first place. The buildings seem to be made of a bricks made from mud, some of which had visible cracks and were crumbling. They were all an extremely dull
gray-brown, adding to your uneasiness. However, you are an adventurer and explorer so your curiosity gets the better of you and you slowly explore the buildings, one by one. You remain on guard, ready for anything that could happen. However, you slowly become more and more relieved. There 
really is no one here. However, the homes look lived in, very well lived in. There is food, cooking equipment, tables, beds, and anything else you'd expect. In one of the houses, you find food that is still warm but you don't dare try to eat it. Whoever was here left this place in a hurry 
and very recently too. Was this the encampment of those Romans you were fighting? Or maybe this was home to civilians who recieved word of your impending arrival and ran away? There is no sign of violence either, making you believe that their departure probably wasn't due to a local or 
domestic problem. Regardless, you leave everything as it was and prepare to move on."""

water = """You come across a river, with crystal clear water, clear enough to where you can perfectly see the pebbles at the bottom. The water is very calm, slowly flowing past you. After all you have been through, refreshing water is what you need. You cup water into your hands and wash your
face and body, trying to rinse off the grim, dirt, and blood on you. You eagerly fill up your canteen and then take massive glups from it, enjoying the slightly sweet water rejuvinating your body and mind. You take this time to quickly wash your dirty equipment too, especially your weapons. 
Once satisfied with your break, you get back on your feet and prepare to move on."""

# Files #

files_intro = """You come across an empty place and prepare to take a breather and prepare your gear for the future encounters. As you are doing so, you notice that there is a table with many papers on it. A lot of them are sketches and drawings of inventions that you cannot understand at all 
but there is a file that you see on the table. At a quick glance, you see that it is a page of writing in Latin, which you can read."""

charger_file = """The Charger is the first combat machine developed in the Labs, the first iteration of a long line of machine research. It arose from the need to field quick, disposable support for frontline troops and for riot control purposes. Chief Researcher Otto developed the concept of 
a suicide robot powered by a small diesel engine. Upon getting close to a target, the machine's software overrides all safety and cooling systems for the engine. By allowing the engine to reach an extremely high internal pressure and by preventing the escape of air inside of it, the engine 
becomes a miniture explosive which is then detonated by a small spark. The legs of the machine have been given powerful motors to allow it to close the distance between it and the opposition as fast as it can before detonation. However, multiple trials showed that maximum speed could only be 
achieved by removing almost all the armor on it, making it weak against a trained opponent and when there is a large distance to cover. Fortunately, the production of this machine is cheap and well within the allocated budget of Project Charger, making mass production very practical. The 
major concern on the current version of the Charger is its simplistic AI. It has no regard for the safety of anyone nearby, ally or enemy, and prioritizes killing its target over protecting its allies. Therefore, all allied personnel must run away from the Charger once the unit is activated. 

Addition: Government agents have reviewed the specifications, blueprints, and documentation. Our concerns about the safety of allied personnel was raised by the agents reassured us that our concerns were unnecessary. Crushing opposition is always a priority. Our design for Project Charger has 
been given the green light to proceed.
"""