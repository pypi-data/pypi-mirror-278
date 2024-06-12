# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# (4, 4)의 유전 객체 생성
def Create_genome():
  return np.random.choice((0, 1), (4, 4))

# (4, 4)의 유전 객체 4개 생성
def Create_4genome():
    gen_list = Create_genome()
    for i in range(3):
        value = Create_genome()
        gen_list = np.vstack((gen_list, value))
    gen_list = np.reshape(gen_list, (-1, 4, 4))
    return gen_list

# 목표값(target)에 대한 적합도 계산
def Appropriate(list_gen, target):
  appro_list = np.array([])
  for genome in list_gen:
    appro = np.array([np.sum(np.abs(target-genome))])
    appro_list = np.concatenate([appro_list, appro], axis=0)
  return appro_list

# 개체 중 적합도가 가장 작은 2개의 객체 선택하기
def Select_appropriate(list_gen, target):
  list_appro = Appropriate(list_gen, target) # 적합도 배열 
  argsort = list_appro.argsort() # 적합도 배열 인덱스 오름차순 정렬
  select_one = list_gen[argsort[0]] # 적합도가 가장 작은 객체
  select_two = list_gen[argsort[1]] # 적합도가 두 번째로 작은 객체
  two_genlist = np.vstack((select_one, select_two)) # 적합도 객체 쌓기 (8, 4)
  two_genlist = np.reshape(two_genlist, (-1, 4, 4)) # shape 재정의 (2, 4, 4)
  return two_genlist

# 감수 분열을 이용한 교차 구현
# 감수 분열을 하면 행 1-2(인덱스 0, 1) , 행 3-4(인덱스 2, 3)로 분열된다. 
# 서로 교차할 물질은 행 3-4번 끼리 서로 교체함.
def Intersect_genome(list_gen):
  temp_list = np.vstack((list_gen[0][2:4], list_gen[1][2:4]))
  copy_list = list_gen.copy()
  copy_list[0][2:4] = temp_list[2:4]
  copy_list[1][2:4] = temp_list[0:2]
  return copy_list

# 돌연변이가 발생하면 위의 행 2개 또는 아래 행 2개를 무작위의 0, 1로 변경됨.
def Mutation(list_gen, prob=0.1):
  event = np.random.choice((0, 1), p=[1-prob, prob])
  if event == True:
    mutant_list = np.random.choice((0, 1), (4, 4))
    copy_list = list_gen.copy()
    high_low = np.random.choice((0, 1), p=[0.5, 0.5])
    if high_low == True:
      copy_list[0][0:2] = mutant_list[0:2]
      copy_list[1][0:2] = mutant_list[2:4]
    else:
      copy_list[0][2:4] = mutant_list[0:2]
      copy_list[1][2:4] = mutant_list[2:4]
    return copy_list
  else:
    return list_gen

# 4개의 객체 중 적합도가 가장 작은 유전 객체 2개 + 유전 객체 2개 교차 구현한 것 합치기
def Combine_genome(list_1, list_2):
  return np.concatenate((list_1, list_2))

def Fit(genlist_four, target, epochs, prob=0.1, period=None):
    for epoch in range(epochs):
        genlist_two= Select_appropriate(genlist_four, target)
        intersect_gen = Intersect_genorm(genlist_two) 
        intersect_gen = Mutation(intersect_gen, prob=0.1)
        genlist_four = Combine_genome(genlist_two, intersect_gen) 
        
        # period 매개변수에 따라 epoch 출력
        if period is not None and (epoch + 1) % period == 0:
            appr = Appropriate(genlist_four, target)
            print(f"Epoch: {epoch + 1}, Appropriate: {appr}")
            Display_image(genlist_four, appr, epoch+1)
    print('Complete!')    
    return genlist_four
    
# 이미지 출력 기능
def Display_image(image, appr=None, epoch=None):
    if image.shape == (4, 4):
        # (4, 4) 이미지가 입력되는 경우
        plt.figure(figsize=(4, 4))
        plt.xticks(np.arange(0, 4, 1))
        plt.yticks(np.arange(0, 4, 1))
        plt.imshow(image, cmap='gray')
        if epoch is not None:
            plt.title(f"Epochs: {epoch}", fontsize=16, loc='center')
        if appr is not None:
            plt.text(0.5, -0.2, f"Appropriate: {appr[0]}", ha='center', transform=plt.gca().transAxes)
        plt.show()
    elif image.shape == (4, 4, 4):
        # (4, 4, 4) 이미지가 입력되는 경우
        plt.figure(figsize=(12, 6))
        for i in range(4):
            plt.subplot(1, 4, i+1)
            plt.xticks(np.arange(0, 4, 1))
            plt.yticks(np.arange(0, 4, 1))
            plt.imshow(image[i], cmap='gray')
        if epoch is not None:
            plt.suptitle(f"Epochs: {epoch}", fontsize=16, position = (0.5, 0.75))
        if appr is not None:
            for j in range(4):
                plt.subplot(1, 4, j+1)
                plt.text(0.5, -0.2, f"Appropriate: {appr[j]}", ha='center', transform=plt.gca().transAxes)
        plt.show()
    else:
        print("입력 이미지의 형태가 올바르지 않습니다.")
