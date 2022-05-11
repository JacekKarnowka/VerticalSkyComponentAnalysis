VSC is a vertical sky component, defined as a measure of the amount of visible sky available from a point on a vertical plane. The reference point used for the calculation is usually the center of the vertical face of the window. The VSC test is the main test used to access the impact of a development on neighbouring properties. 

The VSC will be 0% where the point being measured has a completly obstructed view of the sky, or just under 40% where the view is competely unobstructed. 
The BRE guide explains that diffuse daylight may be adversely affected it, after a development, the VSC is both less than 27% and less than 0.8 times its former value.

Created project is based on previously genereted data by architectonic company. The premise for the project is that data has been sent as appropriate ZIP format (excel files and .jpeg photos) and files have been named properly.

Elements of dashboard:
1. Left menu- allows upload data and choose desire settings. After uploading project and clicking "Refresh" button, different projects will be displayed (related to prepared data) as a checklist. Displayed checklist allows user to choose project/projects for analysis based on generated plots.

2. Scatter plot- shows differen windows, from buildings surounding architectonic project and the color indicates whether the selected window meets the VSC parameter requirements or not. Value from Y axis can be choose from left menu bar.

3. Scatter plot tool tip- shows visualistion view from current window.

4. Clicked plot data- after selecting point from graph, window will be displayed as a static visualisation near plot, allowing to check differences between selected projects.

Github repository contains "Example_data" folder, that could be upload to dashboard.

Used tools and technologies:
- Dash,
- Plotly,
- Bootstrap components,
- Flask,
- Heroku,
- Pandas
