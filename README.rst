=============================
ecreall.handleexternaledition
=============================

When you use zope external editor with some features, you can have great issues:

- if history is enabled on file content type, you don't want that an history entry
  is generated each time user saves the document during the same external edition session

- idem if you have enabled document viewer generation on each update, you want it to be done
  at the end of the session

That's what this product is dedicated to.
