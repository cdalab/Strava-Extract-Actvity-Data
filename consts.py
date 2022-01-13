LOG_LEVEL = 'INFO'
BASE_STRAVA_URL = 'https://www.strava.com/'
ERROR_DEFAULT_MSG = 'Failed while trying to login to STRAVA.'
DEBUG = True
LOG_LEVEL_DICT = {'ERROR': 0, 'WARNING': 1, 'INFO': 2}
TIMEOUT = 3
PASSWORD = '12345678'
OPTIONS_TO_IGNORE = ["/route", "/export_gpx", "/flags/new", "/overview", "/laps"]

UNDESIRED_UNITS = ["feet", "miles", "Degrees Fahrenheit", "miles per hour"]
ACTIVITY_POST_TYPES = ["Activity", "GroupActivity", "ChallengeJoin", "ClubJoin"]

ANALYSIS_PAGE_TYPES = ['/analysis', '/power-curve', '/zone-distribution',
                       '/power-distribution', '/est-power-curve',
                       '/est-power-distribution', '/heartrate']
ACTIVITY_TYPES = ['Ride', 'Indoor Cycling', 'Virtual Ride', 'Ride–Commute', 'Race']
ACTIVITY_TYPES_TO_IGNORE = ['Nordic Ski', 'Run', 'Workout', 'Roller Ski', 'Weight Training', 'Ice Skate', 'Crossfit', 'Walk', 'Winter Sport', 'Treadmill workout', 'Hike']
USERS = [
    r'kvspek@gmail.com',
    r'spektork@post.bgu.ac.il',
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
