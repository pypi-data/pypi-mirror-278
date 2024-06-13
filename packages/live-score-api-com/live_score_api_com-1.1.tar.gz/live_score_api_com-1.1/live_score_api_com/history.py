from .main import LiveScoreAPI

class History(LiveScoreAPI):
    def get_history(self, competition_id=None, from_date=None, to_date=None, page=None, team_id=None, lang=None):
        params = self._get_params(
            competition_id=competition_id,
            from_date=from_date,
            to_date=to_date,
            page=page,
            team_id=team_id,
            lang=lang
        )
        return self._make_request("/matches/history.json", params)
    
    
    def get_history_by_competition(self, competition_id=None, lang=None):
        return self.get_history(competition_id=competition_id, lang=lang)
        

    def get_history_from_date(self, from_date=None, lang=None):
        return self.get_history(from_date=from_date, lang=lang)
    

    def get_history_to_date(self, to_date=None, lang=None):
        return self.get_history(to_date=to_date, lang=lang)
    

    def get_history_by_page(self, page=None, lang=None):
        return self.get_history(page=page, lang=lang)
    

    def get_history_by_team(self, team_id=None, lang=None):
        return self.get_history(team_id==team_id, lang=lang)

