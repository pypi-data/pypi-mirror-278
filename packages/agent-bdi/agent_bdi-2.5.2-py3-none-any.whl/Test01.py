import logging
import time

from holon.HolonicAgent import HolonicAgent

class TestAgent(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)

    # def _run(self):
    #     logging.info(f"Run TestAgent")
    #     time.sleep(2)

if __name__ == '__main__':
    # Helper.init_logging()
    # logging.info('***** Main start *****')
    print('***** TestAgent start *****')

    a = TestAgent()
    a.start()
