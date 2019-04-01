# -*- coding:utf-8 -*-
from math import sqrt
import os

TOPN = 10  # 设置每个用户相似度最高的前TOPN个用户
AMOUNT = 5  # 设置前TOPN个相似用户中每个用户给当前用户推荐的电影数量

# 读取训练集数据文件
filePath = './data/u1.base'
users = []  # 保存所有用户，不重复list类型
userWatchedMovie = {}  # 保存所有用户看过的所有电影，字典嵌套字典类型
movieUser = {}  # 保存用户与用户之间共同看过的电影，字典嵌套字典嵌套list
with open(filePath, 'r') as trainFile:
    # 计算所有的用户以及用户看过的电影和评分,保存到相关字典变量中
    for line in trainFile:
        # type(line)是string类型,其中分离出来的userId等也都是string类型
        # strip()方法是去除指定首尾字符
        (userId, movieId, rating, timestamp) = line.strip('\n').split('\t')
        if userId not in users:
            users.append(userId)
            userWatchedMovie.setdefault(userId, {})
        userWatchedMovie[userId][movieId] = float(rating)


# 计算用户与用户共同看过的电影
for x in range(len(users)-1):
    movieUser.setdefault(users[x], {})
    for y in range(x+1, len(users)):
        movieUser[users[x]].setdefault(users[y], [])
        for m in userWatchedMovie[users[x]].keys():
            if m in userWatchedMovie[users[y]].keys():
                movieUser[users[x]][users[y]].append(m)

# 计算用户与用户之间的相似度，皮尔逊相似度
userSimilarity = {}
for a in movieUser.keys():
    userSimilarity.setdefault(a, {})
    for b in movieUser[a].keys():
        userSimilarity[a].setdefault(b, 0)
        if len(movieUser[a][b]) == 0:
            userSimilarity[a][b] = 0  # 如果两个人没有看过同一部电影，则相似度为0
            continue
        else:
            # 下面开始进行相似度的计算，皮尔森相关系数
            avgUserA = 0  # A用户打分的平均值
            avgUserB = 0  # B用户打分的平均值
            numerator = 0  # Pearson的分子部分
            denominatorA = 0  # Pearson的分母A部分
            denominatorB = 0  # Pearson的分母B部分
            count = len(movieUser[a][b])  # 保存两个用户共同看过的电影的数量
            # 这里用到了一个召回率的因素，因为在前述的实验过程中，发现最相似的用户
            # 相似度达到了 1.0 ，感觉有点不正常，比如说用户1和用户9，共同只看过两部电影，但是相似度却等于 1.0
            # 这个是不太正确的，所以加入了召回率的考量
            # 加入之后，发现用户1和用户9的相似度从1.0下降到0.19，感觉是比较合理的
            factor = 0
            if count > 20:  # 20是自己指定的
                factor = 1.0
            else:
                if count < 0:
                    factor = 0
                else:
                    factor = (-0.0025 * count * count) + (0.1 * count)
            for movie in movieUser[a][b]:  # 对于两个用户都看过的每一部电影，进行计算
                avgUserA += float(userWatchedMovie[a][movie])
                avgUserB += float(userWatchedMovie[b][movie])
            avgUserA = float(avgUserA / count)
            avgUserB = float(avgUserB / count)
            # print(avgUserA)
            # print(avgUserB)
            for m in movieUser[a][b]:
                # print(userWatchedMovie[a][m])
                tempA = float(userWatchedMovie[a][m]) - avgUserA
                tempB = float(userWatchedMovie[b][m]) - avgUserB
                # print(tempA)
                numerator += tempA * tempB
                denominatorA += pow(tempA, 2) * 1.0
                denominatorB += pow(tempB, 2) * 1.0
            # print(numerate)
            if denominatorA != 0 and denominatorB != 0:
                userSimilarity[a][b] = factor * (numerator / (sqrt(denominatorA * denominatorB)))
            else:
                userSimilarity[a][b] = 0


# 每个用户都取前n个最相似的用户，以便后续进行推荐
# singleUserTopNSim = {}
allUserTopNSim = {}

for currentUserId in users:  # 计算当前用户的最相似的前n个用户
    singleUserSim = {}  # 存放单个用户对所有用户的相似度
    allUserTopNSim.setdefault(currentUserId, {})  # 存放所有用户的TopN相似的用户
    for compareUserId in users:
        if currentUserId == compareUserId:
            break
        else:
            singleUserSim[compareUserId] = userSimilarity[compareUserId][currentUserId]
    if int(currentUserId) != len(users):
        singleUserSim.update(userSimilarity[currentUserId])
    # print(currentUserId, end=' ')
    # print(singleUserSim)
    # python中的字典是无序的，但是有时候会根据value值来取得字典中前n个值，
    # 此处思想是将字典转化成list，经过排序，取得前n个值，再将list转化回字典
    # 进行排序，取前N个相似的用户，此时singleSortedSim是一个list类型：[(key,value),(key,value),(key,value),...]
    singleSortedSim = sorted(singleUserSim.items(), key=lambda item: item[1], reverse=True)
    singleTopN = singleSortedSim[:TOPN]  # 取出前N个最相似的值
    for single in singleTopN:
        allUserTopNSim[currentUserId][single[0]] = single[1]  # 保存当前用户计算出的TopN个相似用户以及相似度


# 从最相似的用户中推荐，每个相似用户推荐number部，那么每个用户就能得到推荐的number*10部电影
recommendedMovies = {}
for oneUser in allUserTopNSim.keys():
    recommendedMovies.setdefault(oneUser, {})
    for simUser in allUserTopNSim[oneUser].keys():
        oneMovieList = []
        simUserMovieList = []
        number = 0
        recommendedMovies[oneUser].setdefault(simUser, {})
        for movie in userWatchedMovie[simUser].keys():
            if number >= AMOUNT:  # 每个人推荐数量为number部的电影数
                break
            if movie not in userWatchedMovie[oneUser].keys():  # and (movie not in recommendedMovies[oneUser]):
                # 计算预测权值
                if int(oneUser) < int(simUser):
                    # oneMovieList.append(list(movieUser[oneUser][simUser]))
                    # simUserMovieList.append(list(movieUser[oneUser][simUser]))
                    length = len(movieUser[oneUser][simUser])
                    #simUserMovieList.append(movie)
                    #tupleOne = tuple(oneMovieList)
                    #tupleSim = tuple(simUserMovieList)
                    sumOne = 0.0
                    sumSim = 0.0
                    for i in movieUser[oneUser][simUser]:
                        sumOne += userWatchedMovie[oneUser].get(i)
                        sumSim += userWatchedMovie[simUser].get(i)
                    sumSim += userWatchedMovie[simUser].get(movie)
                    avgOneUser = sumOne / length
                    avgSimUser = sumSim / (length + 1)
                    predictionRating = avgOneUser + (userWatchedMovie[simUser][movie] - avgSimUser)
                    recommendedMovies[oneUser][simUser][movie] = predictionRating  #这是一个需要计算的值
                    number += 1
                else:
                    # oneMovieList.append(movieUser[simUser][oneUser])
                    # simUserMovieList.append(movieUser[simUser][oneUser])
                    length = len(movieUser[simUser][oneUser])
                    # simUserMovieList.append(movie)
                    sumOne = 0
                    sumSim = 0
                    for i in movieUser[simUser][oneUser]:
                        sumOne += userWatchedMovie[oneUser].get(i)
                        sumSim += userWatchedMovie[simUser].get(i)
                    sumSim += userWatchedMovie[simUser].get(movie)
                    avgOneUser = sumOne / length
                    avgSimUser = sumSim / (length + 1)
                    predictionRating = avgOneUser + (userWatchedMovie[simUser][movie] - avgSimUser)
                    recommendedMovies[oneUser][simUser][movie] = predictionRating  #这是一个需要计算的值
                    number += 1
            else:
                continue
'''
# 读取测试集数据文件
filePathTest = './data/u1.test'
usersTest = []  # 保存所有用户，不重复list类型
userWatchedMovieTest = {}  # 保存所有用户看过的所有电影，字典嵌套字典类型
with open(filePathTest, 'r') as testFile:
    # 计算所有的用户以及用户看过的电影和评分,保存到相关字典变量中
    for lineTest in testFile:
        (userIdTest, movieIdTest, ratingTest, timestampTest) = lineTest.strip('\n').split('\t')
        if userIdTest not in usersTest:
            usersTest.append(userIdTest)
            userWatchedMovieTest.setdefault(userIdTest, {})
        userWatchedMovieTest[userIdTest][movieIdTest] = ratingTest
'''
'''
# 要找到在测训练集中用户没有看过，但是在测试集中用户看过并且被推荐过的电影，这样后面好计算MAE(平均绝对误差)
movieRecommendedAlsoInTest = {}
for user in usersTest:
    movieRecommendedAlsoInTest.setdefault(user, [])
    for m in recommendedMovies[user]:
        if m in userWatchedMovieTest[user].keys():
            movieRecommendedAlsoInTest[user].append(m)
'''

'''
writeFilePath = './data/movieuser.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in movieUser.keys():
    for n in movieUser[m].keys():
        writeFile.writelines([m, '\t', n, '\t', str(movieUser[m][n])])
        writeFile.write('\n')
writeFile.close()
'''

writeFilePath = './data/userWatchedMovie.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in userWatchedMovie.keys():
    for n in userWatchedMovie[m].keys():
        writeFile.writelines([m, '\t', n, '\t', str(userWatchedMovie[m][n])])
        writeFile.write('\n')
writeFile.close()

writeFilePath = './data/allUserTop10Sim.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in allUserTopNSim.keys():
    for n in allUserTopNSim[m].keys():
        writeFile.writelines([m, '\t', n, '\t', str(allUserTopNSim[m][n])])
        writeFile.write('\n')
writeFile.close()


writeFilePath = './data/recoMovieWithRating.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in recommendedMovies.keys():
    for n in recommendedMovies[m].keys():
        writeFile.writelines([m, '\t', n, '\t', str(recommendedMovies[m][n])])
        writeFile.write('\n')
writeFile.close()


writeFilePath = './data/userSimilarity.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in userSimilarity.keys():
    for n in userSimilarity[m].keys():
        writeFile.writelines([m, '\t', n, '\t', str(userSimilarity[m][n])])
        writeFile.write('\n')
writeFile.close()
