.. _signals:

Signals
=======

batch_processed
---------------

Provides a single argument which is the ``sendgrid_events.models.Event`` instance
for the single event within the batch. A single batch POST can contain one or more
events.
