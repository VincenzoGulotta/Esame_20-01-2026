from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists_by_min(minimo):

        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                select ar.id as id, ar.name as name, count(*)
                from artist ar, album al
                where al.artist_id = ar.id
                group by ar.id
                having count(*) >= %s
                """
        cursor.execute(query,(minimo,))
        for row in cursor:
            a_id = row['id']
            artist = Artist(id=row['id'], name=row['name'])
            result[a_id] = artist
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni(minimo):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                with selected_artists as(
	            select al.artist_id as id, ar.name as name, count(*) as num_album
	            from artist ar, album al
	            where al.artist_id = ar.id
	            group by ar.id
	            having count(*) >= %s
                )
                select distinct sa.id as id, sa.name as name, t.genre_id as genre_id
                from selected_artists sa, track t
                where t.composer = sa.name
                order by sa.id
                """
        cursor.execute(query,(minimo,))
        for row in cursor:
            genre_id = row['genre_id']
            artist_id = row['id']
            if genre_id in result.keys():
                result[genre_id].append(artist_id)
            else:
                result[genre_id] = []
                result[genre_id].append(artist_id)

        cursor.close()
        conn.close()
        return result



