from flask import Flask,render_template

import pandas as pd
import folium

def get_top_n_confirmed(corona_df,n=None,fields=['Confirmed']):
    by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    return by_country.nlargest(n if n else corona_df.shape[0], 'Confirmed')[fields]

def circle_maker(x):
    print(x)
    folium.Circle(location=[x[0],x[1]],radius=float(x[2]),color="green",fillColor="red",tooltip='Confirmed cases:{}\nDeaths:{}'.format(x[2],x[4])).add_to(m)



app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, html_map=html_map,pairs=pairs)

if __name__=="__main__":

    # Read the dataset
    corona_df = pd.read_csv("DataSet/covid-19-dataset-3.csv")
    # print("Before dropping:",set(corona_df["Country_Region"]),"\n",corona_df.columns)
    corona_df.drop(labels=["Hospitalization_Rate","Testing_Rate","People_Hospitalized","People_Tested","Last_Update","FIPS"],axis=1,inplace=True)
    # print(corona_df)
    corona_df.dropna(inplace=True)
    # print(corona_df)
    # print(set(corona_df["Country_Region"]),"\n",corona_df.columns)

    # Group the dataset by country
    by_country = corona_df.groupby(by="Country_Region").sum()

    cdf = get_top_n_confirmed(by_country,fields=["Confirmed","Deaths"])
    pairs=[(country,confirmed,deaths) for country,confirmed,deaths in zip(cdf.index,cdf['Confirmed'],cdf['Deaths'])]

    m=folium.Map(location=[11.225999,92.968178],zoom_start=3)
    corona_df["Combined_Key"]=f"{corona_df['Province_State']},{corona_df['Country_Region']}"
    corona_df[['Lat','Long_','Confirmed','Combined_Key',"Deaths"]].apply(lambda x:circle_maker(x),axis=1)
    html_map=m._repr_html_()

    app.run(debug=True,port=8000,host="0.0.0.0")
