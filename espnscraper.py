import mechanize
import cookielib


class EspnScraper(object):

    LOGIN_URL = 'http://m.espn.go.com/wireless/login'
    STANDINGS_URL = 'http://games.espn.go.com/ffl/standings?leagueId={0}&seasonId={1}'
    SCOREBOARD_URL = 'http://games.espn.go.com/ffl/scoreboard?leagueId={0}&seasonId={1}'
    ROSTER_URL = 'http://games.espn.go.com/ffl/clubhouse?leagueId={0}&teamId={1}&seasonId={2}'
    FA_URL = 'http://games.espn.go.com/ffl/freeagency?leagueId={0}&teamId={1}'
    SCORING_URL = 'http://games.espn.go.com/ffl/leaders?leagueId={0}&teamId={1}&scoringPeriodId={2}'
    WAIVER_URL = 'http://games.espn.go.com/ffl/tools/waiverorder?leagueId={0}'
    TRANSACTIONS_URL = 'http://games.espn.go.com/ffl/tools/transactioncounter?leagueId={0}'

    def __init__(self, config):
        self.config = dict(config.items('default'))
        self.league = self.config.get('user.league')
        self.season = self.config.get('user.season')
        self.user = self.config.get('user.name')
        self.password = self.config.get('user.password')
        self.browser = self.connect()

    def connect(self):
        cj = cookielib.CookieJar()
        br = mechanize.Browser()
        br.set_cookiejar(cj)
        br.open(self.LOGIN_URL)
        br.form = list(br.forms())[0]
        br.form['username'] = self.user
        br.form['gspw'] = self.password
        br.submit()
        return br

    def standings_html(self):
        self.browser.open(self.STANDINGS_URL.format(self.league, self.season))
        return self.browser.response().read()

    def roster_html(self, team):
        self.browser.open(self.ROSTER_URL.format(self.league, team, self.season))
        return self.browser.response().read()

    def fa_html(self, team):
        self.browser.open(self.FA_URL.format(self.league, team))
        return self.browser.response().read()

    def transactions_html(self):
        self.browser.open(self.TRANSACTIONS_URL.format(self.league))
        return self.browser.response().read()
