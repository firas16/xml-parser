from main.xmlParser import parse_managers_from_path
from pandas._testing import assert_frame_equal
import pandas as pd
from test.utils import assert_frame_not_equal

def test_parseManagers():

    #Given
    path = './resources/thematics_morningstar.xml'
    expected_managers = pd.DataFrame({
        'ManagerStartDate': ['2018-12-20', '2018-12-20', '2020-08-31'],
        'IsFundManager': [True, True, True],
        'Status': ['1', '1', '1'],
        'GivenName': ['Karen', 'Nolan', 'Alexandre'],
        'FamilyName': ['Kharmandarian', 'Hoffmeyer', 'Zilliox']
    })
    not_expected_managers = pd.DataFrame({
        'ManagerStartDate': ['2018-12-21', '2018-12-20', '2020-08-31'],
        'IsFundManager': [True, True, True],
        'Status': ['1', '1', '1'],
        'GivenName': ['Karen', 'Nolan', 'Alexandre'],
        'FamilyName': ['Kharmandarian', 'Hoffmeyer', 'Zilliox']
    })

    #When
    result = parse_managers_from_path(path)

    #Then
    assert_frame_equal(result, expected_managers)
    assert_frame_not_equal(result, not_expected_managers)