class Card:
    def __init__(self, app):
        self.app = app

        self.source_code_url = ""
        self.is_github = ""
        self.left_description = ""
        self.right_description = "Download"

        # if the appimage is hosted from GitHub
        app_links = app["links"]
        is_app_links_valid = app_links is not None

        if (
            is_app_links_valid
            and len(app_links) > 0
            and app_links[0].get("type", None) == "GitHub"
        ):
            self.set_github_specific_attr()

    def set_github_specific_attr(self):
        self.source_code_url = "https://github.com/{}".format(
            self.app["links"][0].get("url")
        )
        self.is_github = "github"
        self.left_description = "GitHub"

    def __getitem__(self, item):
        return self.app[item]

    def __getattr__(self, item):
        return self.app[item]

    @property
    def name_lower_case(self):
        return self.app["name"].lower()
