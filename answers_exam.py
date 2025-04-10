from SearchAlgorithm import *
from SubwayMap import *
from utils import *

if __name__=="__main__":
    ROOT_FOLDER = './CityInformation/Barcelona_City/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)



    ### BELOW HERE YOU CAN CALL ANY FUNCTION THAT yoU HAVE PROGRAMED TO ANSWER THE QUESTIONS OF THE EXAM ###
    ### this code is just for you, you won't have to upload it after the exam ###


    #this is an example of how to call some of the functions that you have programed
    example_path=breadth_first_search(5, 8, map)
    print_list_of_path_with_cost([example_path])

    cost=calculate_cost([Path([5, 4]), Path([4, 3]), Path([3, 2]), Path([2, 1]), Path([1, 7]), Path([7, 8])], map, 2)
    print(cost)
    