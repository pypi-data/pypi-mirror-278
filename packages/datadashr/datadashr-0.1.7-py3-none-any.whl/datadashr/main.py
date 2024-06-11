import panel as pn
from datadashr.app import App


def main():
    app = App()
    pn.serve({'/': app.serve}, show=True, title='Datadashr')


if __name__ == '__main__':
    main()
