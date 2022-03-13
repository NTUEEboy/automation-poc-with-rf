from library.TestRailReporter import TestRailReporter


def Add_Result_to_Testrun(test_run_id: str, test_case_id: str, status: str, comment: str) -> None:
    TestRailReporter().add_result_for_case(
        test_run_id, test_case_id, status, comment)


def Convert_Time_Format_to_Testrail_style(the_time: str) -> None:
    list_time = the_time.split()[:-1]
    if not list_time:  # under 1 sec.
        return '1s'
    else:
        output_list = []
        for _time in list_time:
            if _time[-1] == 'n':  # min
                output_list.append(_time[:-2])
            else:
                output_list.append(_time)
        return ' '.join(output_list)
