# configure for try decoding list
try_encoding_list = ['gb18030', 'utf-8']

def try_decode_once(text, encoding):
	try:
		text = text.decode(encoding, 'strict') 	
		return text
	except UnicodeDecodeError:
		return None

def try_decode(text):
	'''
	try decode based on the list
	'''
	print "Begin try decode"
	for encoding in try_encoding_list:
		decoded = try_decode_once(text, encoding)
		if decoded:
			return decoded

	print 'Try decoding failed' 
	return None

def decode_ignore(text, encoding):
	'''
	decoding and ignore errors
	'''
	return text.decode(encoding, 'ignore')

def encode_ignore(text, encoding):
	'''
	encoding and ignore errors
	'''
	return text.encode(encoding, 'ignore')
