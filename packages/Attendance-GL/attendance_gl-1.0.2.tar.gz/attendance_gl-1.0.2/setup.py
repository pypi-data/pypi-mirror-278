from setuptools import setup, find_packages

setup(
    name='Attendance_GL',
    version='1.0.2', 
    description='A Python package to track attendance in an Excel file and convert it to an HTML file', 
    author='Ankush Sawant', 
    author_email='qaankush@gmail.com', 
    packages=find_packages(),
   # package_dir={'': 'attendance_gl_src'},
    include_package_data=True,
    package_data={
        '': ['resources/*.conf', 'resources/*.properties', 'resources/*.svg'],
    },
    install_requires=[
        'openpyxl',
        'pandas', 
        'configparser',
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'markatt=attendance_gl_src.Runner:main', 
            'scheduleatt=attendance_gl_src.Task_Scheduler:main', 
        ],
    },
)