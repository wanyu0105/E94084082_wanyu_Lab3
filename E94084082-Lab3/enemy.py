#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
import math
import os
from settings import PATH
from settings import PATH2
from settings import GREEN
from settings import RED

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))

press = 0

class Enemy:
    def __init__(self):
        global press
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        # 依據按下"n"鍵的次數來選擇路徑
        if(press % 2 == 1):
            self.path = PATH
        else:
            self.path = PATH2
        self.path_pos = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        # 血條的位置以enemy為參考物件，設置在enemy位置的上方
        pygame.draw.rect(win, GREEN, [(self.x - self.width // 2), (self.y - self.height // 2) - 5, 20, 5])
        pygame.draw.rect(win, RED, [(self.x - self.width // 2) +20, (self.y - self.height // 2) - 5, 20, 5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        pointA_x , pointA_y = self.path[self.path_pos]
        pointB_x , pointB_y = self.path[self.path_pos+1]
        distance_AtoB = math.sqrt((pointA_x - pointB_x)**2 + (pointA_y - pointB_y)**2)
        max_count = int(distance_AtoB / self.stride)  # total footsteps that needed from A to B
        
        if self.move_count < max_count:
            unit_vector_x = (pointB_x - pointA_x) / distance_AtoB   # 計算出 x 方向的單位向量
            unit_vector_y = (pointB_y - pointA_y) / distance_AtoB   # 計算出 y 方向的單位向量
            delta_x = unit_vector_x * self.stride   #計算出 x 方向移動的變化量
            delta_y = unit_vector_y * self.stride   #計算出 y 方向移動的變化量

            # update the coordinate and the counter 依照變化量更新新的座標
            self.x += delta_x
            self.y += delta_y
            self.move_count += 1
        else:
            self.path_pos += 1
            self.move_count = 0   #重置

            
class EnemyGroup:
    def __init__(self):
        self.gen_count = 0   # 記錄到達系館的 enemy 的數量
        self.gen_period = 120   # (unit: frame) 每秒禎數為 120
        self.reserved_members = []
        self.expedition = []
        self.enemy_amount = 0    # 紀錄 enemy 的總數
        self.frame_now = 0   # 記錄當下的禎數
        
    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # 當 enemy 還沒全部到達系館前，如果在當下的禎數等同於所設置的每秒禎數時(即滿 1 秒)則執行下來的動作
        if (self.gen_count < self.enemy_amount and self.frame_now == self.gen_period):
            # 當self.reserved_members 這個 list 中還存在著元素時(即元素還沒被拿空)，則執行接下來的動作
            if(self.is_empty() == False):
                self.expedition.append(self.reserved_members.pop())
                self.gen_count += 1
                self.frame_now = 0
        else:
            self.frame_now += 1
        
        if(self.gen_count == self.enemy_amount):
            self.reserved_members = []
            self.frame_now = 0
            self.gen_count = 0
        

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        global press   #利用"global"關鍵字聲明"press"為全域變數
        self.num = num
        press += 1   #按下n鍵自動加一次
        
        # 執行for迴圈 num 次，創造出 num 個敵人存進 self.reserved_members 這個 list 中
        for i in range(num):
            self.reserved_members.append(Enemy())
        
        self.enemy_amount = num   # enemy 的總數為 num 的數值


    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True   # 當敵人數量不為 0 的時候會 return FALSE

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)

