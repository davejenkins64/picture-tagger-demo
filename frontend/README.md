# Picture Tagger Frontend
The picture tagger frontend is an Angular application.  I've taken
the liberty of only putting a subset of files (src) into git, leaving
node_modules and package-lock.json out.

So, to build, you'll need node, Angular, Angular CLI, and to 
recreate the node_modules directory head to this directory and run
'npm install'.

The front end has controls for limiting the time-period of the
search for pictures with a start/end data filer at the top.  
Each screenful shows 5 pictures at a time
and there are controls for first, previous, next and last pages of
the selected filtered set of pictures.

Individual pictures can be tagged with categories (3 hard-coded for now), or
a miscellaneous category, or can be marked for future deletion.
By "future deletion" I mean that this interface doesn't do the actual
deleting.

The current state of the front-end suffices for the initial tagging,
but a better viewer to review pictures by tag is needed.
