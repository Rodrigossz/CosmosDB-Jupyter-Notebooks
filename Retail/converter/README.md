# Converting Orange Juice into Surface Sales

Files description:

+ oj-original = the original dataset
+ oj-AutoML = version created by the Azure Automated ML team for their demo notebook. It can be downloaded from Azure ML Studio sample notebooks.
+ oj-surface-converter = Python 3 code that converts OJ into Surface. It will create 2 equivalent files, json and csv.
+ SurfaceSales.json = Converted data in json format. It will be ready to be used in Cosmic Notebooks, with the ```%%upload``` magic command.
+ SurfaceSales.csv = converted data in csv format.

To load the json file into Azure Cosmos DB, you need to:

+ Replace **}** with **},**
+ Add square brackets to the file: opening as 1st character and closing as last.
+ Open the json file and you will understand this 2 requests above.
