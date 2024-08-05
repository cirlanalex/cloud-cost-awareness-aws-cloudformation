from mariadb import Error as mariadbError, Cursor

class RelationKeywordController:
    def __init__(self, dbCursor: Cursor):
        self.cursor = dbCursor
    
    def createKeywordsToEvent(self, eventId: int, keywordIds: list, event: str):
        try:
            dbTable = "keywords_" + event + "s"
            dbEvent = event + "_id"
            addedKeywordIds = []
            for keywordId in keywordIds:
                self.cursor.execute(f"INSERT INTO {dbTable} (keyword_id, {dbEvent}) VALUES ('{keywordId}', '{eventId}')")
                addedKeywordIds.append(keywordId)
        except mariadbError:
            self.deleteKeywordsFromEvent(eventId, addedKeywordIds, event)
            raise

    def deleteKeywordsFromEvent(self, eventId: int, keywordIds: list, event: str):
        try:
            dbTable = "keywords_" + event + "s"
            dbEvent = event + "_id"
            for keywordId in keywordIds:
                self.cursor.execute(f"DELETE FROM {dbTable} WHERE keyword_id = {keywordId} AND {dbEvent} = {eventId}")
        except mariadbError:
            raise