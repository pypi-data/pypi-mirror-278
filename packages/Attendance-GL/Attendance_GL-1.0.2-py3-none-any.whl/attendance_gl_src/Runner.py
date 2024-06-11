import time
from attendance_gl_src import Attendance_In_Excel as aie
from attendance_gl_src import Excel_To_Html as eth
# import Attendance_In_Excel as aie
# import Excel_To_Html as eth

def main():
    aie.retrieve_network_info()
    time.sleep(2)
    eth.create_html_calendar()

if __name__ == "__main__":
    main()
