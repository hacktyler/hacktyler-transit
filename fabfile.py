from fabric.api import *

"""
Base configuration
"""
#name of the deployed site if different from the name of the project
env.site_name = 'transit'

env.project_name = 'transit'
env.site_media_prefix = "site_media"
env.admin_media_prefix = "admin_media"
env.repository_url = "git@github.com:hacktyler/hacktyler-transit.git"
env.phonegap_repo = "git@git.phonegap.com:onyxfish/13467_hacktylertransit.git"

"""
Environments
"""
def production():
    """
    Work on production environment
    """
    env.s3_bucket = 'media.hacktyler.com'
    env.app_s3_bucket = 'transit.hacktyler.com'

def staging():
    """
    Work on staging environment
    """
    env.s3_bucket = 'media-beta.hacktyler.com'
    env.app_s3_bucket = 'transit-beta.hacktyler.com'
    
"""
Branches
"""
def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'

def master():
    """
    Work on development branch.
    """
    env.branch = 'master'

def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name
    
"""
Commands - deployment
"""   
def deploy_to_phonegap():
    require('settings', provided_by=[production, staging])
    local('DEPLOYMENT_TARGET=%(settings)s PHONEGAP_REPO=%(phonegap_repo)s ./update_phonegap.sh' % env)

def gzip_assets():
    """
    GZips every file in the assets directory and places the new file
    in the gzip directory with the same filename.
    """
    local('python gzip_assets.py')

def deploy_app_to_s3():
    """
    Deploy the latest project site media to S3.
    """
    require('settings', provided_by=[production, staging])

    gzip_assets()

    env.gzip_path = 'gzip/'
    local('s3cmd -P --add-header=Content-encoding:gzip --guess-mime-type --rexclude-from=s3exclude sync %(gzip_path)s s3://%(app_s3_bucket)s/' % env)
    local('s3cmd put -P app/config-%(settings)s.js s3://%(app_s3_bucket)s/js/config.js' % env)

def local_app():
    """
    Runs a local web server to test the web app
    """
    local('cd app/web && python -m SimpleHTTPServer 8080')

