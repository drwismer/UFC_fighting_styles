# ----------------- Import Libraries and Data ----------------- #

import streamlit as st
import streamlit.components.v1 as components

import pandas as pd

import pickle


# ----------------- Streamlit Formatting ----------------- #

# Wide layout
st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
    .reportview-container {
        background-image: linear-gradient(to bottom right, #000000, #0c0c0c, #1f1f1f, #444444, #676767, #989898, #adadad);
        color: #110022;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ----------------- Streamlit Functions ----------------- #

def make_title(pages, color):
    st.markdown("<h1 style='text-align: left; color: "+color+";'>"+pages+"</h1>", unsafe_allow_html=True)

def make_subtitle(pages, color):
    st.markdown("<h2 style='text-align: left; color: "+color+";'>"+pages+"</h2>", unsafe_allow_html=True)

def blurb(text, color):
    st.markdown("<p style='text-align: left; color: "+color+";'>"+text+"</p>", unsafe_allow_html=True)
    

# ----------------- Fight Style Images and Descriptions ----------------- #


style_dict = {'Chinny Grappler' : {'style_rep_name' : 'Chael Sonnen',
                                   'style_rep_img' : 'chael_sonnen.png',
                                   'box_whisker_img' : ['chinny_grappler/cg_tko_loss.png',
                                                        'chinny_grappler/cg_kd_per_head.png',
                                                        'chinny_grappler/cg_td_att.png',
                                                        'chinny_grappler/cg_clinch_rate.png',
                                                        'chinny_grappler/cg_control.png',
                                                       ],
                                   'desc' : ['',
                                             'The Chinny Grappler fight syle is portrayed by such ' +
                                             'fighers as Chael Sonnen, Curtis Blaydes, and Matt Hughes. ' +
                                             'The name may be a bit harsh, but the basic concept is that ' +
                                             'these fighters aim to control opponents through their ' +
                                             'grappling. When that fails, things may become problematic.',
                                             '',
                                             'Chinny Grapplers generally attempt more takedowns and have ' +
                                             'much more control time than other fight styles. They also ' +
                                             'fight out of the clinch at a higher rate. However, on ' +
                                             'average, they are also more prone to knockdowns from head ' +
                                             'strikes and have a higher rate of loss by TKO. They do not ' +
                                             'often lose by decision.',
                                             '',
                                             'Historically, the Chinny Grappler fares best against ' +
                                             'Stand and Bang fighters, Glass Cannons, and High Risk Sub ' +
                                             'Artists. The Chinny Grappler may be able to neutralize the ' +
                                             'strengths of each of these styles through superior grappling.',
                                             '',
                                             'They struggle most against Tacticians and Grind ' +
                                             'It Out style fighters. Tacticians are likely able to avoid ' +
                                             'their takedowns, while Grind It Out fighters can withstand ' +
                                             'the grappling long enough to find a knockout or grind to a ' +
                                             'decision win.'
                                            ]
                                  },
              'Glass Cannon' : {'style_rep_name' : 'Alistair Overeem',
                                'style_rep_img' : 'alistair_overeem.png',
                                'box_whisker_img' : ['glass_cannon/gc_tko_win.png',
                                                     'glass_cannon/gc_kd_per_head.png',
                                                     'glass_cannon/gc_finish_loss.png',
                                                     'glass_cannon/gc_opp_kd_per_head.png',
                                                     'glass_cannon/gc_opp_control.png',
                                                    ],
                                'desc' : ['',
                                          'The Glass Cannon fight syle is portrayed by such ' +
                                          'fighters as Alistair Overeem, Luke Rockhold, and Josh ' +
                                          'Barnett. As you might expect, Glass Cannons appear more in ' +
                                          'the heavier weight classes, but this isn\'t a perfect rule. ' +
                                          'A Glass Cannon is a fighter that can turn the lights out, ' +
                                          'but is at serious risk of suffering the same fate.',
                                          '',
                                          'Glass Cannons have a higher than average TKO win rate, but ' +
                                          'they also have a higher TKO loss rate and overall opponent ' +
                                          'finish rate. They record more knockdowns per significant ' +
                                          'strike and signficant head strike, but the same is true of ' +
                                          'their opponents. These fighters also have a higher opponent ' +
                                          'control time, as they are likely to tire out when they can\'t ' +
                                          'get the knockout in the early rounds.',
                                           '',
                                          'Historically, the Glass Cannon fares best against Pressure ' +
                                          'Wrestlers, High Risk Sub Artists, and Stick and Move fighters ' +
                                          '(although this last group has the slight edge). Perhaps the Glass ' +
                                          'Cannon is able to count on the takedowns of Pressure Wrestlers ' +
                                          'in order to time their knockout blow.',
                                          '',
                                          'They struggle most against Chinny Grapplers and Stand and Bang ' +
                                          'fighters. Chinny Grapplers are likely to take them down and wear ' +
                                          'out their gas tank, whereas Stand and Bang fighters are able to ' +
                                          'withstand a beating and take Glass Cannons into the deep ' +
                                          'waters of the later rounds.'
                                         ]
                               },
              'Grind It Out' : {'style_rep_name' : 'Tim Elliott',
                                'style_rep_img' : 'tim_elliott.png',
                                'box_whisker_img' : ['grind_it_out/gio_finish_win.png',
                                                     'grind_it_out/gio_dec_loss.png',
                                                     'grind_it_out/gio_opp_control.png',
                                                     'grind_it_out/gio_opp_kd_per_strike.png',
                                                     'grind_it_out/gio_sig_land.png'
                                                    ],
                                'desc' : ['',
                                          'The Grind It Out fight syle is portrayed by such ' +
                                          'fighters as Tim Elliott, Aljamain Sterling, and Neil Magny. ' +
                                          'Many of these fighters are from the lighter weight classes, ' +
                                          'which tend to have better stamina. This is not a common fight ' +
                                          'style, and very few fighters have Grind It Out as their dominant ' +
                                          'style.',
                                          '',
                                          'Grind It Out fighters are more likely to take fights to decision, ' +
                                          'having both a slightly lower finish rate and a higher loss by ' +
                                          'decision rate. While their opponents have a higher control time ' +
                                          'than other styles, Grind It Out fighters are still able, on average, ' +
                                          'to land more significant strikes than other fight styles. They also ' +
                                          'have a slightly lower opponent knockdown per significant strike ' +
                                          'rate. This is all to say that Grind It Out fighters do not ' + 
                                          'necessarily have the best striking or grappling among all fight styles, ' +
                                          'but they make up for it in grit. You might call them "scrappy."',
                                           '',
                                          'Historically, Grind It Out fighters fare best against Chinny ' +
                                          'Grapplers, High Risk Sub Artists, and Glass Cannons. These are all ' +
                                          'styles that perform best against styles with specific weaknesses, ' +
                                          'but Grind It Out fighters can often push through their mistakes.',
                                          '',
                                          'Grind It Out fighters struggle most against Tacticians and Stick ' +
                                          'and Move Fighters. Tactitians are well rounded, and while they may ' +
                                          'not finish Grind It Out fighters, they can win by judges\' ' +
                                          'decision. Stick and Move fighters are adept at staying on their ' + 
                                          'feet and are also likely to outpoint Grind It Out fighters.' 
                                         ]
                               },
              'Head Hunting Wrestler' : {'style_rep_name' : 'Josh Koshcheck',
                                         'style_rep_img' : 'josh_koshcheck.png',
                                         'box_whisker_img' : ['head_hunting_wrestler/hhw_head_rate.png',
                                                              'head_hunting_wrestler/hhw_sig_acc.png',
                                                              'head_hunting_wrestler/hhw_td_land.png',
                                                              'head_hunting_wrestler/hhw_td_abs.png',
                                                              'head_hunting_wrestler/hhw_control.png'
                                                             ],
                                         'desc' : ['',
                                                   'The Head Hunting Wrestler fight syle is portrayed by such ' +
                                                   'fighters as Josh Koshcheck, Brendan Schaub, and Rashad Evans. ' +
                                                   'Fighters with this style can wrestle, and often do, but they ' +
                                                   'also use wrestling to set up their striking. They often go for the ' +
                                                   'knockout, unlike the Pressure Wrestler, for example.',
                                                   '',
                                                   'Head Hunting Wresters have a higher rate of strikes aimed at the ' +
                                                   'head versus other styles. This translates to a lower ' +
                                                   'significant strike accuracy. These fighters also land takedowns ' +
                                                   'at a higher rate and are difficult for an opponent to take down. ' +
                                                   'While they get more takedowns than average, their control time is not ' +
                                                   'particular high, which could be why they go for the knockout at a ' +
                                                   'higher rate.', 
                                                   '',
                                                   'Historically, the Head Hunting Wrestler fares best against High ' +
                                                   'Risk Sub Artists and Pressure Wrestlers. Their grappling may be ' +
                                                   'enough to neutralize the strengths of these fighting styles, while ' +
                                                   'their willingness to go for broke pairs well with the High Risk ' +
                                                   'Sub Artists\' poor striking defense.'
                                                   '',
                                                   'They struggle most against Tacticians and Stick and Move fighters, ' +
                                                   'both of which are adept at avoiding takedowns and power punches.'
                                                  ]
                                        },
              'High Risk Sub Artist' : {'style_rep_name' : 'Alexei Oleinik',
                                        'style_rep_img' : 'alexei_oleinik.png',
                                        'box_whisker_img' : ['high_risk_sub_artist/hrsa_sub_att.png',
                                                             'high_risk_sub_artist/hrsa_sub_win.png',
                                                             'high_risk_sub_artist/hrsa_sig_abs.png',
                                                             'high_risk_sub_artist/hrsa_opp_control.png',
                                                             'high_risk_sub_artist/hrsa_opp_sig_acc.png'
                                                            ],
                                        'desc' : ['',
                                                  'The High Risk Sub Artist fight syle is portrayed by such ' +
                                                  'fighters as Aleksei Oleinik, Gerald Meerschaert, and Mickey Gall. ' +
                                                  'These fighters put themselves in harm\'s way, often leaning on ' +
                                                  'their submission skills as their only out. This is the least ' +
                                                  'effective fight style, holding an advantage over no other styles.',
                                                  '',
                                                  'High Risk Sub Artists allow their opponents to land strikes at a ' +
                                                  'higher rate and with better accuracy than other styles. They also ' +
                                                  'give up more control time to their opponents, on average. As a ' +
                                                  'result, they most often lose by decision, but they have the highest ' + 
                                                  'win by submission rate and attempt more submissions than any other '
                                                  'fight style.',
                                                  '',
                                                  'High Risk Sub Artists do not hold a historical advantage over any ' +
                                                  'other style, but they fare best against Glass Cannons and Patient ' +
                                                  'Power Punchers. In the case of Glass Cannons, the High Risk Sub ' + 
                                                  'Artist is most likely to win by submission in the later rounds as ' +
                                                  'the Glass Cannon tires. For Patient Power Punchers, perhaps they '
                                                  'sometimes get too patient and give the High Risk Sub Artist enough '
                                                  'time to find their submission.',
                                                  '',
                                                  'They struggle most against Tacticians, Stand and Bang fighters, and ' +
                                                  'Pressure Wrestlers. Tactians are too clever to put themselves in ' +
                                                  'dangerous grappling positions, Stand and Bang fighters are adept ' +
                                                  'at keeping the fight on the feet, and Pressure Wrestlers generally ' +
                                                  'control the majority of grappling exchanges.'
                                                 ]
                                       },
              'Patient Power Puncher' : {'style_rep_name' : 'Anthony Johnson',
                                         'style_rep_img' : 'anthony_johnson.png',
                                         'box_whisker_img' : ['patient_power_puncher/ppp_tko_win.png',
                                                              'patient_power_puncher/ppp_sig_land.png',
                                                              'patient_power_puncher/ppp_kd_per_sig.png',
                                                              'patient_power_puncher/ppp_td_att.png',
                                                              'patient_power_puncher/ppp_opp_td_rate.png'
                                                             ],
                                         'desc' : ['',
                                                   'The Patient Power Puncher fight syle is portrayed by such ' +
                                                   'fighters as Anthony "Rumble" Johnson, Vitor Belfort, and Francis ' +
                                                   'Ngannou. These fighters bide their time and search for the ' +
                                                   'knockout blow.',
                                                   '',
                                                   'While Patient Power Punchers land strikes at a lower rate, they ' +
                                                   'boast a very high knockdown per significant strike rate and they ' +
                                                   'win by TKO at a higher rate than any other style. The Patient ' +
                                                   'Power Puncher conserves energy and fights primarily from distance, ' +
                                                   'targeting the head. Their takedown attempts are low, as they are ' +
                                                   'focused on one thing only. Their opponents\' takedown rates are ' +
                                                   'also slightly below average, showing just how important it is for ' + 
                                                   'these fighters to keep it standing.',
                                                   '',
                                                   'Patient Power Punchers are moderately successful in general, but ' +
                                                   'fare particularly well against Glass Cannons, High Risk Sub ' +
                                                   'Artists, and Pressure Wrestlers. Glass Cannons possess the same ' +
                                                   'knockout power, but less effective striking defense. ' +
                                                   'High Risk Sub Artists have even worse striking ' +
                                                   'defense. Pressure Wrestlers have predictable takedowns, and may ' +
                                                   'be susceptible to getting caught while shooting for the takedown.'
                                                   '',
                                                   'Patient Power Punchers struggle most against Tacticians and Stand ' +
                                                   'and Bang fighters. The Stand and Bang fighters can take a bunch ' +
                                                   'better than most, while Tacticians are wise to avoid dangerous ' +
                                                   'striking exchanges with the Patient Power Punchers.'
                                                  ]
                                        },
              'Pressure Wrestler' : {'style_rep_name' : 'Michael Chiesa',
                                     'style_rep_img' : 'michael_chiesa.png',
                                     'box_whisker_img' : ['pressure_wrestler/pw_td_att.png',
                                                          'pressure_wrestler/pw_sig_att.png',
                                                          'pressure_wrestler/pw_dist_rate.png',
                                                          'pressure_wrestler/pw_td_abs.png',
                                                          'pressure_wrestler/pw_control.png'
                                                         ],
                                     'desc' : ['',
                                               'The Pressure Wrestler fight syle is portrayed by such ' +
                                               'fighters as Michael Chiesa, Carla Esparza, and Tito Ortiz. ' +
                                               'These fighters focus on wrestling first, smothering their opponents ' +
                                               'with chain wrestling and giving them no opportunity for offense.',
                                               '',
                                               'Pressure Wrestlers have significantly higher than average takedown ' +
                                               'attempts, and they also get taken down at a higher rate as they force ' +
                                               'their opponents to grapple. Even so, they have one of the highest ' +
                                               'control times of all fighting styles. Pressure Wrestlers have low ' +
                                               'strike attempts, as do their opponents, as the focus is on grappling. ' +
                                               'They have more submission attempts and a higher submission finish ' +
                                               'rate than most other fight styles.',
                                               '',
                                               'Historically, the Pressure Wrestler fares best against High Risk ' +
                                               'Sub Artists and Stand and Bang fighters. High Risk Sub ' +
                                               'Artists likely bite off more than they can chew, getting involved in ' +
                                               'grappling exchanges they cannot win. Stand and Bang fighters are ' +
                                               'generally good at keeping a fight standing, but the Pressure Wrestler ' +
                                               'is relentless in their pursuit of the takedown.',
                                               '',
                                               'They struggle most against Glass Cannons, Stick and Move Fighters, and ' +
                                               'Head Hunting Wrestlers. Glass Cannons are likely able to time their ' +
                                               'predictable takedowns, while Head Hunting Wrestlers have enough ' +
                                               'grappling prowess to keep the fight on the feet, where they have the ' +
                                               'advantage. Stick and Move Fighters, while similar to Stand and Bang ' +
                                               'fighters, may have just enough mobility and takedown defense to ' + 
                                               'maintain a slight edge.'
                                              ]
                                    },
              'Stand and Bang' : {'style_rep_name' : 'Max Holloway',
                                  'style_rep_img' : 'max_holloway.png',
                                  'box_whisker_img' : ['stand_and_bang/sab_sig_land.png',
                                                       'stand_and_bang/sab_sig_abs.png',
                                                       'stand_and_bang/sab_opp_kd_per_strike.png',
                                                       'stand_and_bang/sab_td_att.png',
                                                       'stand_and_bang/sab_td_abs.png'
                                                      ],
                                  'desc' : ['',
                                            'The Stand and Bang fight syle is portrayed by such ' +
                                            'fighters as Max Holloway, Angela Hill, and Calvin Kattar. ' +
                                            'These fighters do what they can to keep the fight on the feet, ' +
                                            'and then they scrap. They have solid chins and are not afraid to ' +
                                            'fight in a phone booth.',
                                            '',
                                            'Stand and Bang fighters land and absorb more significant strikes ' +
                                            'than other styles, on average. They attempt very few takedowns and are ' +
                                            'very difficult to take down themselves. Their opponents have a very ' +
                                            'low knockdown per significant strike rate, and Stand and Bang fighters ' +
                                            'have a slightly higher than average TKO win rate. Basically, they are ' +
                                            'willing to bet they can withstand a war better than you can.'
                                            '',
                                            'Historically, Stand and Bang fighters fare best against High Risk Sub ' +
                                            'Artists, Glass Cannons, and Patient Power Punchers. They can keep the ' +
                                            'fight on the feet, out of danger of the submissions of the High Risk Sub ' +
                                            'Artist. They can withstand the power shots of the Glass Cannons and the ' +
                                            'Patient Power Punchers, dishing it back and often winning by decision or ' +
                                            'by a knockout of their own.'
                                            '',
                                            'They struggle most against Chinny Grapplers, Tacticians, and Pressure ' +
                                            'Wrestlers. Chinny Grapplers and Pressure Wrestlers are often too much ' +
                                            'for Stand and Bang fighters in the grappling game, while Tacticians are ' +
                                            'smart and safe, able to beat out Stand and Bang fighters on the ' +
                                            'scorecards.'
                                           ]
                                 },
              'Stick and Move' : {'style_rep_name' : 'Robert Whittaker',
                                  'style_rep_img' : 'robert_whittaker.png',
                                  'box_whisker_img' : ['stick_and_move/sam_sig_att.png',
                                                       'stick_and_move/sam_sig_acc.png',
                                                       'stick_and_move/sam_dist_rate.png',
                                                       'stick_and_move/sam_opp_sig_acc.png',
                                                       'stick_and_move/sam_opp_control.png'
                                                      ],
                                  'desc' : ['',
                                            'The Stick and Move fight syle is portrayed by such ' +
                                            'fighters as Robert Whittaker, Michael Bisping, and Al Iaquinta. ' +
                                            'These fighters overwhelm with volume, and while they aren\'t ' +
                                            'particularly accurate, they frustrate and outpoint opponents with ' +
                                            'consistent pressure and solid takedown defense.',
                                            '',
                                            'Stick and Move fighters have a high significant strike rate, but ' +
                                            'a below average significant strike accuracy. They fight at a higher than ' +
                                            'average rate from distance, and are very difficult to take down. This ' +
                                            'translates to a low opponent striking accuracy and control time. While ' +
                                            'unlikely to win by finish, Stick and Move fighters are successful against ' +
                                            'most other fight styles.',
                                            '',
                                            'Historically, Stick and Move fighters fare best against Pressure ' +
                                            'Wrestlers, Chinny Grapplers, and Head Hunting Wrestlers. This speaks to ' +
                                            'how well Stick and Move fighters can avoid the takedown. Few styles can ' +
                                            'compete with Stick and Move fighters on the feet.',
                                            '',
                                            'They struggle most against Tacticians and Stand and Band fighters. ' +
                                            'Tacticians and Stand and Bang fighters have many of the same striking ' +
                                            'and defensive accolades, but Tacticians do it a little bit better, ' +
                                            'while Stand and Bang fighters are willing to get dirty.'
                                            
                                           ]
                                 },
              'Tactician' : {'style_rep_name' : 'Valentina Shevchenko',
                             'style_rep_img' : 'valentina_shevchenko.png',
                             'box_whisker_img' : ['tactician/tact_dec_win.png',
                                                  'tactician/tact_strike_acc.png',
                                                  'tactician/tact_sig_abs.png',
                                                  'tactician/tact_opp_td_rate.png',
                                                  'tactician/tact_control.png'
                                                 ],
                             'desc' : ['',
                                       'The Tactician fight syle is portrayed by such ' +
                                       'fighters as Valentina Shevchenko, Georges St. Pierre, and Beneil Dariush. ' +
                                       'These fighters make all the right decisions. They are measured in their ' +
                                       'striking and their grappling, being sure not to overextend or put themselves ' +
                                       'in unnecessary danger. They are patient and effective in many areas. This is ' +
                                       'the most effective of all fighter styles.',
                                       '',
                                       'Tacticians absorb less significant strikes than most other fight styles, and ' +
                                       'they also give up less control time to their opponents, as their opponents ' +
                                       'struggle to take them down. Tacticians attempt fewer significant strikes than ' +
                                       'average, but they land at an average rate, as their striking accuracy is ' +
                                       'high. Tacticians win by decision more than any other fight style.',
                                       '',
                                       'Tacticians hold the advantage over all other styles, but they fare best ' +
                                       'against High Risk Sub Artists, Chinny Grapplers, and Head Hunting Wrestlers. ' +
                                       'In all cases, the Tactician is too careful and patient to wind up in an ' +
                                       'unfavorable grappling situation, opting instead to keep the fight in his or ' +
                                       'her control, either on the feet on in controlled grappling exchanges.'
                                       '',
                                       'They struggle most against Stand and Bang fighters and Stick and Move ' +
                                       'fighters, although they still hold the advantage. These styles are also well ' +
                                       'rounded, capable of solid striking, competent defense, and dictating the pace ' +
                                       'and position of the fight.'
                                      ]
                            }
             }
    
    
# ----------------- Streamlit Page Construction ----------------- #

pages = st.sidebar.selectbox('',
                             ('UFC Fighter Comparison',
                              'UFC Fighter Career Profile',
                              'Fighter Style Descriptions',
                              'Fighter Style Comparison',
                              'Scatter Plot Exploration',
                              'Box and Whisker Exploration',
                              'Histogram Exploration'
                             ))

st.sidebar.write('---')
st.sidebar.write("""This project was built by David Wismer. Find me on [LinkedIn](https://www.linkedin.com/in/david-wismer-0a940656/).""")

st.sidebar.write('---')
st.sidebar.write('This app uses data from [UFCStats.com](http://ufcstats.com/statistics/events/completed). The project required web scraping, database ' +
                 'storage and querying, feature engineering, clustering algorithms, data visualizaiton, and the creation of this web ' +
                 'application. For a full project write-up, [read my blog post on Medium](https://medium.com/@davidrwismer/clustering-ufc-fighters-by-fighting-style-1f65102b4821).')

st.sidebar.write('---')
st.sidebar.write("""For faster dashboard performance, download Tableau Public. You can find the entire workbook on my [Tableau profile](https://public.tableau.com/app/profile/david.wismer).""")

st.sidebar.write('---')
st.sidebar.write("""Visit my [Github](https://github.com/drwismer) to see how the app was built.""")

if pages == 'UFC Fighter Comparison':
    
    make_title(pages, 'white')
    
    blurb('This dashboard can be used to compare two fighters, particularly two fighters slated to fight in an upcoming event.', 'white')
    blurb('Refer to the yellow boxes at the top of the dashboard for parameter and filter instructions.', 'white') 
    blurb('Refer to the bottom of the dashboard for descriptions of the metrics shown on the dashboard.', 'white')

    html = """
    <div class='tableauPlaceholder' id='viz1644870386211' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UFCFighterProfilesandMatchups&#47;Matchup' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1644870386211');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='6527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='6527px';} else { vizElement.style.width='100%';vizElement.style.height='10027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    components.html(html, width=1380, height=6500)

elif pages == 'UFC Fighter Career Profile':
    
    make_title(pages, 'white')
    
    blurb('This dashboard shows how a fighter\'s key statistics and fight style have changed across time.', 'white')
    blurb('Refer to the boxes at the top of the dashboard for parameter and filter instructions, as well as ' + 
          'descriptions of the metrics shown on the dashboard.', 'white')

    html = """
    <div class='tableauPlaceholder' id='viz1644871090986' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UFCFighterProfilesandMatchups&#47;FighterProfile' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1644871090986');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='10027px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='10027px';} else { vizElement.style.width='100%';vizElement.style.height='10027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    components.html(html, width=1380, height=10000)
    
elif pages == 'Fighter Style Descriptions':
    
    make_title(pages, 'white')
    
    col1_a, col2_a, col3_a =st.columns([1, 0.1, 1])
    
    with col1_a:
        styles = st.selectbox('',
                              ('Chinny Grappler',
                               'Glass Cannon',
                               'Grind It Out',
                               'Head Hunting Wrestler',
                               'High Risk Sub Artist',
                               'Patient Power Puncher',
                               'Pressure Wrestler',
                               'Stand and Bang',
                               'Stick and Move',
                               'Tactician'
                              ))
    
    col1_b, col2_b, col3_b =st.columns([1, 0.1, 1])
    
    with col1_b:
        make_subtitle('Style Example: ' + style_dict[styles]['style_rep_name'], 'white')
        st.image('style_rep_images/' + style_dict[styles]['style_rep_img'])
        for txt in style_dict[styles]['desc']:
            blurb(txt, 'white')
        
    with col3_b:
        make_subtitle('Defining Characteristics: ' + styles, 'white')
        for img in style_dict[styles]['box_whisker_img']:
            st.image('stat_screenshots/' + img)
        

elif pages == 'Fighter Style Comparison':
    
    make_title(pages, 'white')
    
    blurb('This dashboard allows for comparing the key characteristics of one fighting style to another style or to all other styles combined.', 'white')
    blurb('Refer to the boxes at the top of the dashboard for parameter and filter instructions.', 'white')
    blurb('Refer to the yellow boxes at the bottom of the dashboard for instructions and metric explanations.', 'white')

    html = """
    <div class='tableauPlaceholder' id='viz1645110113075' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UFCFighterProfilesandMatchups&#47;ClusterComparison' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1645110113075');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='7827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='7827px';} else { vizElement.style.width='100%';vizElement.style.height='10027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    components.html(html, width=1380, height=7800)

elif pages == 'Scatter Plot Exploration':
    
    make_title(pages, 'white')
    
    blurb('This dashboard plots fighters in a Scatter Plot based on user defined parameters and filters.', 'white')
    blurb('Refer to the yellow boxes at the bottom of the dashboard for instructions and metric explanations.', 'white')
    
    html = """
     <div class='tableauPlaceholder' id='viz1644871426898' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UFCFighterProfilesandMatchups&#47;ScatterDash' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1644871426898');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='1627px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='1627px';} else { vizElement.style.width='100%';vizElement.style.height='2377px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1380, height=1600)
    
elif pages == 'Box and Whisker Exploration':
    
    make_title(pages, 'white')
    
    blurb('This dashboard plots fighters in a Box and Whisker Plot based on user defined parameters and filters.', 'white')
    blurb('Refer to the yellow boxes at the bottom of the dashboard for instructions and metric explanations.', 'white')
    
    html = """
     <div class='tableauPlaceholder' id='viz1644871497328' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UFCFighterProfilesandMatchups&#47;BoxWhiskerDash' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1644871497328');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='1627px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='1627px';} else { vizElement.style.width='100%';vizElement.style.height='2327px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1380, height=1600)
    
elif pages == 'Histogram Exploration':
    
    make_title(pages, 'white')
    
    blurb('This dashboard plots fighters in a Histogram Plot based on user defined parameters and filters.', 'white')
    blurb('Refer to the yellow boxes at the bottom of the dashboard for instructions and metric explanations.', 'white')
    
    html = """
     <div class='tableauPlaceholder' id='viz1644871551719' style='position: relative'><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='UFCFighterProfilesandMatchups&#47;HistogramDash' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1644871551719');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='1627px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='1627px';} else { vizElement.style.width='100%';vizElement.style.height='2327px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1380, height=1600)
