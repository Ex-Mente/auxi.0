.. highlight:: python
   :linenothreshold:

Business Modelling
==================

The purpose of this section is to explain a number of concepts and demonstrate the use of the Entity, Component, Activity classes in the auxi.modelling.business module.


Basic Activity
---------------
A basic activity periodically create a transaction between two specified accounts.


To create an basic activity, import the 'BasicActivity' and the create a 'BasicActivity'

.. code-block:: none

    from auxi.modelling.business.basic import BasicActivity

    basic_activity = BasicActivity("NameA",
                                description="DescriptionA",
                                dt_account="Bank\Default",
                                cr_account="Sales\Default",
                                amount=5000,
                                start=datetime(2016, 2, 1),
                                end=datetime(2017, 2, 1),
                                interval=3)
