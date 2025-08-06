import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

## configure page
st.set_page_config(
    page_title="Downtown Salisbury Commuter Survey (Responses) Analysis",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded")

## import data
df = pd.read_csv('data/Downtown Salisbury Commuter Survey (Responses) with Geocoding.csv')

## set page title
st.title("🚘 Downtown Salisbury Commuter Survey (Responses) Analysis")

## extract key metrics

# number of responses
responses = len(df)

# dates of oldest and newest responses
earliest_response = pd.to_datetime(df['Timestamp']).dt.date.min().isoformat()
most_recent_response = pd.to_datetime(df['Timestamp']).dt.date.max().isoformat()


# number of unique employers
unique_employers = df["Where do you work (business name)?"].nunique()

# median commute length (miles)
median_commute_length = df["How many miles is your commute (one-way)?"].median()

## display key metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Number of Responses", responses, border=True)
col2.metric("Earliest Response", earliest_response, border=True)
col3.metric("Most Recent Response", most_recent_response, border=True)
col4.metric("Median Commute Length (Miles)", median_commute_length, border=True)

#######################################################
# WHERE ARE DOWNTOWN EMPLOYEES COMMUTING FROM AND TO? #
#######################################################

st.header("Where are Downtown Employees Commuting From and To?")

col5, col6 = st.columns(2)

## create maps

# map of "home" locations
col5.subheader('"Home" Locations')
home_map = px.scatter_mapbox(df,
                        lat=df["Home Latitude"],
                        lon=df["Home Longitude"],
                         hover_data = {
                                "Home Latitude": False, 
                                "Home Longitude": False,
                                "Where do you live (neighborhood and/or address)?": True
                                },
                        labels={"Where do you live (neighborhood and/or address)?": ""},
                        zoom=9,
                        center={"lat": 38.3607, "lon": -75.5994},
                        mapbox_style="open-street-map",
                        )

home_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
home_map.update_traces(marker=dict(size=15, color="green"), cluster=dict(enabled=True))

# display map of "home" locations
col5.plotly_chart(home_map)

# add context
with col5.expander("💡 More Info"):
    st.write(
        "Where are downtown employees commuting from?\n"
        "- Fruitland\n"
        "- Delmar\n"
        "- Neighborhoods along Pemberton Drive\n"
        "- Camden + neighborhoods between Salisbury University and the Wicomico River\n"
        "- Truitt Street neighborhood area\n"
        "- Rustic Acres neighborhood (off Coulbourn Mill Rd)"
    )
# map of "work" locations
col6.subheader('"Work" Locations')
work_map = px.scatter_mapbox(df,
                        lat=df["Work Latitude"],
                        lon=df["Work Longitude"],
                        hover_name = "Where do you work (business name)?",
                        hover_data = {
                                "Work Latitude": False, 
                                "Work Longitude": False,
                                "Where do you work (business address)?": True
                                },
                        labels={
                            "Where do you work (business name)?": "",
                            "Where do you work (business address)?": ""
                            },
                        zoom=15,
                        center={"lat": 38.3645, "lon": -75.5994},
                        mapbox_style="open-street-map",
                        )

work_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
work_map.update_traces(marker=dict(size=15, color="green"), cluster=dict(enabled=True))

# display map of "work" locations
col6.plotly_chart(work_map)

# add context
with col6.expander("💡 More Info"):
    st.write("From Delmar to downtown, the bike commute is approximately 8 miles (37 minutes). From Hebron it’s about 5 miles (23 minutes).")

##############################################################
# How are Employees Getting to Work Some or All of the Time? #
##############################################################

st.header("How are Employees Commuting Downtown for Work Some or All of the Time?")

# create dataframe
modes_of_transportation_df = pd.DataFrame({
    'Mode of Transportation': [
        'Gas-Powered Vehicle (Alone)', 
        'Electric or Hybrid Vehicle (Alone)', 
        'Carpooling',
        'Bicycle or Scooter',
        'Walking or Running',
        'Public Transportation',
        'Other'
    ],
    'Number of Employees': [
        (df['How many days per week do you commute to downtown using each of the following means of transport? [alone in a gas-powered vehicle]'] != 0).sum(),
        (df['How many days per week do you commute to downtown using each of the following means of transport? [alone in an electric or hybrid vehicle]'] != 0).sum(),
        (df['How many days per week do you commute to downtown using each of the following means of transport? [in a vehicle with someone else (carpooling)]'] != 0).sum(),
        (df['How many days per week do you commute to downtown using each of the following means of transport? [a bicycle or scooter]'] != 0).sum(),
        (df['How many days per week do you commute to downtown using each of the following means of transport? [your feet (walking/running)]'] != 0).sum(),
        (df['How many days per week do you commute to downtown using each of the following means of transport? [public transportation]'] != 0).sum(),
        (df['How many days per week do you commute to downtown using each of the following means of transport? [other]'] != 0).sum()
    ]
})

# plot bar chart
modes_of_transportation_bar = px.bar(modes_of_transportation_df, 
             x='Mode of Transportation', 
             y='Number of Employees',
             text = 'Number of Employees'
)
modes_of_transportation_bar .update_layout(bargap=0.2)
st.plotly_chart(modes_of_transportation_bar )

## add context
with st.expander("💡 More Info"):
    st.write("18/49 commute by walking/running, bike/scooter, or carpooling (~37%).")

#############################################################
# How Would Employees CONSIDER Commuting Downtown for Work? #
#############################################################

col7, col8 = st.columns(2)

col7.subheader("How Would Employees CONSIDER Commuting Downtown for Work?")

# create dataframe
modes_of_transportation_considered_df = pd.DataFrame({
    'Mode of Transportation': [
        'Walking or Running', 
        'Bicycle or Scooter', 
        'Car',
        'Carpooling',
        'Other'
    ],
    'Number of Employees': [
        df['Regardless of how you commute presently, which of the following modes of transportation would you consider for your commute in the future?'].str.contains("walking/running").sum(),
        df['Regardless of how you commute presently, which of the following modes of transportation would you consider for your commute in the future?'].str.contains("bicycle or scooter").sum(),
        df['Regardless of how you commute presently, which of the following modes of transportation would you consider for your commute in the future?'].str.contains("car").sum(),
        df['Regardless of how you commute presently, which of the following modes of transportation would you consider for your commute in the future?'].str.contains("carpooling").sum(),
        df['Regardless of how you commute presently, which of the following modes of transportation would you consider for your commute in the future?'].str.contains("other").sum()
    ]
})

# plot bar chart
modes_of_transportation_considered_bar = px.bar(modes_of_transportation_considered_df, 
             x='Mode of Transportation', 
             y='Number of Employees',
             text = 'Number of Employees'
)
modes_of_transportation_bar .update_layout(bargap=0.2)
col7.plotly_chart(modes_of_transportation_considered_bar )

#################
# Because of... #
#################

col8.subheader("Because of...")

# create dataframe
because_of_df = pd.DataFrame({
    'Reason': [
        'Saving Money', 
        'Improved Physical Health', 
        'Improved Mental Health',
        'Environmental Impact',
        'Other'
    ],
    'Number of Employees': [
        df['Of the modes of transportation you selected above, what makes you interested in considering them?'].str.contains("saving money").sum(),
        df['Of the modes of transportation you selected above, what makes you interested in considering them?'].str.contains("improved physical health").sum(),
        df['Of the modes of transportation you selected above, what makes you interested in considering them?'].str.contains("improved mental health").sum(),
        df['Of the modes of transportation you selected above, what makes you interested in considering them?'].str.contains("environmental impact").sum(),
        df['Of the modes of transportation you selected above, what makes you interested in considering them?'].str.contains("other").sum(),
    ]
})

# plot bar chart
because_of_bar = px.bar(because_of_df, 
             x='Reason', 
             y='Number of Employees',
             text = 'Number of Employees'
)
because_of_bar .update_layout(bargap=0.2)
col8.plotly_chart(because_of_bar)

###################################################
# What are the Barriers to Sustainable Commuting? #
###################################################

st.header("What are the Barriers to Sustainable Commuting?")

# create dataframe
barriers_df = pd.DataFrame({
    'Reason': [
        'Physical Distance from Home to Work', 
        'Lack of Sidewalks and/or Bike Lanes', 
        'Weather Conditions (e.g. rain, snow, heat)',
        'Lack of Time or Need to Get to Work Quickly',
        'Uncertainty about Bike Routes or Walking Paths',
        'Concern about Personal Safety',
        'Lack of Facilities at Work (e.g. bike racks, showers, changing rooms)',
        'Personal Physical Limitations',
        'Other'
    ],
    'Number of Employees': [
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("physical distance from home to work").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("lack of sidewalks and/or bike lanes").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("weather conditions").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("lack of time or need to get to work quickly").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("uncertainty about bike routes or walking paths").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("concern about personal safety").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("lack of facilities at work").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("personal physical limitations").sum(),
        df['What barriers hold you back from considering more sustainable forms of transportation? '].str.contains("other").sum()
    ]
})

# plot bar chart
barriers_bar = px.bar(barriers_df, 
             x='Reason', 
             y='Number of Employees',
             text = 'Number of Employees'
)
barriers_bar .update_layout(bargap=0.2)
st.plotly_chart(barriers_bar)

# create dataframe
accessibility_df = df['How accessible are dedicated bikes lanes or sidewalks between your home and workplace?'].value_counts().reset_index()
accessibility_df.columns = ['Accessibility', 'Number of Employees']

# create pie chart
accessibility_pie = px.pie(accessibility_df, names='Accessibility', values='Number of Employees', title='Accessibility of Dedicated Bikes Lanes or Sidewalks Between Home and Workplace')
st.plotly_chart(accessibility_pie)


############################################################
# How Interested are Employees in Changing their Commute? #
###########################################################
st.header("How Interested are Employees in Changing their Commute?")

col9, col10 = st.columns(2)

# create dataframe
coworkers_df = df['Do you think your coworkers would be more likely to bike or walk to work if more people in your office did?'].value_counts().reset_index()
coworkers_df.columns = ['Likelihood', 'Number of Employees']
# create pie chart
coworkers_pie = px.pie(coworkers_df, names='Likelihood', values='Number of Employees', title='Would Seeing Coworkers Bike/Walk to Work Encourage You to Join?')
col9.plotly_chart(coworkers_pie)

# create dataframe
challenge_df = df['Would you participate in a "walk or bike to work" challenge or group if it were organized by your workplace?'].value_counts().reset_index()
challenge_df.columns = ['Response', 'Number of Employees']
# create pie chart
challenge_pie = px.pie(challenge_df, names='Response', values='Number of Employees', title='Likelihood to Participate in a "Walk/Bike to Work" Challenge or Group')
col10.plotly_chart(challenge_pie)


col11, col12 = st.columns(2)

# create dataframe
rating_df = pd.DataFrame({
    'Rating (1-5)': [
        '1', 
        '2', 
        '3',
        '4',
        '5',
    ],
    'Number of Employees': [
        (df['On a scale of 1-5, how likely are you to consider walking or biking to work in the future? '] == 1).sum(),
        (df['On a scale of 1-5, how likely are you to consider walking or biking to work in the future? '] == 2).sum(),
        (df['On a scale of 1-5, how likely are you to consider walking or biking to work in the future? '] == 3).sum(),
        (df['On a scale of 1-5, how likely are you to consider walking or biking to work in the future? '] == 4).sum(),
        (df['On a scale of 1-5, how likely are you to consider walking or biking to work in the future? '] == 5).sum(),
    ]
})
# plot bar chart
rating_bar = px.bar(rating_df, 
             x='Rating (1-5)', 
             y='Number of Employees',
             title="Likelihood to Consider Walking/Biking to Work",
             text = 'Number of Employees'
)
rating_bar .update_layout(bargap=0.2)
col11.plotly_chart(rating_bar)

# create dataframe
incentives_df = df['If there were more incentives (e.g. subsidies for bikes, discounts, gym memberships, etc) would you be more likely to walk or bike to work? '].value_counts().reset_index()
incentives_df.columns = ['Response', 'Number of Employees']
# create pie chart
incentives_pie = px.pie(incentives_df, names='Response', values='Number of Employees', title='Would More Incentives Increase Your Likelihood to Walk/Bike to Work?')
col12.plotly_chart(incentives_pie)

with st.expander("💡 What Else Did We Learn?"):
    st.write("""
        - Safety was the major concern cited throughout this survey. While some people identified that there is no safe way to travel from their neighborhood into downtown, many more specifics were given around the opportunities for increasing safety for non-drivers. Some specific examples of both challenges and solutions worth sharing:
            - Cars are regularly driving in the bike lanes.
            - Confusing signage for both drivers and cyclists.
            - Lack of a safe-streets mindset within the city and law enforcement. Many people mentioned an interest in having police patrolling areas where there are bike lanes to ensure that cars are stopping at stop signs, that cars aren’t parked in the lanes that people are biking in, and that pedestrians and cyclists are safe generally.
            - More sidewalks and crosswalks are needed across the city with timed passage periods to increase walkability.
            - Protected bike lanes were mentioned repeatedly. One respondent shared that a painted line is not going to make people feel safer.
        - Convenience is high on the minds of community members in terms of getting to work on time, being able to pick up sick children at school, and after-work commitments.
        - A handful of people indicated an interest in public transportation, including buses and trolleys.
        - People are interested in a dedicated bike path where they felt connected to nature to commute on.
        - One respondent identified the need to have public bathrooms available if we are trying to encourage a walking culture in the downtown area.
    """)
