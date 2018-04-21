
### Analysis of the effect of immigration on the nation

### How to run code:

Run this command in the cmd:
python “filepath...\RunAnalysis.py”

### Question:
My project looked to delve into the effects of immigration on a nation’s culture and attitudes. I did this by comparing how various data regarding nations changes over time: GDP growth, happiness, crime rates, unemployment, social spending and inequality of incomes from 2000 to 20015. I then compared how immigration rates in various countries have affected these values through Pearson's Correlation Coefficient.

### Hypothesis:
There are many other factors that affect the data that I was testing. For this reason, I hypothesized I would only be able to find a moderate correlation with immigration rates and the other data sets. I believed that I would be able to find a moderate correlation with a increase in unemployment, increase in GDP and an increase in economic inequality. This is because immigrants, although benefiting the economy, generally compete with low skill workers. This, in turn, would hurt them and increase economic inequality. Unemployment would go up due to an increase in workers in the workforce. Normally this would cause wages to drop, however, with minimum wage, this would reduce employment instead.

### Method:
1. Data was collected
2. Sorted the data into 2d dictionaries where the first key is the iso 3 code for the country that the data was taken from. The second key is the year that the data was taken from.
3. The immigration data was then normalized for the country's population size
4. The first analysis using Pearson's Correlation Coefficient took place. This looked to measure the correlation of characteristics of countries and immigration rates. It did this by not measuring the change of the given countries values given a immigration change. This was largely done due to curiosity, however, it also help to give some context during the analysis. 
4. The data sets were then modified to measure the change of the given values over time, rather than a country's static values: value[year] - value[year-1]
5. The second analysis using Pearson's Correlation Coefficient took place. This looked to measure the effect of immigration changes.
6. The data was graphed

Where was the data collected: https://drive.google.com/open?id=1rJP9qdX5ZOuM2sfjRgx4GZWGQvoB-3rdvRM96-WDsaI

### Results:

### Conclusion:
The first figure found that immigration rates are higher in countries with low unemployment and high life satisfaction. This makes sense due to the fact that these are viewed as positive traits and most would want to come to a place where people are happy and successful. It also makes sense that happy and successful people would be more likely to take the risk of letting people into their country. This is because they are in a better place to take a risk.
Surprisingly, the second figure found a small correlation with a reduction in social spending and unemployment with an increase in immigration rates. This is surprising, however, it must be noted with all my results that correlation does not equal causation. Other factors that would have affected these values have not been accounted for. People could have wanted to come to these countries due to their better economies and dropping unemployment. Also, the correlation with all my results is very small to begin with. Less surprisingly, the second figure found a small correlation with increased inequality of incomes and gdp growth.
