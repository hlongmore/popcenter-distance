import datetime
import math
import os
from csv import DictReader
from glob import glob

import requests
from uszipcode import state_abbr

from popcenter.converters.zip import ZipSearch
from popcenter.coordinates import LatLongCoordinate


DATA_DIR = os.path.abspath(os.path.dirname(__file__))

class CensusDataDownloader:
    """
    Much of the functionality of this class is highly speculative as to how the
    US Census Bureau will name the files in the future. There is no data point
    for the 2000 census to confirm that there is a pattern (or, the 2000 census
    data does not follow the pattern, and ergo, there is no pattern).
    """
    # TODO: the 2000 census data files are named differently, e.g.
    #      http://www2.census.gov/geo/docs/reference/cenpop2000/statecenters.txt
    #      will the 2020 ones also be named differently?

    def __init__(self):
        self.year = None
        self.year_path = None
        self.local_file_name = None
        self.url = None
        self.host = 'www2.census.gov'
        self.reference_path = '/geo/docs/reference'
        self.saved_file = None
        # These two are split up so they can be callable
        self.year_setup()
        self.url_setup()

    def year_setup(self, earlier=False):
        self.year = int(10 * (math.floor(datetime.datetime.now().year / 10.0)))
        if earlier:
            self.year -= 10
        self.year_path = f'/cenpop{self.year}/CenPop{self.year}_Mean_ST.txt'
        self.local_file_name = f'Census_{self.year}_mean_pop_by_state.csv'

    def url_setup(self):
        self.url = f'https://{self.host}{self.reference_path}{self.year_path}'

    def download(self):
        def execute_download(url):
            try:
                result = requests.get(self.url)
                if result.status_code == requests.codes.ok:
                    self.saved_file = os.path.join(DATA_DIR, self.local_file_name)
                    with open(self.saved_file, 'w') as outfile:
                        outfile.write(result.text)
            except requests.RequestException as e:
                print(f'Unable to download: {e}')
                self.saved_file = None
                return requests.codes.server_error
            except (OSError, IOError) as e:
                print(f'Unable to save {self.url} to {self.saved_file}: {e}')
                self.saved_file = None
                raise
            else:
                return result.status_code
        code = execute_download(self.url)
        if code == requests.codes.not_found:
            self.year_setup(earlier=True)
            self.url_setup()
            execute_download(self.url)
        return self.saved_file and os.path.isfile(self.saved_file)


class StateSearch:
    data_dir = DATA_DIR

    def __init__(self):
        downloader = CensusDataDownloader()
        self.data_file = os.path.join(self.data_dir, downloader.local_file_name)
        if not os.path.isfile(self.data_file):
            # Try another year
            y = f'{downloader.year:#}'
            matches = glob(self.data_file.replace(y, '*'), recursive=False)
            if matches:
                self.data_file = max(matches, key=os.path.getmtime)
            else:
                if not downloader.download():
                    raise Exception(
                        'Unable to load census population center data.')
        self.data = {}
        self.read_data()

    def read_data(self):
        with open(self.data_file, 'r', newline=None) as data_file:
            reader = DictReader(data_file)
            for row in reader:
                state = state_abbr.MAPPER_STATE_ABBR_LONG_TO_SHORT[row['STNAME']]
                self.data[state] = {
                    'population': row['POPULATION'],
                    'latitude': row['LATITUDE'],
                    'longitude': row['LONGITUDE'],
                }

    def search(self, state):
        if len(state) > 2:
            state = state_abbr.MAPPER_STATE_ABBR_LONG_TO_SHORT.get(state.title(), state)
        if state not in state_abbr.MAPPER_STATE_ABBR_SHORT_TO_LONG:
            # Let the uszipcodes package guess at what the state is.
            zips = ZipSearch().engine.by_state(state)
            if zips:
                state = zips[0].state
            else:
                print(f'Unable to guess what state should be: {state}')
                raise ValueError(f'Unknown state: {state}')
        data = self.data[state.upper()]
        return LatLongCoordinate(data['latitude'], data['longitude'])

    def search_bulk(self, states):
        state_population_centers = []
        for state in states:
            state_population_centers.append(self.search(state))
        return state_population_centers
