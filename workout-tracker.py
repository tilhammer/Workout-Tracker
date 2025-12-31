from tinydb import TinyDB, Query
import uuid
from datetime import datetime


db = TinyDB('data/training_db.json')


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


def add_training(
    date,
    training_type,
    duration_min,
    difficulty,
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
    'volume': {
        'type': volume_type,
        'value': volume_value
    },
    'notes': notes
    }
    db.insert(entry)


def quit_app():
    print('\n' + 'Bye! See you next time and take care.' + '\n')
    quit()


def input_validation(input_type):
    arg = None
    while arg == None:
        if input_type == 'dialogue.action':
            print('What would you like to run?' + '\n' + '[1] Track workout' + '\n' + '[2] Show statistics' + '\n' + '[3] / [Q] Quit' + '\n')
            _arg = input('Action' + ': ')
            if _arg == 'Quit':
                quit_app()
            if _arg == 'Quit':
                quit_app()
            if _arg in [str(1), str(2), str(3), 'Q']:
                arg = _arg        
            else:
                print('Invalid choice!')
        elif input_type == 'Date':
            print('\n' + 'Enter the date in question in the format YYYY-MM-DD or leave empty to choose the current date, then press Enter.')
            _arg = input(input_type + ': ')
            if _arg == 'Quit':
                quit_app()
            if _arg == '':
                arg = datetime.today().strftime('%Y-%m-%d')
            else:
                try:
                    datetime.strptime(_arg, '%Y-%m-%d')
                    arg = _arg
                except ValueError:
                    print('Invalid choice!')
        elif input_type == 'Type of training':
            print('\n' + 'Choose the training type:' + '\n' + '[1] Jogging' + '\n' + '[2] Taekwondo' + '\n' + '[3] Bicycle' + '\n' + '[4] Push' + '\n' + '[5] Pull' + '\n' + '[6] Legs' + '\n' + '[7] Core' + '\n' + '[8] Other')
            _arg = input(input_type + ': ')
            if _arg == 'Quit':
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a <= 8:
                    arg = ['Jogging', 'Taekwondo', 'Bicycle', 'Push', 'Pull', 'Legs', 'Core', 'Other'][_a - 1]
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')
        elif input_type == 'Duration of training':
            print('\n' + 'Enter the training duration in minutes.')
            _arg = input(input_type + ': ')
            if _arg == 'Quit':
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')
        elif input_type == 'Perceived difficulty':
            print('\n' + 'Enter your perceived difficulty of the training on a scale from 1 to 10 (1 = Easy, 10 = Hard).')
            _arg = input(input_type + ': ')
            if _arg == 'Quit':
                quit_app()
            try:
                _a = float(_arg)
                if 1 <= _a <= 10:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')
        elif input_type == 'Distance':
            print('\n' + 'Enter the distance travelled in km.')
            _arg = input(input_type + ': ')
            if _arg == 'Quit':
                quit_app()
            try:
                _a = float(_arg)
                if 1 <= _a:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')
        elif input_type == 'Sets':
            print('\n' + 'Enter enter the number of completed sets.')
            _arg = input(input_type + ': ')
            if _arg == 'Quit':
                quit_app()
            try:
                _a = int(_arg)
                if 1 <= _a:
                    arg = _a
                else:
                    print('Invalid choice!')
            except ValueError:
                print('Invalid choice!')  
        elif input_type == 'Notes':
            print('\n' + 'Optionally enter notes now.')
            _arg = input(input_type + ': ')
            if _arg == 'Quit':
                quit_app()
            arg = _arg
        else:
            print('\n' + 'There was a problem validating your input.' + '\n' + 'Please make sure you did not change any keywords for input identification.' + '\n' + 'If the problem persist, please contact the dev.')        
    return arg
     

def dialogue():
    print('\n' + 'Welcome! To quit, you can always type "Quit" or press CTL + C.' + '\n')
    choice = input_validation('dialogue.action')
    if choice == '1':
        track_workout()
    elif choice == '2':
        analyse_workouts()
    elif choice in ['3', 'Q']:
        quit_app()
    else:
        print('\n' + 'There was a problem validating your input.' + '\n' + 'Please make sure you did not change any keywords for input identification.' + '\n' + 'If the problem persist, please contact the dev.')        
    

def track_workout():
    print('\n' + 'Please enter some information about your workout.')
    date = input_validation('Date')
    training_type = input_validation('Type of training')
    duration_min = input_validation('Duration of training')
    difficulty = input_validation('Perceived difficulty')
    volume_type = 'distance' if training_type in ['Jogging', 'Bicycle'] else 'sets' if training_type in ['Push', 'Pull', 'Legs', 'Core'] else None
    volume_value = input_validation('Distance') if volume_type == 'distance' else input_validation('Sets') if volume_type == 'sets' else None
    notes = input_validation('Notes')
    add_training(date=date, training_type=training_type, duration_min=duration_min, difficulty=difficulty, volume_type=volume_type, volume_value=volume_value, notes=notes)


dialogue()