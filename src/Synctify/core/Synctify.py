#!/usr/bin/env python
'''
Synctify
'''

# import config;
import logger;

def main():
    log = logger.Logger()
    log.start()
    print("Hello from the Synctify app!")
    log.stop()

if __name__ == "__main__":
    main()

