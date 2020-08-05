from flask import *

app = Flask(__name__)


@app.route('/Diet_profile')
def Diet_profile():
    return render_template('Diet_profile.html')


bm=0 
cm=0 
dm=0
@app.route('/basal_metabolism', methods=['POST', 'GET'])
def basal_metabolism():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        fat_rate = request.form['fat_rate']
        
        if fat_rate is "*":
            return render_template('Diet_profile.html', i=0)  
        elif fat_rate is not "":            
            bmcalc= 500 + (22 * (int(weight) * (1 - int(fat_rate) / 100)))
            # 기초 대사량 = 500 + ( 22 * 제지방량)
            # 제지방량 = (1.10  * 체중kg ) - ( 128 * ( 체중kg제곱 / 키cm제곱 ))  
            global bm 
            bm=bmcalc 
            return render_template('Diet_profile.html', i=bmcalc)            
        elif gender is "m":            
            bmcalc= 66.47 + (13.75 * int(weight)) + (5 * int(height)) - (6.76 * int(age))
            # 남자 : 66.47 + (13.75 X 체중) + (5 X 키) - (6.76 X 나이)
            global cm
            cm=bmcalc
            return render_template('Diet_profile.html', i=bmcalc)
        else :            
            bmcalc= 655.1 + (9.56 * int(weight)) + (1.85 * int(height)) - (4.68 * int(age))
            # 여자 : 655.1 + (9.56 X 체중) + (1.85 X 키) - (4.68 X 나이)
            global dm     
            dm=bmcalc      
            return render_template('Diet_profile.html', i=bmcalc)  
       
    else:
        return '에러'


em=0 
fm=0 
gm=0 
hm=0
@app.route('/active_metabolism', methods=['POST', 'GET'])
def active_metabolism():
    if request.method == 'POST':
        action = request.form['action']
        weight = request.form['weight']

        if action is "c":
            amcalc=int(weight)*7.7
            global em
            em= amcalc
            return render_template('Diet_profile.html', j=int(weight)*7.7)
                                                            #체중 x 활동계수
        elif action is "s":
            amcalc=int(weight)*12.7
            global fm
            fm= amcalc
            return render_template('Diet_profile.html', j=int(weight)*12.7)
                                                            #체중 x 활동계수
        elif action is "w":
            amcalc=int(weight)*14.8
            global gm
            gm= amcalc
            return render_template('Diet_profile.html', j=int(weight)*14.8)
                                                            #체중 x 활동계수
        else:
            amcalc=int(weight)*18.7
            global hm
            hm= amcalc
            return render_template('Diet_profile.html', j=int(weight)*18.7)
                                                            #체중 x 활동계수
    else:
        return '에러'


l=0
k=0
m=0
@app.route('/Diet_calc')
def Diet_calc():
    return render_template('Diet_calc.html', k=0, l=l, m1=0, m2=0, m3=0, bm=bm, cm=cm, dm=dm, em=em, fm=fm, gm=gm, hm=hm)

@app.route('/Diet_cal_result', methods=['POST', 'GET'])
def Diet_cal_result():
    if request.method == 'POST':
        weight = request.form['weight']
        fat_rate = request.form['fat_rate']
        goal_fat_rate = request.form['goal_fat_rate']
        start_cal = request.form['start_cal']
        cutting_cal = request.form['cutting_cal']
        
        daycalc= int(9900 * int(weight) * ((int(fat_rate) / 100 - int(goal_fat_rate) / 100)) / -int(start_cal))
                         #9000*(현재체중-예상체중) / 시작시 줄일 칼로리
                         #(현재체중-예상체중)을 지방의 열량으로 환산 후 (시작시 줄일 칼로리)만큼 매일 빠진다 가정할 때 걸리는 시간
        final_weight= int(weight) - ((int(weight)*int(fat_rate) / 100) - (int(weight)*int(goal_fat_rate) / 100))
                        #현재체중 - ((현재체중*현재체지방률)-(현재체중*목표체지방률))        
        global l
        global k
        global m
        l=daycalc
        k=final_weight
        m=int(weight)
        
        return render_template('Diet_calc.html', k=final_weight, l= daycalc, m1= int(cutting_cal), m2= int(weight), m3= int(start_cal),
                                                    bm=int(bm), cm= int(cm), dm= int(dm), em=int(em), fm=int(fm), gm=int(gm), hm=int(hm))
    else:
        return '에러'


@app.route('/Diet_foodcalc')
def Diet_foodcalc():
    return render_template('Diet_foodcalc.html')
    
    
@app.route('/Diet_memo')
def Diet_memo():
    return render_template('Diet_memo.html')

import sqlite3 as sql

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS tracking1 (date TEXT, weight TEXT)')
print("Table created successfully")
conn.close()


@app.route('/insert')
def insert():    
    return render_template('insert_diet.html')

@app.route('/insert_perform', methods=['POST'])   
def insert_perform():
    if request.method == 'POST':
        date = request.form['date']
        weight = request.form['weight']
        
    conn = sql.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""insert into tracking1 values (:date, :weight)""", [date, weight])
    conn.commit()
    conn.close()
    
    return "입력에 성공했습니다! <a href='/Diet_memo'>뒤로가기</a>"


@app.route('/update')
def update():
    return render_template('update_diet.html')

@app.route('/update_perform', methods=['POST'])   
def update_perform():
    if request.method == 'POST':
        date = request.form['date']
        weight = request.form['weight']   
            
    conn = sql.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""update tracking1 set weight = :weight where date = :date""", [weight, date])
    conn.commit()
    conn.close()
    
    return "수정에 성공했습니다! <a href='/Diet_memo'>뒤로가기</a>"


@app.route('/delete')
def delete():
    return render_template('delete_diet.html')


@app.route('/delete_perform', methods=['POST'])   
def delete_perform():
    if request.method == 'POST':
        date = request.form['date']      
            
    conn = sql.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""delete from tracking1 where date = :date""", [date])
    conn.commit()
    conn.close()
    
    return "삭제에 성공했습니다! <a href='/Diet_memo'>뒤로가기</a>"


@app.route('/select', methods=['POST'])   
def select():    
    rows = []
    if request.method == 'POST':    

        conn = sql.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tracking1 order by date;""")
        rows = cursor.fetchall()
        print(rows)
        conn.close()
            
    return render_template('select_diet.html', sawon = rows)


if __name__ == '__main__':
    app.run(debug=True)
