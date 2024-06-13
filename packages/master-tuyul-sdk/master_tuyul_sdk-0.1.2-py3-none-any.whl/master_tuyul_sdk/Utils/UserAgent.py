import re
from UserAgenter import UserAgent as _UserAgent

class UserAgent:
     
    @staticmethod
    def android_app() -> str:
        # User Agent Class
        ua = _UserAgent()
        # Android User Agent 
        while True:
            random_android_agent = ua.RandomAndroidAgent()
            if len(re.findall('Mozilla/5.0', random_android_agent)) != 0:
                if len(re.findall('Android', random_android_agent)) != 0:
                    return '{})'.format(random_android_agent.replace('Mozilla/5.0', 'Dalvik/2.1.0').split(')')[0])
    
    @staticmethod
    def android_web() -> str:
        # User Agent Class
        ua = _UserAgent()
        # Android User Agent 
        return ua.RandomAgent("Android")

    @staticmethod
    def RandomFirefoxAgent() -> str:
        ua = _UserAgent()
        """Returns a randomly selected Firefox user agent string."""
        return ua.RandomAgent("Firefox")

    @staticmethod
    def RandomChromeAgent() -> str:
        ua = _UserAgent()
        """Returns a randomly selected Chrome user agent string."""
        return ua.RandomAgent("Chrome")

    @staticmethod
    def RandomOperaAgent() -> str:
        ua = _UserAgent()
        """Returns a randomly selected Opera user agent string."""
        return ua.RandomAgent("Opera")

    @staticmethod
    def RandomEdgeAgent() -> str:
        ua = _UserAgent()
        """Returns a randomly selected Edge user agent string."""
        return ua.RandomAgent("Edge")

    @staticmethod
    def RandomSafariAgent() -> str:
        ua = _UserAgent()
        """Returns a randomly selected Safari user agent string."""
        return ua.RandomAgent("Safari")
