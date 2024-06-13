from .main import LiveScoreAPI


class GroupStandings(LiveScoreAPI):
    def get_group_standings(self, group_id=None, include_form=None, lang=None):
        if group_id:
            params = self._get_params(group_id=group_id, include_form=include_form, lang=lang)
            return self._make_request("/groups/table.json", params)
        else:
            raise ValueError('group_id is required.')
        
    def get_group_standings_with_form(self, group_id=None, lang=None):
        return self.get_group_standings(group_id=group_id, include_form=1, lang=lang)
        
    
