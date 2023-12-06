import pygame
import random
from datetime import datetime

# Pygame 초기화
pygame.init()

# 게임창 사이즈 설정
size = [500, 700]
screen = pygame.display.set_mode(size)

# 게임 타이틀
title = "SSBN: Deep Sea Battle"
pygame.display.set_caption(title)

# 게임 내 필요한 설정
clock = pygame.time.Clock() # 이후 FPS 설정 위한 clock 변수 생성
pygame.mixer.init()  # 사운드를 위한 초기화

# 사운드 로드
shoot_sound = pygame.mixer.Sound("C://pmg//test//soundfile.wav")  # 미사일 발사 소리
hit_sound = pygame.mixer.Sound("C://pmg//test//monsterHit.mp3")  # 적이 맞았을 때의 소리

# 클래스
class obj:
    def __init__(self): #매직 매서드
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self, address): # png파일의 경우 .convert_alpha()추가
        if address[-3:] == "png": #파일명의 마지막 3글자, 즉 확장자
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy): # 이미지의 사이즈 조정
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self): #이미지를 지정한 좌표에 맞게 화면에 표시
        screen.blit(self.img, (self.x, self.y)) # blit는 화면에 표시하는 함수  

# 충돌 감지 함수
def crash(a, b):
    if (a.x-b.sx <= b.x) and (b.x <= a.x+a.sx):
        if (a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
    else:
        return False

# 기본 변수 설정
sm = obj()
sm.put_img("C://pmg//test//ship.png")
sm.change_size(40, 90)
sm.x = size[0]/2 - sm.sx/2 
sm.y = size[1] - sm.sy # 최초 x,y 좌표
sm.move = 3 # 이동속도

left_go = False
right_go = False
space_go = False

tp_list = [] #torpedo list
en_list = []

blue = (76,150,180)
white = (255, 255, 255)
k = 0

GO = 0 # 게임 오버 화면을 위한 변수
kill = 0 # 처치한 적의 수
loss = 0 # 놓친 적의 수

# 보스 외계인 관련 변수
boss_appear_time = 30  # 보스가 나타나는 시간 (초)
boss_appeared = False

# 게임 시작 대기 화면
GCU = 0
while GCU == 0:
    clock.tick(40) # FPS(초당 프레임 수) 설정
    for event in pygame.event.get(): 
        # pygame.event.get()는 실시간으로 마우스, 키보드의 동작을 받아오는 함수
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                GCU = 1
    screen.fill(blue)

    ti = obj()
    ti.put_img("C://pmg//test//title.png")
    ti.x = 50
    ti.y = 100
    ti.show()

    font = pygame.font.Font(None, 20)
    text = font.render("PRESS SPACE TO START THE GAME", True, white)
    screen.blit(text, (130, round(size[1]/2))) 

    pygame.display.flip() #화면을 업데이트 하는 함수

# 메인 게임 루프
start_time = datetime.now()
GCU = 0
while GCU == 0:
    clock.tick(40)
    for event in pygame.event.get(): 
    # 동시에 이벤트가 발생할 수 있기 때문에 for 문으로 확인
        if event.type == pygame.QUIT: # 창닫기 누르면 꺼짐
            GCU = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    if left_go == True:
        sm.x -= sm.move
        if sm.x <= 0:
            sm.x = 0 # 화면밖으로 나가는 것 방지
    elif right_go == True:
        sm.x += sm.move
        if sm.x >= size[0] - sm.sx:
            sm.x = size[0] - sm.sx

    if space_go == True and k % 24 == 0:
        shoot_sound.play()
        tp = obj()
        tp.put_img("C://pmg//test//bullet.png")
        tp.change_size(20, 50)
        tp.x = sm.x + sm.sx/2 - tp.sx/2
        tp.y = sm.y - tp.sy + 15
        tp.move = 10
        tp_list.append(tp)
    k += 1

    d_list = [] # 화면 밖으로 나간 어뢰를 지우는 과정
    for i in range(len(tp_list)): #어뢰의 list
        t = tp_list[i]
        t.y -= t.move
        if t.y <= -t.sy:
            d_list.append(i)
    for d in reversed(d_list):
        del tp_list[d]

    if random.random() > 0.95: #적 생성
        en = obj()
        en.put_img("C://pmg//test//enemy.png")
        en.change_size(40, 30)
        en.x = random.randrange(0, size[0]- en.sx - sm.sx/2)
        en.y = 1
        en.move = 1
        en_list.append(en)

    d_list = [] 
    for i in range(len(en_list)):
        e = en_list[i]
        e.y += e.move
        if e.y >= size[1]: #화면 밖으로 나가면 삭제
            d_list.append(i)
    for d in reversed(d_list):
        del en_list[d]
        loss += 1

    now_time = datetime.now()
    delta_time = (now_time - start_time).total_seconds()

    if not boss_appeared and delta_time >= boss_appear_time:
        boss = obj()
        boss.put_img("C://pmg//test//boss.png")
        boss.change_size(200, 150)
        boss.x = random.randrange(0, size[0] - boss.sx)
        boss.y = 10
        boss.move = 5
        en_list.append(boss)
        boss_appeared = True

    #충돌 판정: 어뢰(t)와 괴물(e) 이 충돌
    dt_list = []
    de_list = []
    for i in range(len(tp_list)):
        for j in range(len(en_list)):
            t = tp_list[i]
            e = en_list[j]
            if crash(t, e) == True:
                dt_list.append(i)
                de_list.append(j)
                hit_sound.play()

    for dt in reversed(list(set(dt_list))): # set중복 제거
        del tp_list[dt]                     # 충돌시 제거
    for de in reversed(list(set(de_list))):
        del en_list[de]
        kill += 1

    for i in range(len(en_list)):
        e = en_list[i]
        if crash(e, sm) == True:
            GCU = 1
            GO = 1 

    screen.fill(blue)
    sm.show()

    # 미사일 그리기
    for t in tp_list:
        t.show()

    # 적 그리기
    for e in en_list:
        e.show()

    # 게임 상태 표시
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {kill}", True, white)
    screen.blit(score_text, (10, 5))
    loss_text = font.render(f"Loss: {loss}", True, white)
    screen.blit(loss_text, (size[0] - 100, 5))

    pygame.display.flip()

# 게임 오버 화면
if GO == 1:
    font = pygame.font.Font(None, 55)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (130, round(size[1]/2)))
    pygame.display.flip()
    pygame.time.wait(2000)

pygame.quit()
