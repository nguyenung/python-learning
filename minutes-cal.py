import re

def get_input():
    """
    This function listen prompt from keyboard. Allow only format `minutes:seconds`
    :return: The input from keyboard
    """
    user_input = input('Enter a time in minutes:seconds format (or 'quit' to exit): ')
    if user_input.lower() == 'quit':
        raise SystemExit('Exit program...')
    if not re.match(r"\d+:\d{2}", user_input):
        raise ValueError('Input must be in minutes:seconds format')
    return user_input

def calculate_total_time(inputs):
    """
    This function listen prompt from keyboard. Allow only format `minutes:seconds`
    :param inputs: list string with format `minutes:seconds`
    :return: time in format `hours:minutes:seconds` or `minutes:seconds` if the time is less than 1 hour
    """
    total_seconds = 0
    for input_time in inputs:
        minutes, seconds = map(int, input_time.split(':'))
        total_seconds += minutes * 60 + seconds
    
    hours, remaining_seconds = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remaining_seconds, 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

"""
This program takes the input value from the keyboard in `minutes:seconds` format and sums the input values
"""
inputs = []
while True:
    try:
        user_input = get_input()
        inputs.append(user_input)
        total_time = calculate_total_time(inputs)
        print('>>> Total time: ', total_time)
    except ValueError as e:
        print('Error: ', str(e))
    except KeyboardInterrupt as e:
        raise SystemExit("\nExiting program...")
    