from tinydb import TinyDB, Query
import uuid
from datetime import datetime, timedelta
import math
from collections import Counter
import calendar
import shutil
import sys
from pathlib import Path

def get_base_dir() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent

base_dir = get_base_dir()

data_dir = base_dir / 'data'

data_dir.mkdir(exist_ok=True)

db = TinyDB(data_dir / 'training_db.json')

customisation_data = TinyDB(data_dir / 'customisation_db.json')


if customisation_data.all() == []:
    customisation_data.insert(
        {
            'training_types': ['Jogging', 'Bicycle', 'Push', 'Pull', 'Legs', 'Core', 'Other'],
            'distance_training': ['Jogging', 'Bicycle'],
            'sets_training': ['Push', 'Pull', 'Legs', 'Core']
        }
    )


space_filler = '\n' + '----------------------------------------------------------------------------------------------------------------'


def generate_id():
    return str(uuid.uuid4())


def get_weekday(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return date.weekday() + 1


def generate_display_id(d, t):
    existing = db.search(
    (Query().date == d) & (Query().training_type == t)
    )
    counter = len(existing) + 1
    display_id = f'{d}_{t}_{counter:02d}'
    return display_id


def add_training_to_db(
    date,
    training_type,
    duration_min,
    difficulty,
    fun,
    volume_type,
    volume_value,
    notes=None
    ):
    entry = {
    'id': generate_id(),
    'display_id': generate_display_id(date, training_type),
    'date': date,
    'weekday': get_weekday(date),
    'training_type': training_type,
    'duration_min': duration_min,
    'difficulty': difficulty,
    'fun': fun,
    'volume': {
        'type': volume_type,
        'value': volume_value
    },
    'notes': notes
    }
    db.insert(entry)


def count_days(start_date, end_date, day):
    count = 0
    current = start_date

    while current <= end_date:
        if current.weekday() == day:
            count += 1
        current += timedelta(days=1)

    return count


def is_date_valid(d):
    try:
        _d = datetime.strptime(d, '%Y-%m-%d')
        if _d <= datetime.today():
            return True
        else:
            return False
    except ValueError:
            return False


def is_month_valid(m):
    try:
        _m = datetime.strptime(m, '%Y-%m')
        today = datetime.today()
        current_month = datetime(year=today.year, month=today.month, day=1)
        if _m <= current_month:
            return True
        else:
            return False
    except ValueError:
            return False


def is_year_valid(y):
    try:
        _y = datetime.strptime(y, '%Y')
        today = datetime.today()
        current_year = datetime(year=today.year, month=1, day=1)
        if _y <= current_year:
            return True
        else:
            return False
    except ValueError:
            return False


def get_average_value(entries, t):
    c = 0
    if len(entries) > 0:
        for e in entries:
            if t == 'volume':
                c += e['volume']['value']
            else:
                c += e[t]
        c = c / len(entries)
    return round(c, 1)
    

def print_with_auto_tab(text):
    c = 0
    terminal_width = shutil.get_terminal_size().columns
    tab_width = 20
    line_length = terminal_width - tab_width
    while len(text) > line_length:
        break_index = text.rfind(' ', 0, line_length)        
        if break_index == -1:
            break_index = line_length
        if c == 0:
            print('\t' + text[:break_index].rstrip())
            c += 1
        else:
            print('\t\t' + text[:break_index].rstrip())
        text = text[break_index:].lstrip()
    if text:
        if c == 0:
            print('\t' + text)
        else:
            print('\t\t' + text)


def get_general_metrics(entries, start_date, end_date, time_interval_length):
    print(space_filler)
    print('\n' + f'Here are the metrics from {start_date} to {end_date}, covering a {time_interval_length} days, equal to {round(time_interval_length / 7, 1)} weeks.')
    
    average_sessions_per_day = len(entries) / time_interval_length
    average_sessions_per_week = (len(entries) / time_interval_length) * 7
    average_sessions_per_month = (len(entries) / time_interval_length) * 30.4
    average_sessions_per_year = (len(entries) / time_interval_length) * 365.24
    
    entries_weekdays = [[e for e in entries if e['weekday'] == i] for i in range(1, 8)]
    average_sessions_weekdays = [len(entries_weekdays[i]) / count_days(start_date=datetime.strptime(start_date, '%Y-%m-%d'), end_date=datetime.strptime(end_date, '%Y-%m-%d'), day=i)
                                 if count_days(start_date=datetime.strptime(start_date, '%Y-%m-%d'), end_date=datetime.strptime(end_date, '%Y-%m-%d'), day=i) > 0 
                                 else 0 
                                 for i in range(0, 7)]
    most_common_exercise_weekdays = [
        Counter(e['training_type'] for e in day).most_common(1)[0][0]
        if day else None
        for day in entries_weekdays
        ]
    average_duration_weekdays = [get_average_value(entries_weekdays[i], 'duration_min') for i in range(0, 7)]
    average_fun_weekdays = [get_average_value(entries_weekdays[i], 'fun') for i in range(0, 7)]
    average_difficulty_weekdays = [get_average_value(entries_weekdays[i], 'difficulty') for i in range(0, 7)]
    weekday_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    disciplines = customisation_data.all()[0]['training_types']
    distance_training = customisation_data.all()[0]['distance_training']
    sets_training = customisation_data.all()[0]['sets_training']
    entries_disciplines = [[e for e in entries if e['training_type'] == disciplines[i]] for i in range(0, len(disciplines))]
    entries_unknown_disciplines = [e for e in entries if e['training_type'] not in disciplines]
    average_sessions_per_week_disciplines = [(len(entries_disciplines[i]) / time_interval_length) * 7 for i in range(0, len(disciplines))]
    average_duration_disciplines = [get_average_value(entries_disciplines[i], 'duration_min') for i in range(0, len(disciplines))]
    average_fun_disciplines = [get_average_value(entries_disciplines[i], 'fun') for i in range(0, len(disciplines))]
    average_difficulty_disciplines = [get_average_value(entries_disciplines[i], 'difficulty') for i in range(0, len(disciplines))]
    average_volume_amount_disciplines = [get_average_value(entries_disciplines[i], 'volume')
                                        if disciplines[i] in distance_training or disciplines[i] in sets_training
                                        else 0
                                        for i in range(0, len(disciplines))]
    print(average_volume_amount_disciplines)

    entries_distance = [e for e in entries if e['training_type'] in distance_training]
    entries_sets = [e for e in entries if e['training_type'] in sets_training]
    average_sessions_per_week_distance = (len(entries_distance) / time_interval_length) * 7
    average_sessions_per_week_sets = (len(entries_sets) / time_interval_length) * 7
    
    print('\n' + f'You worked out on {round(average_sessions_per_day * 100)}% of days.' + '\n' + f'Your average amount of training sessions are {round(average_sessions_per_week, 1)} per week, equal to {round(average_sessions_per_month, 1)} per month and {round(average_sessions_per_year, 1)} per year.')
    print('\n' + 'Here are some stats about your weeks.')
    for i in range(0, 7):
        print_with_auto_tab(f'{weekday_list[i]}: You worked out on {round(average_sessions_weekdays[i] * 100)}% of days, equalling {len(entries_weekdays[i])} sessions for {round(average_duration_weekdays[i], 1)} minutes each on average; your favourite workout style was {most_common_exercise_weekdays[i] if isinstance(most_common_exercise_weekdays[i], str) else most_common_exercise_weekdays[i][0] if isinstance(most_common_exercise_weekdays[i], list) else 'none'}. On this weekday, you rated the training with {round(average_difficulty_weekdays[i], 1)}/10 in terms of difficulty and {round(average_fun_weekdays[i], 1)}/10 in terms of fun.')
    print('\n' + 'Here are some stats about your disciplines.')
    print(f'There were {len(entries_unknown_disciplines)} unidentified training sessions in the selected time interval, which means their disciplines cannot be found in your list anymore.')
    for i in range(0, len(disciplines)):
        print_with_auto_tab(f'{disciplines[i]}: You did this training for {len(entries_disciplines[i])} times in the selected period. On average you worked out {round(average_sessions_per_week_disciplines[i], 1)} times per week for {round(average_duration_disciplines[i], 1)} minutes per session. {f'Every session you covered a distance of {average_volume_amount_disciplines[i]}km, which adds up to a total of {average_volume_amount_disciplines[i] * len(entries_disciplines[i])}km. ' if disciplines[i] in distance_training else f'Every session you did {average_volume_amount_disciplines[i]} sets, which adds up to a total of {average_volume_amount_disciplines[i] * len(entries_disciplines[i])} sets for all of your sessions combined. ' if disciplines[i] in sets_training else ''}You rated the difficulty to be {round(average_difficulty_disciplines[i], 1)}/10 and the fun to be {round(average_fun_disciplines[i], 1)}/10.')
    print('\n' + f'For distance-type training, this results in an average of {round(average_sessions_per_week_distance, 1)} sessions per week and for sets-type training in {round(average_sessions_per_week_sets, 1)} sessions.')


def input_validation(input_type, extra_argument = None):
    arg = None
    while arg == None:
        if input_type == 'dialogue.action':
            print('\n' + 'What would you like to run?' + '\n' + '\t[1] Track workout' + '\n' + '\t[2] Remove Workout' + '\n' + '\t[3] Show statistics' + '\n' + '\t[4] Edit disciplines' + '\n' + '\t[5] / [Q] Quit')
            _arg = input('\tAction: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            if _arg in [str(1), str(3), str(4), str(5), 'Q', 'q']:
                arg = _arg
            elif _arg in str(2) and db.all() != []:
                arg = _arg
            elif _arg in str(2):
                print('\n' + 'Start tracking your workouts first!')
            else:
                print('\n' + 'Invalid choice!')

        elif input_type == 'track_workout.date':
            print('\n' + 'Enter the date in question in the format YYYY-MM-DD or leave empty to choose the current date, then press Enter.')
            _arg = input('\tDate: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            if _arg == '':
                arg = datetime.today().strftime('%Y-%m-%d')
            else:
                try:
                    _a = datetime.strptime(_arg, '%Y-%m-%d')
                    if is_date_valid(_arg):
                        arg = _arg
                    else:
                        print('Invalid choice!')
                except ValueError:
                    print('Invalid choice!')

        elif input_type == 'track_workout.training_type':
            print('\n' + 'Choose the training type:')
            for i in range(0, len(customisation_data.all()[0]['training_types'])):
                print(f'\t[{i + 1}] {customisation_data.all()[0]['training_types'][i]}')
            _arg = input('\tType of training: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a <= 8:
                    arg = customisation_data.all()[0]['training_types'][_a - 1]
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'track_workout.duration':
            print('\n' + 'Enter the training duration in minutes.')
            _arg = input('\tDuration: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'track_workout.difficulty':
            print('\n' + 'Enter your perceived difficulty of the training on a scale from 1 to 10 (1 = Easy, 10 = Very hard).')
            _arg = input('\tDifficulty: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = float(_arg)
                if 1 <= _a <= 10:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'track_workout.fun':
            print('\n' + 'Estimate the fun you had during the training on a scale from 1 to 10 (1 = Sucks, 10 = Super fun).')
            _arg = input('\tFun: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = float(_arg)
                if 1 <= _a <= 10:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'track_workout.distance':
            print('\n' + 'Enter the distance travelled in km.')
            _arg = input('\tDistance: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = float(_arg)
                if 1 <= _a:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'track_workout.sets':
            print('\n' + 'Enter enter the number of completed sets.')
            _arg = input('\tSets: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')  

        elif input_type == 'track_workout.notes':
            print('\n' + 'Optionally enter notes now.')
            _arg = input('\tNotes: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            arg = _arg

        elif input_type == 'analyse_workouts.time_choice':
            print('\n' + 'Please choose what time you want to analyse.' + '\n' + '\t[1] From the first to the latest entry' + '\n' + '\t[2] From the first entry to today' + '\n' + '\t[3] Specific month' + '\n' + '\t[4] Specific year' + '\n' + '\t[5] Current year until now' + '\n' + '\t[6] Custom time interval')
            _arg = input('\tChoice: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a <= 6:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'analyse_workouts.month_choice':
            print('\n' + 'Please enter the month in question in the following format: YYYY-MM')
            _arg = input('\tMonth: ').strip()
            if _arg in ['quit', 'Quit']:
                quit_app()
            if is_month_valid(_arg):
                arg = datetime.strptime(_arg, '%Y-%m')
            else:
                print('Invalid choice!')

        elif input_type == 'analyse_workouts.year_choice':
            print('\n' + 'Please enter the year in question in the following format: YYYY')
            _arg = input('\tYear: ').strip()
            if _arg in ['quit', 'Quit']:
                quit_app()
            if is_year_valid(_arg):
                arg = _arg
            else:
                print('Invalid choice!')

        elif input_type == 'analyse_workouts.metrics_choice':
            print('\n' + 'Please choose what metrics you want to analyse.' + '\n' + '\t[1] General Metrics' + '\n' + '\t[2] Diagrams')
            _arg = input('\tChoice: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a <= 2:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'custom_disciplines.disciplines':
            print('\n' + 'Please enter the disciplines you would like to add.' + '\n' + 'They must not be similar to existing disciplines.' + '\n' + 'To add multiple at once, put a space between them. Discipline names must not contain spaces or underscores.' + '\n' + 'If you would like to remove any of the existing disciplines, write /<discipline-name>' + '\n' + 'To completely reset your disciplines, simply type "RESET". This has to be the only input and be capitalised to work, otherwise will you create a new discipline called "Reset".' + '\n' + 'To go back, type "BACK", same as with "RESET".')
            _arg = input('\tDisciplines: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            elif _arg == '':
                print('Please enter disciplines as described above or quit.')
            elif '_' in _arg:
                print('Please do not use underscores in discipline names.')
            elif _arg == 'RESET':
                customisation_data.update({
                    'training_types': ['Jogging', 'Bicycle', 'Push', 'Pull', 'Legs', 'Core', 'Other'],
                    'distance_training': ['Jogging', 'Bicycle'],
                    'sets_training': ['Push', 'Pull', 'Legs', 'Core']
                    })
                print('\n' + 'Successful reset of your disciplines.')
                arg = 'RESET'
            elif _arg == 'BACK':
                arg = 'BACK'
            else:
                _arg = _arg.strip().split()
                _arg_add = [a.lower().title() for a in _arg if a[0] != '/']
                _arg_rm = [a[1:].lower().title() for a in _arg if a[0] == '/']
                _arg_add_valid = True
                for a in _arg_add:
                    if a in customisation_data.all()[0]['training_types']:
                        print(f'Invalid input! Discipline {a} already exists.')
                        _arg_add_valid = False
                _arg_rm_valid = True
                for a in _arg_rm:
                    if a not in customisation_data.all()[0]['training_types'] or a == 'Other':
                        print(f'Invalid input! Discipline {a} does not exist or cannot be touched.')
                        _arg_rm_valid = False
                if _arg_add_valid and _arg_rm_valid:
                    arg = [_arg_add, _arg_rm]    

        elif input_type == 'custom_disciplines.value_type':
            print('\n' + f'Which metric should be used to measure {extra_argument}?' + '\n' + '\t[1] Distance in km' + '\n' + '\t[2] Sets' + '\n' + '\t[3] None')
            _arg = input('\tMetric: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a <= 3:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')

        elif input_type == 'remove_workout.id':
            print('\n' + 'Please enter the ID to remove. Or name a date to search; type "TODAY" for the date of today.' + '\n' + 'IDs have the following form: <DATE (YYYY-MM-DD)>_<DISCIPLINE NAME>_<TWO-CHARACTER NUMBER OF THE SESSION FOR THE DAY OF INTEREST>; for example: 2025-12-30_Pull_01')
            _arg = input('\tChoice: ')
            if _arg in ['quit', 'Quit']:
                quit_app()
            elif _arg == 'TODAY':
                _arg = datetime.today().strftime('%Y-%m-%d')
            try:
                _a = datetime.strptime(_arg, '%Y-%m-%d')
                if _a <= datetime.today():
                        dates = {
                            (_a - timedelta(days=1)).strftime('%Y-%m-%d'),
                            _a.strftime('%Y-%m-%d'),
                            (_a + timedelta(days=1)).strftime('%Y-%m-%d'),
                            }
                        sessions = db.search(Query().date.one_of(dates))
                        if sessions == []:
                            print('\n' + 'No sessions were found on this date ±1 day.')
                        else:
                            print('\n' + 'The following sessions were found:')
                            for s in sessions:
                                print(f'\t{s['display_id']}')
                else:
                    print('Invalid choice!')
            except ValueError:
                _a = _arg.split('_')
                if len(_a) == 3 and is_date_valid(_a[0]) and _a[1] in customisation_data.all()[0]['training_types'] and len(db.search(Query().display_id == _arg)) == 1:
                    arg = _arg
                else:
                    print('Invalid input!')

        else:
            print('\n' + 'There was a problem validating your input.' + '\n' + 'Please make sure you did not change any keywords for input identification.' + '\n' + 'If the problem persist, please contact the dev.')        
    return arg
     

def dialogue():
    print('\n' + 'Welcome! To quit, you can always type "Quit" or press CTL + C.')
    while True:
        choice = input_validation('dialogue.action')
        if choice not in ['5', 'Q', 'q']:
            print(space_filler)
        if choice == '1':
            track_workout()
        elif choice == '2':
            remove_workout()
        elif choice == '3':
            analyse_workouts()
        elif choice == '4':
            custom_disciplines()
        elif choice in ['5', 'Q', 'q']:
            quit_app()
        else:
            print('\n' + 'There was a problem validating your input.' + '\n' + 'Please make sure you did not change any keywords for input identification.' + '\n' + 'If the problem persist, please contact the dev.')                


def track_workout():
    print('\n' + 'Please enter some information about your workout.')
    date = input_validation('track_workout.date')
    training_type = input_validation('track_workout.training_type')
    duration_min = input_validation('track_workout.duration')
    difficulty = input_validation('track_workout.difficulty')
    fun = input_validation('track_workout.fun')
    volume_type = 'distance' if training_type in customisation_data.all()[0]['distance_training'] else 'sets' if training_type in customisation_data.all()[0]['sets_training'] else None
    volume_value = input_validation('track_workout.distance') if volume_type == 'distance' else input_validation('track_workout.sets') if volume_type == 'sets' else None
    notes = input_validation('track_workout.notes')
    add_training_to_db(date=date, training_type=training_type, duration_min=duration_min, difficulty=difficulty, fun=fun, volume_type=volume_type, volume_value=volume_value, notes=notes)
    print('\n' + 'Successfully tracked the training session.')
    print(space_filler)


def remove_workout():
    id = input_validation('remove_workout.id')
    db.remove(Query().display_id == id)
    print('\n' + 'Successfully removed the session.')
    print(space_filler)


def analyse_workouts():
    time_choice = input_validation('analyse_workouts.time_choice')
    if time_choice == 1:
        start_date = min(
            db.all(),
            key=lambda e: datetime.strptime(e['date'], '%Y-%m-%d')
            )['date']
        end_date = max(
            db.all(),
            key=lambda e: datetime.strptime(e['date'], '%Y-%m-%d')
            )['date']
    elif time_choice == 2:
        start_date = min(
            db.all(),
            key=lambda e: datetime.strptime(e['date'], '%Y-%m-%d')
            )['date']
        end_date = datetime.today().strftime('%Y-%m-%d')
    elif time_choice == 3:
        month = input_validation('analyse_workouts.month_choice')
        start_date = month.strftime('%Y-%m-01')
        end_date = f'{month.year}-{month.month:02d}-{calendar.monthrange(month.year, month.month)[1]:02d}'
    elif time_choice == 4:
        year = input_validation('analyse_workouts.year_choice')
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
    elif time_choice == 5:
        start_date = f'{datetime.today().year}-01-01'
        end_date = datetime.today().strftime('%Y-%m-%d')
    elif time_choice == 6:
        print('Coming soon.')
    else:
        print('\n' + 'There was a problem validating your input.' + '\n' + 'Please make sure you did not change any keywords for input identification.' + '\n' + 'If the problem persist, please contact the dev.')                
    entries = db.search(
    (Query().date >= start_date) &
    (Query().date <= end_date)
    )
    time_interval_length = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
    metrics_choice = input_validation('analyse_workouts.metrics_choice')
    if metrics_choice == 1:
        get_general_metrics(entries=entries, start_date=start_date, end_date=end_date, time_interval_length=time_interval_length)
    elif metrics_choice == 2:
        print('\n' + 'Coming soon.')
    print(space_filler)


def custom_disciplines():
    print('\n' + 'Current disciplines:')
    for i in range(0, len(customisation_data.all()[0]['training_types'])):
        print_with_auto_tab(f'{i + 1}. {customisation_data.all()[0]['training_types'][i]}')
    disciplines = input_validation('custom_disciplines.disciplines')
    if disciplines not in ['RESET', 'BACK']:
        _training_types = customisation_data.all()[0]['training_types']
        _distance_training = customisation_data.all()[0]['distance_training']
        _sets_training = customisation_data.all()[0]['sets_training']
        if len(disciplines[0]) > 0:
            for a in disciplines[0]:
                _training_types.insert(-1, a)
                value_type = input_validation('custom_disciplines.value_type', a)
                if value_type == 1:
                    _distance_training.append(a)
                elif value_type == 2:
                    _sets_training.append(a)
                elif value_type != 3:
                    print('\n' + 'There was a problem validating your input.' + '\n' + 'Please make sure you did not change any keywords for input identification.' + '\n' + 'If the problem persist, please contact the dev.')                
            customisation_data.update({'training_types': _training_types})            
            print('\n' + 'Successfully added discipline(s).')
        if len(disciplines[1]) > 0:
            for a in disciplines[1]:
                _training_types.remove(a)
                if a in _distance_training:
                    _distance_training.remove(a)
                elif a in _sets_training:
                    _sets_training.remove(a)
            customisation_data.update({'training_types': _training_types})
            print('\n' + 'Successfully removed discipline(s).')
        customisation_data.update({'distance_training': _distance_training})
        customisation_data.update({'sets_training': _sets_training}) 
    print(space_filler)


def quit_app():
    print(space_filler)
    print('\n' + 'Bye! See you next time and take care.' + '\n')
    sys.exit()


dialogue()