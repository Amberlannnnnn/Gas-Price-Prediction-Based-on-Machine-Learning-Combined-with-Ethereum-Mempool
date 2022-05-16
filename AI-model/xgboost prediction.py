from turtle import color
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import seaborn as sns

# 读文件
data = pd.read_csv('D:/Documents/blockdata/14414732-CP.csv')
data.dropna(axis=0, subset=['middlle_gp'], inplace=True)

# 切分数据输入：特征 输出：预测目标变量
y = data.middlle_gp
X = data.drop(['middlle_gp'], axis=1).select_dtypes(exclude=['object'])

# 切分训练集、测试集,切分比例7.5 : 2.5
train_X, test_X, train_y, test_y = train_test_split(X.values, y.values, test_size=0.25)

#sns.pairplot(data[0:500],vars=["base_fee_per_gas","avg_mf","avg_mp","gasnow_rpd","middlle_gp"],kind="reg",palette="husl")
#plt.show

# 空值处理，默认方法：使用特征列的平均值进行填充
my_imputer = SimpleImputer()
train_X = my_imputer.fit_transform(train_X)
test_X = my_imputer.transform(test_X)

# 调用XGBoost模型，使用训练集数据进行训练（拟合）
# Add verbosity=2 to print messages while running boosting
my_model = xgb.XGBRegressor(objective='reg:squarederror', verbosity=2)  # xgb.XGBClassifier() XGBoost分类模型
my_model.fit(train_X, train_y, verbose=False)

#print(my_model.get_params())

predictions_t = my_model.predict(train_X)

# 6.使用模型对测试集数据进行预测
predictions = my_model.predict(test_X)

#训练集评判指标
print("Mean Absolute Error : " + str(mean_absolute_error(predictions_t, train_y)))
print("Mean Squared Error : " + str(mean_squared_error(train_y, predictions_t)))
#rmse_test=mean_squared_error(predictions, test_y) ** 0.5
print("RMSE : " + str(mean_squared_error(train_y,predictions_t)** 0.5))
print("r2_score : " +str(r2_score(train_y, predictions_t)))

# 7.对模型的预测结果进行评判（平均绝对误差）
print("Mean Absolute Error : " + str(mean_absolute_error(predictions, test_y)))
print("Mean Squared Error : " + str(mean_squared_error(test_y, predictions)))
#rmse_test=mean_squared_error(predictions, test_y) ** 0.5
print("RMSE : " + str(mean_squared_error(test_y,predictions)** 0.5))
print("r2_score : " +str(r2_score(test_y, predictions)))

fig = plt.figure(facecolor='white')
ax = fig.add_subplot(111)
#ax.axis["right"].set_visible(False)
#ax.axis["top"].set_visible(False)
ax.plot(test_y[1000:1100], label='True Data', color = 'black', linewidth= 1.7)
plt.plot(predictions[1000:1100], label='Prediction', color = 'lime', linewidth= 1.7, linestyle='dashdot')
plt.legend(frameon = False, loc='upper right',fontsize='small')
#plt.rcParams['figure.figsize']=(6.0,4.0)
plt.rcParams['savefig.dpi'] = 720 #像素
plt.rcParams['figure.dpi'] = 720 #分辨率
plt.show()