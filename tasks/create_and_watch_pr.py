from github import Github
import os
import time
import string


newFile = '''
# apiVersion: v1
# kind: Pod
# metadata:
#   name: nginx
# spec:
#   containers:
#   - name: nginx
#     image: nginx:1.14.2
#     ports:
#     - containerPort: 80
# ---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: testapp
spec:
  replicas: 1
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: testapp
  template:
    metadata:
      labels:
        app: testapp
    spec:
      containers:
      - image: docker.io/1mihirpandya/testapp:latest
        name: testapp
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: testapp
spec:
  ports:
  - port: 5000
    targetPort: 5000
  selector:
    app: testapp
'''

source = "main"
letters = string.ascii_lowercase
new_branch = "test-" + ''.join(random.choice(letters) for i in range(10))

token = os.getenv('GITHUB_TOKEN')
g = Github(token)
repo = g.get_repo("mihirpandya-greenops/verkada-demo")
sb = repo.get_branch(source)
#Creating new branch
repo.create_git_ref(ref='refs/heads/' + new_branch, sha=sb.commit.sha)
#Updating new branch
contents = repo.get_contents("/manifest/argo-manifest.yml", ref=new_branch)
repo.update_file(contents.path, "updating release", newFile, contents.sha, branch=new_branch)
#Creating pull request
pr = repo.create_pull(title="Updating release", body="updates", head=new_branch, base=source)

#Waiting for merge
while not pr.is_merged():
    time.sleep(10)
