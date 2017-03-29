import requests, time


def check_deploy_status(sourceUrl,appId):
        appUrl = sourceUrl + appId
        depApp = requests.get(url=appUrl)
        depData = depApp.json()
        depData = depData['app']
        deploying = depData['deployments']
        while deploying:
            print ('still deploying ' + appId)
            time.sleep(15)
            depApp = requests.get(url=appUrl)
            depData = depApp.json()
            depData = depData['app']
            deploying = depData['deployments']
        print ("deployment for " + appId + " complete!")


def get_vhost(app):
    labels = app['labels']
    vhost = labels['HAPROXY_0_VHOST']
    vhost = vhost.split(",")[0]
    return vhost

