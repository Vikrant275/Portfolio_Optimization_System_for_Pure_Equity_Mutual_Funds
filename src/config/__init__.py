from framework.fetch_config import GetConfig

'''
pipeline constant
'''

ARTIFACT = GetConfig(config_file='dir_path.yaml',variables='artifact').get()

