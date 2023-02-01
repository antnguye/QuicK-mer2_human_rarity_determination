import qm2-human-rarity


def test_find_dups():
    test_array = np.array([1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 2, 1])
    test_answer = [[[3, 2], [4, 3], [5, 4], [6, 5]]]
    dup_windows = qm2_human_rarity.find_dups(test_array)
    assert test_answer == dup_windows, "The correct test array is "
