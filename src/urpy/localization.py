import gettext


def lcl(s: str, domain=None):
    """ Marks a string for localization. """
    return s


class Localization:  # TODO default localedir
    def __init__(self, localedir='', default_language='fr', default_domain='bot_base', user_based=False):
        self._localedir = localedir
        self.languages = {}  # TODO make languages a class
        self._default_language = default_language
        self.users_custom_language = {}
        self._current_user_id = ''
        self.user_based = user_based
        self._default_domain = default_domain
        self._current_domain = None
        # TODO add handling of several domains (context manager)

    def add_translation(self, domain, codes, *aliases):  # TODO make aliases
        language = gettext.translation(domain, self._localedir, codes, fallback=True)
        if codes[0] not in self.languages:
            self.languages[codes[0]] = {}
        if 'en' not in self.languages:
            self.languages['en'] = {}

        self.languages[codes[0]][domain] = language.gettext
        if domain not in self.languages['en']:
            self.add_translation(domain, ['en'])

    def set_default_language(self, lang_code):
        if lang_code in self.languages:
            self._default_language = lang_code
            return True
        else:
            return False

    def set_user_language(self, lang_code):
        if lang_code in self.languages:
            if lang_code == self._default_language:
                if self._current_user_id in self.users_custom_language:
                    del self.users_custom_language[self._current_user_id]
            else:
                self.users_custom_language[self._current_user_id] = lang_code
            return True
        else:
            return False

    def set_current_user(self, user_id):
        self._current_user_id = user_id

    def set_current_domain(self, domain):
        self._current_domain = domain

    def gettext(self, s, domain=None):
        if domain is None:
            if self._current_domain is not None:
                domain = self._current_domain
            else:
                domain = self._default_domain

        if self._current_user_id in self.users_custom_language:
            lang = self.users_custom_language[self._current_user_id]
        else:
            lang = self._default_language
        #  TODO automatize fallback based on folder name
        if lang in self.languages:
            lang = self._default_language if domain not in self.languages[lang] else lang
            return self.languages[lang][domain](s)
        else:
            return s

    def set_localedir(self, param):
        self._localedir = param
