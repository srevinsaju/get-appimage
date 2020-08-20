class Card:
    def __init__(self, app):
        self.app = app

        self.source_code_url = ''
        self.is_github = ''
        self.left_description = ''
        self.right_description = 'Download'

        # if the appimage is hosted from GitHub
        if app['github'] is not None:
            self.set_github_specific_attr()

    def set_github_specific_attr(self):
        self.source_code_url = \
            "https://github.com/{}".format(self.app['github'][0].get('url'))
        self.is_github = 'github'
        self.left_description = 'GitHub'

    def __getitem__(self, item):
        return self.app[item]

    def __getattr__(self, item):
        return self.app[item]

    @property
    def name_lower_case(self):
        return self.app['name'].lower()

