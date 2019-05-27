在这之前所做的推荐系统的工作中，我们考虑并且比较了最相似用户数量`TOPN`和推荐的电影数`AMOUNT`两个变量对推荐系统结果的影响，具体可以查看前文的结果分析，在最后，同样也做了一些其他的考虑，由于诸多因素，还未能仔细验证。本次改进是针对授课老师所提出的几点想法进行的，主要在两个方面：（1）看与不看本身是否能影响评分相似度。也就是说，如果我们只是考虑用户看或者不看这部电影，不考虑评分，在这种情况下，用户之间的相似度会如何？（2）只考虑高分或者只考虑低分是否能影响评分相似度。也就是说，如果只是考虑用户共同看过的评分都高（记评分大于`3.5`为高分）的电影，那么会对相似度有怎样的影响？只考虑低分呢？  
根据以上想法，我们将之前推荐系统的`AMOUNT`设置为`5`，`TOPN`设置为`10`固定不变，并以此为`Baseline Model`，在改变一些条件后，对运算出来的结果进行比较。  
在本次实验中，我们考虑的是第二个方面，即只考虑用户共同看过的评分都高于`3.5`的电影，然后在这个基础上计算用户之间的相似度，从而进行推荐。数据方面，依然是使用前述实验中的`MovieLens`数据集。  
+ **对代码稍作改动，在计算用户之间共同看过的电影数是，增加判断条件如下：**  

	  for x in range(len(users)-1):  
		    movieUser.setdefault(users[x], {})  
		  for y in range(x+1, len(users)):  
			  movieUser[users[x]].setdefault(users[y], [])  
			  for m in userWatchedMovie[users[x]].keys():  
				  if m in userWatchedMovie[users[y]].keys() and (userWatchedMovie[users[y]][m] > 3.0 and userWatchedMovie[users[x]][m] > 3):  
					  movieUser[users[x]][users[y]].append(m)
+ **前后计算出的用户共同看过的电影数对比**  
  ![movieUser](../pictures/movieUser.png "Baseline Model下用户看过的电影")  
  上图是`Baseline Model`下用户看过的电影，下图是在考虑高分情况下用户看过的电影。  
  ![movieUser_highRating](../pictures/movieUser_highRating.png "考虑高分情况下用户看过的电影")  
+ **相似度的比较**   
  ![similarity_highRating](../pictures/similarity_highRating.png "相似度的比较")  
+ **`TOP10`相似度用户的比较**  
  ![allUserTop10Sim_highRating](../pictures/allUserTop10Sim_highRating.png "Top10相似度用户的比较")  
+ **系统`MAE`结果的比较**  
  ![MAE_highRating](../pictures/MAE_highRating.png "MAE结果的比较")  
  ![chart1_highRating](../pictures/chart1_highRating.png "MAE比较图表显示")  
  

@Date : 2019/5/6  
@Author : [Freator Tang](https://github.com/freator)  
@Email : bingcongtang@gmail.com  

Update（5/19）
----------
我们使用数据分割将原数据`u.data`分割成训练集`TrainData`和测试集`TestData`（根据时间戳区分，按照用户和时间戳排序后对每个用户进行了`8:2`的分割），然后再次进行了如下实验：  
+ **只考虑每个人的推荐数量`AMOUNT`和相似度最高的推荐人数`TOPN`**  
   `AMOUNT = 5`，`TOPN = 10`的推荐结果是**0.922849**  
   ![result1_0513](../pictures/result1_0513.png "结果1")  
   `AMOUNT = 10`，`TOPN = 10`的推荐结果是**0.886590**  
   ![result2_0513](../pictures/result2_0513.png "结果2")  
+ **只考虑高分的情况**  
   `AMOUNT = 5`，`TOPN = 10`的推荐结果是**0.871738**  
   ![result3_0513](../pictures/result3_0513.png "结果3")  
   `AMOUNT = 10`，`TOPN = 10`的推荐结果是**0.915294**  
   ![result4_0513](../pictures/result4_0513.png "结果4")  

----  
考虑到数据集本身可能给实验结果带来的影响，所以又使用了另外一组相对更多的数据（`2.36M`）来进行实验，同样按照上述过程先进行数据的分割，然后进行实验，结果如下表格和折线图所示：  
>    | |Amount=5|Amount=10|
>    |:--:|:--:|:--:|
>    |BaseLine|0.847794|0.801307|
>    |HighRating|0.888999|0.839014|
>    |LowRating|0.859086|0.864883|  
    
>    ![resultMAE_0513](../pictures/resultMAE_0513.png "MAE比较图表显示")  

除此之外，还用了更大的数据进行测试`23.6M`，但是测试时间比较长，平均每次需要`20`分钟左右。下面贴上`Amount=10`，`TOPN=10`的测试结果：  
![result7_0513](../pictures/result7_0513.png "结果7")  



@Date : 2019/5/19  
@Author : [Freator Tang](https://github.com/freator)  
@Email : bingcongtang@gmail.com  


Update（5/27）
----------  
在本周的实验过程中，我们只考虑用户共同看过的电影中的低分情况对推荐系统的影响，通过实验比较，发现该种情况还是存在一定的问题。与前述实验相同的是，使用数据分割将原数据分割成训练集`TrainData`和测试集`TestData`（根据时间戳区分，按照用户和时间戳排序后对每个用户进行了`8:2`的分割），不同的是，我们增大了数据量，本次实验使用的是`MovieLens`中数据大小为`2.36M`的数据，进行了实验，实验变量依旧为最相似用户数量`TOPN`和推荐的电影数`AMOUNT`。实验结果如下：  
+ **最相似用户数量不变 `TopN=10`，逐渐增大推荐的电影数量**  

>    | Amount|MAE|  
>    |:--:|:--:|  
>    |5|0.882669|  
>    |7|0.869766|  
>    |10|0.848181|  
>    |15|0.829320|  
>    |20|0.826171|  

>    ![resultMAE_052701](../pictures/resultMAE_052701.png "MAE比较图表显示")  
>    从图片结果上，明显可以看出在最相似的用户数量不变的情况下，推荐的电影数量越多，MAE越小。可以想到的是，在训练集中推荐的电影数量越多，也就能能更大几率的在测试集中命中跟多的电影，从而使得结果看起来越来越好。  

+ **推荐的电影数量不变 `AMOUNT=5`，逐渐增大最相似用户的个数**   

>    | TOPN|MAE|  
>    |:--:|:--:|  
>    |5|0.850309|  
>    |10|0.882669|  
>    |15|0.920586|  
>    |20|0.938450|  
>    |25|0.969128|  

>    ![resultMAE_052702](../pictures/resultMAE_052702.png "MAE比较图表显示")  
>    从结果上看，并不理想，笔者有以下几点考虑：（1）单从低分的角度看，虽然存在用户比较喜欢这个类型的电影，只是因为电影质量等问题打了低分的情况，但是更多更常见的情况还是用户因为不喜欢，电影不好看所以才打了低分，所以在只考虑低分的情况下，能够正确预测用户喜欢的电影的概率不高，换而言之，推荐效果并不好；（2）推荐电影数量不变，逐渐增大相似用户个数的情况下，感觉像是有点将越来越不相似的用户都加进来计算了，这样得到的推荐电影数量会增多，但是能够正确命中的和正确预测的电影数量并不多，从而也会导致推荐结果变差。  


@Date : 2019/5/27  
@Author : [Freator Tang](https://github.com/freator)  
@Email : bingcongtang@gmail.com  
