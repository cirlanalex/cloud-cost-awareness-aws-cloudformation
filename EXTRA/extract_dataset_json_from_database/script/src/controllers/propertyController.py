from models.plotElement import PlotElement

from mariadb import Error as mariadbError, Cursor, Connection

class PropertyController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def getPropertiesOfCommit(self, plotElement: PlotElement):
        try:
            query = """
            SELECT p.property_id FROM cloudformation.repos r
            INNER JOIN cloudformation.commits c ON c.repo_id = r.id
            INNER JOIN cloudformation.re_effects_commits e ON e.commit_id = c.id
            INNER JOIN cloudformation.re_actions_commits a ON a.commit_id = c.id
            INNER JOIN cloudformation.re_properties_commits p ON p.commit_id = c.id WHERE c.id = ? ORDER BY p.property_id
            """
            self.cursor.execute(query, (plotElement.commitId,))
            if self.cursor.rowcount == 0:
                return None
            else:
                for (propertyId,) in self.cursor:
                    if propertyId == 1:
                        plotElement.alert = True
                    elif propertyId == 2:
                        plotElement.area = True
                    elif propertyId == 3:
                        plotElement.billing_mode = True
                    elif propertyId == 4:
                        plotElement.cluster = True
                    elif propertyId == 5:
                        plotElement.cpu = True
                        plotElement.instance = True
                    elif propertyId == 6:
                        plotElement.domain = True
                        plotElement.networking = True
                    elif propertyId == 7:
                        plotElement.feature = True
                    elif propertyId == 8:
                        plotElement.instance = True
                    elif propertyId == 9:
                        plotElement.logging = True
                    elif propertyId == 10:
                        plotElement.nat = True
                        plotElement.networking = True
                    elif propertyId == 11:
                        plotElement.networking = True
                    elif propertyId == 12:
                        plotElement.policy = True
                    elif propertyId == 13:
                        plotElement.provider = True
                    elif propertyId == 14:
                        plotElement.ram = True
                        plotElement.instance = True
                    elif propertyId == 15:
                        plotElement.report = True
                    elif propertyId == 16:
                        plotElement.service = True
                    elif propertyId == 17:
                        plotElement.storage = True
                    elif propertyId == 18:
                        plotElement.vpn = True
                        plotElement.networking = True

        except mariadbError as e:
            raise mariadbError(f"Failed to get actions for commit {plotElement.commitId}: {e}")