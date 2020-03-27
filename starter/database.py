from models import OrbitPath, NearEarthObject
import csv


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        self.filename = filename
        self.date_to_NEOs = {}
        self.NEOs = {}

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """
        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # TODO: Load data from csv file.
        # TODO: Where will the data be stored?
        with open(filename) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # List version of the row
                attributes_list = list(row.items())
                # Dict version of the row
                attributes_dict = dict(attributes_list)
                NEO = NearEarthObject(**attributes_dict)
                orbit = OrbitPath(**attributes_dict)
                NEO.update_orbits(orbit)
                # Getting the close approach date of this orbit
                orbit_date = orbit.close_approach_date
                if self.date_to_NEOs.get(orbit_date) is None:
                    self.date_to_NEOs[f'{orbit_date}'] = [NEO]
                else:
                    self.date_to_NEOs[f'{orbit_date}'].append(NEO)

                # Making sure only unique objects are contained 
                if self.NEOs.get(NEO.name) is None:
                    self.NEOs[NEO.name] = NEO
                else:
                    pass

        return None
