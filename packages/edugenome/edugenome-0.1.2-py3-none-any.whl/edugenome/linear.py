# 수정사항, Display_genome 함수에서 왜 target이 안되는 것인가

# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# 표준편차 sigma, 평균 mu인 정규분포에서 3개를 추출
# 각각 w_1, w_2, b임
def Create_genome(sigma=1, mu=1):
    value = sigma*np.random.randn(3) + mu
    return value

# 유전 객체 4개 만들기
def Create_4genome(sigma=1, mu=1):
    gen_list = np.array([])
    for i in range(4):
        value = Create_genome(sigma, mu)
        gen_list = np.concatenate([gen_list, value], axis=0)
    gen_list = np.reshape(gen_list, (-1, 3))
    return gen_list

# 적합도 계산 : |target - x_1w_1 + x_2w_2 + b|
def Appropriate(list_gen, x, y):
  appro_list = np.array([])
  for gen in list_gen:
    w = gen[:2]
    b = gen[2]
    appro = np.array([np.abs(y - np.sum(x@w + b))])
    appro = np.round(appro, 2)
    appro_list = np.concatenate([appro_list, appro], axis=0)
  return appro_list

# 개체 중 적합도가 가장 작은 2개의 객체 선택하기
def Select_appropriate(list_gen, x, y):
  list_appro = Appropriate(list_gen, x, y)
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


# 확률적 돌연변이, 확률에 따라 돌연변이가 발생하도록 한다.
# 돌연변이 조건에 해당하면 유전물질을 아예 새로 생성
def Mutation(list_gen, prob=0.1):
  event = np.random.choice((0, 1), p=[1-prob, prob])
  if event == True:
    mutant_list = np.array([])
    for i in range(2):
      value = Create_genome()
      mutant_list = np.concatenate([mutant_list, value], axis=0)
    
    mutant_list = np.reshape(mutant_list, (-1, 3))
    return mutant_list
  else:
    return list_gen

# 4개의 객체 중 적합도가 가장 작은 유전 객체 2개 
# + 유전 객체 2개 교차 구현한 것 합치기
def Combine_genome(list_1, list_2):
  return np.concatenate((list_1, list_2), axis=0)

def Fit(genlist_four, x, y, epochs, prob=0.1, period=None):
    for epoch in range(epochs):
        genlist_two= Select_appropriate(genlist_four, x, y)
        change_num = np.random.choice(3, 1)
        intersect_gen = Intersect_genome(genlist_two, change_num[0]) 
        intersect_gen = Mutation(intersect_gen, prob)
        genlist_four = Combine_genome(genlist_two, intersect_gen)  
        # period 매개변수에 따라 epoch 출력
        if period is not None and (epoch + 1) % period == 0:
            appr = Appropriate(genlist_four, x, y)
            print(f"Epoch: {epoch + 1}, Appropriate: {appr}")
            Display_genome(genlist_four, target=y, appr=appr, epoch=epoch+1)
    print('Complete!')
    return genlist_four

def Display_genome(genome, target, appr=None, epoch = None):
    # 유전자 값을 세로 막대 그래프로 표현
    if genome.ndim == 1:  # 1개의 유전자 입력
        plt.figure(figsize=(2, 4))
        
        # 파스텔 톤의 RGB 색상 사용
        green = (0.8, 0.9, 0.8)  # 연한 녹색
        violet = (0.9, 0.8, 0.9)  # 연한 보라색
        blue = (0.8, 0.8, 0.9)  # 연한 파란색
        
        # 각 유전자를 다른 색상의 겹쳐진 막대로 표현
        gene1, gene2, gene3 = genome
        
        # 세로 축 최대 높이를 20으로 설정
        plt.ylim(0, 20)
        
        plt.bar(0, gene1, color=green, width=0.5)
        plt.bar(0, gene2, bottom=gene1, color=violet, width=0.5)
        plt.bar(0, gene3, bottom=gene1+gene2, color=blue, width=0.5)
        
        # 각 유전자 값을 텍스트로 표시
        plt.text(0.15, gene1/2, f"w1x1: {gene1:.2f}", va='center', ha='right', color='k')
        plt.text(0.15, gene1+gene2/2, f"w2x2: {gene2:.2f}", va='center', ha='right', color='k')
        plt.text(0.06, gene1+gene2+gene3/2, f"b: {gene3:.2f}", va='center', ha='right', color='k')
        
        
        plt.xticks([])
        plt.yticks([0, target])
        if appr is not None:
            plt.text(-0.23, -1, f"Appropriate: {appr[0]}", va='top', ha='left', color='k')
        if epoch is not None:
            plt.suptitle(f"Epochs: {epoch}", fontsize=16, position = (0.5, 1))
        plt.show()
    else:  # 4개의 유전자 입력
        plt.figure(figsize=(8, 4))
        
        # 파스텔 톤의 RGB 색상 사용
        green = (0.8, 0.9, 0.8)  # 연한 녹색
        violet = (0.9, 0.8, 0.9)  # 연한 보라색
        blue = (0.8, 0.8, 0.9)  # 연한 파란색
        
        # 4개의 유전자를 subplot으로 표현
        for i, genes in enumerate(genome):
            plt.subplot(1, 4, i+1)
            
            gene1, gene2, gene3 = genes
            
            # 세로 축 최대 높이를 20으로 설정
            plt.ylim(0, 20)
            
            plt.bar(0, gene1, color=green, width=0.5)
            plt.bar(0, gene2, bottom=gene1, color=violet, width=0.5)
            plt.bar(0, gene3, bottom=gene1+gene2, color=blue, width=0.5)
            
            # 각 유전자 값을 텍스트로 표시
            plt.text(0.15, gene1/2, f"w1x1: {gene1:.2f}", va='center', ha='right', color='k')
            plt.text(0.15, gene1+gene2/2, f"w2x2: {gene2:.2f}", va='center', ha='right', color='k')
            plt.text(0.06, gene1+gene2+gene3/2, f"b: {gene3:.2f}", va='center', ha='right', color='k')
            
            plt.xticks([])
            plt.yticks([0, target])
        if appr is not None:
            for j in range(4):
                plt.subplot(1, 4, j+1)
                plt.text(-0.23, -1, f"Appropriate: {appr[j]}", va='top', ha='left', color='k')    
        if epoch is not None:
            plt.suptitle(f"Epochs: {epoch}", fontsize=16, position = (0.5, 1))
            
        plt.tight_layout()
        plt.show()