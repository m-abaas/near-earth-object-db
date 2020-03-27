class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?

        self.orbits = []
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.string_hazard = kwargs.get('is_potentially_hazardous_asteroid')
        if(self.string_hazard == 'True'):
            self.is_potentially_hazardous_asteroid = True
        else:
            self.is_potentially_hazardous_asteroid = False
        self.diameter_min_km = float(kwargs.get('estimated_diameter_min_kilometers'))
        self.miss_distance_kilometers = float(kwargs.get('miss_distance_kilometers'))

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        # TODO: How do we connect orbits back to the Near Earth Object?
        self.orbits.append(orbit)

    def __repr__(self):
        return(f'id: {self.id} \nname: {self.name} \norbits: {self.orbits}')

class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        # TODO: What instance variables will be useful for storing on the Near Earth Object?
        self.neo_name = kwargs.get('name')
        self.close_approach_date = kwargs.get('close_approach_date')
        self.miss_distance_kilometers = float(kwargs.get('miss_distance_kilometers'))

    def __repr__(self):
        return(f'neo_name: {self.neo_name} \n'\
        f'close_approach_date: {self.close_approach_date} \n'\
        f'miss_distance_kilometers: {self.miss_distance_kilometers}')
