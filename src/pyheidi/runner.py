from main_application import MainApplication
from utilities.byte_sized_strings import byteSizedStrings

if __name__ == '__main__':
	print byteSizedStrings(128)
	print byteSizedStrings(9201)
	print byteSizedStrings(10291)
	print byteSizedStrings(123456)
	print byteSizedStrings(9201123)
	print byteSizedStrings(6220112323)
	mainApplication = MainApplication()
