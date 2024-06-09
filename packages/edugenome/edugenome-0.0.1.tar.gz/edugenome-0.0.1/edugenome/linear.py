# -*- coding: utf-8 -*-
import numpy as np

# 표준편차 sigma, 평균 mu인 정규분포에서 3개를 추출
# 각각 w_1, w_2, b임
def Create_genome(sigma=2, mu=0):
    value = sigma*np.random.randn(3) + mu
    return value

# 유전 객체 4개 만들기
def Create_4genome(sigma=2, mu=0):
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

# 감수분열은 부모 유전자를 나누고 뒤집은 것으로 하자
# 번식은 부모 유전자에 감수분열된 값을 더한 것으로 한다.
def Intersect_genorm(list_gen):
  temp_list = list_gen.copy()
  temp_list = temp_list/2 # 2로 나눔
  temp_list = temp_list[::-1] # 뒤집어줌

  copy_list = list_gen.copy()
  copy_list[0] = copy_list[0] + temp_list[0]
  copy_list[1] = copy_list[1] + temp_list[1]
  return copy_list

# 확률적 돌연변이, 확률에 따라 돌연변이가 발생하도록 한다.
# 돌연변이 조건에 해당하면 유전물질을 아예 새로 생성
def Mutation(list_gen, prob=0.2):
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

def Fit(genlist_four, x, y, epochs, prob=0.1):
    for epoch in range(epochs):
        genlist_two= Select_appropriate(genlist_four, x, y)
        intersect_gen = Intersect_genorm(genlist_two) 
        intersect_gen = Mutation(intersect_gen, prob)
        genlist_four = Combine_genome(genlist_two, intersect_gen)  
    print('Complete!')
    return genlist_four
