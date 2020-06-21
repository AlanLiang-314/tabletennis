from vpython import *
import math
#待完成:碰撞、自由球、雙人(攻防交換，輸贏判斷，黑、A、B三種球)

# 1. 參數設定, 設定變數及初始值
size = 1 # 小球半徑
g = 9.8 # 地球重力加速度 9.8 m/s^2
t = 0 # 計算時間用參數
dt = 0.01 # 時間間隔
floorfric = 0.01
wallbounce = 0.01
batangle=pi/2
batlength = 30
batforce = 5


#設定球，及球初速、加速
ballinhole=[]
ballA=[]   # 利用列表 儲存  球
N=16 #共有 N個球 白球  被擊之球  及其他
balld=math.sqrt(3*size)
ballpos=[vector(0,-50,0),vector(0,40,0),vector(1,40+balld,0),vector(-1,40+balld,0),vector(2,40+2*balld,0),vector(0,40+2*balld,0),vector(-2,40+2*balld,0),vector(3,40+3*balld,0),vector(1,40+3*balld,0),vector(-1,40+3*balld,0),vector(-3,40+3*balld,0),vector(4,40+4*balld,0),vector(2,40+4*balld,0),vector(0,40+4*balld,0),vector(-2,40+4*balld,0),vector(-4,40+4*balld,0),]
for  i in range(0,N): # 所有球之位置為 任意位置 
    ball = sphere(pos = ballpos[i], radius = size, color = color.red , make_trail=False) 
    ballA.append(ball)
    ballA[i].v = vector(0.,0.,0.)
    ballinhole.append(0)
    ballA[i].pos.z=0  #讓所有球的 Z方向位置為零

holeA=[]#球洞
holepos=[vector(-40,80,-2),vector(-40,0,-2),vector(-40,-80,-2),vector(40,80,-2),vector(40,0,-2),vector(40,-80,-2)]
for i in range(0,6) :
  hole =sphere(pos = holepos[i] ,radius = 4*size, color = color.white)
  holeA.append(hole)


#設定球桌
table = box(pos = vector(0, 0, -2), length = 80, height = 160+balld,width = 2, color = color.blue)#桌
quan = box(pos = vector(0, 0, -2), length = 90, height = 170, width= 1, color = color.cyan)#框
bat = arrow(pos=vector(0,-80,0), axis=vector(0,batlength,0), shaftwidth=1)#球桿

#設定球參數，及球初速、加速
ballA[0].pos = vector(0, -50, 0)
ballA[0].v = vector(0, 0, 0)
ballA[0].a = vector(0, 0, 0)

#箭頭(球桿)
bat.pos=vector(ballA[0].pos.x-(batlength+batforce)*cos(batangle),ballA[0].pos.y-(batlength+batforce)*sin(batangle),0)
bat.axis=vector(ballA[0].pos.x-bat.pos.x,ballA[0].pos.y-bat.pos.y,0)

#3 小球運動部分,小球撞牆時反彈=> 無窮迴圈
while True : #While true裡的程式不斷執行

  bat.opacity=0
  while (ballA[0].v.mag>=4) :
  #球速度、位置的變化
    ballA[0].v=ballA[0].v*(1-floorfric) # v=v0+a*t
    ballA[0].pos=ballA[0].pos+ballA[0].v*dt # S=s0+v*t
    rate(200) #動畫更新時間間隔 1秒

  #撞地板的反彈
    if(ballA[0].pos.y <= -80 ) :
      ballA[0].pos.y = -80
      ballA[0].v.y = -ballA[0].v.y*(1-wallbounce)

  #撞天花板的反彈
    if(ballA[0].pos.y >= 80 ) :
      ballA[0].pos.y = 80
      ballA[0].v.y = -ballA[0].v.y*(1-wallbounce)

  #撞右牆的反彈
    if( ballA[0].pos.x >= 40 ) :
      ballA[0].pos.x = 40
      ballA[0].v.x = -ballA[0].v.x*(1-wallbounce)
      
  #撞左牆的反彈
    if( ballA[0].pos.x <= -40 ) :
      ballA[0].pos.x = -40  
      ballA[0].v.x = -ballA[0].v.x*(1-wallbounce)
  #進洞
    #print(ballA[0].pos,holeA[i].pos)
    for j in range (0,10):
      for i in range (0,6):
        d=mag(ballA[i].pos-holeA[i].pos)
        if (d<=7*size):
          ballA[i].opacity=0
          ballinhole[i]=1
          ballA[i].pos.z=(-10)
          ballA[i].v=vector(0,0,0)
  #目前時間+時間間格<== 設定新時間為下一個時間
    t=t+dt

    #如果白球進洞跳回中間
    if (ballinhole[0]==1):
      ballA[0].opacity=100
      ballA[0].pos=vector(0,-50,0)
      print(ballA[0].pos)
      ballinhole[0]==0
   #箭頭(球桿)
  bat.pos=vector(ballA[0].pos.x-(batlength+batforce)*cos(batangle),ballA[0].pos.y-(batlength+batforce)*sin(batangle),0)
  bat.axis=vector(batlength*cos(batangle),batlength*sin(batangle),0)
  batforce = 5
  batangle=pi/2 #單位 弳
  while True:
    rate(100) 
    bat.opacity=100
    k=keysdown()
    if 'left' in k:
      batangle=batangle-0.01
    if 'right' in k:
      batangle=batangle+0.01
    if 'up' in k:
      batforce=batforce+1
    if 'down' in k:
      batforce=batforce-1
    #print(batangle,batforce, k) 
    if batforce<5:  #球棒最近距離
        batforce=5
    if batforce>20: #球棒最遠距離
        batforce=20
    bat.pos=vector(ballA[0].pos.x-(batlength+batforce)*cos(batangle),ballA[0].pos.y-(batlength+batforce)*sin(batangle),0)
    bat.axis=vector(batlength*cos(batangle),batlength*sin(batangle),0)
    if ' ' in k:
      ballA[0].v=vector(10*batforce*cos(batangle),10*batforce*sin(batangle),0)
      for q in range (batforce,0,-1):
          rate(200)
          bat.pos=vector(ballA[0].pos.x-(batlength+batforce)*cos(batangle),ballA[0].pos.y-(batlength+batforce)*sin(batangle),0)
          batforce-=1
      break
