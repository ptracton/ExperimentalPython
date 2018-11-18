
import os
import urllib.request

import nba_api
from nba_api.stats.endpoints import  *
from nba_api.stats.static import *

class NBA_Player():
    """
    Hold information about an NBA Player
    """
    def __init__(self, fullName=None):

        self.__is_valid = False
        
        self.playerID = self.__nameToID(fullName)
        if self.playerID is not False:
            self.__is_valid = True
        else:
            return

        # os.mkdir will throw an exception if the directory already
        # exists, so catch it and move on
        try:
            os.mkdir("Images")
        except:
            pass

        self.imageFileName = "Images/{}.png".format(self.playerID)
        
        # https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/commonplayerinfo.md
        self.commonInfoList = commonplayerinfo.CommonPlayerInfo(player_id=self.playerID).get_dict()["resultSets"][0]["rowSet"][0]
        print(self.commonInfoList)

        # https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playercareerstats.md
        #self.careerStatsDict = playercareerstats.PlayerCareerStats(player_id=self.playerID).get_dict()
        #print(self.careerStatsDict)
        return 

    def isValid(self):
        """
        Returns the flag to indicate if this is a valid record.
        A valid record is a player that exists
        """
        return self.__is_valid
    
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


    def getImage(self):
        """
        Get the player's picture
        """
        imageURL = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/{}/2018/260x190/{}.png".format(self.commonInfoList[16], self.playerID)
        local_file, r = urllib.request.urlretrieve(imageURL, self.imageFileName)
