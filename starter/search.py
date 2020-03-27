import datetime
import operator as op

from collections import namedtuple
from enum import Enum

from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        # TODO: What instance variables will be useful for storing on the Query object?
        self.output_format = kwargs.get('output')
        self.return_object = kwargs.get('return_object')
        self.date = kwargs.get('date')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.number = kwargs.get('number')
        self.filter = kwargs.get('filter')

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """

        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        if(self.date is not None):
            date_search = Query.DateSearch(type = 'single_date', values = self.date)
        else:
            date_search = Query.DateSearch(type = 'interval', values = [self.start_date, self.end_date])

        Selector = Query.Selectors(date_search = date_search, number = self.number, filters = self.filter, return_object = None)
        return Selector


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        'diameter': 'diameter_min_km',
        'distance': 'miss_distance_kilometers',
        'is_hazardous': 'is_potentially_hazardous_asteroid'
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
        '=': op.eq,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param field:  str representing object to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    def __repr__(self):
        return(f'field: {self.field} \nobject: {self.object} \noperation: {self.operation} \nvalue: {self.value}')


    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """
        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        defaultdict = {'NEO': [], 'Path': []}
        for filter_option in filter_options:
            elements = filter_option.split(':')
            field = elements[0]
            operation = elements[1]
            value = elements[2]

            if(field == 'distance'):
                defaultdict['Path'].append(Filter(field, 'Orbit', operation, value))
            else:
                defaultdict['NEO'].append(Filter(field, 'NEO', operation, value))

        return defaultdict


    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results
        filtered_results = []
        if(self.field == 'is_hazardous'):
            # Casting for the value in the filter
            if(self.value == 'True'):
                casted_value = True
            else:
                casted_value = False
        else:
            casted_value = float(self.value)

        neo_property = Filter.Options[self.field]
        for result in results:
            if(Filter.Operators[self.operation](getattr(result, neo_property), casted_value)): 
                filtered_results.append(result)
            

        return filtered_results


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?
        self.NEOs = db.NEOs
        self.date_to_NEOs = db.date_to_NEOs

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
        date_search = query.date_search
        number = query.number
        filters = query.filters
        return_object = query.return_object
        results = self.simple_search(date_search)


        if filters != None:
            filters_dict = Filter.create_filter_options(filters)
            for i in range(len(filters_dict['NEO'])):
                results = filters_dict['NEO'][i].apply(results)

            for j in range(len(filters_dict['Path'])):
                results = filters_dict['Path'][j].apply(results)


        # Last step is to cut by number
        results = self.cut_by_number(results, number)
    
        return results

        
    def simple_search(self, date_search):
        # If only a sinlge date search is required
        results = []
        if(date_search.type == 'single_date'):
            for i in range(len(self.date_to_NEOs[date_search.values])):
            
                NEO_name = self.date_to_NEOs[date_search.values][i].name
                if(NEO_name in self.NEOs.keys()):
                    # To make sure only unique NEOs are printed
                    results.append(self.NEOs[NEO_name])
                    self.NEOs.pop(NEO_name, None)
                    

        else:
            start_date = datetime.datetime.strptime(date_search.values[0], '%Y-%m-%d')  
            end_date = datetime.datetime.strptime(date_search.values[1], '%Y-%m-%d')  
            step = datetime.timedelta(days=1)

            while(start_date <= end_date):
                temp_date = start_date.date()
                tmp_date_str = temp_date.strftime('%Y-%m-%d')
                start_date += step 
                for i in range(len(self.date_to_NEOs[tmp_date_str])):
                    NEO_name = self.date_to_NEOs[tmp_date_str][i].name

                    if(NEO_name in self.NEOs.keys()):
                        # To make sure only unique NEOs are printed
                        results.append(self.NEOs[NEO_name])
                        self.NEOs.pop(NEO_name, None)
                        

        return results


    def cut_by_number(self, results, number):
        if(len(results) > number):
            # To make sure that the results won't be larger than the required number
            results =  results[:number]
        else:
            pass

        return results
