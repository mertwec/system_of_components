before creating: bring components to the same form

create "report file" for parsing with "parsing_file_reports.py":

into P-CAD2006 PCB
	File -- Reports

select:
	Bill of Materials (csv),
	File
	Separated list = ';'

"Customise...":
	Format: 
		File Extension = 'csv'
	
	Selection:
		1 Count
		2 ComponentName
		3 RefDes	
		4 PatternName
		5 Value

Generate