import requests


class SlackReporter:
    def __init__(self, slack_bot_key, channel_id):
        self._slack_bot_key = slack_bot_key
        self._channel_id = channel_id
        self._color = '#36a64f'
        self._body = {}
        self._header = {}

    def get_body(self, passed, failed, machine, url):
        button = 'primary'
        status = ':kirby: Pass'
        if (failed != '0'):
            self._color = '#E01E5A'
            button = 'danger'
            status = 'Fail'
        self._body = {
            "channel": self._channel_id,
            "attachments": [
                {
                    "callback_id": "sqa_test_report",
                    "text": f"Run the test on `{machine}`.",
                    "fields": [
                        {
                            "title": status,
                            "value": f"Passed: `{passed}` failed: `{failed}`"
                        }
                    ],
                    "color": self._color,
                    "author_name": "Github actions",
                    "author_link": "https://github.com/NZXTCorp/work-playground/actions",
                    "author_icon": "https://raw.githubusercontent.com/github/explore/2c7e603b797535e5ad8b4beb575ab3b7354666e1/topics/actions/actions.png",
                    "actions": [
                        {
                            "type": "button",
                            "text": "Testrail Report",
                            "url": f"{url}",
                            "style": button,
                        }
                    ],
                }
            ],
        }

    def post_msg(self):
        headers = {"Authorization": "Bearer " + self._slack_bot_key}
        requests.post(
            "https://slack.com/api/chat.postMessage", headers=headers, json=self._body)
