def byteSizedStrings(value):
	"""
	@type value: int
	@param value:
	@return:
	@rtype: str
	"""

	value = float(value)

	if value < 1024:
		suffix = ''
	elif value < 1048576:
		value /= 1024
		suffix = 'KB'
	elif value < 1073741824:
		value /= 1048576
		suffix = 'MB'
	else:
		value /= 1073741824
		suffix = 'GB'

	return "%s %s" % (str(round(value, 2)).rstrip('.0'), suffix)
