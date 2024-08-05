from models.plotElement import PlotElement

from mariadb import Error as mariadbError, Cursor, Connection

class PropertyController:
    def __init__(self, dbCursor: Cursor, dbConnection: Connection):
        self.cursor = dbCursor
        self.connection = dbConnection

    def getPropertiesOfCommit(self, plotElement: PlotElement, table: str):
        try:
            query = f"""
            SELECT p.property_id FROM cloudformation.repos r
            INNER JOIN cloudformation.commits c ON c.repo_id = r.id
            INNER JOIN cloudformation.effects_{table} e ON e.commit_id = c.id
            INNER JOIN cloudformation.actions_{table} a ON a.commit_id = c.id
            INNER JOIN cloudformation.properties_{table} p ON p.commit_id = c.id WHERE c.id = ? ORDER BY p.property_id
            """
            self.cursor.execute(query, (plotElement.commitId, ))
            if self.cursor.rowcount == 0:
                return None
            else:
                for (propertyId,) in self.cursor:
                    if propertyId == 1:
                        plotElement.area = True
                    elif propertyId == 2:
                        plotElement.billing_mode = True
                    elif propertyId == 3:
                        plotElement.cluster = True
                    elif propertyId == 4:
                        plotElement.cpu = True
                        plotElement.instance = True
                    elif propertyId == 5:
                        plotElement.domain = True
                        plotElement.networking = True
                    elif propertyId == 6:
                        plotElement.feature = True
                    elif propertyId == 7:
                        plotElement.instance = True
                    elif propertyId == 8:
                        plotElement.nat = True
                        plotElement.networking = True
                    elif propertyId == 9:
                        plotElement.networking = True
                    elif propertyId == 10:
                        plotElement.policy = True
                    elif propertyId == 11:
                        plotElement.provider = True
                    elif propertyId == 12:
                        plotElement.ram = True
                        plotElement.instance = True
                    elif propertyId == 13:
                        plotElement.storage = True
                    elif propertyId == 14:
                        plotElement.vpn = True
                        plotElement.networking = True
                    elif propertyId == 15:
                        plotElement.logging = True
                    elif propertyId == 16:
                        plotElement.permissions = True

        except mariadbError as e:
            raise mariadbError(f"Failed to get actions for commit {plotElement.commitId}: {e}")