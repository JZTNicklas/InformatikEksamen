'''
Import appen, og start serveren hvis __name__ == "__main__"
host='0.0.0.0' betyder alle åbne porte
'''

from store import app

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')