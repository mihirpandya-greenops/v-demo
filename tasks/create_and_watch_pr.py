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
---
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: testapp
spec:
  selector:
    matchLabels:
      app: testapp
  template:
    metadata:
      labels:
        app: testapp
    spec:
      containers:
      - name: testapp
        image: docker.io/1mihirpandya/testapp
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
  strategy:
    canary:
      steps:
      - setWeight: 25
      - pause: {duration: 5s}
      - setWeight: 50
      - pause: {duration: 5s}
      - setWeight: 75
      - pause: {duration: 5s}
      - setWeight: 100
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
