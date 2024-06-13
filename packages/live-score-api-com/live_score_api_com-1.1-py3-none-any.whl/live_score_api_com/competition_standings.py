from .main import LiveScoreAPI


class CompetitionStandings(LiveScoreAPI):
    def get_competition_standings(self, competition_id=None, include_form=None, season=None,lang=None):
        if competition_id:
            params = self._get_params(competition_id=competition_id, include_form=include_form, season=season, lang=lang)
            return self._make_request("/competitions/table.json", params)
        else:
            raise ValueError("competition_id is required")
        
    def get_competition_standings_with_form(self, competition_id=None, lang=None):
        return self.get_competition_standings(competition_id=competition_id, include_form=1, lang=lang)
        
    def get_competition_standings_by_season(self, competition_id=None, season=None, lang=None):
        if season:
            return self.get_competition_standings(competition_id=competition_id, season=season, lang=lang)
        else:
            raise ValueError("season is required")
