# -*- coding: utf-8 -*-
import os

# 读取推荐文件以及推荐的电影和预测评分文件
recommendedWithRating = {}
fileRecom = './data/recoMovieWithRating.txt'
reader = open(fileRecom, 'r')
for line in reader:
    (oneUser, simUser, movieRating) = line.strip('\n').split('\t')
    recommendedWithRating.setdefault(oneUser, {})
    recommendedWithRating[oneUser].setdefault(simUser, eval(movieRating))
reader.close()


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
        userWatchedMovieTest[userIdTest][movieIdTest] = float(ratingTest)

# 从推荐的电影和测试集中找到一起看过的电影，这样好计算MAE
movieAlsoInTest = {}  # 保存推荐的电影正好也在用户测试数据中的那一些电影
for oneUser in usersTest:  # 这里用userTest是因为里面会少了一些训练集中的user，即userId是不连续和不完整的
    movieAlsoInTest.setdefault(oneUser, [])
    for simUser in recommendedWithRating[oneUser].keys():
        for movie in recommendedWithRating[oneUser][simUser].keys():
            if movie in userWatchedMovieTest[oneUser].keys():
                movieAlsoInTest[oneUser].append(movie)
            else:
                continue


# 判断推荐的电影的数量，如果为0，则表示不命中
countNull = 0
countNotNull = 0
for i in movieAlsoInTest.keys():
    if len(movieAlsoInTest[i]) != 0:
        countNotNull += 1
    else:
        countNull += 1

# 计算每个用户被推荐的每部电影的次数和平均分
averageRating = {}  # 保存每个用户对被推荐的电影的预测平均分
for oneUser in usersTest:
    averageRating.setdefault(oneUser, {})
    for simUser in recommendedWithRating[oneUser].keys():
        for movie in recommendedWithRating[oneUser][simUser].keys():
            averageRating[oneUser].setdefault(movie, [0, 0.0, 0.0])  # list中第一个是记录的推荐了这部电影的次数，第二个是记录的推荐了该电影的预测评分的总和，第三个是取预测平均值
            averageRating[oneUser][movie][0] += 1
            averageRating[oneUser][movie][1] += recommendedWithRating[oneUser][simUser].get(movie)
    for each in averageRating[oneUser].keys():
        averageRating[oneUser][each][2] = averageRating[oneUser][each][1] / averageRating[oneUser][each][0]


# 计算对每个用户而言的 MAE
eachUserMAE = {}
for oneUser in averageRating.keys():
    count = 0  # MAE的分母部分
    sumD = 0.0  # MAE的分子部分
    eachUserMAE.setdefault(oneUser, 0.0)
    for movie in movieAlsoInTest[oneUser]:
        count += 1
        sumD += abs(averageRating[oneUser][movie][2] - userWatchedMovieTest[oneUser].get(movie))
    if count == 0:
        eachUserMAE[oneUser] = -1
    else:
        eachUserMAE[oneUser] = sumD / count

# 计算总体的 MAE
recommendedMAE = 0.0
countMAE = 0  # 保存有效的MAE，考虑到有些推荐未命中，即无法验证，这一部分就剔除，不做计数
for oneUser in eachUserMAE.keys():
    if eachUserMAE[oneUser] != -1:
        countMAE += 1
        recommendedMAE += eachUserMAE[oneUser]
recommendedMAE = recommendedMAE / countMAE


writeFilePath = './data/movieAlsoInTest.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in movieAlsoInTest.keys():
    writeFile.writelines([m, '\t', str(movieAlsoInTest[m])])
    writeFile.write('\n')
writeFile.close()

writeFilePath = './data/averageRating.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in averageRating.keys():
    for n in averageRating[m].keys():
        writeFile.writelines([m, '\t', n, '\t', str(averageRating[m][n])])
        writeFile.write('\n')
writeFile.close()

writeFilePath = './data/eachUserMAE.txt'
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)
writeFile = open(writeFilePath, 'w')
for m in eachUserMAE.keys():
    writeFile.writelines([m, '\t', str(eachUserMAE[m])])
    writeFile.write('\n')
writeFile.close()
'''
print(recommendedWithRating)
print(userWatchedMovieTest)
print(movieAlsoInTest)
print(len(usersTest))
print(countNotNull)
print(countNull)
print(averageRating)
print(eachUserMAE)
print(recommendedMAE)
'''
