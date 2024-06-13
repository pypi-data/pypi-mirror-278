import logging
import os
import pandas as pd
import numpy as np
from io import StringIO
from nwae.math.datasource.Csv import Csv
from nwae.math.lang.LangChar import LangChar
from nwae.math.lang.translate.TranslateMain import Translate
from nwae.utils.Environ import Env
from nwae.math.utils.EnvironRepo import EnvRepo


class LmAnalyzeData:

    SAMPLE_SIMPLE = """
class,label,type,text
0,food,trn,"bread and butter"
0,food,trn,"fish and chips"
0,food,trn,"chicken rice with soup"
0,food,trn,"street lamb kebab"
0,food,trn,"tasty Kyiv chicken dish"
0,food,trn,"seafood spicy hotpot"
0,food,trn,"sushi, sashimi, wasabi"
0,food,trn,"shrimp burger from Wendy's"
0,food,trn,"fried potato leaves"
0,food,trn,"Cheese bread pizza & kachapuri"
0,food,val,"bread and butter"
0,food,val,"English fish & chips"
0,food,val,"hangover soup with Chinese noodles"
0,food,val,"sausages, scrambled eggs or hash browns"
,,,
1,tech,trn,"computers and laptops"
1,tech,trn,"code programming"
1,tech,trn,"8 bits one byte"
1,tech,trn,"operating systems"
1,tech,trn,"application servers on cloud"
1,tech,trn,"interpreted byte code"
1,tech,trn,"object-oriented design"
1,tech,trn,"automated unit tests"
1,tech,trn,"virtual machines"
1,tech,trn,"modular & robust systems"
1,tech,val,"operating systems"
1,tech,val,"a semi-virtual layer above the OS"
1,tech,val,"customized processor units GPU & TPU"
1,tech,val,"compile to specific platform"
,,,
2,sports,trn,"Tennis grass court"
2,sports,trn,"Soccer world cup"
2,sports,trn,"50m freestyle record under 21s"
2,sports,trn,"Liverpool beat AC Milan in the Champions League 2005"
2,sports,trn,"E-sports rising in popularity"
2,sports,trn,"Sports gambling operators"
2,sports,trn,"Horce racing and lottery"
2,sports,trn,"Outdoor exercise and gym training"
2,sports,trn,"Chess and Go board game tournaments"
2,sports,trn,"China dominates the table tennis rankings"
2,sports,val,"50m freestyle record under 21s"
2,sports,val,"Gym training with weights"
2,sports,val,"The soccer finals will be hosted on a neutral ground"
2,sports,val,"Ivan Lendl dominated the men's singles in the 1990's"
,,,
3,medicine,trn,"Diagnosis and treatment options"
3,medicine,trn,"Changing lifestyle habits over surgery & prescriptions"
3,medicine,trn,"Genomic basis for RNA alterations in cancer"
3,medicine,trn,"Cryotherapy versus laser destruction"
3,medicine,trn,"Chronic Hives can occur without reason or cause"
3,medicine,trn,"86% of drug candidates developed were not approved"
3,medicine,trn,"AI-focused drug molecule design"
3,medicine,trn,"Most Asian & African countries still use traditional medicine for primary healthcare"
3,medicine,trn,"40% of pharmaceutical products are from nature and traditional knowledge, such as aspirin"
3,medicine,trn,"isoniazid and rifampicin are 2 most effective first-line TB drugs"
3,medicine,val,"Drug development process can be aided by AI"
3,medicine,val,"MDR-TB remains a public health crisis and a health security threat"
3,medicine,val,"Blood pressure tends to increase during the cold weather months"
,,,
4,genetics,trn,"Only 20 amino acids form all life proteins, like 26 alphabets forming all words"
4,genetics,trn,"Genetic 'bit' is made of only 4 amino acids, forming a 3-bit codon 'byte'"
4,genetics,trn,"Phenylalanine was the first decoded genetic code as UUU in 1961"
4,genetics,trn,"Start codons are not general to all sequences, as they may be interpreted differently in other cells"
4,genetics,trn,"By programming cells to switch between two aging pathways, it doubled the lifespan of the cells"
4,genetics,trn,"Making copying or replication mistakes is the basis of mutation and variations in all life"
4,genetics,trn,"Most environmentally induced DNA damage is repaired, only 0.1% actually becoming permanent mutations"
4,genetics,trn,"Mutation rates 1 in 10 billion can accumulate quickly in rapidly reproducing organisms like bacteria"
4,genetics,trn,"Mutations accumulate in bacteria population to provide ample genetic variation to become drug resistant"
4,genetics,trn,"Not all mutations are bad, but most mutations cause cancer"
4,genetics,val,"Mutations accumulate in bacteria population to provide ample genetic variation to become drug resistant"
4,genetics,val,"Mutation accumulates quickly in bacteria making them resistant to drugs"
4,genetics,val,"Stop codons can sometimes be coded using a non-standard amino acid"
4,genetics,val,"As the number of bacteria mutations increases, so too does the likelihood that one of them will develop a drug-resistant phenotype"
,,,
"""

    # For data file
    COL_CLASS = 'class'     # Standardized 0, 1, 2, ...
    COL_LABEL = 'label'     # Arbitrary human label text
    COL_TYPE = 'type'       # train ("trn") or validate ("val")
    COL_TEXT = 'text'

    # For csv cache file
    COL_LANG_SRC = 'lang_src'
    COL_LANG_TGT = 'lang_tgt'
    COL_TEXT_ORIGINAL = 'text_original'
    COL_TEXT_TRANSLATED = 'text_translated'
    CSV_CACHE_COLUMNS = (COL_LANG_SRC, COL_LANG_TGT, COL_TEXT_ORIGINAL, COL_TEXT_TRANSLATED,)

    LANG_RANDOM = '--'

    def __init__(
            self,
            lang_data,
            lang_tgt,
            label_text_csvpath = None,
            csv_colmap = None,
            cache_dir = None,
            tl_engines = (Translate.TRANS_GOOGLE,),
            match_phrase = None,
            logger = None,
    ):
        self.lang_data = lang_data
        self.lang_tgt = lang_tgt
        self.label_text_csvpath = label_text_csvpath
        self.csv_colmap = csv_colmap if csv_colmap is not None else {}
        self.cache_dir = cache_dir if cache_dir is not None else Env.get_home_download_dir()
        self.tl_engines = tl_engines
        self.match_phrase = {} if match_phrase is None else match_phrase
        self.logger = logger if logger is not None else logging.getLogger()

        self.csvcol_text = self.csv_colmap.get(self.COL_TEXT, self.COL_TEXT)
        self.csvcol_label = self.csv_colmap.get(self.COL_LABEL, self.COL_LABEL)

        self.cache_csvpath = self.cache_dir + '/.cache.lm_analyze_data.csv'
        if not os.path.exists(self.cache_csvpath):
            pd.DataFrame(columns=list(self.CSV_CACHE_COLUMNS)).to_csv(
                path_or_buf = self.cache_csvpath,
                index = False,
            )
            self.logger.info('Created new csv cache file "' + str(self.cache_csvpath) + '"')

        self.cache_csv = Csv(
            filepath = self.cache_csvpath,
            logger = self.logger,
        )

        self.df_label_text = None
        if self.label_text_csvpath is not None:
            self.df_label_text = pd.read_csv(filepath_or_buffer=self.label_text_csvpath)
            self.logger.info(
                'Read from file "' + str(self.label_text_csvpath)
                + '" of total lines ' + str(len(self.df_label_text))
            )
        else:
            self.df_label_text = pd.read_csv(filepath_or_buffer=StringIO(self.SAMPLE_SIMPLE))
            self.logger.info('Using default simple data of total lines ' + str(len(self.df_label_text)))

        self.df_label_text.dropna(inplace=True)
        for k, v in self.match_phrase.items():
            if k in self.df_label_text.columns:
                condition = self.df_label_text[k] == v
                self.df_label_text = self.df_label_text[condition].reset_index(drop=True)
        self.logger.info(
            'Filtered NAs and match phrase ' + str(self.match_phrase)
            + ' to new data shape ' + str(self.df_label_text.shape)
        )

        self.tl = Translate.get_singleton(
            ClassType = Translate,
            lang_tgt  = self.lang_tgt,
            lang_src  = (self.lang_data, ),
            cache_dir = self.cache_dir,
            logger    = self.logger,
            params_other = {
                Translate.KEY_PARAMS_PREFERRED_TL: self.tl_engines,
            },
        )
        self.__prepare_data()
        return

    def __prepare_data(
            self,
    ):
        translated_list = []
        text_list = self.df_label_text[self.csvcol_text].tolist()

        if self.lang_tgt != self.lang_data:
            self.logger.info(
                'Translating total lines ' + str(len(self.df_label_text))
                + ' from "' + str(self.lang_data) + '" to "' + str(self.lang_tgt) + '"'
            )

            for i, txt in enumerate(text_list):
                record_cache = self.cache_csv.get(
                    match_phrase = {
                        self.COL_LANG_SRC: self.lang_data,
                        self.COL_LANG_TGT: self.lang_tgt,
                        self.COL_TEXT_ORIGINAL: txt,
                    },
                    tablename_or_index = self.cache_csvpath,
                    params_other = None,
                )
                self.logger.debug(
                    '#' + str(i) + '. Cache result for lang src "' + str(self.lang_data)
                    + '", lang target "' + str(self.lang_tgt) + '", text "' + str(txt) + '": ' + str(record_cache)
                )
                if len(record_cache) >= 1:
                    txt_translated = record_cache[0][self.COL_TEXT_TRANSLATED]
                else:
                    tr_result_list = self.translate_training_data(
                        lang_tgt = self.lang_tgt,
                        txt_list = [txt],
                        random_translate = self.lang_tgt == self.LANG_RANDOM,
                    )
                    txt_translated = tr_result_list[0]
                    self.cache_csv.add(
                        records = [{
                            self.COL_LANG_SRC: self.lang_data,
                            self.COL_LANG_TGT: self.lang_tgt,
                            self.COL_TEXT_ORIGINAL: txt,
                            self.COL_TEXT_TRANSLATED: txt_translated,
                        }]
                    )
                    self.logger.info(
                        '#' + str(i) + '. Translated from lang src "' + str(self.lang_data)
                        + '" to lang target "' + str(self.lang_tgt)
                        + '" as "' + str(txt_translated) + '", from source text "' + str(txt) + '"'
                    )
                translated_list.append(txt_translated)
        else:
            translated_list = self.df_label_text[self.csvcol_text]

        self.df_label_text[self.COL_TEXT_TRANSLATED] = translated_list
        self.df_label_text[self.COL_TEXT_ORIGINAL] = text_list
        return

    def translate_training_data(
            self,
            lang_tgt,
            txt_list,
            random_translate = False,
    ):
        if random_translate:
            lc = LangChar()
            return [lc.random_sent(n_words=np.random.randint(low=5, high=10, size=1)[0]) for _ in txt_list]
        else:
            return [t['translation'] for t in self.tl.translate(lang_tgt=lang_tgt, text_list=txt_list)]

    def get_data(
            self,
    ):
        columns_keep = [self.csvcol_label, self.COL_TEXT_TRANSLATED, self.COL_TEXT_ORIGINAL]
        df_ret = self.df_label_text[columns_keep]
        return df_ret

    SAMPLE_BBC = """
no,class,label,text
0,0,business,disney settles disclosure charges walt disney has settled charges from us federal regulators that it failed to disclose how family members of directors were employed by the company
1,0,business,five million germans out of work germany s unemployment figure rose above the psychologically important level of five million last month.
2,0,business,japanese banking battle at an end japan s sumitomo mitsui financial has withdrawn its takeover offer for rival bank ufj holdings  enabling the latter to merge with mitsubishi tokyo
3,0,business,uk economy facing  major risks  the uk manufacturing sector will continue to face  serious challenges  over the next two years  the british chamber of commerce (bcc) has said.
4,0,business,uk interest rates held at 4.75% the bank of england has left interest rates on hold again at 4.75%  in a widely-predicted move.  rates went up five times from november 2003
5,0,business,venezuela and china sign oil deal venezuelan president hugo chavez has offered china wide-ranging access to the country s oil reserves.  the offer  made as part of a trade deal bet
6,0,business,air passengers win new eu rights air passengers who are unable to board their flights because of overbooking  cancellations or flight delays can now demand greater compensation.
7,0,business,budget aston takes on porsche british car maker aston martin has gone head-to-head with porsche s 911 sports cars with the launch of its cheapest model yet.
8,0,business,india opens skies to competition india will allow domestic commercial airlines to fly long haul international routes  a move it hopes will stoke competition and drive down prices.
9,0,business,ad sales boost time warner profit quarterly profits at us media giant timewarner jumped 76% to $1.13bn (£600m) for the three months to december  from $639m year-earlier.
10,0,business,parmalat sues 45 banks over crash parmalat has sued 45 banks as it tries to reclaim money paid to banks before the scandal-hit italian dairy company went bust last year.
11,0,business,monsanto fined $1.5m for bribery the us agrochemical giant monsanto has agreed to pay a $1.5m (£799 000) fine for bribing an indonesian official.
12,0,business,buyers snap up jet airways  shares investors have snapped up shares in jet airways  india s biggest airline  following the launch of its much anticipated initial public offer (ipo)
13,0,business,circuit city gets takeover offer circuit city stores  the second-largest electronics retailer in the us  has received a $3.25bn (£1.7bn) takeover offer.
14,0,business,us manufacturing expands us industrial production increased in december  according to the latest survey from the institute for supply management (ism).
15,0,business,making your office work for you our mission to brighten up your working lives continues - and this time  we re taking a long hard look at your offices.
16,0,business,quiksilver moves for rossignol shares of skis rossignol  the world s largest ski-maker  have jumped as much as 15% on speculation that it will be bought by us surfwear firm
17,0,business,trade gap narrows as exports rise the uk s trade gap narrowed in november  helped by a 7.5% rise in exports outside the european union.
18,0,business,card fraudsters  targeting web  new safeguards on credit and debit card payments in shops has led fraudsters to focus on internet and phone payments  an anti-fraud agency has said.
19,0,business,palestinian economy in decline despite a short-lived increase in palestinian jobs in 2003  the economy is performing well below its potential  said a world bank report.
20,0,business,bush to outline  toughest  budget president bush is to send his toughest budget proposals to date to the us congress  seeking large cuts in domestic spending to lower the deficit.
21,1,entertainment,indie film nominations announced mike leigh s award-winning abortion drama vera drake has scooped seven nominations at this year s british independent film awards.
22,1,entertainment,totp turns to elvis impersonator top of the pops has turned to the star of elvis presley musical jailhouse rock after the late rock legend scooped the uk s 1 000th number one single
23,1,entertainment,films on war triumph at sundance a study of the united states at war in the past 50 years has picked up one of the main awards at the 2005 sundance film festival in utah
24,1,entertainment,spector facing more legal action music producer phil spector is facing legal action from the mother of the actress he has been accused of killing.
25,1,entertainment,celebrities get to stay in jungle all four contestants still remain in i m a celebrity ... get me out of here as no evictions were made on the television show on saturday.
26,1,entertainment,spark heads world booker list dame muriel spark is among three british authors who have made the shortlist for the inaugural international booker prize.
27,1,entertainment,dvd review: spider-man 2 it s a universal rule that a film can either be a superhero special effects extravaganza or it can be good. but spider-man 2 breaks that rule in two.
28,1,entertainment,no uk premiere for rings musical the producers behind the lord of the rings musical have abandoned plans to premiere the show in london because no suitable theatre was available.
29,1,entertainment,hillbillies singer scoggins dies country and western musician jerry scoggins has died in los angeles at the age of 93  his family has said.
30,1,entertainment,prodigy join v festival line-up essex act prodigy are to headline the second stage at this year s v festival  joining main stage headliners scissor sisters and franz ferdinand.
31,1,entertainment,actor foxx sees globe nominations us actor jamie foxx has been given two nominations for golden globe awards  with meryl streep  morgan freeman and cate blanchett also up for prize
32,1,entertainment,mumbai bombs movie postponed the release of a film about the mumbai (bombay) blasts in 1993 has been postponed following protests by those on trial for the bombings.
33,1,entertainment,hard act to follow for outkast us rap duo outkast s trio of trophies at the mtv europe awards crowns a year of huge success for the band.
34,1,entertainment,aaliyah claim dismissed by court late r&b star aaliyah s record company has failed in an attempt to sue the video producer who booked the ill-fated flight on which she died in 2001
35,1,entertainment,da vinci film to star tom hanks actor tom hanks and director ron howard are reuniting for the da vinci code  an adaptation of the international best-selling novel by dan brown.
36,1,entertainment,little britain vies for tv trophy bbc hits little britain and strictly come dancing are among numerous british shows nominated for the prestigious golden rose television awards
37,2,politics,tories unveil quango blitz plans plans to abolish 162 quangos have been unveiled by the conservatives as part of their effort to show how government red tape can be cut.
38,2,politics,schools to take part in mock poll record numbers of schools across the uk are to take part in a mock general election backed by the government.
39,2,politics,lib dems unveil women s manifesto the liberal democrats are attempting to woo female voters with the launch of their manifesto for women.
40,2,politics,blair labour s longest-serving pm tony blair has become the labour party s longest-serving prime minister.  the 51-year-old premier has marked his 2 838th day in the post
41,2,politics,conservative mp defects to labour a conservative mp and former minister has defected to labour.  robert jackson  58  mp for wantage in oxfordshire  said he was disillusioned
42,2,politics,row over  police  power for csos the police federation has said it strongly opposes giving community support officers (csos) the power to detain suspects for up to 30 minutes.
43,2,politics,kennedy criticises  unfair  taxes gordon brown has failed to tackle the  fundamental unfairness  in the tax system in his ninth budget  charles kennedy has said.
44,2,politics,kilroy-silk quits  shameful  ukip ex-chat show host robert kilroy-silk has quit the uk independence party and accused it of betraying its supporters.
45,2,politics,borders rail link campaign rally campaigners are to stage a rally calling for a borders rail link which was closed in 1969 to be reopened.
46,2,politics,labour seeks to quell feud talk labour s leadership put on a show of unity at a campaign poster launch after mps criticised tony blair and gordon brown over reports of their rift.
47,2,politics,blair congratulates bush on win tony blair has said he looks forward to continuing his strong relationship with george bush and working with him during his second term as president
48,2,politics,citizenship event for 18s touted citizenship ceremonies could be introduced for people celebrating their 18th birthday  charles clarke has said.
49,2,politics,blair  pressing us on climate  tony blair is pressing the us to cut greenhouse gases despite its unwillingness to sign the kyoto protocol  downing street has indicated.
50,2,politics,could rivalry overshadow election  tony blair and gordon brown are desperately trying to stuff the genie of their rivalry back into the bottle.
51,2,politics,lords wrong on detainees - straw jack straw has attacked the decision by britain s highest court that detaining foreign terrorist suspects without trial breaks human rights laws.
52,2,politics,howard rebuts asylum criticisms tory leader michael howard has gone on the offensive in response to people questioning how a son of immigrants can propose asylum quotas.
53,2,politics,guantanamo four questioned the four britons freed from us custody in guantanamo bay are expected to be allowed a visit by one relative.
54,2,politics,job cuts  false economy   - tuc plans to shed 71 000 civil service jobs will prove to be a  false economy  that could hamper public sector reforms  according to a tuc report.
55,2,politics,game warnings  must be clearer  violent video games should carry larger warnings so parents can understand what their children are playing
56,2,politics,uk  needs true immigration data  a former home office minister has called for an independent body to be set up to monitor uk immigration.
57,2,politics,blair told to double overseas aid tony blair is being urged to use all his negotiating powers to end poor countries  debt and double aid.
58,3,sport,hingis hints at playing comeback martina hingis has admitted that she might consider a competitive return to tennis if an appearance in thailand later this month goes well.
59,3,sport,dogged federer claims dubai crown world number one roger federer added the dubai championship trophy to his long list of successes - but not before he was given a test
60,3,sport,holmes back on form in birmingham double olympic champion kelly holmes was back to her best as she comfortably won the 1 000m at the norwich union birmingham indoor grand prix.
61,3,sport,federer claims dubai crown world number one roger federer added the dubai championship trophy to his long list of successes - but not before he was given a test by ivan ljubicic.
62,3,sport,palace threat over cantona masks manchester united fans wearing eric cantona masks will not be allowed in selhurst park on saturday.
63,3,sport,hamm bows out for us women s football legend mia hamm has played her final game.  hamm  32  who officially retired after this year s athens olympics
64,3,sport,pavey focuses on indoor success jo pavey will miss january s view from great edinburgh international cross country to focus on preparing for the european indoor championships
65,3,sport,lewis-francis eyeing world gold mark lewis-francis says his olympic success has made him determined to bag world championship 100m gold in 2005.
66,3,sport,campbell lifts lid on united feud arsenal s sol campbell has called the rivalry between manchester united and the gunners  bitter and personal
67,3,sport,roddick into san jose final andy roddick will play cyril saulnier in the final of the sap open in san jose on sunday.
68,3,sport,rusedski forced out in marseille greg rusedski was forced to withdraw from the open 13 in marseille on thursday with a rib injury
69,3,sport,african double in edinburgh world 5000m champion eliud kipchoge won the 9.2km race at the view from great edinburgh cross country
70,3,sport,koubek suspended after drugs test stefan koubek says he has been banned for three months by the international tennis federation (itf) after testing positive for a banned substance.
71,3,sport,henman overcomes rival rusedski tim henman saved a match point before fighting back to defeat british rival greg rusedski 4-6 7-6 (8-6) 6-4 at the dubai tennis championships
72,3,sport,aragones angered by racism fine spain coach luis aragones is furious after being fined by the spanish football federation for his comments about thierry henry
73,3,sport,souness backs smith for scotland graeme souness believes walter smith would be the perfect choice to succeed berti vogts as scotland manager.
74,3,sport,dent continues adelaide progress american taylor dent reached the final of the australian hardcourt event in adelaide with a crushing 6-1 6-1 win over argentine juan ignacio chela.
75,3,sport,sa return to mauritius top seeds south africa return to the scene of one of their most embarrassing failures when they face the seychelles in the cosafa cup next month.
76,3,sport,hingis to make unexpected return martina hingis makes her return to competitve tennis after two years out of the game at the volvo women s open in pattaya  thailand  on tuesday.
77,3,sport,britain boosted by holmes double athletics fans endured a year of mixed emotions in 2004 as stunning victories went hand-in-hand with disappointing defeats and more drugs scandals.
78,3,sport,holmes starts 2005 with gb events kelly holmes will start 2005 with a series of races in britain.  holmes will make her first track appearance on home soil
79,3,sport,kirwan demands italy consistency italy coach john kirwan has challenged his side to match the performance they produced in pushing ireland close when they meet wales on saturday.
80,3,sport,wenger dejected as arsenal slump arsenal manager arsene wenger claimed their display in the 3-1 defeat against bayern munich was  our worst peformance in the champions league
81,3,sport,henman decides to quit davis cup tim henman has retired from great britain s davis cup team.  the 30-year-old  who made his davis cup debut in 1994  is now set to fully focus
82,3,sport,solskjaer raises hopes of return manchester united striker ole gunnar solskjaer said he hoped to return next season following a career-threatening injury to his right knee
83,3,sport,mourinho plots impressive course chelsea s win at fulham - confirming their position at the premiership summit - proves that they now have everything in place
84,4,tech,bush website blocked outside us surfers outside the us have been unable to visit the official re-election site of president george w bush.
85,4,tech,china net cafe culture crackdown chinese authorities closed 12 575 net cafes in the closing months of 2004  the country s government said.
86,4,tech,pc ownership to  double by 2010  the number of personal computers worldwide is expected to double by 2010 to 1.3 billion machines  according to a report by analysts
87,4,tech,creator of first apple mac dies jef raskin  head of the team behind the first macintosh computer  has died.  mr raskin was one of the first employees at apple
88,4,tech,court mulls file-sharing future judges at the us supreme court have been hearing evidence for and against file-sharing networks
89,4,tech,ultra fast wi-fi nears completion ultra high speed wi-fi connections moved closer to reality on thursday when intel said it would list standards for the technology later this year
90,4,tech,global digital divide  narrowing  the  digital divide  between rich and poor nations is narrowing fast  according to a world bank report
91,4,tech,2d metal slug offers retro fun like some drill sergeant from the past  metal slug 3 is a wake-up call to today s gamers molly-coddled with slick visuals and fancy trimmings
92,4,tech,more movies head to sony s psp movies open water and saw are among those to be made available for sony s psp games console.  film studio lions gate entertainment has announced
93,4,tech,us duo in first spam conviction a brother and sister in the us have been convicted of sending hundreds of thousands of unsolicited e-mail messages to aol subscribers
94,4,tech,progress on new internet domains by early 2005 the net could have two new domain names.  the .post and .travel net domains have been given preliminary approval
95,4,tech,xbox power cable  fire fear  microsoft has said it will replace more than 14 million power cables for its xbox consoles due to safety concerns
96,4,tech,broadband challenges tv viewing the number of europeans with broadband has exploded over the past 12 months  with the web eating into tv viewing habits  research suggests.
97,4,tech,mobile networks seek turbo boost third-generation mobile (3g) networks need to get faster if they are to deliver fast internet surfing on the move and exciting new services.
98,4,tech,brainwave  cap controls computer a team of us researchers has shown that controlling devices with the brain is a step closer.
99,4,tech,sony psp console hits us in march us gamers will be able to buy sony s playstation portable from 24 march  but there is no news of a europe debut.
"""


if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    logging.basicConfig(level=logging.INFO)
    er = EnvRepo()

    ana = LmAnalyzeData(
        lang_data = 'en',
        lang_tgt = 'ru',
        label_text_csvpath = er.NLP_DATASET_DIR + '/lang-model-test/data.csv',
        cache_dir = er.NLP_DATASET_DIR,
        match_phrase = {LmAnalyzeData.COL_TYPE: 'trn'}
    )
    print(ana.get_data())
    exit(0)
