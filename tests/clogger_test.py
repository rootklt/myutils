from myutils.loggerUtils import Logger
import logging


def test():

    logger = Logger('root')
    #logger.set_formatter('%(asctime)s %(levelname)s - %(message)s')

    logger.fatal('aaaa')
    logger.critical('bbbbb')
    logger.error('ccccc')
    logger.warning('eeeeeee')
    logger.debug('ffffff')
    logger.info('ggggggg')
    logger.success('hhhhhh')

    try:
        a = 1/0
    except Exception as e:
        logger.exceptioin(f'dddddd{e}')


if __name__ == '__main__':
    test()
