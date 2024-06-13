from .main import LiveScoreAPI


class LiveScores(LiveScoreAPI):
    def get_live_scores(self, competition_id=None, country_id=None, fixture_id=None, team_id=None,lang=None):
        params = self._get_params(competition_id=competition_id, country_id=country_id, fixture_id=fixture_id, team_id=team_id, lang=lang)
        return self._make_request("/matches/live.json", params)


    def get_live_scores_by_competition(self, competition_id=None, lang=None):
        return self.get_live_scores(competition_id=competition_id, lang=lang)


    def get_live_scores_by_country(self, country_id=None, lang=None):
        return self.get_live_scores(country_id=country_id, lang=lang)


    def get_live_scores_by_fixture(self, fixture_id=None, lang=None):
        return self.get_live_scores(fixture_id=fixture_id, lang=lang)


    def get_live_scores_by_team(self, team_id=None, lang=None):
        return self.get_live_scores(team_id=team_id, lang=lang)
