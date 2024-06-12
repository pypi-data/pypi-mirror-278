# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

dice = np.array([1, 5, 6, 8, 3, 7, 3, 5, 9, 0], dtype=np.int32)

#주사위 던지기 -> np.array 1_dimension
def Throw_dice():
  value = np.random.choice(dice, 1)
  return value

#유전자 만들기 -> np.array 1_dimension 3 element
def Create_genome():
  genome = np.array([])
  for i in range(3):
    value = Throw_dice()
    genome = np.concatenate([genome, value], axis=0)
  return genome

#유전자 만들기 -> np.array 2_dimension (4, 3 element)
def Create_4genome():
    gen_list = np.array([])
    for i in range(4):
        value = Create_genome()
        gen_list = np.concatenate([gen_list, value], axis=0)
    gen_list = np.reshape(gen_list, (-1, 3))
    return gen_list

# 적합도 계산 -> 적합도는 |20-유전자|로 계산됨. np.array 1_dimension
def Appropriate(list_gen):
  appro_list = np.array([])
  for gen in list_gen:
    gen_sum = np.sum(gen)
    appro = np.array([np.abs(20-gen_sum)])
    appro_list = np.concatenate([appro_list, appro], axis=0)
  return appro_list

# 개체 중 적합도가 가장 작은 2개의 객체 선택하기
def Select_appropriate(list_gen):
  list_appro = Appropriate(list_gen)
  argsort = list_appro.argsort()
  two_genlist = np.array([])
  two_genlist = np.concatenate([two_genlist, list_gen[argsort[0]]], axis=0)
  two_genlist = np.concatenate([two_genlist, list_gen[argsort[1]]], axis=0)
  two_genlist = np.reshape(two_genlist, (-1, 3))
  return two_genlist

#유전자 객체 교차 구현하기
def Intersect_genome(list_gen, state):
  temp_list = np.array([])
  for gen in list_gen:
    value = gen[state]
    value = np.array([value])
    temp_list = np.concatenate([temp_list, value], axis=0)
  
  copy_list = list_gen.copy()
  copy_list[0][state] = temp_list[1]
  copy_list[1][state] = temp_list[0]
  return copy_list

# 4개의 객체 중 적합도가 가장 작은 유전 객체 2개 + 유전 객체 2개 교차 구현한 것 합치기
def Combine_genome(list_1, list_2):
  return np.concatenate((list_1, list_2), axis=0)

# 주사위 숫자가 5일 때 돌연변이 일으키기
# 돌연변이를 일으킬 위치(인덱스 0, 1, 2)를 랜덤하게 생성
def Mutation(list_gen, prob=0.1):
  mutant_list = list_gen.copy()
  event = np.random.choice((0, 1), p=[1-prob, prob])
  if event == True :
    mutant_state = np.random.choice(np.arange(0, 3), 1)
    for mutant in mutant_list:
      mutant_dice = Throw_dice()
      mutant[mutant_state[0]] = mutant_dice[0]
  return mutant_list

def Fit(genlist_four, epochs, prob=0.1, period=None):
    for epoch in range(epochs):
        genlist_two= Select_appropriate(genlist_four)
        change_num = np.random.choice(3, 1)
        intersect_gen = Intersect_genome(genlist_two, change_num[0]) 
        intersect_gen = Mutation(intersect_gen, prob)
        genlist_four = Combine_genome(genlist_two, intersect_gen) 
        # period 매개변수에 따라 epoch 출력
        if period is not None and (epoch + 1) % period == 0:
            appr = Appropriate(genlist_four)
            print(f"Epoch: {epoch + 1}, Appropriate: {appr}")
            Display_genome(genlist_four, appr=appr, epoch=epoch+1)
    print('Complete!')    
    return genlist_four
    
def Display_genome(genome, appr=None, epoch = None):
    
    if genome.ndim != 2:
        genome = np.expand_dims(genome, axis=0)
    # genome 갯수 계산
    num_genome = genome.shape[0]
    
    # 유전자 값을 세로 막대 그래프로 표현
    plt.figure(figsize=(2*num_genome, 4))
        
    # 파스텔 톤의 RGB 색상 사용
    red = (1, 0.7, 0.7)
    green = (0.7, 1, 0.7)
    blue = (0.7, 0.7, 1)
    
    # 1~4개의 유전자를 subplot으로 표현
    for i, genes in enumerate(genome):
        plt.subplot(1, num_genome, i+1)
            
        gene1, gene2, gene3 = genes
            
        # 세로 축 최대 높이를 20으로 설정
        plt.ylim(0, 20)
            
        plt.bar(0, gene1, color=red, width=0.5)
        plt.bar(0, gene2, bottom=gene1, color=green, width=0.5)
        plt.bar(0, gene3, bottom=gene1+gene2, color=blue, width=0.5)
        
        plt.text(0.07, gene1/2, f"{gene1:.2f}", va='center', ha='right', color='k')
        plt.text(0.07, gene1+gene2/2, f"{gene2:.2f}", va='center', ha='right', color='k')
        plt.text(0.07, gene1+gene2+gene3/2, f"{gene3:.2f}", va='center', ha='right', color='k')    
       
        plt.xticks([])
        plt.yticks([0, 5, 10, 15, 20])
    if appr is not None:
        for j in range(num_genome):
            plt.subplot(1, num_genome, j+1)
            plt.text(-0.23, -1, f"Appropriate: {appr[j]}", va='top', ha='left', color='k')

    if epoch is not None:
        plt.suptitle(f"Epochs: {epoch}", fontsize=16, position = (0.5, 1))
            
    plt.tight_layout()
    plt.show()