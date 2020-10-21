# Picture Tagger Demo
Over the years and several digital cameras and phones, my family has accumulated
thousands of digital images.  These exist in multiple backups on my file server
so their are duplicates and the original dates may be lost.

The goal of the picture tagger system is to make these pictures 
searchable and sortable.  The plan is to use the create date from the metadata
inside the jpeg file and the cksum of the file (combined) as a unique
identifier for each picture.  The server-side provides a RESTful interface
to access these pictures, and allows the client to mark each picture
with one or more tags like #Deleted (to mark as deleted) plus other tags
(like children's names).  It assumes a client-side web app for viewing
and tagging the pictures.

The server is in the backend directory, while the client is in the frontend
directory.

