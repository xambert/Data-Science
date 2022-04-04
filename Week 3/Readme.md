
[Data](wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
[App](wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py")

Understand :         filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site].groupby(["Launch Site", "class"]).\
size().reset_index(name="class count")
