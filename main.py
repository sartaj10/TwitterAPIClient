from flask import Flask, render_template, request, redirect, json, url_for

app = Flask(__name__)

# Home Page
@app.route('/')
def main():
	return render_template('index.html')

# Run the app
if __name__ == '__main__':
	app.run(debug=True, port = 5002)
