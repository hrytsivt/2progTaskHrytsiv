import folium
from geopy.geocoders import ArcGIS


def readingFromFile(enteredFile):
    """
    (file) -> list
    Returns list of lists. Every inside list contains an information about
    every line in the file. -1 item is the location.
    """
    myFile = open(enteredFile, 'r')
    myFile = myFile.readlines()
    myFile = [i.strip().split('\t') for i in myFile]

    return myFile


def readingAllFilms(year, file):
    """
    (int) -> list
    Takes a year as the parameter and returns list of locations, where
    films were filmed in that year
    """
    year = '(' + str(year) + ')'
    fileWithFilms = readingFromFile(file)
    listOfLocations = []

    for i in fileWithFilms:
        if year in i[0]:
            listOfLocations.append(i[-1])

    return listOfLocations


def namesOfFilms(year):
    """
    (int) -> list
    Takes a year as the parameter and returns list of all names of the films,
    which were filmed in that year
    """
    temporaryList = []
    notJoinedList = []
    finalNamesList = []
    listOfNamesWithYear = []
    year = '(' + str(year) + ')'
    fileWithFilms = readingFromFile("locations.list")

    for i in fileWithFilms:
        if year in i[0]:
            listOfNamesWithYear.append(i[0])

    for i in listOfNamesWithYear:
        temporaryList.append(list(i))

    for i in temporaryList:
        for j in i:
            if j == "(":
                notJoinedList.append(i[0:(i.index(j) - 1)])

    for i in notJoinedList:
        c = ''.join(i)
        finalNamesList.append(c)

    return finalNamesList


def gettingCoordinates(listOfLocations):
    """
    (list) -> list
    Takes the list of locations as the parameter and returns list of all
    coordinates of these parameters
    """
    geolocator = ArcGIS()
    listOfCoordinates = []

    for i in listOfLocations:
        try:
            location = geolocator.geocode(i)
            locations = [location.latitude, location.longitude]
            listOfCoordinates.append(locations)
        except:
            pass

    return listOfCoordinates


def creatingMap():
    """
    (None) -> map
    Creates and returns the map
    """
    maps = folium.Map()

    return maps


def mainFunction(year, fileWithLoc):
    """
    (int) -> None
    Takes a year as the parameter. Calls out previous functions to mark
    on the map places where films were filmed in the given year. Shows the
    population amount from the lightest colour to the darkest.Shows the
    amount of films, filmed in the given year, from the lightest colour to
    the darkest.
    """
    myMap = creatingMap()
    listOfCoordinates = gettingCoordinates(readingAllFilms(year, fileWithLoc))

    groupFilms = folium.FeatureGroup(name='Films')
    for i in listOfCoordinates:
        groupFilms.add_child(folium.Marker(location=i,
                                           icon=folium.Icon(color='black')))

    groupPopulation = folium.FeatureGroup(name="Population")
    groupPopulation.add_child(folium.GeoJson(data=open('world.json', 'r',
                                             encoding='utf-8-sig').read(),
        style_function=lambda x: {'fillColor': 'white'
        if x['properties']['POP2005'] < 10000000
        else '#ffff99' if 10000000 <= x['properties']['POP2005'] < 50000000
        else '#600080' if 50000000 <= x['properties']['POP2005'] < 100000000
        else 'black'}))

    groupFilmsAmount = folium.FeatureGroup(name="Films Amount")
    groupFilmsAmount.add_child(folium.GeoJson(data=open('world.json', 'r',
                                              encoding='utf-8-sig').read(),
        style_function=lambda x: {'fillColor': 'white'
        if len(x['geometry']['coordinates']) < 10
        else '#4dffdb' if 10 <= len(x['geometry']['coordinates']) < 125
        else '#1a001a' if 125 <= len(x['geometry']['coordinates']) < 400
        else '#ff3333'}))

    myMap.add_child(groupFilmsAmount)
    myMap.add_child(groupPopulation)
    myMap.add_child(groupFilms)
    myMap.add_child(folium.LayerControl())
    myMap.save("map.html")


mainFunction(1895, "locations.list")
