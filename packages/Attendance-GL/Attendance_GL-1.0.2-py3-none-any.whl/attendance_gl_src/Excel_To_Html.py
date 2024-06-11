import pandas as pd
import json
import configparser
from pathlib import Path
import logging
import logging.config

# Load logging configuration from the file
logging.config.fileConfig(Path(__file__).resolve().parent / 'resources' / 'logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def create_html_calendar():
    logger.info("############################### Creating HTML Calendar ###############################")

    #get logo image src path
    logo_path = Path(__file__).resolve().parent / 'resources' / 'logo.svg'
    #get the directory path from the config file
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent / 'resources' / 'config.properties'
    config.read(config_path)
    directory = config['data']['dir.path']
    fileName = config['data']['attendance_excel_name']

    # Read the Excel file
    df = pd.read_excel(directory + fileName)

    # Convert datetime objects to strings
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    # Convert the dataframe to a dictionary
    data = df.to_dict(orient='records')

    # Convert the data to JSON format
    json_data = json.dumps(data)

    # Prepare the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calendar</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .calendar {{ display: table; width: 100%; max-width: 600px; margin: 0 auto; border-collapse: collapse; }}
            .calendar th, .calendar td {{ border: 1px solid #999; padding: 10px; text-align: center; }}
            .calendar th {{ background-color: #f2f2f2; }}
            .calendar .green {{ background-color: green; color: white; }}
            .calendar .LightBlue {{ background-color: LightBlue; color: white; }}
            .calendar-title {{ text-align: center; font-size: 1.5em; margin-bottom: 10px; }}
            .navigation-buttons {{ text-align: center; margin-bottom: 10px; }}
        #header {{
            background-color: #f37038;
            color: white;
            text-align: center;
            padding: 10px;
             margin-bottom: 50px;
        }}
        #logo {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }}
        </style>
    </head>
    <body>
     <div id="header">
        <img src="{logo_path}" class="custom-logo svg-logo-desktop" width="196" height="45" alt="GlobalLogic India" title="GlobalLogic-Logo-White | GlobalLogic">
        <h1>Attendance Report</h1>
    </div>
        <div class="navigation-buttons">
            <button id="prevButton" style="background-color: #f37038; color: white;">Previous</button>
            <span id="monthYear" style="font-weight: bold;"></span>
            <button id="nextButton" style="background-color: #f37038; color: white;">Next</button>
        </div>
        <div id="calendarContainer"></div>
        <script>
            const data = {json_data};

            function createCalendar(year, month) {{
                const calendarDiv = document.getElementById('calendarContainer');
                calendarDiv.innerHTML = '';

                const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

                const monthYearSpan = document.getElementById('monthYear');
                monthYearSpan.innerText = monthNames[month] + ' ' + year;

                const table = document.createElement('table');
                table.className = 'calendar';

                const header = document.createElement('thead');
                const headerRow = document.createElement('tr');
                dayNames.forEach(day => {{
                    const th = document.createElement('th');
                    th.innerText = day;
                    headerRow.appendChild(th);
                }});
                header.appendChild(headerRow);
                table.appendChild(header);

                const body = document.createElement('tbody');
                const firstDay = new Date(year, month, 1).getDay();
                const daysInMonth = new Date(year, month + 1, 0).getDate();

                let date = 1;
                for (let i = 0; i < 6; i++) {{
                    const row = document.createElement('tr');
                    for (let j = 0; j < 7; j++) {{
                        const cell = document.createElement('td');
                        if (i === 0 && j < firstDay) {{
                            cell.innerText = '';
                        }} else if (date > daysInMonth) {{
                            break;
                        }} else {{
                            const currentDate = new Date(year, month, date);
                            const dateString = currentDate.getFullYear() + 
                                '-' + (currentDate.getMonth() + 1).toString().padStart(2, '0') + 
                                '-' + currentDate.getDate().toString().padStart(2, '0');

                            cell.innerText = date;
                            if (data.some(item => item.Date.split(' ')[0] === dateString && item.Office)) {{
                                cell.className = 'green';
                            }}

                            // Check if the day is Saturday or Sunday
                            const dayOfWeek = currentDate.getDay();
                            if (dayOfWeek === 0 || dayOfWeek === 6) {{
                                cell.className = 'LightBlue';
                            }}

                            // Check if the date is today's date
                            const today = new Date();
                            if (currentDate.getDate() === today.getDate() && currentDate.getMonth() === today.getMonth() && currentDate.getFullYear() === today.getFullYear()) {{
                                cell.style.border = '2px solid red';
                            }}

                            date++;
                        }}
                        row.appendChild(cell);
                    }}
                    body.appendChild(row);
                }}
                table.appendChild(body);
                calendarDiv.appendChild(table);
            }}

            function loadCalendar() {{
                const today = new Date();
                let year = today.getFullYear();
                let month = today.getMonth();

                createCalendar(year, month);

                const prevButton = document.getElementById('prevButton');
                const nextButton = document.getElementById('nextButton');

                prevButton.onclick = () => {{
                    if (month === 0) {{
                        month = 11;
                        year--;
                    }} else {{
                        month--;
                    }}
                    createCalendar(year, month);
                }};

                nextButton.onclick = () => {{
                    if (month === 11) {{
                        month = 0;
                        year++;
                    }} else {{
                        month++;
                    }}
                    createCalendar(year, month);
                }};
            }}

            document.addEventListener('DOMContentLoaded', loadCalendar);
        </script>
    </body>
    </html>
    """

    # Save the HTML content to a file
    logger.info("Creating calendar.html file...")
    with open(directory + 'calendar.html', 'w') as file:
        file.write(html_content)
    logger.info("calendar.html file created successfully!")
