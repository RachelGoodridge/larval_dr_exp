from module import find_small, sort_worm


def test_find_small():
    """ Tests find_small function """
    
    # first parameter : a list of four non-empty lists of floats
    # second parameter : an integer or a float
    # return : a float
    assert callable(find_small)
    assert isinstance(find_small([[7.6], [7.8], [7.9], [8.0]], 0.5), float)
    
    # the function should return the smallest number rounded down to the nearest value indicated
    assert find_small([[7.6], [7.8], [7.9], [8.0]], 0.5) == 7.5
    assert find_small([[7.9, 8.6], [7.8, 8.7], [7.4, 9.3], [8.0, 8.1]], 0.5) == 7.0
    assert find_small([[7.8], [7.6], [7.7, 7.7], [8.9]], 1) == 7.0

    
def test_sort_worm():
    """ Tests sort_worm function """
    
    # first parameter : an integer from the list [0, 1, 2, 3]
    # second parameter : list of lists, each containing two floats
    # third parameter : a list of four lists of floats
    # return : list of lists of the same length as the second parameter
    assert callable(sort_worm)
    test_bins = [[5.5, 8.5], [7.0, 10.0], [8.5, 11.5], [10.0, 13.0]]
    assert isinstance(sort_worm(0, test_bins, [[7.9, 8.6], [7.8, 8.7], [7.4, 9.3], [8.0, 8.1]]), list)
    
    # the first parameter indicates which list of the third parameter will be sorted
    # the values of that list will go into bins (the second parameter) if they fall between the lower and upper bound
    assert sort_worm(0, test_bins, [[7.9, 11.0], [7.8, 8.7], [7.4, 9.3], [8.0, 8.1]]) == [[7.9], [7.9], [11.0], [11.0]]
    test_bins = [[5.5, 8.5], [7.0, 10.0], [8.5, 11.5]]
    assert sort_worm(2, test_bins, [[7.9], [7.8, 18.4], [7.4, 9.3], []]) == [[7.4], [7.4, 9.3], [9.3]]
    assert sort_worm(2, test_bins, [[7.9, 11.0], [7.8, 8.7], [], [8.0]]) == [[], [], []]