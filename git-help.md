First, let's ensure we are up-to-date (don't when you have changes that are not yet online)

> git pull origin master

Make new branch "gravwaves" and check it out:

> git checkout -b gravwaves 

Modify code, compile, etc. to make sure it is not totally useless (so until some (sub)-task has been achieved). 

Check what git has already noticed what has happened to the project (changes to files).

> git status 

Still need to manually select the updated files that are important to a "commit"

> git add FILENAME

This can be repeated.

Re-check with 

> git status

[One can make git blind to include local files and folders that will never be important for others. This works by adding stuff to the .gitignore file (it may be invisible but is in the main folder). For example, this can be applied to the build directory or the Makefile if it is modified for own purposes. If git status then shows *only* useful changes, git add all can be used to track all changes at once instead of git add FILENAME1 FILENAME2 ... ]

The actual change is then commited, that is a snapshot of the modification to the project is made, via 

> git branch

> git commit -m "added gw lum distance"

(Here we have double-checked first that we are really on the right branch gravwaves where we want to do our changes. but this info is already given by git status, so this step is not necessary) It is important to choose a good message.

We can now switch back and forth between the old version and the new version by changing branches. Don't do before the commit! Changes would be lost - git really changes your files on your hard drive. 

To go back to old version, with standard branch name "master": 

> git checkout master 

(You can check that your modifications have disappeared) To get the modifications back:

> git checkout gravwaves

(There is no -b here unlike before because we do not want to create a NEW branch)

There are two options to proceed. We can integrate the changes of the branch gravwaves into the master, and publish that. Or we publish the branch as a branch, not yet integrated. 

For the latter, 

> git push -u origin gravwaves

(Origin is the standard name of the online version of the repository.) This makes sense if the change is big enough and important but work-in-progress with possible side effects, or a quite separate thing in general. For a small thing that will be useful in general for the project, we can integrate it locally into the main project first and only publish that. 
That is the former option. 

For the former, go to master branch

> git checkout master

and make sure again that our master branch is up-to-date

> git pull origin master 

Merge the changes, locally, into master

> git merge gravwaves

And publish

> git push origin master
