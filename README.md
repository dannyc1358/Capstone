Capstone Project: 

Optimizing Listing Price Recommendations for Brooklyn Properties

Research Question:

The research question was to what extent the age of the building, gross square feet, and number of residential units influence the predicted sale price used to determine the optimal listing price of the property. 

This research question is justified because accurate property pricing is crucial in the real estate market, as overpricing can lead to an extended time on the market, and underpricing can result in lost revenue. Thus, traditional pricing methods, such as an agent’s intuition or pricing based on a comparable sale, may not fully incorporate the complex relationships between characteristics, neighborhood dynamics, and market behavior. 

This research focused on residential property sales, where features such as building age, gross square footage, and number of residential units are known before listing. Analysis of historical sales data can help determine how these characteristics influence the sale price and how those insights can be used to recommend the optimal listing price.

Analysis:

The analysis examined the relationship between the characteristics and the property sale price using a log-linear multiple regression model. Next, the model was validated by splitting the dataset into a training, validation, and test dataset. Once the predicted sale price was determined, the optimization framework was used to calculate the optimal listing price. 

A multiple linear regression model was employed to assess the impact of each predictor variable on the target variable. The advantage of using this model is that it returns coefficients that explain the impact of each predictor. A disadvantage of this model is that it is sensitive to multicollinearity and assumes a linear relationship between the variables. The regression model can be represented as ln(sale price) = 13.2016 + (-0.1089 * Residential Units) + (0.0002 * Gross Sq Ft) + (0.0051 * Building Age).  
	As shown in the equation, a log transformation was applied to the target variable due to the extreme sale price values. An advantage of this technique is that it reduces skewness and improves model stability. A disadvantage is that small sale price values may be exaggerated with this technique, which is addressed by setting a minimum threshold.
	 
The model performance was evaluated with the train-test split technique. This was achieved by splitting the dataset into 70% training, 15% validation, and 15% testing sets. An advantage of this approach is that it ensures the model generalizes well to unseen data. A disadvantage is that it reduces the number of observations for training. Once the data has been split, the root mean squared error was calculated for both the validation dataset and the test set to evaluate predictive accuracy. The validation RMSE was 0.6349, and the test RMSE was 0.6058, which indicated that the model generalizes well to unseen data.
	 
Once the predicted sale price was obtained, the optimization framework was implemented to determine the optimal listing price. A dynamic pricing margin was applied to simulate actual market behavior based on building age and gross square footage. The equation to calculate the margin was: 
	margin = 0.04 + 0.02 (Building age < 25) + 0.01 (gross square footage> 1100) + 0.01 (gross square footage> 2000). 
	Then, optimal listing price = predictive sale price (1 + margin). 
	The advantage of this approach is that it displays predictive outputs as actionable pricing decisions. The disadvantage is that these rule-based margins may not capture all market determinants.

Results:

The results of the log-linear multiple regression analysis with optimization indicate that the building age, gross square footage, and the number of residential units have a statistically significant influence on the predicted sale price. The regression coefficient indicates that building age and gross square footage have a positive influence on the sale price. In contrast, the number of residential units has a negative impact on the sale price. Based on the coefficients, for every additional residential unit, the predicted sale price decreases by approximately 10.32%. For every additional gross square footage, there is a 0.022 percent increase in the predicted sale price. For every additional building age, the predicted sale price increases by 0.51%. Regarding the log constant of 13.2016, which represents the log sale price when all predictors are equal to zero, it is not interpretable since, in the actual real estate market, a building cannot have an age of 0, a size of 0, etc. As mentioned earlier, the validation RMSE was 0.6349 and the test RMSE was 0.6058, indicating a regression model that generalizes well to unseen data. Thus, these results reject the null hypotheses, supporting the alternative hypotheses that building age, gross square feet, and residential units significantly influence the predicted sale price used to determine the optimal listing price.

