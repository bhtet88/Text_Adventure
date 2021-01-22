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

throw_water = """As disgusting as the thought of it is, it beats a future of suffering in this hell hole. You wait for a guard to pass by your cell on their patrol, quickly cup your hands inside the bowl, scoop out some water, and throw it on the guard. You then continue to throw water at them 
while they shout, 'What the...! I'm going to beat your sorry ass and drown you in that toilet myself!' The guard swipes the key card on the reader and takes out their baton and presses a button, causing the front half of the weapon to pulse with electricity. However, as they approach you, the 
guard slips on the floor and lands head first on the ground."""

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

escape = """You know for a fact that your little victory is going to be short lived. Your shuffle made a lot of noise and the second guard must have heard something. Hearing a second set of footsteps rushing towards you, you quickly try to put on the first guard's armor and grab the stun baton."""

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

guards_retreat = """{0} The guards shuffle back as much as they can but then turn around and break into a sprint, dashing towards the stairs to Level B. 'Command, command, this is Sergeant Ryder! We need reinforcements! The {1} too much for us to handle! My unit and I are retreating to Level B!' The Sergeant's yelling echoes throughout Level C and then all is quiet."""

levelc_rest_solo = """Using this down time, you scavenge the bodies of the fallen guards, finding some armor and several healing items. You also notice the cells on this level and examine one closely. The cells, similar to the rest of the prison thus far, have the same white tile aesthetic. However, each cell also has a table, a bed with pillows instead of a stone bench, blankets, and shelves. Some even have personal items like toys, pictures, drawings, or even laptops. It is clear that equality isn't a principle of this prison and, from your experiences above ground, isn't one in society either. There is no key card for these cells, only a slot for a key. You were unable to find any keys on the guards during your searching so you will have to leave these prisoners behind. Not that they should complain since their lives are miles better than anything in Level D."""

levelc_rest_revolt = """Using this down time, you scavenge the bodies of the fallen guards, finding some armor and several healing items. You also notice the cells on this level and examine one closely. The cells, similar to the rest of the prison thus far, have the same white tile aesthetic. However, each cell also has a table, a bed with pillows instead of a stone bench, blankets, and shelves. Some even have personal items like toys, pictures, drawings, or even laptops. It is clear that equality isn't a principle of this prison and, from your experiences above ground, isn't one in society either. There is no key card for these cells, only a slot for a key. As the prisoners loot the guards, one yells 'Y'all I found the key!' and begins unlocking as many cells as possible. Others attempt to lockpick the cells open with success. The revolt is exponentially growing in size. The newly freed prisoners shower their Level D saviors with praise and make promises to spread the word of how honorable they are."""

levelc_reinforcements = """As you prepare to move on, having only at most five minutes to rest, you hear multiple pops in front of you. Then, clouds of white smoke form a barrier in front of you, making {0} cough and forcing you to retreat a few feet. Out of the smoke steps out a multiple heavily armored figures. However, they look even more prepared than the guards you just faced! Many of them are covered head to toe in armor and padding, including flak jackets, ballistic vests, and additional ceramic plates. Their helmets only cover the top and sides of their heads, exposing their faces. Some wear balaclavas, masking their entire face except for their eyes. Others wear caps or hoods instead of helmets and only wear chest pieces similar to the guards fought previously. On some vests, you see grenades, belts of ammo, and other pouches of who knows what? Most of them are carrying some sort of rifle or firearm while a select few have large, towering glass shields that say 'Federation' on their front. When standing together, they look like one unit, wearing all black with red accents. Every member seems to have their own patches on their armor and sleeves, perhaps to show ranks and their accomplishments."""

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

volk_dialogue = ["'Are you kidding? Forget my 'kind!' I'll serve under you even if I had to pay you!'", "'Hmmm, you drive a hard bargin but I surrender!'", "'What kind of spineless trash do you think I am? I'll never surrender!'", "'Fuck you, just try to kill me!'"]

volk_surrender = """Following your surrender, Volk honored his promise and didn't waste any time placing you in the unit's recruit training camp. With your experiences on the dangerous streets in the slums of the city, you proved to be an extremely capable warrior, passing test after test 
with the highest rankings. During weapons training, you showed your superiors how deadly you could be with anything, including knives, grenades, pistols, rifles, and heavy weapons. When it was time for field exercises and the final grueling weeks long testing, your bravery and leadership skills 
earned the respect of all your peers. Soon after graduation as a marksman of the 48th Rapid Response Regiment, you are promoted to Corporal and given a small squad of soldiers to command during your regular patrols of New Hope. You all get along well and become solid comrades over your months 
and years of duty. When given assignments to stop riots from the filth of the ghettos and slums, you and your team show no hesitation, making critical moves that stop the rebellion dead in its tracks and retain peace in society. Eventually, you earn enough to have a nice home in the nice part 
of the city and are able to live to your heart's content. You have earned your freedom...at the expense of others."""

volk_fight = """'Very well, it is a shame that someone like you would not like an opportunity like this. Many of your fellow prisoners wouldn't even think there was a choice. It seems you really do embody the traitorous ideals that harm the stability of the Federation. Always resisting, always 
asking for more, never knowing your place in life. You know, I looked into your prison record before coming here. The gentlemen at the CCTV room advised me to. What did you expect would happen if you tried to take part in a riot? And what's worse is that the riot was pointless too, asking for 
more food and medicine and housing when the Federation has given you more than you deserve. My men got injured in that riot, good people too. I guess this is payback for all the fine people you have hurt and killed in your sad attempt to change our perfect society! Now prepare to burn!'"""

volk_death = """'AAAAAAA!' Volk yells in pain. Then, he violently leans back against the wall and slides down, obviously too wounded from the battle to even stand up. He places his hand on a large, spurting wound, looks at his bloody glove, and opens his helmet's visor. As you approach him to deliver the final blow, he quickly grabs his radio. 'Command, this is Volk! The prisoner has defeated my entire unit and is coming to finish me off! Activate all defenses we have in the labs, including prototypes. Detonate the charges on the elevator! They must not reach the surface! It was an honor serving you! Glory to the Federation!' He then pulls out a pistol, aims it his forehead, and pulls the trigger. Someone who only wanted to go out on his own terms huh? You don't know whether to be awed by that or disgusted by it. Regardless, you take a massive breath and stand in a silent prison, surround by death everywhere. However, there is also no time to rest as after Level B, you will have reached the surface! You scavenge items you need from Volk's body and run up the stairs towards Level B. As you head upwards, you also hear an explosion and the sound of an elevator plummeting down."""

### Level B Labs ###

labs_intro = """Having reached the top of the stairs and making it to Level B, you find that there is only one way forwards: a large doorway with the words 'Labs' written above it. From what you remember from the diagram in Level D, Level B seems to be split into two distinct parts. It is about the same size as Level C horizontally but the first half of it appears taken up by what looked like machinary and robotics labs while the rest are medical labs. You notice that the ceiling is very high, about three stories tall like Level C and the entire place has the same clean white tile aesthetic of the two lower levels. There are no guards in sight. In fact, there is no enemy in sight at all. You were expecting at least some form of resistance trying to kill you, especially since Volk seemed determined to never let you leave. What about the prison guards from earlier, the ones led by a Sergeant Ryder? Where did they go? You guess you will find out as you keep going. After a deep breath, you step through the entrance to the Labs."""

first_machine = """As you continue to walk forwards, you pass through a hallway with many small rooms on either side. They all have clear glass walls, white boards and long tables in the center. Since these are the labs, you guess that this is where researchers and engineers would come together to discuss ideas and work on solutions to their problems. Other rooms seem very small but the small glass window on the metal door shows a little office, complete with a chair, desk, and computer. After passing about twenty or so rooms and not seeing a soul in sight, you become anxious and prepare for an ambush. However, you then enter a long, large room that, like Level C, is one long yet wide corridor. Instead of cells, this place has rows of lab benches, conveyor belts, assembly machines, and other things you would expect for a hub of engineers and scientists. These devices populate the entire room, essentially making it one giant workshop, where teams working on various projects or pieces of the same project can openly communicate. Many of the assembly machines have robots or some sort of machine on them, standing tall and motionless. However, as you pass the first set of robots, it suddently jerks awake and jumps off of the raised platform, blocking your path. Various other robots do the same and start approaching your position. From behind tall machinery, several humans in white shirts in next to no armor and holding wrenches come out and join the crowd. These people stand behind the machines and instead of wearing helmets, wear hard hats. Seems like these are the defenses Volk was referring to."""

### Event dialogues ###

# Files #

files_intro = """You come across an empty place and prepare to take a breather and prepare your gear for the future encounters. As you are doing so, you notice that there is a table with many papers on it. A lot of them are sketches and drawings of inventions that you cannot understand at all but there is a file that you see on the table. There is a large red CLASSIFIED, NEED TO KNOW BASIS written on the cover. Opening the file, you find a few white papers written in all English along with some pictures of the topic of the file."""

file_laser_rifle = """The creation of the LP-2043 Laser Pistol by FedTec Arms took the firearms industry by storm, mainly due to the hype of using laser powered weapons rather than their effectiveness. While not a perfect weapon by any means, the LP-2043 was the most accurate weapon of its time and is still renowned as a precision sidearm. After laser technology was proven to be practical for small arms, the weapons industry and many government owned research labs, including this one, began working on creating a new standard issue rifle that could also harness laser technology. The main issue during development was the build up of heat during prolonged fire at the fire rates desired of a fully automatic rifle. Initially, our lab created a prototype that reduced the overheating issue by making the rifle only semi automatic but the onset of new wars against threats in Asia and the Middle East caused the Federation to give severe backlash to such a soloution. Therefore, the teams went back to the drawing board, creating a completely new rifle from scratch. During a late night at the lab on December 10, 2046, Dr. Atlas and her assistant Dr. Powers made a ground breaking discovery that solved the overheating issue far before any other competitor. They managed to invent a new compound they called 'LiquiFreeze' which requires an immense about of heat to increase in temperature. Engineers set forth to making a weapon design that had a system of LiquiFreeze tubes and pipes that encased the firing mechanism and barrel. With this design, our lab managed to eliminate the overheating system entirely and by the following year, the Laser Rifle 2047, 7th iteration, designated LR 2047-7 was introduced to the Federation's Defense Force.

The LR 2047-7 proved to be an extremely capable weapon when used against all threats, foreign or domestic. It has a fire rate of 800 RPM and a battery capable of firing 50 lasers before requiring a recharge or reload. A muzzle brake is standard issue on all of these rifles to direct superheated gas from the barrel during firing upwards, creating a downward force that actively fights recoil. However, this is not a perfect system and therefore this weapon still has strong recoil, lowering its accuracy. Each rifle is also designed to come with a top rail or optical attachments and an underbarrel rail for other accessories."""