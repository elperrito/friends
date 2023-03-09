"""Assignment 1: Friend of a Friend

Please complete these functions, to answer queries given a dataset of
friendship relations, that meet the specifications of the handout
and docstrings below.

Notes:
- you should create and test your own scenarios to fully test your functions, 
  including testing of "edge cases"
"""
import copy

from py_friends.friends import Friends

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""


def load_pairs(filename):
    """
    Args:
        filename (str): name of input file

    Returns:
        List of pairs, where each pair is a Tuple of two strings

    Notes:
    - Each non-empty line in the input file contains two strings, that
      are separated by one or more space characters.
    - You should remove whitespace characters, and skip over empty input lines.
    """
    list_of_pairs = []
    with open(filename, 'rt') as infile:

        # ------------ BEGIN YOUR CODE ------------

        for line_text in infile:
            single_pair = line_text.lstrip().rstrip()
            if len(single_pair) > 0 and not single_pair.isspace():
                first_character, second_character = single_pair.rstrip().lstrip().split()
                list_of_pairs.append((first_character, second_character))

    # ------------ END YOUR CODE ------------

    return list_of_pairs

def make_friends_directory(pairs):
    """Create a directory of persons, for looking up immediate friends

    Args:
        pairs (List[Tuple[str, str]]): list of pairs

    Returns:
        Dict[str, Set] where each key is a person, with value being the set of 
        related persons given in the input list of pairs

    Notes:
    - you should infer from the input that relationships are two-way: 
      if given a pair (x,y), then assume that y is a friend of x, and x is 
      a friend of y
    - no own-relationships: ignore pairs of the form (x, x)
    """
    directory = dict()

    for pair_friends in pairs:
        friend1 = pair_friends[0]
        friend2 = pair_friends[1]

        if friend1 == friend2:
            continue

        friends_tuples = [(friend1, friend2), (friend2, friend1)]

        for friend_tuple in friends_tuples:
            if friend_tuple[0] not in directory.keys():
                directory[friend_tuple[0]] = {friend_tuple[1]}
            if friend_tuple[1] not in directory[friend_tuple[0]]:
                directory[friend_tuple[0]].add(friend_tuple[1])

    return directory


def find_all_number_of_friends(my_dir):
    """List every person in the directory by the number of friends each has

    Returns a sorted (in decreasing order by number of friends) list 
    of 2-tuples, where each tuples has the person's name as the first element,
    the number of friends as the second element.
    """
    friends_list = []

    # ------------ BEGIN YOUR CODE ------------

    for person, friends in my_dir.items():
        person_friends = (person, len(friends))
        friends_list.append(person_friends)

    friends_list.sort(reverse=True, key=lambda x: x[1])
    # ------------ END YOUR CODE ------------

    return friends_list


def make_team_roster(person, my_dir):
    """Returns str encoding of a person's team of friends of friends
    Args:
        person (str): the team leader's name
        my_dir (Dict): dictionary of all relationships

    Returns:
        str of the form 'A_B_D_G' where the underscore '_' is the
        separator character, and the first substring is the 
        team leader's name, i.e. A.  Subsequent unique substrings are 
        friends of A or friends of friends of A, in ascii order
        and excluding the team leader's name (i.e. A only appears
        as the first substring)

    Notes:
    - Team is drawn from only within two circles of A -- friends of A, plus 
      their immediate friends only
    """
    assert person in my_dir
    label = person

    # ------------ BEGIN YOUR CODE ------------

    person_friends = set(my_dir[person])
    all_friends = person_friends
    for friend in person_friends:
        friends_of_friends = set(my_dir[friend])
        all_friends = all_friends.union(friends_of_friends)

    if person in all_friends:
        all_friends.remove(person)

    list_all_friends = sorted(all_friends)

    labels = ""
    for friend in list_all_friends:
        labels += "_" + friend

    label += labels

    # ------------ END YOUR CODE ------------

    return label


def find_smallest_team(my_dir):
    """Find team with smallest size, and return its roster label str
    - if ties, return the team roster label that is first in ascii order
    """
    smallest_teams = []

    teams = []
    for person in my_dir:
        team = str(make_team_roster(person, my_dir))
        team_size = team.count("_") + 1
        teams.append((team, team_size))

    teams.sort(key=lambda x: x[1])
    small_team_size = teams[0][1]

    for team in teams:
        if team[1] > small_team_size:
            break
        smallest_teams.append((team[0]))

    smallest_teams.sort()

    return smallest_teams[0] if smallest_teams else ""


if __name__ == '__main__':
    # To run and examine your function calls

    print('\n1. run load_pairs')
    my_pairs = load_pairs('myfrieds3.txt')
    print(my_pairs)

    print('\n2. run make_directory')
    my_dir = make_friends_directory(my_pairs)
    print(my_dir)

    print('\n3. run find_all_number_of_friends')
    print(find_all_number_of_friends(my_dir))

    print('\n4. run make_team_roster')
    #my_person = 'DARTHVADER'  # test with this person as team leader
    my_person = 'C'
    team_roster = make_team_roster(my_person, my_dir)
    print(team_roster)

    print('\n5. run find_smallest_team')
    print(find_smallest_team(my_dir))

    print('\n6. run Friends iterator')
    friends_iterator = Friends(my_dir)
    for num, pair in enumerate(friends_iterator):
        print(num, pair)
        if num == 1000:
            break
    print(len(list(friends_iterator)) + num)
