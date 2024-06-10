from flask import Flask

app = Flask('production_ready')

@app.route('/')
def status():
    return 'OK'

def main():
  print('production ready!')
  app.run()

if __name__ == '__main__':
  main()
