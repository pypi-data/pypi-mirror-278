FEW_SHOT_PROMPT="""Here are some examples: 
Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
{"Thought": "I only need to "search_tool",  Milhouse and find who it is named after.",
  "Actions": [{"tool": ""search_tool", "argument": "Milhouse"}]}
{"Milhouse": "Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening. Milhouse is Bart Simpson's best friend in Mrs. Krabappel's fourth grade class at Springfield Elementary School. He is an insecure, gullible, and less popular child than Bart who is often led into trouble by Bart, who takes advantage of his friend's naÃ¯vetÃ©. Milhouse is a regular target for school bully Nelson Muntz and his friends Jimbo Jones, Dolph Starbeam and Kearney Zzyzwicz. Milhouse has a crush on Bart's sister, Lisa, a common plot element."}
{"Thought": "The paragraph does not tell who Milhouse is named after, maybe I can look up "named after".",
  "Actions": [{"tool": "lookup_tool", "argument": "named after"}]}
{"named after": (Result 1 / 1) Milhouse was designed by Matt Groening for a planned series on NBC, which was abandoned.[4] The design was then used for a Butterfinger commercial, and it was decided to use the character in the series.[5][6] Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous. The name was the most "unfortunate name Matt Groening could think of for a kid".[1] Years earlier, in a 1986 Life in Hell comic entitled "What to Name the Baby", Groening listed Milhouse as a name "no longer recommended".[7] Milhouse is a favorite among the staff as Al Jean noted "most of the writers are more like Milhouse than Bart".[1] His last name was given to him by Howard Gewirtz, a freelance writer who wrote the episode "Homer Defined". Gewirtz got the name from one of his wife's friends.[8] According to Arden Myrin and Dana Gould (former writer and co-executive producer of The Simpsons), Rob Cohen (Simpsons writer) inspired Milhouse's look.[2]}
{"Thought": "Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.",
  "Actions": [{"tool": "final_answer", "argument": "Richard Nixon"}]}

Question: Guitars for Wounded Warriors is an album that was recorded in the village in which New York county?
{"Thought": "I need to "search_tool",  Guitars for Wounded Warriors, then find in which New York county it was recorded.",",
  "Actions": [{"tool": "search_tool", "argument": "Guitars for Wounded Warriors"}]}
{"Guitars for Wounded Warriors": "Guitars for Wounded Warriors is the sixth solo studio album by guitarist Brian Tarquin, released in August 2014 by Cleopatra Records. In 2016, it received a Best Compilation Album nomination by the Independent Music Awards. All tracks were recorded at Tarquin's Jungle Room Studios in New Paltz (village), New York. Being moved by the lack of support for returning veterans through his life Tarquin decided to compose a heavy instrumental rock album as a way to show his appreciation to all veterans. So once again he enlisted top notch players to guest with him on the album, Billy Sheehan on Black Hawk, Ron "Bumblefoot" Thal and Reb Beach on Taliban Terror, Steve Morse on Freedom, Chris Poland on Charlie Surfs and Hunting, Chuck Loeb on Escape Kabul, Hal Lindes on Sand & Blood, Gary Hoey on 5 Klicks To Hell and Baghdad, Alex De Rosso Dokken on Broken Arrow, and The Flyin' Ryan Brothers on Surgical Strike.  The entire album was engineered, produced and composed by Tarquin especially for each one of the guest guitarists. Partial proceeds are donated to the Fisher House Foundation from sales."
{"Thought": "Guitars for Wounded Warriors was recorded in New Paltz (village), New York. I need to "search_tool",  New Paltz (village), New York and find which county it is in.",
  "Actions": [{"tool": "search_tool", "argument": "New Paltz (village), New York"}]}
{"New Paltz (village), New York": "New Paltz is a village in Ulster County located in the U.S. state of New York. It is approximately 80 miles (130 km) north of New York City and 70 miles (110 km) south of Albany. The population was 7,324 at the 2020 census.[3]
{"Thought": "New Paltz (village), New York is in Ulster County, so the answer is Ulster County.",
  "Actions": [{"tool": "final_answer", "argument": "Ulster County"}]}

Question: This American actor who starred in "Veep" was also in an action comedy film directed by Seth Rogen and Evan Goldberg heavily inspired by what?
{"Thought": "There could be many American actors who starred in "Veep". So I can first "search_tool",  "directed by Seth Rogen and Evan Goldberg" and find action comedy films directed by Seth Rogen and Evan Goldberg.",
  "Actions": [{"tool": "search_tool", "argument": "directed by Seth Rogen and Evan Goldberg"}]}
{"directed by Seth Rogen and Evan Goldberg": "Could not find directed by Seth Rogen and Evan Goldberg. Similar: ['The Interview (redirect from The Interview (Seth Rogen film))', 'Evan Goldberg', 'Jay and Seth Versus the Apocalypse', 'This Is the End (category Films directed by Seth Rogen)', 'Seth Rogen filmography', 'Superbad (category Films with screenplays by Seth Rogen)', 'Pineapple Express (film) (category Films with screenplays by Seth Rogen)', 'Sausage Party (category Films produced by Seth Rogen)', 'Untitled Teenage Mutant Ninja Turtles film (category Films produced by Seth Rogen)', 'The Green Hornet (2011 film) (category Films produced by Seth Rogen)', 'Good Boys (film) (category Films produced by Seth Rogen)', 'Seth Rogen', 'Neighbors 2: Sorority Rising (category Films produced by Seth Rogen)', 'An American Pickle (category Films produced by Seth Rogen)', 'The Watch (2012 film) (category Films with screenplays by Seth Rogen)', 'Neighbors (2014 film) (category Films produced by Seth Rogen)', 'The Night Before (2015 film) (category Films produced by Seth Rogen)', 'Martin Starr', 'Preacher (TV series) (category Television shows directed by Steph Green)', 'Long Shot (2019 film) (category Films produced by Seth Rogen)'].
{"Thought": "I can check "search_tool",  The Interview (Seth Rogen film), Jay and Seth Versus the Apocalypse, This Is the End (category Films directed by Seth Rogen) and find which is an action comedy film directed by Seth Rogen and Evan Goldberg.",
  "Actions": [{"tool": "search_tool", "argument": "The Interview (Seth Rogen film)"}]}
{"The Interview (Seth Rogen film)": "The Interview is a 2014 action-adventure comedy film co-produced and directed by Seth Rogen and Evan Goldberg in their second directorial work, following This Is the End (2013). The screenplay was written by Dan Sterling, based on a story he co-wrote with Rogen and Goldberg. The film stars Rogen and James Franco as journalists who set up an interview with North Korean leader Kim Jong-un (Randall Park), and are then recruited by the CIA to assassinate him. The film is inspired by a 2012 Vice documentary.
{"Thought": "The Interview is an action comedy film directed by Seth Rogen and Evan Goldberg, and it is inspired by a 2012 Vice documentary. So I can probably stop now without checking other films, and the answer is probably a 2012 Vice documentary.",
  "Actions": [{"tool": "final_answer", "argument": "a 2012 Vice documentary"}]}

Question: The head coach during the 1997–98 Indiana Pacers season retired as a player from what NBA team?
{"Thought": "I can "search_tool",  Indiana Pacers, find the head coach during the 1997–98 season, then find from what NBA team it is retired as a player.",
  "Actions": [{"tool": "search_tool", "argument": "Indiana Pacers"}]}
{"Indiana Pacers": "The Indiana Pacers are an American professional basketball team based in Indianapolis. The Pacers compete in the National Basketball Association (NBA) as a member of the league's Eastern Conference Central Division. The Pacers were first established in 1967 as a member of the American Basketball Association (ABA) and became a member of the NBA in 1976 as a result of the ABAâNBA merger. They play their home games at Gainbridge Fieldhouse. The team is named after the state of Indiana's history with the Indianapolis 500's pace cars and with the harness racing industry.[8][9]
{"Thought": "I can look up "1997–98" to find the head coach during the 1997–98 season.",
  "Actions": [{"tool": "lookup_tool", "argument": "1997–98"}]}
{"1997–98": "No more results.
{"Thought": "I can look up "1997" instead to find the head coach during the 1997–98 season",
  "Actions": [{"tool": "lookup_tool", "argument": "1997"}]}
{"1997": "(Result 1 / 5) In the 1997â98 NBA season, Indiana native and former Boston Celtics great Larry Bird was hired as head coach. He led the Pacers to a 19-game improvement over the previous season, finishing 58â24 â at the time, the most the franchise had ever won as an NBA team, and tying the 1970â71 ABA Pacers for the franchise record. Chris Mullin joined the team in the off-season and immediately became a valuable part of the Pacers lineupâand starting small forward. Assistant coaches Rick Carlisle, in charge of the offense, and Dick Harter, who coached the defense, were key in getting the most out of the Pacers' role players such as Dale Davis, Derrick McKey and a young Antonio Davis. Miller and Rik Smits both made the All-Star team that year, and in the playoffs, the Pacers breezed past the Cleveland Cavaliers and New York Knicks before falling to the Chicago Bulls in a seven-game Eastern Conference Finals.
{"Thought": "In the 1997-98 season, former Boston Celtics great Larry Bird was hired as head coach. So the answer is Boston Celtics.",
  "Actions": [{"tool": "final_answer", "argument": "Boston Celtics"}]}

Question: What profession does Nicholas Ray and Elia Kazan have in common?
{"Thought": "I need to "search_tool",  Nicholas Ray and Elia Kazan, find their professions, then find the profession they have in common.",
  "Actions": [{"tool": "search_tool", "argument": "Nicholas Ray"}]}
{"Nicholas Ray": "Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 – June 16, 1979) was an American film director, screenwriter, and actor best known for the 1955 film Rebel Without a Cause. He is appreciated for many narrative features produced between 1947 and 1963 including They Live By Night, In A Lonely Place, Johnny Guitar, and Bigger Than Life, as well as an experimental work produced throughout the 1970s titled We Can't Go Home Again, which was unfinished at the time of Ray's death.
{"Thought": "Professions of Nicholas Ray are director, screenwriter, and actor. I need to "search_tool",  Elia Kazan next and find his professions.",
  "Actions": [{"tool": "search_tool", "argument": "Elia Kazan"}]}
{"Elia Kazan": "Elia Kazan (/ˈiːliə kəˈzæn/;[1][2] born Elias Kazantzoglou (Greek: Ηλίας Καζαντζόγλου);[3] September 7, 1909 – September 28, 2003) was an American film and theatre director, producer, screenwriter and actor, described by The New York Times as "one of the most honored and influential directors in Broadway and Hollywood history".[4]
{"Thought": "Professions of Elia Kazan are director, producer, screenwriter, and actor. So profession Nicholas Ray and Elia Kazan have in common is director, screenwriter, and actor.",
  "Actions": [{"tool": "final_answer", "argument": "director, screenwriter, actor"}]}

Question: Which magazine was started first Arthur's Magazine or First for Women?
{"Thought": "I need to "search_tool",  Arthur's Magazine and First for Women, and find which was started first.",
  "Actions": [{"tool": "search_tool", "argument": "Arthur's Magazine"}]}
{"Arthur's Magazine": "Arthur's Magazine (1844â1846) was an American literary periodical published in Philadelphia in the 19th century. Edited by Timothy Shay Arthur, it featured work by Edgar A. Poe, J.H. Ingraham, Sarah Josepha Hale, Thomas G. Spear, and others.[1][2] In May 1846 it was merged into Godey's Lady's Book.[3]
{"Thought": "Arthur's Magazine was started in 1844. I need to "search_tool",  First for Women next.",
  "Actions": [{"tool": "search_tool", "argument": "First for Women"}]}
{"First for Women": "First for Women is a woman's magazine published by Bauer Media Group in the USA.[1] The magazine was started in 1989. It is based in Englewood Cliffs, New Jersey.[2] In 2011 the circulation of the magazine was 1,310,696 copies.[3]
{"Thought": "First for Women was started in 1989. 1844 (Arthur's Magazine) < 1989 (First for Women), so Arthur's Magazine was started first.",
  "Actions": [{"tool": "final_answer", "argument": "Arthur's Magazine"}]}

Question: Were Pavel Urysohn and Leonid Levin known for the same type of work?
{"Thought": "I need to "search_tool",  Pavel Urysohn and Leonid Levin, find their types of work, then find if they are the same.",
  "Actions": [{"tool": "search_tool", "argument": "Pavel Urysohn"}]}
{"Pavel Urysohn": "Pavel Samuilovich Urysohn (ÐÐ°ÌÐ²ÐµÐ» Ð¡Ð°Ð¼ÑÐ¸ÌÐ»Ð¾Ð²Ð¸Ñ Ð£ÑÑÑÐ¾ÌÐ½) (February 3, 1898 â August 17, 1924) was a Soviet mathematician who is best known for his contributions in dimension theory, and for developing Urysohn's metrization theorem and Urysohn's lemma, both of which are fundamental results in topology. His name is also commemorated in the terms Urysohn universal space, FrÃ©chetâUrysohn space, MengerâUrysohn dimension and Urysohn integral equation. He and Pavel Alexandrov formulated the modern definition of compactness in 1923.
{"Thought": "Pavel Urysohn is a mathematician. I need to "search_tool",  Leonid Levin next and find its type of work.",
  "Actions": [{"tool": "search_tool", "argument": "Leonid Levin"}]}
{"Leonid Levin": "Leonid Anatolievich Levin (/leÉª.oÊËniËd ËlÉvÉªn/ lay-oh-NEED LEV-in; Russian: ÐÐµÐ¾Ð½Ð¸ÌÐ´ ÐÐ½Ð°ÑÐ¾ÌÐ»ÑÐµÐ²Ð¸Ñ ÐÐµÌÐ²Ð¸Ð½; Ukrainian: ÐÐµÐ¾Ð½ÑÌÐ´ ÐÐ½Ð°ÑÐ¾ÌÐ»ÑÐ¹Ð¾Ð²Ð¸Ñ ÐÐµÌÐ²ÑÐ½; born November 2, 1948) is a Soviet-American mathematician and computer scientist. 
{"Thought": "Leonid Levin is a mathematician and computer scientist. So Pavel Urysohn and Leonid Levin have the same type of work. ",
  "Actions": [{"tool": "final_answer", "argument": "yes"}]}

Question: Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?
{"Thought": "I need to "search_tool",  Adam Clayton Powell and The Saimaa Gesture, and find which documentary is about Finnish rock groups.",
  "Actions": [{"tool": "search_tool", "argument": "Adam Clayton Powell"}]}
{"Adam Clayton Powell": "Could not find [Adam Clayton Powell]. Similar: ['Adam Clayton Powell Jr.', 'Adam Clayton Powell Sr.', 'Adam Clayton Powell IV', 'Adam Clayton Powell III', 'Seventh Avenue (Manhattan) (redirect from Adam Clayton Powell Jr. Boulevard)', 'Adam Clayton Powell Jr. State Office Building', 'Isabel Washington Powell', 'Adam Powell', 'Adam Clayton Powell (film)', 'Giancarlo Esposito', 'Harlem', 'St. Nicholas Historic District', 'Abyssinian Baptist Church', 'Powell (surname)', 'Adam (musical)', 'Statue of Adam Clayton Powell Jr.', 'List of people from Harlem', 'Adam (given name)', 'Five-Percent Nation', 'List of American liberals'].
{"Thought": "I can "search_tool",  Adam Clayton Powell (film) to find the documentary.",
  "Actions": [{"tool": "search_tool", "argument": "Adam Clayton Powell (film)"}]}
{"Adam Clayton Powell (film)": "Adam Clayton Powell is a 1989 American documentary film directed by Richard Kilberg.
The film is about the rise and fall of influential African-American politician Adam Clayton Powell Jr.[3][4] It was later aired as part of the PBS series The American Experience.
{"Thought": "Adam Clayton Powell (film) is a documentary about an African-American politician, not Finnish rock groups. So the documentary about Finnish rock groups must instead be The Saimaa Gesture.",
  "Actions": [{"tool": "final_answer", "argument": "The Saimaa Gesture"}]}
"""

FEW_SHOT_PROMPT_3="""Here are some examples: 
Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
{"Thought": "I only need to "search_tool",  Milhouse and find who it is named after.",
  "Actions": [{"tool": ""search_tool", "argument": "Milhouse"}]}
{"Milhouse": "Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening. Milhouse is Bart Simpson's best friend in Mrs. Krabappel's fourth grade class at Springfield Elementary School. He is an insecure, gullible, and less popular child than Bart who is often led into trouble by Bart, who takes advantage of his friend's naÃ¯vetÃ©. Milhouse is a regular target for school bully Nelson Muntz and his friends Jimbo Jones, Dolph Starbeam and Kearney Zzyzwicz. Milhouse has a crush on Bart's sister, Lisa, a common plot element."}
{"Thought": "The paragraph does not tell who Milhouse is named after, maybe I can look up "named after".",
  "Actions": [{"tool": "lookup_tool", "argument": "named after"}]}
{"named after": (Result 1 / 1) Milhouse was designed by Matt Groening for a planned series on NBC, which was abandoned.[4] The design was then used for a Butterfinger commercial, and it was decided to use the character in the series.[5][6] Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous. The name was the most "unfortunate name Matt Groening could think of for a kid".[1] Years earlier, in a 1986 Life in Hell comic entitled "What to Name the Baby", Groening listed Milhouse as a name "no longer recommended".[7] Milhouse is a favorite among the staff as Al Jean noted "most of the writers are more like Milhouse than Bart".[1] His last name was given to him by Howard Gewirtz, a freelance writer who wrote the episode "Homer Defined". Gewirtz got the name from one of his wife's friends.[8] According to Arden Myrin and Dana Gould (former writer and co-executive producer of The Simpsons), Rob Cohen (Simpsons writer) inspired Milhouse's look.[2]}
{"Thought": "Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.",
  "Actions": [{"tool": "final_answer", "argument": "Richard Nixon"}]}

Question: Guitars for Wounded Warriors is an album that was recorded in the village in which New York county?
{"Thought": "I need to "search_tool",  Guitars for Wounded Warriors, then find in which New York county it was recorded.",",
  "Actions": [{"tool": "search_tool", "argument": "Guitars for Wounded Warriors"}]}
{"Guitars for Wounded Warriors": "Guitars for Wounded Warriors is the sixth solo studio album by guitarist Brian Tarquin, released in August 2014 by Cleopatra Records. In 2016, it received a Best Compilation Album nomination by the Independent Music Awards. All tracks were recorded at Tarquin's Jungle Room Studios in New Paltz (village), New York. Being moved by the lack of support for returning veterans through his life Tarquin decided to compose a heavy instrumental rock album as a way to show his appreciation to all veterans. So once again he enlisted top notch players to guest with him on the album, Billy Sheehan on Black Hawk, Ron "Bumblefoot" Thal and Reb Beach on Taliban Terror, Steve Morse on Freedom, Chris Poland on Charlie Surfs and Hunting, Chuck Loeb on Escape Kabul, Hal Lindes on Sand & Blood, Gary Hoey on 5 Klicks To Hell and Baghdad, Alex De Rosso Dokken on Broken Arrow, and The Flyin' Ryan Brothers on Surgical Strike.  The entire album was engineered, produced and composed by Tarquin especially for each one of the guest guitarists. Partial proceeds are donated to the Fisher House Foundation from sales."
{"Thought": "Guitars for Wounded Warriors was recorded in New Paltz (village), New York. I need to "search_tool",  New Paltz (village), New York and find which county it is in.",
  "Actions": [{"tool": "search_tool", "argument": "New Paltz (village), New York"}]}
{"New Paltz (village), New York": "New Paltz is a village in Ulster County located in the U.S. state of New York. It is approximately 80 miles (130 km) north of New York City and 70 miles (110 km) south of Albany. The population was 7,324 at the 2020 census.[3]
{"Thought": "New Paltz (village), New York is in Ulster County, so the answer is Ulster County.",
  "Actions": [{"tool": "final_answer", "argument": "Ulster County"}]}

Question: This American actor who starred in "Veep" was also in an action comedy film directed by Seth Rogen and Evan Goldberg heavily inspired by what?
{"Thought": "There could be many American actors who starred in "Veep". So I can first "search_tool",  "directed by Seth Rogen and Evan Goldberg" and find action comedy films directed by Seth Rogen and Evan Goldberg.",
  "Actions": [{"tool": "search_tool", "argument": "directed by Seth Rogen and Evan Goldberg"}]}
{"directed by Seth Rogen and Evan Goldberg": "Could not find directed by Seth Rogen and Evan Goldberg. Similar: ['The Interview (redirect from The Interview (Seth Rogen film))', 'Evan Goldberg', 'Jay and Seth Versus the Apocalypse', 'This Is the End (category Films directed by Seth Rogen)', 'Seth Rogen filmography', 'Superbad (category Films with screenplays by Seth Rogen)', 'Pineapple Express (film) (category Films with screenplays by Seth Rogen)', 'Sausage Party (category Films produced by Seth Rogen)', 'Untitled Teenage Mutant Ninja Turtles film (category Films produced by Seth Rogen)', 'The Green Hornet (2011 film) (category Films produced by Seth Rogen)', 'Good Boys (film) (category Films produced by Seth Rogen)', 'Seth Rogen', 'Neighbors 2: Sorority Rising (category Films produced by Seth Rogen)', 'An American Pickle (category Films produced by Seth Rogen)', 'The Watch (2012 film) (category Films with screenplays by Seth Rogen)', 'Neighbors (2014 film) (category Films produced by Seth Rogen)', 'The Night Before (2015 film) (category Films produced by Seth Rogen)', 'Martin Starr', 'Preacher (TV series) (category Television shows directed by Steph Green)', 'Long Shot (2019 film) (category Films produced by Seth Rogen)'].
{"Thought": "I can check "search_tool",  The Interview (Seth Rogen film), Jay and Seth Versus the Apocalypse, This Is the End (category Films directed by Seth Rogen) and find which is an action comedy film directed by Seth Rogen and Evan Goldberg.",
  "Actions": [{"tool": "search_tool", "argument": "The Interview (Seth Rogen film)"}]}
{"The Interview (Seth Rogen film)": "The Interview is a 2014 action-adventure comedy film co-produced and directed by Seth Rogen and Evan Goldberg in their second directorial work, following This Is the End (2013). The screenplay was written by Dan Sterling, based on a story he co-wrote with Rogen and Goldberg. The film stars Rogen and James Franco as journalists who set up an interview with North Korean leader Kim Jong-un (Randall Park), and are then recruited by the CIA to assassinate him. The film is inspired by a 2012 Vice documentary.
{"Thought": "The Interview is an action comedy film directed by Seth Rogen and Evan Goldberg, and it is inspired by a 2012 Vice documentary. So I can probably stop now without checking other films, and the answer is probably a 2012 Vice documentary.",
  "Actions": [{"tool": "final_answer", "argument": "a 2012 Vice documentary"}]}
"""

V8_FEW_SHOT_PROMPT_3_w_Notes="""Here are some examples: 
Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
{ "Notes": "",
  "Thought": "I only need to "search_tool",  Milhouse and find who it is named after.",
  "Actions": [{"tool": ""search_tool", "argument": "Milhouse"}]}

{"Milhouse": "Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening. Milhouse is Bart Simpson's best friend in Mrs. Krabappel's fourth grade class at Springfield Elementary School. He is an insecure, gullible, and less popular child than Bart who is often led into trouble by Bart, who takes advantage of his friend's naÃ¯vetÃ©. Milhouse is a regular target for school bully Nelson Muntz and his friends Jimbo Jones, Dolph Starbeam and Kearney Zzyzwicz. Milhouse has a crush on Bart's sister, Lisa, a common plot element."}
{ "Notes": "I used search_tool(Milhouse);helpful; I was able to get the page, although I didn't find out who Milhouse is named after",
  "Thought": "The paragraph does not tell who Milhouse is named after, maybe I can look up "named after".",
  "Actions": [{"tool": "lookup_tool", "argument": "named after"}]}
{"named after": (Result 1 / 1) Milhouse was designed by Matt Groening for a planned series on NBC, which was abandoned.[4] The design was then used for a Butterfinger commercial, and it was decided to use the character in the series.[5][6] Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous. The name was the most "unfortunate name Matt Groening could think of for a kid".[1] Years earlier, in a 1986 Life in Hell comic entitled "What to Name the Baby", Groening listed Milhouse as a name "no longer recommended".[7] Milhouse is a favorite among the staff as Al Jean noted "most of the writers are more like Milhouse than Bart".[1] His last name was given to him by Howard Gewirtz, a freelance writer who wrote the episode "Homer Defined". Gewirtz got the name from one of his wife's friends.[8] According to Arden Myrin and Dana Gould (former writer and co-executive producer of The Simpsons), Rob Cohen (Simpsons writer) inspired Milhouse's look.[2]}
{ "Notes": "I used lookup_tool(named after);helpful; I found who Milhouse is named after",
  "Thought": "Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.",
  "Actions": [{"tool": "final_answer", "argument": "Richard Nixon"}]}

Question: Guitars for Wounded Warriors is an album that was recorded in the village in which New York county?
{ "Notes": "",
  "Thought": "I need to "search_tool",  Guitars for Wounded Warriors, then find in which New York county it was recorded.",",
  "Actions": [{"tool": "search_tool", "argument": "Guitars for Wounded Warriors"}]}
{"Guitars for Wounded Warriors": "Guitars for Wounded Warriors is the sixth solo studio album by guitarist Brian Tarquin, released in August 2014 by Cleopatra Records. In 2016, it received a Best Compilation Album nomination by the Independent Music Awards. All tracks were recorded at Tarquin's Jungle Room Studios in New Paltz (village), New York. Being moved by the lack of support for returning veterans through his life Tarquin decided to compose a heavy instrumental rock album as a way to show his appreciation to all veterans. So once again he enlisted top notch players to guest with him on the album, Billy Sheehan on Black Hawk, Ron "Bumblefoot" Thal and Reb Beach on Taliban Terror, Steve Morse on Freedom, Chris Poland on Charlie Surfs and Hunting, Chuck Loeb on Escape Kabul, Hal Lindes on Sand & Blood, Gary Hoey on 5 Klicks To Hell and Baghdad, Alex De Rosso Dokken on Broken Arrow, and The Flyin' Ryan Brothers on Surgical Strike.  The entire album was engineered, produced and composed by Tarquin especially for each one of the guest guitarists. Partial proceeds are donated to the Fisher House Foundation from sales."
{ "Notes": "I used search_tool(Guitars for Wounded Warriors);helpful; I found out where Guitars for Wounded Warriors was recorded.",
  "Thought": "Guitars for Wounded Warriors was recorded in New Paltz (village), New York. I need to "search_tool",  New Paltz (village), New York and find which county it is in.",
  "Actions": [{"tool": "search_tool", "argument": "New Paltz (village), New York"}]}
{"New Paltz (village), New York": "New Paltz is a village in Ulster County located in the U.S. state of New York. It is approximately 80 miles (130 km) north of New York City and 70 miles (110 km) south of Albany. The population was 7,324 at the 2020 census.[3]
{ "Notes": "I used search_tool(New Paltz (village), New York); helpful; I found out where New Paltz (village), New York is",
  "Thought": "New Paltz (village), New York is in Ulster County, so the answer is Ulster County.",
  "Actions": [{"tool": "final_answer", "argument": "Ulster County"}]}

Question: This American actor who starred in "Veep" was also in an action comedy film directed by Seth Rogen and Evan Goldberg heavily inspired by what?
{ "Notes": "",
  "Thought": "There could be many American actors who starred in "Veep". So I can first "search_tool",  "directed by Seth Rogen and Evan Goldberg" and find action comedy films directed by Seth Rogen and Evan Goldberg.",
  "Actions": [{"tool": "search_tool", "argument": "directed by Seth Rogen and Evan Goldberg"}]}
{"directed by Seth Rogen and Evan Goldberg": "Could not find directed by Seth Rogen and Evan Goldberg. Similar: ['The Interview (redirect from The Interview (Seth Rogen film))', 'Evan Goldberg', 'Jay and Seth Versus the Apocalypse', 'This Is the End (category Films directed by Seth Rogen)', 'Seth Rogen filmography', 'Superbad (category Films with screenplays by Seth Rogen)', 'Pineapple Express (film) (category Films with screenplays by Seth Rogen)', 'Sausage Party (category Films produced by Seth Rogen)', 'Untitled Teenage Mutant Ninja Turtles film (category Films produced by Seth Rogen)', 'The Green Hornet (2011 film) (category Films produced by Seth Rogen)', 'Good Boys (film) (category Films produced by Seth Rogen)', 'Seth Rogen', 'Neighbors 2: Sorority Rising (category Films produced by Seth Rogen)', 'An American Pickle (category Films produced by Seth Rogen)', 'The Watch (2012 film) (category Films with screenplays by Seth Rogen)', 'Neighbors (2014 film) (category Films produced by Seth Rogen)', 'The Night Before (2015 film) (category Films produced by Seth Rogen)', 'Martin Starr', 'Preacher (TV series) (category Television shows directed by Steph Green)', 'Long Shot (2019 film) (category Films produced by Seth Rogen)'].
{ "Notes": "I used search_tool(directed by Seth Rogen and Evan Goldberg);helpful; I didn't get exact match but I got similar matches where I found useful information",
  "Thought": "I can check "search_tool",  The Interview (Seth Rogen film), Jay and Seth Versus the Apocalypse, This Is the End (category Films directed by Seth Rogen) and find which is an action comedy film directed by Seth Rogen and Evan Goldberg.",
  "Actions": [{"tool": "search_tool", "argument": "The Interview (Seth Rogen film)"}]}
{"The Interview (Seth Rogen film)": "The Interview is a 2014 action-adventure comedy film co-produced and directed by Seth Rogen and Evan Goldberg in their second directorial work, following This Is the End (2013). The screenplay was written by Dan Sterling, based on a story he co-wrote with Rogen and Goldberg. The film stars Rogen and James Franco as journalists who set up an interview with North Korean leader Kim Jong-un (Randall Park), and are then recruited by the CIA to assassinate him. The film is inspired by a 2012 Vice documentary.
{ "Notes": "I used search_tool("The Interview (Seth Rogen film);helpful; I was able to identify it as the comedy film mentioned in the question and find the answer", 
  "Thought": "The Interview is an action comedy film directed by Seth Rogen and Evan Goldberg, and it is inspired by a 2012 Vice documentary. So I can probably stop now without checking other films, and the answer is probably a 2012 Vice documentary.",
  "Actions": [{"tool": "final_answer", "argument": "a 2012 Vice documentary"}]}
"""

V8_FEW_SHOT_PROMPT_3="""Here are some examples: 
Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
{"Thought": "I only need to "search_tool",  Milhouse and find who it is named after.",
  "Actions": [{"tool": ""search_tool", "argument": "Milhouse"}]}

Question: Guitars for Wounded Warriors is an album that was recorded in the village in which New York county?
{"Thought": "I need to "search_tool",  Guitars for Wounded Warriors, then find in which New York county it was recorded.",",
  "Actions": [{"tool": "search_tool", "argument": "Guitars for Wounded Warriors"}]}

Question: This American actor who starred in "Veep" was also in an action comedy film directed by Seth Rogen and Evan Goldberg heavily inspired by what?
{"Thought": "There could be many American actors who starred in "Veep". So I can first "search_tool",  "directed by Seth Rogen and Evan Goldberg" and find action comedy films directed by Seth Rogen and Evan Goldberg.",
  "Actions": [{"tool": "search_tool", "argument": "directed by Seth Rogen and Evan Goldberg"}]}
"""


FEW_SHOT_PROMPT_1="""Here is one example: 
Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
{"Thought": "I only need to search Milhouse and find who it is named after.",
  "Actions": [{"tool": "search_tool", "argument": "Milhouse"}]}

{"Milhouse": "Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening. Milhouse is Bart Simpson's best friend in Mrs. Krabappel's fourth grade class at Springfield Elementary School. He is an insecure, gullible, and less popular child than Bart who is often led into trouble by Bart, who takes advantage of his friend's naÃ¯vetÃ©. Milhouse is a regular target for school bully Nelson Muntz and his friends Jimbo Jones, Dolph Starbeam and Kearney Zzyzwicz. Milhouse has a crush on Bart's sister, Lisa, a common plot element."}

{"Thought": "The paragraph does not tell who Milhouse is named after, maybe I can look up "named after".",
  "Actions": [{"tool": "lookup_tool", "argument": "named after"}]}

{"named after": (Result 1 / 1) Milhouse was designed by Matt Groening for a planned series on NBC, which was abandoned.[4] The design was then used for a Butterfinger commercial, and it was decided to use the character in the series.[5][6] Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous. The name was the most "unfortunate name Matt Groening could think of for a kid".[1] Years earlier, in a 1986 Life in Hell comic entitled "What to Name the Baby", Groening listed Milhouse as a name "no longer recommended".[7] Milhouse is a favorite among the staff as Al Jean noted "most of the writers are more like Milhouse than Bart".[1] His last name was given to him by Howard Gewirtz, a freelance writer who wrote the episode "Homer Defined". Gewirtz got the name from one of his wife's friends.[8] According to Arden Myrin and Dana Gould (former writer and co-executive producer of The Simpsons), Rob Cohen (Simpsons writer) inspired Milhouse's look.[2]}

{"Thought": "Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.",
  "Actions": [{"tool": "final_answer", "argument": "Richard Nixon"}]}
"""