import pymysql
from prettytable import PrettyTable

def player_info(year, position, player_name=None):

    position = position.lower()
    year = int(year)
    if not (2001 <= year <= 2023):
        return "Error: Year must be between 2001 and 2023"

    valid_position = ["hitter", "pitcher", "defender", "runner"]
    if position not in valid_position:
        return "Error: Position must be one of the following: hitter, pitcher, defender, runner" 
    try:
        # MySQL 연결 설정
        conn = pymysql.connect(
            host='222.111.68.205', 
            user='root',
            password='1322', 
            database='baseball_stat',
            charset='utf8'
        )

        # 커서 생성
        cursor = conn.cursor()

        # 테이블 이름 생성
        table_name = f"regular_{year}_{position}"

        if position == "hitter":
            po = "ht"
        elif position == "pitcher":
            po = "pt"
        elif position == "defender":
            po = "df"
        elif position == "runner":
            po = "run"
        else:
            print("Invalid position")

        # 선수 정보 검색 쿼리 실행
        if player_name:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {po}_Playername=%s", (player_name,))
        else:
            cursor.execute(f"SELECT * FROM {table_name}")
        
        player_info = cursor.fetchall()

        # 결과를 딕셔너리 형태로 반환
        players = []
        for info in player_info:
            if po == "ht":
                player = {
                    '선수 이름': info[0],
                    '팀': info[1],
                    '평균 타율': info[2],
                    '경기': info[3],
                    '타석': info[4],
                    '타수': info[5],
                    '득점': info[6],
                    '안타': info[7],
                    '2루타': info[8],
                    '3루타': info[9],
                    '홈런': info[10],
                    '루타': info[11],
                    '타점': info[12],
                    '희생번트': info[13],
                    '희생플라이': info[14]
                }
            elif po == "pt":
                player = {
                    '선수 이름': info[0],
                    '팀': info[1],
                    '평균 자책점': info[2],
                    '경기': info[3],
                    '완투': info[4],
                    '완봉': info[5],
                    '승리': info[6],
                    '패배': info[7],
                    '세이브': info[8],
                    '홀드': info[9],
                    '승률': info[10],
                    '타자수': info[11],
                    '이닝': info[12],
                    '피안타': info[13],
                    '홈런': info[14],
                    '볼넷': info[15],
                    '사구': info[16],
                    '삼진': info[17],
                    '실점': info[18],
                    '자책점': info[19]
                }
            elif po == "df":
                player = {
                    '선수 이름': info[0],
                    '팀': info[1],
                    '포지션': info[2],
                    '경기': info[3],
                    '선발경기': info[4],
                    '수비이닝': info[5],
                    '실책': info[6],
                    '견제사': info[7],
                    '풋아웃': info[8],
                    '어시스트': info[9],
                    '병살': info[10],
                    '수비율': info[11],
                    '포일': info[12],
                    '도루허용': info[13],
                    '도루실패': info[14],
                    '도루저지율': info[15]
                }
            elif po == "run":
                player = {
                    '선수 이름': info[0],
                    '팀': info[1],
                    '경기': info[2],
                    '도루시도': info[3],
                    '도루허용': info[4],
                    '도루실패': info[5],
                    '도루성공률': info[6],
                    '주루사': info[7],
                    '견제사': info[8]
                }
            players.append(player)

        # 연결 종료
        conn.close()

        if players == []:
            return "Error: Player name must be provided"

        return players

    except pymysql.Error as err:
        print(f"MySQL 오류: {err}")
        return None
    
    
def homerun_rank(year, limit=50):
    year = int(year)
    limit = int(limit)
    
    if not (2001 <= year <= 2023):
        return "Error: Year must be between 2001 and 2023"
    if not (1 <= limit <= 50):
        return "Error: Rank must be between 1 and 50"
    
    conn = pymysql.connect(
        host='222.111.68.205', 
        user='root',
        password='1322', 
        database='baseball_stat',
        charset='utf8'
    )
    
    cursor = conn.cursor()
    
    # 테이블명 생성
    table_name = f"regular_{year}_hitter"
    
    # 쿼리 실행
    query = f"""
    SELECT ht_Playername, ht_Teamname, ht_HR
    FROM {table_name}
    ORDER BY ht_HR DESC
    LIMIT {limit}
    """
    cursor.execute(query)
    
    # 결과 가져오기
    results = cursor.fetchall()
    
    # PrettyTable 생성
    table = PrettyTable()
    table.field_names = ["Rank", "Player", "Team", "Homerun"]
    
    for rank, (player, team, homerun) in enumerate(results, start=1):
        table.add_row([rank, player, team, homerun])
    
    # 연결 종료
    conn.close()

    return table.get_string()