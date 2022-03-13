from library.SlackReporter import SlackReporter
from library.ConfigLoader import ConfigLoader
from library.common import Add_Result_to_Testrun

import xml.etree.ElementTree as ET
import os
import socket


def main():
    # Extract result from ouput XML
    tree = ET.parse('output.xml')
    root = tree.getroot()

    # Get passed cases and failed cases from the XML
    pass_num = root.findall('./statistics//total//stat')[1].attrib['pass']
    fail_num = root.findall('./statistics//total//stat')[1].attrib['fail']

    # Get error msg if the case is failed
    msg = ''
    status_msg = 'PASS'
    status = root.findall('./suite//test//status')
    if (fail_num != '0'):
        msg = 'error msg: '
        for i in range(len(status)):
            if (status[i].attrib['status'] == 'FAIL' and status[i].text != None):
                msg += status[i].text + ' '
                status_msg = 'FAIL'

    config = ConfigLoader(os.path.dirname(__file__) +
                          "\\config", "global").config

    # Get machine name
    machine = socket.gethostname()

    # Add the result to Testrail
    Add_Result_to_Testrun(config['testrail']['run_id'],
                          config[machine]['case_id'],
                          status_msg, msg)

    # Send result to the Slack channel
    instance = SlackReporter(
        config['slack']['bot_key'],
        config['slack']['channel_id'])

    instance.get_body(pass_num,
                      fail_num,
                      machine,
                      "https://nzxt.testrail.io/index.php?/runs/view/" + config['testrail']['run_id'])

    instance.post_msg()


if __name__ == "__main__":
    main()
