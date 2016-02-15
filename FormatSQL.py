__author__ = 'Will Wagner'

# maximum formatted line length
line_length = 100

# tab number of spaces to indent 
indent_depth = 2

filename = 'Roster_1ProcessStudentData.sql'
output_query = ''
current_line = ''
indent_flag = 0
comment_flag = False
on_flag = False
paren_flag = False

def reduce_string(string):
	return string[:-1]

def calculate_line_fit(word):
	if len(output_query) < 1:
		return True
	line_length = 0
	output_copy = output_query
	while output_copy[-1] != '\n':
		output_copy = reduce_string(output_copy)
		line_length += 1
	if len(word) + line_length > 100:
		return False
	else:
		return True

def get_current_indent(command_word=False):
	if command_word:
		if indent_flag > 0:
			return (indent_flag - 1) * indent_depth * ' '  
		else:
			return ''
	else:
		return indent_flag * indent_depth * ' '

# words that always get their own lines, with the lines below futher indented
command_keywords = ['SELECT', 'FROM', 'WHERE', 'HAVING', 'GROUP', 'ORDER', 
				    'GO', 'UPDATE', 'SET', 'INTO']
# words that always start a line
start_line_words = ['JOIN', 'LEFT', 'RIGHT', 'FULL', 'INNER', 'OUTER', 'USE', 'AND', 'OR', 'WHEN']
# words that always start a line with increased indent
indent_start_line_words = ['ON']
# words that always end a line, and increase indent below them
case_words = ['CASE']
# words that reduce indent
end_of_case_words = ['END']

with open(filename) as file:
	input_query = file.read().split()

for word in input_query:
	if not calculate_line_fit(word):
		output_query += '\n'
	if '*/' in word:
		comment_flag = False
		output_query += word + '\n'
	elif comment_flag:
		output_query += word + ' '
	elif '/*' in word:
		comment_flag = True
		output_query += '\n' + word + ' '
	# word is a function without spaces
	elif '(' in word and ')' in word:
		if output_query[-1] == '\n':
			output_query += get_current_indent() + word + ' '
		else:
			output_query += word + ' '
	# word is the end of a list
	elif ')' in word:
		paren_flag = False
		output_query += word + ' '
	# word is the beginning of a list
	elif '(' in word:
		if output_query[-1] == '\n':
			output_query += get_current_indent()
		paren_flag = True
		output_query += word + ' '
	elif word.upper() in command_keywords:
		if indent_flag > 0:
			indent_flag -= 1
		if output_query[-1] == '\n':
			output_query += get_current_indent(True) + word.upper() + '\n'
		else:
			output_query += '\n' + get_current_indent(True) + word.upper() + '\n'
		indent_flag += 1
	elif word.upper() in start_line_words:
		output_query += '\n' + get_current_indent() + word.upper() + ' '
	# ToDo: Figure out how to identify when to remove this newline
	# elif word.upper() in indent_start_line_words:
	# 	indent_flag += 1
	# 	output_query += '\n' + get_current_indent() + word.upper() + ' '
	elif word.upper() in case_words:
		output_query += word.upper()
		indent_flag += 1
	elif word.upper() in end_of_case_words:
		output_query += word.upper() + ' '
		indent_flag -= 1
	else:
		# if there's a comma, insert a line break at the end
		if ',' in word and get_current_indent() and not paren_flag:
			output_query += word + '\n'
		# otherwise, just add the word
		elif output_query[-1] == '\n':
			output_query += get_current_indent() + word + ' '
		else:
			output_query += word + ' '

if output_query[-1] != ';':
	output_query += ';'

output = open(filename[:-4] + '_Formatted.sql', 'w')
output.write(output_query)
output.close()