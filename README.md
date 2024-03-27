# ISO14091-assessment-climate-data
Scripts utilized for processing climate data retrieved from http://pclima.inpe.br/analise/, employed in a climate change risk assessment.
=============================== ENGLISH ==========================================

The data was manually obtained from the platform "http://pclima.inpe.br/analise/" as automated data retrieval via API was down.

The selections made were:

Data set: Regional Model
Model: Eta
Experiment: All (BESM, CANESM2, HADGEM2-ES, MIROC5)
Scenarios: All (Historical, RCP4.5, and RCP8.5)
Period (for RCP4.5 and RCP8.5): All (2011/2040, 2041/2070, 2071/2100)
Type: (Mean and Anomaly)
Variables: CDD, CWD, R95p, RX1day, RX5day, SDII, TX90p, UR, W10M
Frequency: Annual

The location "São Sebastião-SP" was selected by typing it into the search.
Clicked on the "line graph" button and within the pop-up clicked on "save.csv". These data are saved in the "Raw_Data" folder organized by model and variable.

After obtaining the various data, the three periods were joined into a single .csv file for each combination of variable, model, scenario, and type using the script "aggregate-data.py". For example, the three csv files containing the periods (2011/2040), (2041/2070), and (2071/2100) for the means of the CDD variable in the BESM model in the RCP8.5 scenario were merged into a single file containing this information in the filename. These new files were saved in the "Compiled-Data" folder.

Then, using the script "slopes-plot-trendlines.py", the lines were calculated via linear regression, the graphs of the points and the trend line were plotted, and with the script "mann-kendall.py", the Mann-Kendall tests were performed for each data set, i.e., for each file obtained from the first script. The script asks for the end year of the calculation and is saved in a folder containing "Processed-Data/chosen year".

Finally, with the p-values obtained from the Mann-Kendall test, a combined p-value was obtained using the Fischer method via the script "fischer-confidence.py". Confidence in the result was ranked using the following criteria:
Very High Confidence: p-value < 0.01
High Confidence: 0.01 ≤ p-value < 0.05
Medium Confidence: 0.05 ≤ p-value < 0.1
Low Confidence: 0.1 ≤ p-value < 0.2
Very Low Confidence: p-value ≥ 0.2


=============================== PORTUGUESE ==========================================

Os dados foram obtidos manualmente na plataforma "http://pclima.inpe.br/analise/" dado que a obtenção de dados automatizada via API estava fora do ar.

As seleções adotadas foram:

Conjunto de dados: Modelo Regional
Modelo: Eta
Experimento: Todos (BESM, CANESM2, HADGEM2-ES, MIROC5)
Cenários: Todos (Histórico, RCP4.5 e RCP8.5)
Período (para RCP4.5 e RCP8.5): Todos (2011/2040, 2041/2070, 2071/2100)
Tipo: (Média e Anomalia)
Variáveis: CDD, CWD, R95p, RX1day, RX5day, SDII, TX90p, UR, W10M
Frequência: Anual

Foi selecionado o ponto digitando "São Sebastião-SP" na busca.
Clicou-se no botão "gráfico de linha" e dentro do pop-up clicou-se em "salvar.csv". Esses dados estão salvos na pasta "Raw_Data", organizados por modelo e variável.

Após a obteção dos diversos dados, juntaram-se os três períodos em um mesmo arquivo .csv para cada combinação de variável, modelo, cenário e tipo usando o script "agregate-data.py". Por exemplo, os três arquivos csv contendo os períodos (2011/2040), (2041/2070) e (2071/2100) para as médias da variável CDD no modelo BESM no cenário RCP8.5 foram juntadas em um único arquivo contendo essas informações no nome do arquivo. Esses novos arquivos foram salvos na pasta "Compiled-Data"

Em seguida, usando o script "slopes-plot-trendlines.py" foram calculadas as retas via regressão linear, plotados os gráficos dos pontos e da reta de tendência e, com o script "mann-kendall.py", foram realizados os testes de Mann Kendall para cada conjunto de dados, ou seja, para cada arquivo obtido do primeiro script. O script pede o ano de término do cálculo e é salvo numa pasta contendo "Processed-Data/ano escolhido".

Por fim, com os p-values obtidos do teste de Mann-Kendall foi obtido um p-value combinado usando o método de Fischer via script "fischer-confidence.py". A confiança no resultado foi rankeada usando os seguintes critérios:
Very High Confidence: p-value < 0.01
High Confidence: 0.01 ≤ p-value < 0.05
Medium Confidence: 0.05 ≤ p-value < 0.1
Low Confidence: 0.1 ≤ p-value < 0.2
Very Low Confidence: p-value ≥ 0.2
