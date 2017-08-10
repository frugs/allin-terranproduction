import aiohttp.web
import pkg_resources

import uploader


class App(aiohttp.web.Application):

    def __init__(self):
        super().__init__()

        replay_uploader = uploader.ReplayUploader(lambda x: "analysis.html?data={}".format(x))

        self.router.add_post("/upload", replay_uploader.upload_replay)
        self.router.add_static('/', pkg_resources.resource_filename(__name__, "public"))


def main():
    aiohttp.web.run_app(App(), port=32432)
    pass


if __name__ == "__main__":
    main()