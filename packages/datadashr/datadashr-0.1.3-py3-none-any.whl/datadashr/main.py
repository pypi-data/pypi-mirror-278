import panel as pn
from .app import App


def main():
    app = App()
    pn.serve({'/': app.serve}, show=True)
