import nba_api
from nba_api.stats.endpoints import  *
from nba_api.stats.static import *

class NBA_Player():
    """
    Hold information about an NBA Player
    """
    def __init__(self, fullName=None):
       
        self.playerID = self.__nameToID(fullName)
        print(self.playerID)
        if not self.playerID:
            return False
        # https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/commonplayerinfo.md
        self.commonInfoList = commonplayerinfo.CommonPlayerInfo(player_id=self.playerID).get_dict()["resultSets"][0]["rowSet"][0]
        print(self.commonInfoList[6])

        # https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playercareerstats.md
        #self.careerStatsDict = playercareerstats.PlayerCareerStats(player_id=self.playerID).get_dict()
        #print(self.careerStatsDict)
        return


    def __nameToID(self, fullName=None):
        """
        Takes a players name and turns it into the ID used
        for all other searches
        """
        playersList = players.find_players_by_full_name(fullName)
        if len(playersList) > 0:
            person = playersList[0] 
            return person["id"]
        else:
            return False
