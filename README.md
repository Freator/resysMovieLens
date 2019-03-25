# 推荐系统课程作业  
本次课程作业在small-movielens数据集的基础上，对用户（待续）  
**1. 变量说明**  
users :保存所有用户，不重复list类型  
userWatchedMovie :保存所有用户看过的所有电影，字典嵌套字典类型  
movieUser :保存用户与用户之间共同看过的电影，字典嵌套字典嵌套list  
userSimilarity :保存用户与用户之间的相似度（皮尔逊相似度）  
allUserTopNSim :保存每个用户都取前n(n=10)个最相似的用户，以及相似度  
recommendedMovies :从最相似的用户中推荐，每个相似用户推荐两部，同时计算出预测值并保存在这个变量里  
usersTest :测试集文件中的所有用户，同users  
userWatchedMovieTest :测试集文件中所有用户看过的所有电影，同userWatchedMovie  
movieAlsoInTest :保存推荐的电影正好也在用户测试数据中看过的那一些电影，以便后面进行MAE计算  
averageRating :保存每个用户对被推荐的电影的预测平均分  
eachUserMAE :保存对每个用户而言计算出的MAE
