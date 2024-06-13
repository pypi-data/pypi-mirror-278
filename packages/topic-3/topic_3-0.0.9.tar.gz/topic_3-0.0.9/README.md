# Introduction
This project aims to provide a method to replicate our experiment results. 
We are expected to utilize Elastic Weight Consolidation (EWC) algorithm to 
improve the performance of multivariate time-series prediction.

# Model Choice
This project provides eight algorithm to choose, including 
MLP / CNN/ GDN / RNN/ GRU/ LSTM/ LSTMVAE / Transformer.


# Dataset Structure
- steel
  - TEst
    - Task1(拉速1.2)
       - 板柸1_9后半段数据
          - list.txt (names of multiple sensors)
          - test.csv (multivariate time series data)
    - Task2(拉速1)
       - 板柸2_4后半段数据
          - list.txt 
          - test.csv
    - Task3(拉速1.4)
       - 板柸3_3后半段数据
          - list.txt
          - test.csv
  - TRain
     - Task1(拉速1.2)
        - 板柸1_1数据
           - list.txt
           - train.csv
        - 板柸1_2数据
           - list.txt
           - train.csv
        - 板柸1_9数据
           - list.txt
           - train.csv
        - 板柸1_10数据
           - list.txt
           - train.csv
        - 板柸1_11数据
           - list.txt
           - train.csv
    - Task2(拉速1.2)
        - 板柸2_1数据
           - list.txt
           - train.csv
        - 板柸2_4前半段数据
           - list.txt
           - train.csv
    - Task3(拉速1.4)
        - 板柸3_1数据
           - list.txt
           - train.csv
        - 板柸3_3前半段数据
           - list.txt
           - train.csv
 
# Experimental Results
When you successfully complete the experiment, you should see the following figures in each task stage:

- Loss Curve for validation dataset
![image](topic_3/show_img/Figure_1.png)

- Loss Curve for training dataset
![image](topic_3/show_img/Figure_2.png)
  
- Comparison with prediction and observation 
![image](topic_3/show_img/Figure_3.png)
  
- Scatter plot with Regression Line
![image](topic_3/show_img/Figure_4.png)
  
- Residual Distribution
![image](topic_3/show_img/Figure_5.png)
  
# Requirements
- python==3.10.2
- torch==1.12.0
- torch-geometric==2.2.0
- torch-scatter==2.0.9
- torch-sparse==0.6.14
- numpy==1.22.3
- matplotlib==3.5.2
