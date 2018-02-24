import pandas as pd

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


namesCSV = "csvs/Belly Button Biodiversity Data_17Nov12.xlsx"
metaCSV = "csvs/Belly_Button_Biodiversity_Metadata.csv"
sampleCSV = "csvs/belly_button_biodiversity_samples.csv"

names = pd.read_excel(namesCSV,"Belly Button Meta Data Matrix")
namesDF = pd.DataFrame(names)
namesDF = namesDF.set_index("Data")
namesDF = namesDF.T
lastRow = len(namesDF)
namesDF = namesDF.drop(namesDF.index[lastRow - 1])
namesDF = namesDF.reset_index()
namesDF = namesDF.rename(columns={"index":"Data"})
namesDF["Data"] = "BB_" + namesDF["Data"].astype(str)
namesData = namesDF["Data"].tolist()

metaDF = pd.read_csv(metaCSV)
metaDF["SAMPLEID"] = "BB_" + metaDF["SAMPLEID"].astype(str)
metaDF.head()

#----------------------------------------------------------------------------------------------------
@app.route("/", methods=['GET'])
def index():
    
    return render_template("index.html", namesData = namesData)

#----------------------------------------------------------------------------------------------------
@app.route("/names")
def names():

    return jsonify(namesData)

#----------------------------------------------------------------------------------------------------
@app.route("/otu")
def otu():

    otu = pd.read_excel(namesCSV)
    otuDF = pd.DataFrame(otu)

    otuData = otuDF["Lowest Taxonomic Level of Bacteria/Archaea Found"].tolist()

    return jsonify(otuData)

#----------------------------------------------------------------------------------------------------
@app.route("/metadata/<sample>")
def sampleData(sample):

    bbSample = metaDF.loc[metaDF["SAMPLEID"] == sample]
    bbSample = bbSample[['AGE','BBTYPE','ETHNICITY','GENDER','LOCATION','SAMPLEID']]
    bbSample = bbSample.to_json(orient = 'records')

    return bbSample

#----------------------------------------------------------------------------------------------------
@app.route("/wfreq/<sample>")
def wFreq(sample):

    washAmt = namesDF.loc[namesDF["Data"] == sample]

    return jsonify(washAmt["Washing Frequency (belly button scrubs per week)"].tolist())

#----------------------------------------------------------------------------------------------------
@app.route('/samples/<sample>')
def otuID(sample):

    sampleDF = pd.read_csv(sampleCSV)
    sampleDF = sampleDF.sort_values(by=sample, ascending=False)
    sample1 = sampleDF[sample]
    sample1 = sample1.head(25)
    sample1 = sample1.tolist()

    sample2 = sampleDF["otu_id"]
    sample2 = sample2.head(25)
    sample2 = sample2.tolist()

    return jsonify([dict(sampleID=sample1, otuID=sample2)])

#----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)