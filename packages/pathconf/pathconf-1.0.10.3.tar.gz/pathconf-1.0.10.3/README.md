## I do not recommend using this project as it's bad and so am I.

As stated in the short description this project simply uses os.walk to traverse a filesystem, starting in the users home directory, looking for a given file.
It was created for internal use as there are several of us in the office running python scripts which are located on a onedrive and each time a new machine was initialised onedrive would have wildly different paths.
Originally we were just using a simple function at the start of each script which would return the onedrive path but as different parts of the path started changing with new devices I realised this would quickly become an incredibly intricate and inneficient solution so I wrote this to help solve it. Published here for easier distribution around the office.

## use:

```
import pathconf

pathconf.find('filename.filetype')
```

Alternatively you can give it a partial directory.

```
pathconf.find('folder/filename.filetype')
```
or
```
pathconf.find('foldera/folderb/filename.filetype')
```
If no filetype is specified and the folder param is not passed, eg:
```
pathconf.find('filename')	
```
Then the search will be done without taking file extension into account.
If a file name has a . in it, like *filename.filename.txt*, it should still work. The workaround was to take the part after the . as an extension only if it is 5 characters or less.
This however causes problems with files such as *file.name.txt* as if you do not specify the extension *.name* will be taken as the extension instead.
This issue exists only in the defining of the search term as when searching for files I just looked for a second . and split there.

This functionality is available but not recommended, you're better off just giving the extension.

Passing the optional *folder=* parameter will search for a folder instead of a file.
```	
pathconf.find('folderName', folder=True)
```

Passing the optional *starting_dir=* parameter will change the starting directory from the users home directory.
```	
pathconf.find('filename.filetype', starting_dir='C:\\')
# for windows

#or

pathconf.find('filename.filetype', starting_dir='/')
# for unix
```	
Will start the search from the specified directory, in the example above this is the root directory.

This will create a *.file_paths* json file in *~/.config/pathconf/* if it doesn't already exist and then will search for your file. Once found it will add that file to the pathconf file for quicker access in future runs. 
If the file does already exist it will lookup your desired file and if it exists in the *pathconf.json* it will then check that the file exists where stated.
If the file exists where the *pathconf.json* says it does then it will use that file, if the file doesn't exist there or the file doesn't appear in the *pathconf.json* then it will search for the file and append it to the *pathconf.json*.

Other functions: remove(), reset(), get_paths(), list_paths(), and index().

```
pathconf.list_paths()
```

Will list all key and value pairs in the *pathconf.json*.

```
pathconf.get_paths()	
```
Will return a dictionary of paths held in the *pathconf.json*.

```
pathconf.reset()
```

Will reset the *pathconf.json* to a blank file.

```
pathconf.remove('filename.filetype')
```

Will remove the entry for filename.filetype from the *pathconf.json*.

```
pathconf.index('PathToIndex')
```

Will return a dictionary of all files and their full paths in that directory as well as writing that to its own json with the lowest level folder as the name.
For example:
```
pathconf.index('/home/joe/Documents')
```
Will return a dictionary of files within /home/joe/Documents/ and their full paths. This dictionary is also written to *Documents.json* in *~/.config/pathconf/*

Optional arguments for index() are:
depth (int): index() Will only search folders up to this depth, so for depth=3 it will index 3 down from the starting directory.
exceptions (list): You can pass a list of folders to be ignored when indexing. **Note: if passed with folders=True then the folders in exceptions will not be returned or added to the .json**
folders (bool): If True then index will return a dictionary of folders int the given directory.


## Installation:

Easiest way to install is using pip

```
pip install pathconf
```


## Current issues:

Haven't yet run into but understand that this will always take the first match it finds, if there are files with the same name and type elsewhere in your home directory then it will use them if found first, even if they're not the desired file. Current attempts to work around this are a default argument of *deprecated=False*, which will skip the search of any folder containing *deprecated* in the name (since most of our duplicates exist in 'deprecated' folders, this can be overridden by passing *deprecated=True*), the other attempt for a workaround was the the ability to give partial directories as *Documents/file* is a little more precise than *file*.
