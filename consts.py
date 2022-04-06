LOG_LEVEL = 'INFO'
BASE_STRAVA_URL = 'https://www.strava.com/'
LOGGED_OUT_SLEEP = 15 * 60  # 15 minutes
LOGIN_URL = f'{BASE_STRAVA_URL}login'
ONBOARD_URL = f'{BASE_STRAVA_URL}onboarding'
DASHBOARD_URL = f'{BASE_STRAVA_URL}dashboard'
# ===== new user links =====
WELCOME_URL = f'{BASE_STRAVA_URL}athlete/consents/welcome'
TERMS_OF_SERVICE_URL = f'{BASE_STRAVA_URL}athlete/consents/terms_of_service'
PRIVACY_POLICY_URL = f'{BASE_STRAVA_URL}athlete/consents/privacy_policy'
HEALTH_URL = f'{BASE_STRAVA_URL}athlete/consents/health'
ALL_SET_URL = f'{BASE_STRAVA_URL}athlete/consents/all_set'
# ==========================
FILE_HANDLER_PATH = 'link/file_handler.txt'
MAIN_PAGE_HANDLER_PATH = 'link/processed_rider_main_page_files.txt'
YEAR_TIME_INTERVAL_HANDLER_PATH = 'link/processed_year_intervals_files.txt'
WEEK_TIME_INTERVAL_HANDLER_PATH = 'link/processed_week_intervals_files.txt'
ACTIVITY_HANDLER_PATH = 'link/processed_activity_files.txt'

TIME_INTERVAL_DIR_PATH = 'link/riders_time_interval_pages'
TIME_INTERVAL_HANDLERS_PATHS = [MAIN_PAGE_HANDLER_PATH,YEAR_TIME_INTERVAL_HANDLER_PATH,WEEK_TIME_INTERVAL_HANDLER_PATH]
ERROR_DEFAULT_MSG = 'Failed while trying to login to STRAVA.'
DEBUG = True
LOG_LEVEL_DICT = {'ERROR': 0, 'WARNING': 1, 'INFO': 2}
TIMEOUT = 3
PASSWORD = '12345678'

DOWNLOAD_AGAIN_FILE_PATH = 'link/links_to_download_again.csv'

OPTIONS_TO_IGNORE = ["/route", "/export_gpx", "/flags/new", "/overview", "/laps"]

UNDESIRED_UNITS = ["feet", "miles", "Degrees Fahrenheit", "miles per hour"]
ACTIVITY_POST_TYPES = ["Activity", "GroupActivity", "ChallengeJoin", "ClubJoin"]

ACTIVITY_ANALYSIS_FILES = {'/overview': ['overview'],
                           '/analysis': ['analysis_distance', 'analysis_time'],
                           '/power-curve': ['power-curve_watts', 'power-curve_watts-kg'],
                           '/zone-distribution': ['zone-distribution'],
                           '/power-distribution': ['power-distribution'],
                           '/est-power-curve': ['est-power-curve_watts', 'est-power-curve_watts-kg'],
                           '/est-power-distribution': ['est-power-distribution'],
                           '/heartrate': ['heartrate']
                           }

ANALYSIS_PAGE_TYPES = list(ACTIVITY_ANALYSIS_FILES.keys())

ACTIVITY_TYPES = ['Ride', 'Indoor Cycling', 'Virtual Ride', 'Ride–Commute', 'Race']
ACTIVITY_TYPES_TO_IGNORE = ['Nordic Ski', 'Run', 'Workout', 'Roller Ski', 'Weight Training', 'Yoga', 'Swim',
                            'Alpine Ski', 'Ice Skate', 'Long Run', 'Virtual Run', 'Run – Commute',
                            'Winter Sport', 'Backcountry Ski', 'Crossfit', 'Walk', 'E-Bike Ride', 'Stand Up Paddling',
                            'Rowing', 'Treadmill workout', 'Hike']

WORKOUTS_STRAVA_COLS = ['rider_id','activity_id','activity_type','Date','Duration','Location', 'Moving Time','MaxSpeed',
                        'Relative Effort', 'Distance', 'Elevation', 'AvgCadence', 'Temperature', 'AvgHeart Rate', 'Intensity',
                        'Historic Relative Effort', 'Elapsed Time', 'Calories', 'AvgSpeed', 'MaxCadence', 'AvgPower', 'Massive Relative Effort',
                        'MaxPower', 'Tough Relative Effort', 'Energy Output', 'Weighted Avg Power', 'Total Work', 'Device',
                        'Training Load', 'MaxHeart Rate', 'Estimated Avg Power', 'Speed','Perceived Exertion','Feels like',
                        'Humidity', 'Weather', 'Wind Direction', 'Wind Speed']
# TODO: ask robert -   'E-Bike Ride'

# 876 users, 42 computers, 20.857 users/comp
USERS = [r'cyc161@proton.com',
        r'cyc162@proton.com',
        r'cyc163@proton.com',
        r'cyc164@proton.com',
        r'cyc165@proton.com',
        r'cyc166@proton.com',
        r'cyc167@proton.com',
        r'cyc168@proton.com',
        r'cyc169@proton.com',
        r'cyc170@proton.com',
        r'cyc171@proton.com',
        r'cyc172@proton.com',
        r'cyc173@proton.com',
        r'cyc174@proton.com',
        r'cyc175@proton.com',
        r'cyc176@proton.com',
        r'cyc177@proton.com',
        r'cyc178@proton.com',
        r'cyc179@proton.com',
        r'cyc180@proton.com',
        r'cyc181@proton.com',
        r'cyc182@proton.com',
        r'cyc183@proton.com',
        r'cyc184@proton.com',
        r'cyc185@proton.com',
        r'cyc186@proton.com',
        r'cyc187@proton.com',
        r'cyc188@proton.com',
        r'cyc189@proton.com',
        r'cyc190@proton.com',
        r'cyc191@proton.com',
        r'cyc192@proton.com',
        r'cyc193@proton.com',
        r'cyc194@proton.com',
        r'cyc195@proton.com',
        r'cyc196@proton.com',
        r'cyc197@proton.com',
        r'cyc198@proton.com',
        r'cyc199@proton.com',
        r'cyc200@proton.com',
        r'cyc201@proton.com',
        r'cyc202@proton.com',
        r'cyc203@proton.com',
        r'cyc204@proton.com',
        r'cyc205@proton.com',
        r'cyc206@proton.com',
        r'cyc207@proton.com',
        r'cyc208@proton.com',
        r'cyc209@proton.com',
        r'cyc210@proton.com',
        r'cyc211@proton.com',
        r'cyc212@proton.com',
        r'cyc213@proton.com',
        r'cyc214@proton.com',
        r'cyc215@proton.com',
        r'cyc216@proton.com',
        r'cyc217@proton.com',
        r'cyc218@proton.com',
        r'cyc219@proton.com',
        r'cyc220@proton.com',
        r'cyc221@proton.com',
        r'cyc222@proton.com',
        r'cyc223@proton.com',
        r'cyc224@proton.com',
        r'cyc225@proton.com',
        r'cyc226@proton.com',
        r'cyc227@proton.com',
        r'cyc228@proton.com',
        r'cyc229@proton.com',
        r'cyc230@proton.com',
        r'cyc231@proton.com',
        r'cyc232@proton.com',
        r'cyc233@proton.com',
        r'cyc234@proton.com',
        r'cyc235@proton.com',
        r'cyc237@proton.com',
        r'cyc238@proton.com',
        r'cyc239@proton.com',
        r'cyc240@proton.com',
        r'cyc241@proton.com',
        r'cyc242@proton.com',
        r'cyc243@proton.com',
        r'cyc244@proton.com',
        r'cyc245@proton.com',
        r'cyc246@proton.com',
        r'cyc247@proton.com',
        r'cyc248@proton.com',
        r'cyc249@proton.com',
        r'cyc250@proton.com',
        r'cyc251@proton.com',
        r'cyc252@proton.com',
        r'cyc253@proton.com',
        r'cyc254@proton.com',
        r'cyc255@proton.com',
        r'cyc256@proton.com',
        r'cyc257@proton.com',
        r'cyc259@proton.com',
        r'cyc260@proton.com',
        r'cyc261@proton.com',
        r'cyc262@proton.com',
        r'cyc263@proton.com',
        r'cyc264@proton.com',
        r'cyc265@proton.com',
        r'cyc266@proton.com',
        r'cyc267@proton.com',
        r'cyc268@proton.com',
        r'cyc269@proton.com',
        r'cyc270@proton.com',
        r'cyc271@proton.com',
        r'cyc272@proton.com',
        r'cyc273@proton.com',
        r'cyc274@proton.com',
        r'cyc275@proton.com',
        r'cyc276@proton.com',
        r'cyc277@proton.com',
        r'cyc278@proton.com',
        r'cyc279@proton.com',
        r'cyc280@proton.com',
        r'cyc281@proton.com',
        r'cyc283@proton.com',
        r'cyc284@proton.com',
        r'cyc285@proton.com',
        r'cyc286@proton.com',
        r'cyc287@proton.com',
        r'cyc288@proton.com',
        r'cyc289@proton.com',
        r'cyc290@proton.com',
        r'cyc291@proton.com',
        r'cyc292@proton.com',
        r'cyc293@proton.com',
        r'cyc294@proton.com',
        r'cyc295@proton.com',
        r'cyc296@proton.com',
        r'cyc297@proton.com',
        r'cyc298@proton.com',
        r'cyc299@proton.com',
        r'cyc300@proton.com',
        r'cyc301@proton.com',
        r'cyc302@proton.com',
        r'cyc303@proton.com',
        r'cyc304@proton.com',
        r'cyc305@proton.com',
        r'cyc306@proton.com',
        r'cyc307@proton.com',
        r'cyc308@proton.com',
        r'cyc309@proton.com',
        r'cyc310@proton.com',
        r'cyc311@proton.com',
        r'cyc312@proton.com',
        r'cyc313@proton.com',
        r'cyc314@proton.com',
        r'cyc315@proton.com',
        r'cyc316@proton.com',
        r'cyc317@proton.com',
        r'cyc318@proton.com',
        r'cyc319@proton.com',
        r'cyc320@proton.com',
        r'cyc321@proton.com',
        r'cyc322@proton.com',
        r'cyc323@proton.com',
        r'cyc324@proton.com',
        r'cyc325@proton.com',
        r'cyc326@proton.com',
        r'cyc327@proton.com',
        r'cyc328@proton.com',
        r'cyc329@proton.com',
        r'cyc330@proton.com',
        r'cyc331@proton.com',
        r'cyc332@proton.com',
        r'cyc333@proton.com',
        r'cyc334@proton.com',
        r'cyc335@proton.com',
        r'cyc336@proton.com',
        r'cyc337@proton.com',
        r'cyc338@proton.com',
        r'cyc339@proton.com',
        r'cyc340@proton.com',
        r'cyc341@proton.com',
        r'cyc342@proton.com',
        r'cyc343@proton.com',
        r'cyc344@proton.com',
        r'cyc345@proton.com',
        r'cyc346@proton.com',
        r'cyc347@proton.com',
        r'cyc348@proton.com',
        r'cyc349@proton.com',
        r'cyc350@proton.com',
        r'cyc351@proton.com',
        r'cyc352@proton.com',
        r'cyc353@proton.com',
        r'cyc354@proton.com',
        r'cyc355@proton.com',
        r'cyc356@proton.com',
        r'cyc357@proton.com',
        r'cyc358@proton.com',
        r'cyc359@proton.com',
        r'cyc360@proton.com',
        r'cyc361@proton.com',
        r'cyc362@proton.com',
        r'cyc363@proton.com',
        r'cyc364@proton.com',
        r'cyc365@proton.com',
        r'cyc366@proton.com',
        r'cyc367@proton.com',
        r'cyc368@proton.com',
        r'cyc369@proton.com',
        r'cyc370@proton.com',
        r'cyc371@proton.com',
        r'cyc372@proton.com',
        r'cyc373@proton.com',
        r'cyc374@proton.com',
        r'cyc375@proton.com',
        r'cyc376@proton.com',
        r'cyc377@proton.com',
        r'cyc378@proton.com',
        r'cyc379@proton.com',
        r'cyc380@proton.com',
        r'cyc381@proton.com',
        r'cyc382@proton.com',
        r'cyc383@proton.com',
        r'cyc384@proton.com',
        r'cyc385@proton.com',
        r'cyc386@proton.com',
        r'cyc387@proton.com',
        r'cyc388@proton.com',
        r'cyc389@proton.com',
        r'cyc390@proton.com',
        r'cyc391@proton.com',
        r'cyc392@proton.com',
        r'cyc393@proton.com',
        r'cyc394@proton.com',
        r'cyc395@proton.com',
        r'cyc396@proton.com',
        r'cyc397@proton.com',
        r'cyc398@proton.com',
        r'cyc399@proton.com',
        r'cyc400@proton.com',
        r'cyc401@proton.com',
        r'cyc402@proton.com',
        r'cyc403@proton.com',
        r'cyc404@proton.com',
        r'cyc405@proton.com',
        r'cyc406@proton.com',
        r'cyc407@proton.com',
        r'cyc408@proton.com',
        r'cyc409@proton.com',
        r'cyc410@proton.com',
        r'cyc411@proton.com',
        r'cyc412@proton.com',
        r'cyc413@proton.com',
        r'cyc414@proton.com',
        r'cyc415@proton.com',
        r'cyc416@proton.com',
        r'cyc417@proton.com',
        r'cyc418@proton.com',
        r'cyc419@proton.com',
        r'cyc420@proton.com',
        r'cyc421@proton.com',
        r'cyc422@proton.com',
        r'cyc423@proton.com',
        r'cyc424@proton.com',
        r'cyc425@proton.com',
        r'cyc426@proton.com',
        r'cyc427@proton.com',
        r'cyc428@proton.com',
        r'cyc429@proton.com',
        r'cyc430@proton.com',
        r'cyc431@proton.com',
        r'cyc432@proton.com',
        r'cyc433@proton.com',
        r'cyc434@proton.com',
        r'cyc435@proton.com',
        r'cyc436@proton.com',
        r'cyc437@proton.com',
        r'cyc438@proton.com',
        r'cyc439@proton.com',
        r'cyc440@proton.com',
        r'cyc441@proton.com',
        r'cyc442@proton.com',
        r'cyc443@proton.com',
        r'cyc444@proton.com',
        r'cyc445@proton.com',
        r'cyc446@proton.com',
        r'cyc447@proton.com',
        r'cyc448@proton.com',
        r'cyc449@proton.com',
        r'cyc450@proton.com',
        r'cyc451@proton.com',
        r'cyc452@proton.com',
        r'cyc453@proton.com',
        r'cyc454@proton.com',
        r'cyc455@proton.com',
        r'cyc456@proton.com',
        r'cyc457@proton.com',
        r'cyc458@proton.com',
        r'cyc459@proton.com',
        r'cyc460@proton.com',
        r'cyc461@proton.com',
        r'cyc462@proton.com',
        r'cyc463@proton.com',
        r'cyc464@proton.com',
        r'cyc465@proton.com',
        r'cyc466@proton.com',
        r'cyc467@proton.com',
        r'cyc468@proton.com',
        r'cyc469@proton.com',
        r'cyc470@proton.com',
        r'cyc471@proton.com',
        r'cyc472@proton.com',
        r'cyc473@proton.com',
        r'cyc474@proton.com',
        r'cyc475@proton.com',
        r'cyc476@proton.com',
        r'cyc477@proton.com',
        r'cyc478@proton.com',
        r'cyc479@proton.com',
        r'cyc480@proton.com',
        r'cyc481@proton.com',
        r'cyc482@proton.com',
        r'cyc483@proton.com',
        r'cyc484@proton.com',
        r'cyc485@proton.com',
        r'cyc486@proton.com',
        r'cyc487@proton.com',
        r'cyc488@proton.com',
        r'cyc489@proton.com',
        r'cyc490@proton.com',
        r'cyc491@proton.com',
        r'cyc492@proton.com',
        r'cyc493@proton.com',
        r'cyc494@proton.com',
        r'cyc495@proton.com',
        r'cyc496@proton.com',
        r'cyc497@proton.com',
        r'cyc498@proton.com',
        r'cyc499@proton.com',
        r'cyc500@proton.com',
        r'cyc501@proton.com',
        r'cyc502@proton.com',
        r'cyc503@proton.com',
        r'cyc504@proton.com',
        r'cyc505@proton.com',
        r'cyc506@proton.com',
        r'cyc507@proton.com',
        r'cyc508@proton.com',
        r'cyc509@proton.com',
        r'cyc510@proton.com',
        r'cyc511@proton.com',
        r'cyc512@proton.com',
        r'cyc513@proton.com',
        r'cyc514@proton.com',
        r'cyc515@proton.com',
        r'cyc516@proton.com',
        r'cyc517@proton.com',
        r'cyc518@proton.com',
        r'cyc519@proton.com',
        r'cyc520@proton.com',
        r'cyc521@proton.com',
        r'cyc522@proton.com',
        r'cyc523@proton.com',
        r'cyc525@proton.com',
        r'cyc526@proton.com',
        r'cyc527@proton.com',
        r'cyc528@proton.com',
        r'cyc529@proton.com',
        r'cyc530@proton.com',
        r'cyc531@proton.com',
        r'cyc532@proton.com',
        r'cyc533@proton.com',
        r'cyc534@proton.com',
        r'cyc535@proton.com',
        r'cyc536@proton.com',
        r'cyc537@proton.com',
        r'cyc538@proton.com',
        r'cyc539@proton.com',
        r'cyc540@proton.com',
        r'cyc541@proton.com',
        r'cyc542@proton.com',
        r'cyc543@proton.com',
        r'cyc544@proton.com',
        r'cyc545@proton.com',
        r'cyc546@proton.com',
        r'cyc547@proton.com',
        r'cyc548@proton.com',
        r'cyc549@proton.com',
        r'cyc550@proton.com',
        r'cyc551@proton.com',
        r'cyc552@proton.com',
        r'cyc553@proton.com',
        r'cyc554@proton.com',
        r'cyc555@proton.com',
        r'cyc556@proton.com',
        r'cyc557@proton.com',
        r'cyc558@proton.com',
        r'cyc559@proton.com',
        r'cyc560@proton.com',
        r'cyc561@proton.com',
        r'cyc562@proton.com',
        r'cyc563@proton.com',
        r'cyc564@proton.com',
        r'cyc565@proton.com',
        r'cyc566@proton.com',
        r'cyc567@proton.com',
        r'cyc568@proton.com',
        r'cyc569@proton.com',
        r'cyc570@proton.com',
        r'cyc571@proton.com',
        r'cyc572@proton.com',
        r'cyc573@proton.com',
        r'cyc574@proton.com',
        r'cyc575@proton.com',
        r'cyc576@proton.com',
        r'cyc577@proton.com',
        r'cyc578@proton.com',
        r'cyc579@proton.com',
        r'cyc580@proton.com',
        r'cyc581@proton.com',
        r'cyc582@proton.com',
        r'cyc583@proton.com',
        r'cyc584@proton.com',
        r'cyc585@proton.com',
        r'cyc586@proton.com',
        r'cyc587@proton.com',
        r'cyc588@proton.com',
        r'cyc589@proton.com',
        r'cyc590@proton.com',
        r'cyc591@proton.com',
        r'cyc592@proton.com',
        r'cyc593@proton.com',
        r'cyc594@proton.com',
        r'cyc595@proton.com',
        r'cyc596@proton.com',
        r'cyc597@proton.com',
        r'cyc598@proton.com',
        r'cyc599@proton.com',
        r'cyc600@proton.com',
        r'cyc601@proton.com',
        r'cyc602@proton.com',
        r'cyc603@proton.com',
        r'cyc604@proton.com',
        r'cyc605@proton.com',
        r'cyc606@proton.com',
        r'cyc607@proton.com',
        r'cyc608@proton.com',
        r'cyc609@proton.com',
        r'cyc610@proton.com',
        r'cyc611@proton.com',
        r'cyc612@proton.com',
        r'cyc613@proton.com',
        r'cyc614@proton.com',
        r'cyc615@proton.com',
        r'cyc616@proton.com',
        r'cyc617@proton.com',
        r'cyc618@proton.com',
        r'cyc619@proton.com',
        r'cyc620@proton.com',
        r'cyc621@proton.com',
        r'cyc622@proton.com',
        r'cyc623@proton.com',
        r'cyc624@proton.com',
        r'cyc625@proton.com',
        r'cyc626@proton.com',
        r'cyc627@proton.com',
        r'cyc628@proton.com',
        r'cyc629@proton.com',
        r'cyc630@proton.com',
        r'cyc631@proton.com',
        r'cyc632@proton.com',
        r'cyc633@proton.com',
        r'cyc634@proton.com',
        r'cyc635@proton.com',
        r'cyc636@proton.com',
        r'cyc637@proton.com',
        r'cyc638@proton.com',
        r'cyc639@proton.com',
        r'cyc640@proton.com',
        r'cyc641@proton.com',
        r'cyc642@proton.com',
        r'cyc643@proton.com',
        r'cyc644@proton.com',
        r'cyc645@proton.com',
        r'cyc646@proton.com',
        r'cyc647@proton.com',
        r'cyc648@proton.com',
        r'cyc649@proton.com',
        r'cyc650@proton.com',
        r'cyc651@proton.com',
        r'cyc652@proton.com',
        r'cyc653@proton.com',
        r'cyc654@proton.com',
        r'cyc655@proton.com',
        r'cyc656@proton.com',
        r'cyc657@proton.com',
        r'cyc658@proton.com',
        r'cyc659@proton.com',
        r'cyc660@proton.com',
        r'cyc661@proton.com',
        r'cyc662@proton.com',
        r'cyc663@proton.com',
        r'cyc664@proton.com',
        r'cyc665@proton.com',
        r'cyc666@proton.com',
        r'cyc667@proton.com',
        r'cyc668@proton.com',
        r'cyc669@proton.com',
        r'cyc670@proton.com',
        r'cyc671@proton.com',
        r'cyc672@proton.com',
        r'cyc673@proton.com',
        r'cyc674@proton.com',
        r'cyc675@proton.com',
        r'cyc676@proton.com',
        r'cyc677@proton.com',
        r'cyc678@proton.com',
        r'cyc679@proton.com',
        r'cyc680@proton.com',
        r'cyc681@proton.com',
        r'cyc682@proton.com',
        r'cyc683@proton.com',
        r'cyc684@proton.com',
        r'cyc685@proton.com',
        r'cyc686@proton.com',
        r'cyc687@proton.com',
        r'cyc688@proton.com',
        r'cyc689@proton.com',
        r'cyc690@proton.com',
        r'cyc691@proton.com',
        r'cyc692@proton.com',
        r'cyc693@proton.com',
        r'cyc694@proton.com',
        r'cyc695@proton.com',
        r'cyc696@proton.com',
        r'cyc697@proton.com',
        r'cyc698@proton.com',
        r'cyc699@proton.com',
        r'cyc700@proton.com',
        r'cyc701@proton.com',
        r'cyc702@proton.com',
        r'cyc703@proton.com',
        r'cyc704@proton.com',
        r'cyc705@proton.com',
        r'cyc706@proton.com',
        r'cyc707@proton.com',
        r'cyc708@proton.com',
        r'cyc709@proton.com',
        r'cyc710@proton.com',
        r'cyc711@proton.com',
        r'cyc712@proton.com',
        r'cyc713@proton.com',
        r'cyc714@proton.com',
        r'cyc715@proton.com',
        r'cyc716@proton.com',
        r'cyc717@proton.com',
        r'cyc718@proton.com',
        r'cyc719@proton.com',
        r'cyc720@proton.com',
        r'cyc721@proton.com',
        r'cyc722@proton.com',
        r'cyc723@proton.com',
        r'cyc724@proton.com',
        r'cyc725@proton.com',
        r'cyc726@proton.com',
        r'cyc727@proton.com',
        r'cyc728@proton.com',
        r'cyc729@proton.com',
        r'cyc730@proton.com',
        r'cyc731@proton.com',
        r'cyc732@proton.com',
        r'cyc733@proton.com',
        r'cyc734@proton.com',
        r'cyc735@proton.com',
        r'cyc736@proton.com',
        r'cyc737@proton.com',
        r'cyc738@proton.com',
        r'cyc739@proton.com',
        r'cyc740@proton.com',
        r'kev_backup@yahoo.com',
        r'cool_table@yahoo.com',
        r'cool_table2@yahoo.com',
        r'cool_table3@yahoo.com',
        r'cool_table4@yahoo.com',
        r'cool_table5@yahoo.com',
        r'cool_table6@yahoo.com',
        r'cool_table7@yahoo.com',
        r'cool_table8@yahoo.com',
        r'bot_alon1@yahoo.com',
        r'bot_alon2@yahoo.com',
        r'bot_alon3@yahoo.com',
        r'bot_alon4@yahoo.com',
        r'bot_alon5@yahoo.com',
        r'bot_alon6@yahoo.com',
        r'bot_alon7@yahoo.com',
        r'bot_alon8@yahoo.com',
        r'bot_alon9@yahoo.com',
        r'proton_velo1@protonmail.com',
        r'proton_velo2@protonmail.com',
        r'proton_velo3@protonmail.com',
        r'proton_velo4@protonmail.com',
        r'proton_velo5@protonmail.com',
        r'velo.yan1@yandex.com',
        r'velo.yan2@yandex.com',
        r'velo.yan3@yandex.com',
        r'velo.yan4@yandex.com',
        r'velo.yan5@yandex.com',
        r'velo.yan6@yandex.com',
        r'velo.yan7@yandex.com',
        r'velo.yan8@yandex.com',
        r'velo.yan9@yandex.com',
        r'velo.yan10@yandex.com',
        r'velo.yan11@yandex.com',
        r'velo.yan12@yandex.com',
        r'velo.yan13@yandex.com',
        r'velo.yan14@yandex.com',
        r'velo.yan15@yandex.com',
        r'velo.yan16@yandex.com',
        r'velo.yan16@yandex.com',
        r'velo.yan18@yandex.com',
        r'velo.yan19@yandex.com',
        r'velo.yan20@yandex.com',
        r'velo.yan21@yandex.com',
        r'velo.yan22@yandex.com',
        r'velo.yan24@yandex.com',
        r'velo.yan25@yandex.com',
        r'velo.yan26@yandex.com',
        r'velo.yan28@yandex.com',
        r'velo.yan29@yandex.com',
        r'velo.yan17@yandex.com',
        r'velo.yan23@yandex.com',
        r'velo.yan27@yandex.com',
        r'velo.yan30@yandex.com',
        r'velo.yan31@yandex.com',
        r'velo.yan32@yandex.com',
        r'velo.yan33@yandex.com',
        r'velo.yan34@yandex.com',
        r'velo.yan35@yandex.com',
        r'velo.yan36@yandex.com',
        r'velo.yan37@yandex.com',
        r'velo.yan38@yandex.com',
        r'velo.yan39@yandex.com',
        r'velo.yan40@yandex.com',
        r'velo.yan41@yandex.com',
        r'velo.yan42@yandex.com',
        r'velo.yan43@yandex.com',
        r'velo.yan44@yandex.com',
        r'velo.yan45@yandex.com',
        r'velo.yan46@yandex.com',
        r'velo.yan47@yandex.com',
        r'velo.yan48@yandex.com',
        r'velo.yan49@yandex.com',
        r'velo.yan50@yandex.com',
        r'velo.yan51@yandex.com',
        r'velo.yan52@yandex.com',
        r'velo.yan53@yandex.com',
        r'velo.yan54@yandex.com',
        r'velo.yan55@yandex.com',
        r'velo.yan56@yandex.com',
        r'velo.yan57@yandex.com',
        r'velo.yan58@yandex.com',
        r'velo.yan59@yandex.com',
        r'velo.yan61@yandex.com',
        r'velo.yan62@yandex.com',
        r'velo.yan63@yandex.com',
        r'velo.yan64@yandex.com',
        r'velo.yan65@yandex.com',
        r'velo.yan66@yandex.com',
        r'velo.yan67@yandex.com',
        r'velo1@yandex.com',
        r'velo2@yandex.com',
        r'velo3@yandex.com',
        r'velo4@yandex.com',
        r'velo5@yandex.com',
        r'velo6@yandex.com',
        r'velo7@yandex.com',
        r'velo8@yandex.com',
        r'velo9@yandex.com',
        r'velo10@yandex.com',
        r'velo11@yandex.com',
        r'velo12@yandex.com',
        r'velo13@yandex.com',
        r'velo14@yandex.com',
        r'velo14@yandex.com',
        r'velo15@yandex.com',
        r'velo16@yandex.com',
        r'velo17@yandex.com',
        r'velo18@yandex.com',
        r'velo19@yandex.com',
        r'cyc1@yandex.com',
        r'cyc2@yandex.com',
        r'abc@yandex.com',
        r'mkm@yandex.com',
        r'zxc@yandex.com',
        r'xcv@yandex.com',
        r'asd@yandex.com',
        r'sdf@yandex.com',
        r'ggg@yandex.com',
        r'qqq@yandex.com',
        r'jjj@yandex.com',
        r'eee@yandex.com',
        r'nvb@yan.com',
        r'cyc1@aol.com',
        r'cyc2@aol.com',
        r'cyc3@aol.com',
        r'cyc4@aol.com',
        r'cyc5@aol.com',
        r'cyc6@aol.com',
        r'cyc7@aol.com',
        r'cyc8@aol.com',
        r'cyc9@aol.com',
        r'cy10@aol.com',
        r'cyc11@aol.com',
        r'cyc12@aol.com',
        r'cyc13@aol.com',
        r'cyc14@aol.com',
        r'cyc15@aol.com',
        r'cyc1@gmx.com',
        r'cyc2@gmx.com',
        r'cyc3@gmx.com',
        r'cyc1@yahoo.com',
        r'cyc1@proton.com',
        r'cyc2@proton.com',
        r'cyc3@proton.com',
        r'cyc4@proton.com',
        r'cyc5@proton.com',
        r'cyc6@proton.com',
        r'cyc7@proton.com',
        r'cyc8@proton.com',
        r'cyc9@proton.com',
        r'cyc10@proton.com',
        r'cyc11@proton.com',
        r'cyc12@proton.com',
        r'cyc13@proton.com',
        r'cyc14@proton.com',
        r'cyc15@proton.com',
        r'cyc16@proton.com',
        r'cyc17@proton.com',
        r'cyc18@proton.com',
        r'cyc19@proton.com',
        r'cyc20@proton.com',
        r'cyc21@proton.com',
        r'cyc22@proton.com',
        r'cyc23@proton.com',
        r'cyc24@proton.com',
        r'cyc25@proton.com',
        r'cyc26@proton.com',
        r'cyc27@proton.com',
        r'cyc28@proton.com',
        r'cyc29@proton.com',
        r'cyc30@proton.com',
        r'cyc31@proton.com',
        r'cyc32@proton.com',
        r'cyc33@proton.com',
        r'cyc34@proton.com',
        r'cyc35@proton.com',
        r'cyc36@proton.com',
        r'cyc37@proton.com',
        r'cyc38@proton.com',
        r'cyc39@proton.com',
        r'cyc40@proton.com',
        r'cyc41@proton.com',
        r'cyc42@proton.com',
        r'cyc43@proton.com',
        r'cyc44@proton.com',
        r'cyc45@proton.com',
        r'cyc46@proton.com',
        r'cyc47@proton.com',
        r'cyc48@proton.com',
        r'cyc49@proton.com',
        r'cyc50@proton.com',
        r'cyc51@proton.com',
        r'cyc52@proton.com',
        r'cyc53@proton.com',
        r'cyc54@proton.com',
        r'cyc55@proton.com',
        r'cyc56@proton.com',
        r'cyc57@proton.com',
        r'cyc58@proton.com',
        r'cyc59@proton.com',
        r'cyc60@proton.com',
        r'cyc61@proton.com',
        r'cyc62@proton.com',
        r'cyc63@proton.com',
        r'cyc64@proton.com',
        r'cyc65@proton.com',
        r'cyc66@proton.com',
        r'cyc67@proton.com',
        r'cyc68@proton.com',
        r'cyc69@proton.com',
        r'cyc70@proton.com',
        r'cyc71@proton.com',
        r'cyc72@proton.com',
        r'cyc73@proton.com',
        r'cyc74@proton.com',
        r'cyc75@proton.com',
        r'cyc76@proton.com',
        r'cyc77@proton.com',
        r'cyc78@proton.com',
        r'cyc79@proton.com',
        r'cyc80@proton.com',
        r'cyc81@proton.com',
        r'cyc82@proton.com',
        r'cyc83@proton.com',
        r'cyc84@proton.com',
        r'cyc85@proton.com',
        r'cyc86@proton.com',
        r'cyc87@proton.com',
        r'cyc88@proton.com',
        r'cyc89@proton.com',
        r'cyc90@proton.com',
        r'cyc91@proton.com',
        r'cyc92@proton.com',
        r'cyc93@proton.com',
        r'cyc94@proton.com',
        r'cyc95@proton.com',
        r'cyc96@proton.com',
        r'cyc97@proton.com',
        r'cyc98@proton.com',
        r'cyc99@proton.com',
        r'cyc100@proton.com',
        r'cyc101@proton.com',
        r'cyc102@proton.com',
        r'cyc103@proton.com',
        r'cyc104@proton.com',
        r'cyc105@proton.com',
        r'cyc106@proton.com',
        r'cyc107@proton.com',
        r'cyc108@proton.com',
        r'cyc109@proton.com',
        r'cyc110@proton.com',
        r'cyc111@proton.com',
        r'cyc112@proton.com',
        r'cyc113@proton.com',
        r'cyc114@proton.com',
        r'cyc115@proton.com',
        r'cyc116@proton.com',
        r'cyc117@proton.com',
        r'cyc118@proton.com',
        r'cyc119@proton.com',
        r'cyc120@proton.com',
        r'cyc121@proton.com',
        r'cyc122@proton.com',
        r'cyc123@proton.com',
        r'cyc124@proton.com',
        r'cyc125@proton.com',
        r'cyc126@proton.com',
        r'cyc127@proton.com',
        r'cyc128@proton.com',
        r'cyc129@proton.com',
        r'cyc130@proton.com',
        r'cyc131@proton.com',
        r'cyc132@proton.com',
        r'cyc134@proton.com',
        r'cyc135@proton.com',
        r'cyc136@proton.com',
        r'cyc137@proton.com',
        r'cyc138@proton.com',
        r'cyc139@proton.com',
        r'cyc140@proton.com',
        r'cyc141@proton.com',
        r'cyc142@proton.com',
        r'cyc143@proton.com',
        r'cyc144@proton.com',
        r'cyc145@proton.com',
        r'cyc146@proton.com',
        r'cyc147@proton.com',
        r'cyc148@proton.com',
        r'cyc149@proton.com',
        r'cyc150@proton.com',
        r'cyc151@proton.com',
        r'cyc152@proton.com',
        r'cyc153@proton.com',
        r'cyc154@proton.com',
        r'cyc155@proton.com',
        r'cyc156@proton.com',
        r'cyc158@proton.com',
        r'cyc159@proton.com',
        r'cyc160@proton.com',
        ]
WORKOUTS_COLS = ['workout_id', 'workout_tp_id', 'workout_strava_id', 'cyclist_id', 'type', 'tags', 'workout_week',
                 'workout_month', 'workout_datetime', 'workout_location', 'total_time', 'workout_title', 'cyclist_mass',
                 'elevation_gain',
                 'elevation_loss', 'elevation_average', 'elevation_maximum', 'elevation_minimum', 'temp_avg',
                 'temp_min', 'temp_max', '_1000_to_1500_m', '_1500_to_2000_m', '_2000_to_2500_m', '_2500_to_3000_m',
                 '_3000_to_3500_m', 'relative_effort', 'training_load', 'intensity', 'distance', 'energy', 'calories',
                 'if', 'tss_actual', 'tss_calculation_method', 'hidden', 'locked']
WORKOUTS_HRS_COLS = ['workout_id', 'workout_strava_id', 'hr_maximum', 'hr_average', 'hr_5_seconds', 'hr_10_seconds',
                     'hr_12_seconds', 'hr_20_seconds', 'hr_30_seconds', 'hr_1_minute', 'hr_2_minutes', 'hr_5_minutes',
                     'hr_6_minutes', 'hr_10_minutes', 'hr_12_minutes', 'hr_20_minutes', 'hr_30_minutes', 'hr_1_hour',
                     'hr_90_minutes', 'hr_3_hours', 'hr_zone_1', 'hr_zone_2', 'hr_zone_3', 'hr_zone_4', 'hr_zone_5',
                     'hr_zone_1_min', 'hr_zone_2_min', 'hr_zone_3_min', 'hr_zone_4_min', 'hr_zone_5_min']
WORKOUTS_CADENCES_COLS = ['workout_id', 'workout_strava_id', 'cadence_5_seconds', 'cadence_10_seconds',
                          'cadence_12_seconds', 'cadence_20_seconds', 'cadence_30_seconds', 'cadence_1_minute',
                          'cadence_2_minutes', 'cadence_5_minutes', 'cadence_6_minutes', 'cadence_10_minutes',
                          'cadence_12_minutes', 'cadence_20_minutes', 'cadence_30_minutes', 'cadence_1_hour',
                          'cadence_90_minutes', 'cadence_3_hours', 'cadence_maximum', 'cadence_average']
WORKOUTS_POWERS_COLS = ['workout_id', 'workout_strava_id', 'power_maximum', 'power_average', 'normalized_power',
                        'power_5_seconds', 'power_10_seconds', 'power_12_seconds', 'power_20_seconds',
                        'power_30_seconds', 'power_1_minute', 'power_2_minutes', 'power_5_minutes', 'power_6_minutes',
                        'power_10_minutes', 'power_12_minutes', 'power_20_minutes', 'power_30_minutes',
                        'power_1_hour', 'power_90_minutes', 'power_3_hours', 'power_zone_1', 'power_zone_2',
                        'power_zone_3', 'power_zone_4', 'power_zone_5', 'power_zone_6', 'power_zone_7',
                        'power_zone_1_min', 'power_zone_2_min', 'power_zone_3_min', 'power_zone_4_min',
                        'power_zone_5_min', 'power_zone_6_min', 'power_zone_7_min']
WORKOUTS_SPEEDS_COLS = ['workout_id', 'workout_strava_id', 'speed_maximum', 'speed_average', 'speed_5_seconds',
                        'speed_10_seconds', 'speed_12_seconds', 'speed_20_seconds', 'speed_30_seconds',
                        'speed_1_minute', 'speed_2_minutes', 'speed_5_minutes', 'speed_6_minutes', 'speed_10_minutes',
                        'speed_12_minutes', 'speed_20_minutes', 'speed_30_minutes', 'speed_1_hour',
                        'speed_90_minutes', 'speed_3_hours', 'speed_zone_1', 'speed_zone_2', 'speed_zone_3',
                        'speed_zone_4', 'speed_zone_5', 'speed_zone_6', 'speed_zone_7', 'speed_zone_1_min',
                        'speed_zone_2_min', 'speed_zone_3_min', 'speed_zone_4_min', 'speed_zone_5_min',
                        'speed_zone_6_min', 'speed_zone_7_min']
