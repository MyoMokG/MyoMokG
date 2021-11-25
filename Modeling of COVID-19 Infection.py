### COVID-19 확산 시뮬레이션 ###
## 상명대학교 알고리즘과게임컨텐츠 2021학년도 2학기 팀프로젝트
## 한배 = [박소은, 김우석, 박준희, 유민상]




## 이 문단은 수정하지 마세요.

people = [] # 전체 사람(터틀)들 리스트
corona_list = [] # 확진자 리스트
dead_list = [] # 사망자 리스트
immune_list = [] # 완치자 리스트
noncorona_list = [] # 미확진자 리스트
yester_corona_list = [] # 어제 기준 확진자 리스트
yester_noncorona_list = [] # 어제 기준 미확진자 리스트
time = [] # 시간 리스트
isolation_list = [] # 격리되었었는지 확인하는 리스트 (1==격리중, 2==격리해제)
day = 1 # 날짜


## 이 문단의 변수값을 원하는 대로 수정하세요.

isolation_time = 3 # 확진된 후 격리되기까지의 시간
center_probability = 10 # 터틀이 중심부에 들어갈 확률(%)
immune_probability = 30 # 확진자가 면역을 얻을 확률(%)
infection_probability = 20 # 감염반경 안의 다른 터틀을 감염시킬 확률(%)
dead_line = 7 # 확진된 후 사망하기까지의 날짜
box = 400 # 방의 크기
s = 30 # 이동거리
r = 8 # 터틀의 갯수 = r^2
dis = 100 # 터틀들간의 거리
infection_radius = 250 # 감염반경
immune_start = 3 # 완치에 필요한 최소 날짜




import turtle
from turtle import Turtle
import random


## window setup
window = turtle.Screen()
window.title("전염병 시뮬레이션")
window.setup(1900,900)
window.bgcolor("white")


## 사용자 선택 받기 단계
while True:
    try:
        user_selection=(int(input("안녕하세요, 전염병 시뮬레이터입니다. \n어떤 시뮬레이션을 수행하시시겠습니까? \n(1. 기본 전염 양상, 2. 중심부에 방문할 때, 3. 확진자를 격리시킬 때): \n")))
        if user_selection not in [1,2,3]:
            print("정확한 답변을 해 주세요.")
            continue
        else:
            break
    except:
        print("잘못된 답변입니다. 다시 입력해주세요.")


## 경계 그리기 단계
turtle.penup()

# 1번을 선택했을 때 or 2번을 선택했을 때
if user_selection == 1 or user_selection == 2:
    turtle.setpos(box,box)
    turtle.pendown()
    turtle.hideturtle()
    for i in range(4):
        turtle.right(90)
        turtle.forward(2*box)
    turtle.penup()

    # 2번을 선택했을 때, 중심부
    if user_selection ==2:
        turtle.setpos(box/3,box/3)
        turtle.pendown()
        for i in range(4):
            turtle.right(90)
            turtle.forward(2*box/3)
            turtle.hideturtle()


# 3번을 선택했을 때
else:
    turtle.setpos(box*3/2,box)
    turtle.pendown()
    turtle.hideturtle()
    for i in range(4):
        turtle.right(90)
        turtle.forward(2*box)
    
    turtle.penup()

    # 3번을 선택했을 때, 격리실
    turtle.setpos(-box/2-infection_radius,box/2)
    turtle.pendown()
    for i in range(4):
        turtle.right(90)
        turtle.forward(box)



## 사람(터틀)들 세팅 단계
for i in range(r):
    for j in range(r):
        k=r*i+j
        people.append(k)

        people[k] = Turtle()
        people[k].shape('triangle')
        people[k].up()
        people[k].color("blue")
        people[k].speed(0)

        # user_selection에 따라 사람들이 배치되는 패턴
        if user_selection == 1 or user_selection == 2:
            people[k].setpos(dis*(j-(r-1)/2),dis*(i-(r-1)/2))
        if user_selection == 3:
            people[k].setpos(box/2 + dis*(j-(r-1)/2),dis*(i-(r-1)/2))



people_num = [] # people 내의 원소들을 숫자로 변환중

for i in range(k+1):
    people_num.append(i) 
    time.append(0)
    noncorona_list.append(i)
    yester_noncorona_list.append(i)
    isolation_list.append(i)


# 초기 확진자의 위치 설정
first = random.randint(0, k) 
people[first].color('red')
corona_list.append(first)
noncorona_list.remove(first)


## 시뮬레이션 시작
while True:
    print(str(day) + '일차', end=" - ") # 하루 지날 때마다 며칠차인지 알려주기
    print("미확진자 " + str(len(noncorona_list)) + "명, 확진자 "+str(len([x for x in corona_list if x not in dead_list]))+"명, 완치자 "+str(len(immune_list))+"명, 사망자 "+str(len(dead_list))+"명")
    
    for i in [x for x in corona_list if x not in yester_corona_list]: # 어제 기준 확진자 리스트 업데이트 중
        yester_corona_list.append(i)
    for i in [x for x in yester_corona_list if x not in corona_list]: 
        yester_corona_list.remove(i)

    for i in [x for x in noncorona_list if x not in yester_noncorona_list]:# 어제 기준 미확진자 리스트 업데이트 중
        yester_noncorona_list.append(i)
    for i in [x for x in yester_noncorona_list if x not in noncorona_list]:
        yester_noncorona_list.remove(i)
    
    day += 1 # 하루 더 지남
    
    for i in yester_corona_list: # 감염일수 +1
        
        time[i] +=1
        
        if time[i] >= immune_start and i not in dead_list: # 완치에 필요한 최소 날짜가 지나고 살아있을 경우
            if random.randint(0,100) <= immune_probability: # 일정 확률로 완치됨
                people[i].color('green')
                time[i] = dead_line+1
                yester_corona_list.remove(i)
                corona_list.remove(i)
                immune_list.append(i)

        if time[i] == dead_line: # 죽을 날까지 완치되지 못하면
            people[i].color("black") # 죽음
            people[i].stamp()
            dead_list.append(i)

            
        if user_selection==3: # 3을 선택했을 때
            
            # 확진된 지 2일이 지난 자는 1로 표시하고 격리시키기
            if time[i] >= isolation_time and i in corona_list:  
                isolation_list[i] = 1
                people[i].goto(random.randint(int(-box*3/2-infection_radius), int(-box/2-infection_radius)), random.randint(int(-box/2),int(box/2)))
                
            # 격리된 사람들 중 면역자가 생기면 2로 표시하고 사회로 돌려보내주기
            if i in immune_list and isolation_list[i] == 1: 
                isolation_list[i] = 2
                people[i].goto(random.randint(int(box*3/2),int(box*3/2)), random.randint(-box,box))


            
    # 생존자 이동 패턴
    for i in [x for x in people_num if x not in dead_list]:

        if user_selection == 2 and -box/3 < people[i].xcor() < box/3 and -box/3 < people[i].ycor() < box/3 : # 2를 선택했고, 중심부에 머무르는 중이면
            people[i].setpos(people[i].xcor() + random.randint(-1,1)*box*2/3, people[i].ycor()+ random.randint(-1,1)*box*2/3) # 위치를 중심부 밖으로 바꾸기 (1/9 확률로 하루 더 머무름)
            
        elif user_selection == 2 and random.randint(0,100) <= center_probability: # 2를 선택했고, 중심부에 머무르는 중이 아니며, 중심부를 방문할 확률에 해당하면
            people[i].setpos(random.randint(int(-box/3+s),int(box/3-s)),random.randint(int(-box/3+s),int(box/3-s))) # 위치를 중심부 안으로 바꾸기


        # 기본 이동 규칙
        people[i].right(random.randint(1,360)) # 각도
        people[i].forward(s) # 거리


        # 경계 밖으로 나갈 경우 되돌아오기
        if user_selection == 3 and isolation_list[i] != 1: # 3번을 선택했을 때
            
            if people[i].xcor() < -box/2:
                people[i].setx(people[i].xcor()+2*s)

            elif people[i].xcor() > box*3/2:
                people[i].setx(people[i].xcor()-2*s)

            if people[i].ycor() < -box:
                people[i].sety(people[i].ycor()+2*s)

            elif people[i].ycor() > box:
                people[i].sety(people[i].ycor()-2*s)
                
        
        else: # 1번을 선택했을 때 or 2번을 선택했을 때
            if people[i].xcor() < -box: 
                people[i].setx(people[i].xcor()+2*s)

            elif people[i].xcor() > box:
                people[i].setx(people[i].xcor()-2*s)

            if people[i].ycor() < -box:
                people[i].sety(people[i].ycor()+2*s)

            elif people[i].ycor() > box:
                people[i].sety(people[i].ycor()-2*s)



    # 미확진자 i와 확진자 n 사이의 감염   
    for i in yester_noncorona_list:
        for n in yester_corona_list: 
        
            if people[i].distance(people[n].xcor(), people[n].ycor()) <= infection_radius : # 확진자와 미확진자 사이의 거리가 감염반경 이하이면
                if random.randint(0,100) <= infection_probability :# 미확진자가 확률적으로 감염됨
                    people[i].color("red")
                    noncorona_list.remove(i)
                    corona_list.append(i)
                    time[i] += 1
                break

        
    if len([x for x in corona_list if x not in dead_list]) == 0: # 확진자가 0명이면 break
        break

    
print(str(day) + '일차', end=" - ") # 하루 지날 때마다 며칠인지 알려주기
print("미확진자 " + str(len(noncorona_list)) + "명, 확진자 "+str(len([x for x in corona_list if x not in dead_list]))+"명, 완치자 "+str(len(immune_list))+"명, 사망자 "+str(len(dead_list))+"명")
input("결과를 보려면 Enter키를 누르세요.")


for i in range(k+1): # 사람들 지우기
    people[i].reset()
    people[i].hideturtle()


turtle.reset()
turtle.penup()
turtle.hideturtle()


turtle.setpos(0,100) # 결과창 메세지
fin1= "바이러스는 " + str(day) + " 일 후에 끝났습니다."
turtle.write(fin1, align = "center", font =("궁서", 20, "bold") )
turtle.setpos(0,0)
fin2 = "총 "+ str(k+1)+ " 명 중 살아남은 사람들은 총 " +str(len(immune_list)+len(noncorona_list)) + " 명입니다."
turtle.write(fin2, align = "center", font =("궁서", 18, "bold"))
turtle.setpos(0,-50)
fin3 = "미확진자 " + str(len(noncorona_list)) + "명, 확진자 "+str(len([x for x in corona_list if x not in dead_list]))+"명, 완치자 "+str(len(immune_list))+"명, 사망자 "+str(len(dead_list))+"명"
turtle.write(fin3, align = "center", font =("궁서", 18, "bold"))
turtle.setpos(0,-100)
fin4 = "클릭하여 종료하기"
turtle.write(fin4, align = "center", font =("궁서", 12, "bold"))
window.exitonclick()
