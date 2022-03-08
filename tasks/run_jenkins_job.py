import jenkins
import os
import sys
import time
    

jenkins_url = os.getenv('JENKINS_URL')
print(jenkins_url)
jenkins_username = 'admin' #os.getenv('JENKINS_USERNAME')
jenkins_password = os.getenv('JENKINS_PASSWORD')
job_name = os.getenv('JOB_NAME')
# token_name = os.getenv('TOKEN_NAME')

jenkins_srv = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
next_build_number = jenkins_srv.get_job_info(job_name)['nextBuildNumber']
jenkins_srv.build_job(job_name)#, token=token_name)

while True:
    time.sleep(10)
    build_info = jenkins_srv.get_build_info(job_name, next_build_number)
    if build_info['result'] != None:
        print(build_info['result'])
        if build_info['result'] == "FAILURE":
            sys.exit(1)
        break
sys.exit(0)
