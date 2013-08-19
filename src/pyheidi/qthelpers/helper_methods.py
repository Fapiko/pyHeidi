from PyQt4.QtCore import QStringList


def buildQStringList(items):
	"""
	@rtype: QStringList
	"""
	returnData = QStringList()
	for item in items:
		returnData.append(item)

	return returnData