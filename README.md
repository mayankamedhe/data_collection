# data_collection

#### Description data collected by- test.py
#### Gaze data collected by- gaze.py

### Clone to Local Repository

```bash
$ git clone https://github.com/mayankamedhe/data_collection.git
```

### Go to the top of the local repository

```bash
$ cd data_collection    # go to the local repository
```

### Update Local Repository

```bash
$ git checkout main   # set main branch as the current branch
$ git fetch origin main    # download the main branch from remote repository
$ git reset --hard origin/main  # reset the local main branch same as remote repository
```

### Creating a Branch

To list all branches-

```bash
$ git branch -a   # list all branches, showing the current branch 
```

To create a new branch-

```bash
$ git branch task0   # create task0 branch
$ git checkout task0  # switch into the task0 branch
```

### Compile the Code 

Make sure you already have a folder named CSV
```bash
$ python test.py
```

### Upload changes to task0 branch

```bash
cd data_collection   # go to the top of the repository
git status  # check the changes
git add .   # stage the changes
git status  # check the staged changes
git commit -m "task0 finished"   # the comment can be anything
git push --set-upstream origin task0  # up date the task0 branch of the remote repository
```

Go to the GitHub webpage and make a pull request

folder structure:

data collection
	- images 
		-	All input images
	- text_data
		- CSV files of text input for all users
	- gaze_data
		- CSV files of gaze data for all users
	- eye-tracker.py {userID}
	- test.py {userID}


