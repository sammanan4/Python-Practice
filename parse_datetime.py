from sys import exc_info
import dateutil.parser
from datetime import datetime
import itertools
from settings import StreamKeys
from scripts.logger import create_logger
import re

LOG = create_logger()

class AnalyseDate:

    @classmethod
    def get_min_and_max_date(cls, first_rows: list, last_rows: list):
        try:
            first_rows = list(first_rows)
            last_rows = list(last_rows)
            min_date = dateutil.parser.parse(first_rows[0], fuzzy=False)
            max_date = dateutil.parser.parse(first_rows[0], fuzzy=False)
            formats = []
            for date_as_str in first_rows:
                try:
                    date_as_datetime = dateutil.parser.parse(date_as_str, fuzzy=False)
                    formats.append(cls.get_date_format(date_as_str))
                    if date_as_datetime < min_date:
                        min_date = date_as_datetime
                    elif date_as_datetime > max_date:
                        max_date = date_as_datetime
                except Exception as e:
                    continue

            for date_as_str in last_rows:
                try:
                    date_as_datetime = dateutil.parser.parse(date_as_str, fuzzy=False)
                    formats.append(cls.get_date_format(date_as_str))
                    if date_as_datetime < min_date:
                        min_date = date_as_datetime
                    elif date_as_datetime > max_date:
                        max_date = date_as_datetime
                except Exception as e:
                    continue

            min_date_dict = {
                "day": min_date.day,
                "month": min_date.month, 
                "year": min_date.year,
                "hour": min_date.hour,
                "minute": min_date.minute,
                "second": min_date.second
            }
            max_date_dict = {
                "day": max_date.day,
                "month": max_date.month, 
                "year": max_date.year,
                "hour": max_date.hour,
                "minute": max_date.minute,
                "second": max_date.second
            }
            filled_sets = [s for s in formats if s]
            first_set = filled_sets[0]
            for i in range(1, len(filled_sets)):
                intersection = first_set.intersection(filled_sets[i])
                if intersection:
                    first_set = intersection

            return min_date_dict, max_date_dict, first_set.pop()
        except Exception as e:
            LOG.debug('error occurred while getting min and max date', exc_info=True)
            return None, None, None


    # Checks if column is a date field
    @classmethod
    def check_date(cls, col):
        try:
            for item in col:
                dateutil.parser.parse(item, fuzzy=False)

            return True
        except Exception as e:
            return False

    @classmethod
    def get_date_format(cls, date_str) -> set: 
        FORMAT_CODES = (
            r'%a', r'%A', r'%w', r'%d', r'%b', r'%B', r'%m', r'%y', r'%Y',
            r'%H', r'%I', r'%p', r'%M', r'%S', r'%f', r'%z', r'%Z', r'%j',
            r'%U', r'%W',
        )

        TWO_LETTERS_FORMATS = (
            r'%p',
        )

        THREE_LETTERS_FORMATS = (
            r'%a', r'%b'
        )

        LONG_LETTERS_FORMATS = (
            r'%A', r'%B', r'%z', r'%Z',
        )

        SINGLE_DIGITS_FORMATS = (
            r'w',
        )

        TWO_DIGITS_FORMATS = (
            r'%d', r'%m', r'%y', r'%H', r'%I', r'%M', r'%S', r'%U', r'%W',
        )

        THREE_DIGITS_FORMATS = (
            r'%j',
        )

        FOUR_DIGITS_FORMATS = (
            r'%Y',
        )

        LONG_DIGITS_FORMATS = (
            r'%f',
        )

        # Non format code symbols
        SYMBOLS = (
            '\\/',
            '\\-',
            ':',
            '+',
            'Z',
            ',',
            ' ',
        )

        date_str = date_str.upper()

        # Split with non format code symbols
        pattern = r'[^{}]+'.format(''.join(SYMBOLS))

        components = re.findall(pattern, date_str)

        # Create a format placeholder, eg. '{}-{}-{} {}:{}:{}+{}'
        placeholder = re.sub(pattern, '{}', date_str)

        formats = []
        for comp in components:
            if re.match(r'^\d{1}$', comp):
                formats.append(SINGLE_DIGITS_FORMATS)
            elif re.match(r'^\d{2}$', comp):
                formats.append(TWO_DIGITS_FORMATS)
            elif re.match(r'^\d{3}$', comp):
                formats.append(THREE_DIGITS_FORMATS)
            elif re.match(r'^\d{4}$', comp):
                formats.append(FOUR_DIGITS_FORMATS)
            elif re.match(r'^\d{5,}$', comp):
                formats.append(LONG_DIGITS_FORMATS)
            elif re.match(r'^[a-zA-Z]{2}$', comp):
                formats.append(TWO_LETTERS_FORMATS)
            elif re.match(r'^[a-zA-Z]{3}$', comp):
                formats.append(THREE_LETTERS_FORMATS)
            elif re.match(r'^[a-zA-Z]{4,}$', comp):
                formats.append(LONG_LETTERS_FORMATS)
            else:
                formats.append(FORMAT_CODES)

        # Create a possible format set
        possible_set = itertools.product(*formats)

        result_set = set()
        for possible_format in possible_set:
            # Create a format with possible format combination
            dt_format = placeholder.format(*possible_format)
            try:
                dt = datetime.strptime(date_str, dt_format)
                # Use the format to parse the date, and format the 
                # date back to string and compare with the origin one
                if dt.strftime(dt_format).upper() == date_str:
                    result_set.add(dt_format)
            except Exception:
                continue

        return result_set



    @classmethod
    def analyse(cls, first_rows, last_rows, col_name, **kwargs):
        LOG.debug('<FUNCTION START> AnalyseDate.analyse')

        if cls.check_date(first_rows):
            min_date, max_date, fmt = cls.get_min_and_max_date(first_rows, last_rows)


            LOG.debug(f"{col_name} found to be of type date")
            return {
                StreamKeys.SCHEMA__SOURCE.value: 'Numbers.date_time',
                StreamKeys.SCHEMA__ARGS.value: {
                    'start': min_date,
                    'end': max_date,
                    'format': fmt,
                    'example': first_rows[0]
                }
            }
        
        try:
            if re.match(r'.*(date|date[ \.\-_\/]time|time).*', col_name, re.IGNORECASE):
                LOG.debug(f'{col_name} matched Numbers.date_time')
                return {
                    StreamKeys.SCHEMA__SOURCE.value: 'Numbers.date_time',
                    StreamKeys.SCHEMA__ARGS.value: {
                        'example': first_rows[0]
                    }
                }
        except Exception as e:
            pass

        return None
