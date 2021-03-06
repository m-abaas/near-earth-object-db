from enum import Enum
import csv


class OutputFormat(Enum):
    """
    Enum representing supported output formatting options for search results.
    """
    display = 'display'
    csv_file = 'csv_file'

    @staticmethod
    def list():
        """
        :return: list of string representations of OutputFormat enums
        """
        return list(map(lambda output: output.value, OutputFormat))


class NEOWriter(object):
    """
    Python object use to write the results from
    supported output formatting options.
    """

    def __init__(self):
        # TODO: How can we use the OutputFormat in the NEOWriter?
        pass

    def write(self, format, data, **kwargs):
        """
        Generic write interface that, depending
        on the OutputFormat selected calls the
        appropriate instance write function

        :param format: str representing the OutputFormat
        :param data: collection of NearEarthObject or OrbitPath results
        :param kwargs: Additional attributes used for formatting
        output e.g. filename
        :return: bool representing if write successful or not
        """
        # TODO: Using the OutputFormat, how can we organize
        # our 'write' logic for output to stdout vs to csvfile
        # TODO: into instance methods for NEOWriter? Write instance
        # methods that write() can call to do the necessary
        # TODO: output format.
        if format == OutputFormat.display.value:
            self.display(data)
        else:
            self.write_to_csv(data)

        return True

    @classmethod
    def display(self, data):
        if(len(data) == 0):
            print("No results found, try different search.")
        else:
            self.nice_print()
            print(f'Found {len(data)} results for the given search criteria')
            self.nice_print()
            for i in range(len(data)):
                print(f'The NEO number #{i}')
                self.nice_print()
                print(data[i])
                self.nice_print()

    @classmethod
    def nice_print(self):
        print('='*50)

    @classmethod
    def write_to_csv(self, data):
        if(len(data) == 0):
            print("No results found, try different search.")
        else:
            self.nice_print()
            print("Results can be found at results.csv file.")
            self.nice_print()
            with open('./results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["NEO_id", "NEO_name",
                                 "miss_distance", "orbit_date"])
                for i in range(len(data)):
                    for j in range(len(data[i].orbits)):
                        writer.writerow([data[i].id, data[i].name,
                                         data[i].orbits[j].miss_distance_kilometers,
                                         data[i].orbits[j].close_approach_date])

            file.close()
