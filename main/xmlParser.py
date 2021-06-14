
import xml.etree.ElementTree as ET
import pandas as pd

def parse_managers_from_path(path):
    """
    extracts list of managers from xml file containing fund data
    :param path: string path for XML file
    :return: dataframe of managers
    """
    fundElements = ET.parse(path)
    myroot = fundElements.getroot()
    columns = ['ManagerStartDate', 'IsFundManager', 'Status', 'GivenName', 'FamilyName']
    managersList = []
    managersDetails = myroot.find('Fund').find('FundManagement').find('ManagerList').findall('ManagerDetail')
    for manager in managersDetails:
        start_date = manager.find('StartDate').text
        professional_information =  manager.find('ProfessionalInformation')
        status = professional_information.get('_Status')

        IsFundManager = professional_information.get('_IsFundManager')
        is_fund_manager = IsFundManager == "true" or is_fund_manager == "True"
        personel_infomation = professional_information.find('PersonalInformation')
        given_name = personel_infomation.find('GivenName').text
        family_name = personel_infomation.find('FamilyName').text
        managersList.append([start_date, is_fund_manager, status, given_name, family_name])

    managers = pd.DataFrame(managersList, columns = columns)
    return  managers

def parse_managers_from_root(myroot):
    """
    extracts list of managers from ElementTree data
    :param path: string path for XML file
    :return: dataframe of managers
    """

    columns = ['ManagerStartDate', 'IsFundManager', 'Status', 'GivenName', 'FamilyName']
    managersList = []
    managersDetails = myroot.find('Fund').find('FundManagement').find('ManagerList').findall('ManagerDetail')
    for manager in managersDetails:
        start_date = manager.find('StartDate').text
        professional_information =  manager.find('ProfessionalInformation')
        status = professional_information.get('_Status')

        IsFundManager = professional_information.get('_IsFundManager')
        is_fund_manager = IsFundManager == "true" or is_fund_manager == "True"
        personel_infomation = professional_information.find('PersonalInformation')
        given_name = personel_infomation.find('GivenName').text
        family_name = personel_infomation.find('FamilyName').text
        managersList.append([start_date, is_fund_manager, status, given_name, family_name])

    managers = pd.DataFrame(managersList, columns = columns)
    return  managers

def parse_managers_iter(path):
    """
    extracts list of managers from xml file containing fund data using iterparse
    NB: more optimzed for heavy files
    :param path: string path for XML file
    :return: dataframe of managers
    """
    columns = ['ManagerStartDate', 'IsFundManager', 'Status', 'GivenName', 'FamilyName']
    managersList = []

    # get an iterable
    context = ET.iterparse(path, events=("start", "end"))
    # turn it into an iterator
    event, root = next(context)

    for event, elem in context:
        if event == "end" and elem.tag == "ManagerList":
            for managerDetail in elem.findall('ManagerDetail'):
                start_date = managerDetail.find('StartDate').text
                professional_information = managerDetail.find('ProfessionalInformation')
                status = professional_information.get('_Status')

                is_fund_manager = professional_information.get('_IsFundManager')
                personel_infomation = professional_information.find('PersonalInformation')
                given_name = personel_infomation.find('GivenName').text
                family_name = personel_infomation.find('FamilyName').text
                managersList.append([start_date, is_fund_manager, status, given_name, family_name])
                elem.clear()
                root.clear()
    managers = pd.DataFrame(managersList, columns=columns)
    return managers

def parse_performance(path):
    """

    :param path: string path for XML file
    :return: dataframe of fund performances over years
    """
    fundElements = ET.parse(path)
    myroot = fundElements.getroot()
    perfList = []
    historical_performance = myroot\
        .find('ClassPerformance')\
        .find('Performance')\
        .find('HistoricalPerformance')
    for yearly_perf in historical_performance.iter('HistoricalPerformanceDetail'):
        for return_history in yearly_perf.iter('ReturnHistory'):
            for returnElem in return_history.iter('Return'):
                returnType = returnElem.get('Type')
                if(returnType == "1"):
                    end_date = returnElem.find('EndDate').text
                    return_detail = returnElem.find('ReturnDetail')
                    time_period = return_detail.get('TimePeriod')
                    value = float(return_detail.find('Value').text)
                    if(time_period == "M1"):
                        perfList.append([end_date, value, time_period, returnType])


    performances = pd.DataFrame(perfList, columns = ['EndDate', 'Value', 'TimePeriod', 'PerformanceType']).sort_values(by=['EndDate'])
    performances["perf"] = performances["Value"]/100 + 1
    performances["perf"] = performances["perf"].cumprod()

    return performances

def parse_managers_and_performance(path):
    """

    :param path: string path for XML file
    :return: (performnces, managers) returns list of two datafarmes containing performances and managers
    """
    #parse XML
    fundElements = ET.parse(path)
    myroot = fundElements.getroot()

    # extract Managers
    columns = ['ManagerStartDate', 'IsFundManager', 'Status', 'GivenName', 'FamilyName']
    managersList = []
    managersDetails = myroot.find('Fund').find('FundManagement').find('ManagerList').findall('ManagerDetail')
    for manager in managersDetails:
        start_date = manager.find('StartDate').text
        professional_information = manager.find('ProfessionalInformation')
        status = professional_information.get('_Status')

        is_fund_manager = professional_information.get('_IsFundManager')
        personel_infomation = professional_information.find('PersonalInformation')
        given_name = personel_infomation.find('GivenName').text
        family_name = personel_infomation.find('FamilyName').text
        managersList.append([start_date, is_fund_manager, status, given_name, family_name])
    managers = pd.DataFrame(managersList, columns=columns)

    #extract & compute performance
    perfList = []
    historical_performance = myroot \
        .find('ClassPerformance') \
        .find('Performance') \
        .find('HistoricalPerformance')
    for yearly_perf in historical_performance.iter('HistoricalPerformanceDetail'):
        for return_history in yearly_perf.iter('ReturnHistory'):
            for returnElem in return_history.iter('Return'):
                returnType = returnElem.get('Type')
                if (returnType == "1"):
                    end_date = returnElem.find('EndDate').text
                    return_detail = returnElem.find('ReturnDetail')
                    time_period = return_detail.get('TimePeriod')
                    value = float(return_detail.find('Value').text)
                    if (time_period == "M1"):
                        perfList.append([end_date, value, time_period, returnType])

    performances = pd.DataFrame(perfList, columns=['EndDate', 'Value', 'TimePeriod', 'PerformanceType']).sort_values(
        by=['EndDate'])
    performances["perf"] = performances["Value"] / 100 + 1
    performances["perf"] = performances["perf"].cumprod()

    return (performances, managers)

