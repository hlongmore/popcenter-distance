from uszipcode import SearchEngine


def get_search_engine(simple=True):
    useless_enum = SearchEngine.SimpleOrComprehensiveArgEnum
    simple = useless_enum.simple if simple else useless_enum.comprehensive
    return SearchEngine(simple_or_comprehensive=simple)
