import uvicorn

from integra_python_connect.src.builder import Builder

app = Builder.start()

if __name__ == '__main__':
    uvicorn.run(app="__main__:app", host='localhost', port=8002)
